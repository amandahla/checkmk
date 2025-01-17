#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# pylint: disable=redefined-outer-name

from pathlib import Path

import pytest

import cmk.utils.tags as tags

import cmk.gui.watolib.tags
import cmk.gui.watolib.utils
from cmk.gui.watolib.tags import TagConfigFile


@pytest.fixture()
def test_pre_16_cfg(monkeypatch):
    multisite_dir = Path(cmk.gui.watolib.utils.multisite_dir())
    multisite_dir.mkdir(parents=True, exist_ok=True)
    hosttags_mk = multisite_dir / "hosttags.mk"

    with hosttags_mk.open("w", encoding="utf-8") as f:
        f.write(u"""# Created by WATO
# encoding: utf-8

wato_host_tags += [
    ('criticality', u'Criticality', [
        ('prod', u'Productive system', ['bla']),
        ('critical', u'Business critical', []),
        ('test', u'Test system', []),
        ('offline', u'Do not monitor this host', [])]),
    ('networking', u'Networking Segment', [
        ('lan', u'Local network (low latency)', []),
        ('wan', u'WAN (high latency)', []),
        ('dmz', u'DMZ (low latency, secure access)', []),
    ]),
]

wato_aux_tags += [("bla", u"bläää")]
""")

    cfg = tags.TagConfig()
    cfg.parse_config(TagConfigFile().load_for_reading())

    yield cfg

    if hosttags_mk.exists():
        hosttags_mk.unlink()


@pytest.fixture()
def test_cfg(test_pre_16_cfg):
    multisite_dir = Path(cmk.gui.watolib.utils.multisite_dir())
    tags_mk = multisite_dir / "tags.mk"
    hosttags_mk = multisite_dir / "hosttags.mk"

    with tags_mk.open("w", encoding="utf-8") as f:
        f.write(u"""# Created by WATO
# encoding: utf-8

wato_tags = %s
""" % repr(test_pre_16_cfg.get_dict_format()))

    with hosttags_mk.open("w", encoding="utf-8") as f:
        f.write(u"")

    cfg = tags.TagConfig()
    cfg.parse_config(TagConfigFile().load_for_reading())

    yield cfg

    if tags_mk.exists():
        tags_mk.unlink()


def test_tag_config_load_pre_16(test_pre_16_cfg):
    assert len(test_pre_16_cfg.tag_groups) == 2
    tag_group = test_pre_16_cfg.tag_groups[0]
    assert tag_group.id == "criticality"
    assert tag_group.title == u"Criticality"
    assert tag_group.topic is None

    tag_group = test_pre_16_cfg.tag_groups[1]
    assert tag_group.id == "networking"
    assert tag_group.title == u"Networking Segment"
    assert tag_group.topic is None

    assert len(test_pre_16_cfg.aux_tag_list.get_tags()) == 1
    aux_tag = test_pre_16_cfg.aux_tag_list.get_tags()[0]
    assert aux_tag.topic is None
    assert aux_tag.id == "bla"
    assert aux_tag.title == u"bläää"


def test_tag_config_load(test_cfg):
    assert len(test_cfg.tag_groups) == 2
    assert len(test_cfg.aux_tag_list.get_tags()) == 1


@pytest.mark.usefixtures("test_cfg")
def test_tag_config_save(mocker):
    export_mock = mocker.patch.object(cmk.gui.watolib.tags, "_export_hosttags_to_php")

    config_file = TagConfigFile()
    base_config_mock = mocker.patch.object(config_file, "_save_base_config")

    cfg = tags.TagConfig()
    cfg.insert_tag_group(tags.TagGroup(("tgid2", "Topics/titlor", [("tgid2", "tagid2", [])])))
    config_file.save(cfg.get_dict_format())

    export_mock.assert_called_once()
    base_config_mock.assert_called_once()

    cfg = tags.TagConfig()
    cfg.parse_config(config_file.load_for_reading())
    assert len(cfg.tag_groups) == 1
    assert cfg.tag_groups[0].id == "tgid2"
