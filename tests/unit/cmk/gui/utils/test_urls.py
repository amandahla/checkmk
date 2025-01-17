#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.gui.utils.urls import urlencode, urlencode_vars


@pytest.mark.parametrize("inp,out", [
    ([], ""),
    ([("c", "d"), ("a", "b")], "a=b&c=d"),
    ([("a", 1), ("c", "d")], "a=1&c=d"),
    ([("a", u"ä"), ("c", "d")], "a=%C3%A4&c=d"),
    ([("a", u"abcä")], "a=abc%C3%A4"),
    ([("a", "_-.")], "a=_-."),
    ([("a", "#")], "a=%23"),
    ([("a", "+")], "a=%2B"),
    ([("a", " ")], "a=+"),
    ([("a", "/")], "a=%2F"),
    ([("a", None)], "a="),
])
def test_urlencode_vars(inp, out):
    assert urlencode_vars(inp) == out


@pytest.mark.parametrize(
    "inp,out",
    [
        (u"välue", "v%C3%A4lue"),
        # TODO: None / int handling inconsistent with urlencode_vars()
        (None, ""),
        ("ä", "%C3%A4"),
        ("_-.", "_-."),
        ("#", "%23"),
        ("+", "%2B"),
        (" ", "+"),
        ("/", "%2F"),
    ])
def test_urlencode(inp, out):
    assert urlencode(inp) == out
