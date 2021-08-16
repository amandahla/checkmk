// Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the
// terms and conditions defined in the file COPYING, which is part of this
// source code package.

#ifndef DowntimeRenderer_h
#define DowntimeRenderer_h

#include "config.h"  // IWYU pragma: keep

#include <string>

#include "ListLambdaColumn.h"
#include "MonitoringCore.h"
class ListRenderer;

class DowntimeRenderer : public ListColumnRenderer<DowntimeData> {
public:
    enum class verbosity { none, medium, full };
    DowntimeRenderer(verbosity v) : verbosity_{v} {}
    void output(ListRenderer &l, const DowntimeData &downtime) const;

private:
    verbosity verbosity_;
};

template <>
inline std::string detail::column::serialize(const DowntimeData &data) {
    return std::to_string(data._id);
}
#endif  // DowntimeRenderer_h