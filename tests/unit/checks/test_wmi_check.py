#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from tests.testlib import Check

from cmk.base.check_api import MKCounterWrapped

from .checktestlib import assertDiscoveryResultsEqual, CheckResult, DiscoveryResult

pytestmark = pytest.mark.checks

#   .--infos---------------------------------------------------------------.
#   |                        _        __                                   |
#   |                       (_)_ __  / _| ___  ___                         |
#   |                       | | '_ \| |_ / _ \/ __|                        |
#   |                       | | | | |  _| (_) \__ \                        |
#   |                       |_|_| |_|_|  \___/|___/                        |
#   |                                                                      |
#   '----------------------------------------------------------------------'

info_wmi_timeout = [[u'WMItimeout']]

info_subsection_wmi_timeout = [
    [u'[system_perf]'],
    [u'WMItimeout'],
    [u'[computer_system]'],
    [u'name', u'unimportant', u'data'],
]

info_wmi_cpuload_1 = [
    [u'[system_perf]'],
    [
        u'AlignmentFixupsPersec', u'Caption', u'ContextSwitchesPersec', u'Description',
        u'ExceptionDispatchesPersec', u'FileControlBytesPersec', u'FileControlOperationsPersec',
        u'FileDataOperationsPersec', u'FileReadBytesPersec', u'FileReadOperationsPersec',
        u'FileWriteBytesPersec', u'FileWriteOperationsPersec', u'FloatingEmulationsPersec',
        u'Frequency_Object', u'Frequency_PerfTime', u'Frequency_Sys100NS', u'Name',
        u'PercentRegistryQuotaInUse', u'PercentRegistryQuotaInUse_Base', u'Processes',
        u'ProcessorQueueLength', u'SystemCallsPersec', u'SystemUpTime', u'Threads',
        u'Timestamp_Object', u'Timestamp_PerfTime', u'Timestamp_Sys100NS'
    ],
    [
        u'0', u'', u'469922985', u'', u'222849', u'6503221217', u'72494625', u'75272330',
        u'111617810637', u'68676492', u'34750951332', u'6595838', u'0', u'10000000', u'2156247',
        u'10000000', u'', u'250803278', u'-1', u'384', u'0', u'2144858950', u'131983188065000000',
        u'5534', u'131983336220258827', u'31947393930', u'131983372220250000'
    ], [u'[computer_system]'],
    [
        u'AdminPasswordStatus', u'AutomaticManagedPagefile', u'AutomaticResetBootOption',
        u'AutomaticResetCapability', u'BootOptionOnLimit', u'BootOptionOnWatchDog',
        u'BootROMSupported', u'BootStatus', u'BootupState', u'Caption', u'ChassisBootupState',
        u'ChassisSKUNumber', u'CreationClassName', u'CurrentTimeZone', u'DaylightInEffect',
        u'Description', u'DNSHostName', u'Domain', u'DomainRole', u'EnableDaylightSavingsTime',
        u'FrontPanelResetStatus', u'HypervisorPresent', u'InfraredSupported', u'InitialLoadInfo',
        u'InstallDate', u'KeyboardPasswordStatus', u'LastLoadInfo', u'Manufacturer', u'Model',
        u'Name', u'NameFormat', u'NetworkServerModeEnabled', u'NumberOfLogicalProcessors',
        u'NumberOfProcessors', u'OEMLogoBitmap', u'OEMStringArray', u'PartOfDomain',
        u'PauseAfterReset', u'PCSystemType', u'PCSystemTypeEx', u'PowerManagementCapabilities',
        u'PowerManagementSupported', u'PowerOnPasswordStatus', u'PowerState', u'PowerSupplyState',
        u'PrimaryOwnerContact', u'PrimaryOwnerName', u'ResetCapability', u'ResetCount',
        u'ResetLimit', u'Roles', u'Status', u'SupportContactDescription', u'SystemFamily',
        u'SystemSKUNumber', u'SystemStartupDelay', u'SystemStartupOptions', u'SystemStartupSetting',
        u'SystemType', u'ThermalState', u'TotalPhysicalMemory', u'UserName', u'WakeUpType',
        u'Workgroup'
    ],
    [
        u'3', u'1', u'1', u'1', u'', u'', u'1', u'<array>', u'Normal boot', u'SERG-DELL', u'3',
        u'Notebook', u'Win32_ComputerSystem', u'60', u'0', u'AT/AT COMPATIBLE', u'SERG-DELL',
        u'WORKGROUP', u'0', u'1', u'3', u'0', u'0', u'', u'', u'3', u'', u'Dell Inc.',
        u'XPS 15 9570', u'SERG-DELL', u'', u'1', u'12', u'1', u'', u'<array>', u'0', u'-1', u'2',
        u'2', u'', u'', u'3', u'0', u'3', u'', u'sk', u'1', u'-1', u'-1', u'<array>', u'OK', u'',
        u'XPS', u'087C', u'', u'', u'', u'x64-based PC', u'3', u'34077048832', u'SERG-DELL\\sk',
        u'6', u'WORKGROUP'
    ]
]

info_wmi_cpuload_2 = [
    [u'[system_perf]'], [u'WMItimeout'], [u'[computer_system]'],
    [
        u'AdminPasswordStatus', u'AutomaticManagedPagefile', u'AutomaticResetBootOption',
        u'AutomaticResetCapability', u'BootOptionOnLimit', u'BootOptionOnWatchDog',
        u'BootROMSupported', u'BootStatus', u'BootupState', u'Caption', u'ChassisBootupState',
        u'ChassisSKUNumber', u'CreationClassName', u'CurrentTimeZone', u'DaylightInEffect',
        u'Description', u'DNSHostName', u'Domain', u'DomainRole', u'EnableDaylightSavingsTime',
        u'FrontPanelResetStatus', u'HypervisorPresent', u'InfraredSupported', u'InitialLoadInfo',
        u'InstallDate', u'KeyboardPasswordStatus', u'LastLoadInfo', u'Manufacturer', u'Model',
        u'Name', u'NameFormat', u'NetworkServerModeEnabled', u'NumberOfLogicalProcessors',
        u'NumberOfProcessors', u'OEMLogoBitmap', u'OEMStringArray', u'PartOfDomain',
        u'PauseAfterReset', u'PCSystemType', u'PCSystemTypeEx', u'PowerManagementCapabilities',
        u'PowerManagementSupported', u'PowerOnPasswordStatus', u'PowerState', u'PowerSupplyState',
        u'PrimaryOwnerContact', u'PrimaryOwnerName', u'ResetCapability', u'ResetCount',
        u'ResetLimit', u'Roles', u'Status', u'SupportContactDescription', u'SystemFamily',
        u'SystemSKUNumber', u'SystemStartupDelay', u'SystemStartupOptions', u'SystemStartupSetting',
        u'SystemType', u'ThermalState', u'TotalPhysicalMemory', u'UserName', u'WakeUpType',
        u'Workgroup'
    ],
    [
        u'3', u'1', u'1', u'1', u'', u'', u'1', u'<array>', u'Normal boot', u'SERG-DELL', u'3',
        u'Notebook', u'Win32_ComputerSystem', u'60', u'0', u'AT/AT COMPATIBLE', u'SERG-DELL',
        u'WORKGROUP', u'0', u'1', u'3', u'0', u'0', u'', u'', u'3', u'', u'Dell Inc.',
        u'XPS 15 9570', u'SERG-DELL', u'', u'1', u'12', u'1', u'', u'<array>', u'0', u'-1', u'2',
        u'2', u'', u'', u'3', u'0', u'3', u'', u'sk', u'1', u'-1', u'-1', u'<array>', u'OK', u'',
        u'XPS', u'087C', u'', u'', u'', u'x64-based PC', u'3', u'34077048832', u'SERG-DELL\\sk',
        u'6', u'WORKGROUP'
    ]
]

info_wmi_cpuload_3 = [
    [u'[system_perf]'],
    [
        u'AlignmentFixupsPersec', u'Caption', u'ContextSwitchesPersec', u'Description',
        u'ExceptionDispatchesPersec', u'FileControlBytesPersec', u'FileControlOperationsPersec',
        u'FileDataOperationsPersec', u'FileReadBytesPersec', u'FileReadOperationsPersec',
        u'FileWriteBytesPersec', u'FileWriteOperationsPersec', u'FloatingEmulationsPersec',
        u'Frequency_Object', u'Frequency_PerfTime', u'Frequency_Sys100NS', u'Name',
        u'PercentRegistryQuotaInUse', u'PercentRegistryQuotaInUse_Base', u'Processes',
        u'ProcessorQueueLength', u'SystemCallsPersec', u'SystemUpTime', u'Threads',
        u'Timestamp_Object', u'Timestamp_PerfTime', u'Timestamp_Sys100NS'
    ],
    [
        u'0', u'', u'469922985', u'', u'222849', u'6503221217', u'72494625', u'75272330',
        u'111617810637', u'68676492', u'34750951332', u'6595838', u'0', u'10000000', u'2156247',
        u'10000000', u'', u'250803278', u'-1', u'384', u'0', u'2144858950', u'131983188065000000',
        u'5534', u'131983336220258827', u'31947393930', u'131983372220250000'
    ], [u'[computer_system]'], [u'WMItimeout']
]

info_wmi_cpuload_4 = [[u'[system_perf]'], [u'WMItimeout'], [u'[computer_system]'], [u'WMItimeout']]

info_wmi_cpuload_5 = [
    [u'[system_perf]'],
    [
        u'AlignmentFixupsPersec', u'Caption', u'ContextSwitchesPersec', u'Description',
        u'ExceptionDispatchesPersec', u'FileControlBytesPersec', u'FileControlOperationsPersec',
        u'FileDataOperationsPersec', u'FileReadBytesPersec', u'FileReadOperationsPersec',
        u'FileWriteBytesPersec', u'FileWriteOperationsPersec', u'FloatingEmulationsPersec',
        u'Frequency_Object', u'Frequency_PerfTime', u'Frequency_Sys100NS', u'Name',
        u'PercentRegistryQuotaInUse', u'PercentRegistryQuotaInUse_Base', u'Processes',
        u'ProcessorQueueLength', u'SystemCallsPersec', u'SystemUpTime', u'Threads',
        u'Timestamp_Object', u'Timestamp_PerfTime', u'Timestamp_Sys100NS', u'WMIStatus'
    ],
    [
        u'0', u'', u'469922985', u'', u'222849', u'6503221217', u'72494625', u'75272330',
        u'111617810637', u'68676492', u'34750951332', u'6595838', u'0', u'10000000', u'2156247',
        u'10000000', u'', u'250803278', u'-1', u'384', u'0', u'2144858950', u'131983188065000000',
        u'5534', u'131983336220258827', u'31947393930', u'131983372220250000', u'OK'
    ], [u'[computer_system]'],
    [
        u'AdminPasswordStatus', u'AutomaticManagedPagefile', u'AutomaticResetBootOption',
        u'AutomaticResetCapability', u'BootOptionOnLimit', u'BootOptionOnWatchDog',
        u'BootROMSupported', u'BootStatus', u'BootupState', u'Caption', u'ChassisBootupState',
        u'ChassisSKUNumber', u'CreationClassName', u'CurrentTimeZone', u'DaylightInEffect',
        u'Description', u'DNSHostName', u'Domain', u'DomainRole', u'EnableDaylightSavingsTime',
        u'FrontPanelResetStatus', u'HypervisorPresent', u'InfraredSupported', u'InitialLoadInfo',
        u'InstallDate', u'KeyboardPasswordStatus', u'LastLoadInfo', u'Manufacturer', u'Model',
        u'Name', u'NameFormat', u'NetworkServerModeEnabled', u'NumberOfLogicalProcessors',
        u'NumberOfProcessors', u'OEMLogoBitmap', u'OEMStringArray', u'PartOfDomain',
        u'PauseAfterReset', u'PCSystemType', u'PCSystemTypeEx', u'PowerManagementCapabilities',
        u'PowerManagementSupported', u'PowerOnPasswordStatus', u'PowerState', u'PowerSupplyState',
        u'PrimaryOwnerContact', u'PrimaryOwnerName', u'ResetCapability', u'ResetCount',
        u'ResetLimit', u'Roles', u'Status', u'SupportContactDescription', u'SystemFamily',
        u'SystemSKUNumber', u'SystemStartupDelay', u'SystemStartupOptions', u'SystemStartupSetting',
        u'SystemType', u'ThermalState', u'TotalPhysicalMemory', u'UserName', u'WakeUpType',
        u'Workgroup', u'WMIStatus'
    ],
    [
        u'3', u'1', u'1', u'1', u'', u'', u'1', u'<array>', u'Normal boot', u'SERG-DELL', u'3',
        u'Notebook', u'Win32_ComputerSystem', u'60', u'0', u'AT/AT COMPATIBLE', u'SERG-DELL',
        u'WORKGROUP', u'0', u'1', u'3', u'0', u'0', u'', u'', u'3', u'', u'Dell Inc.',
        u'XPS 15 9570', u'SERG-DELL', u'', u'1', u'12', u'1', u'', u'<array>', u'0', u'-1', u'2',
        u'2', u'', u'', u'3', u'0', u'3', u'', u'sk', u'1', u'-1', u'-1', u'<array>', u'OK', u'',
        u'XPS', u'087C', u'', u'', u'', u'x64-based PC', u'3', u'34077048832', u'SERG-DELL\\sk',
        u'6', u'WORKGROUP', u'OK'
    ]
]

info_wmi_cpuload_6 = [
    [u'[system_perf]'],
    [
        u'AlignmentFixupsPersec', u'Caption', u'ContextSwitchesPersec', u'Description',
        u'ExceptionDispatchesPersec', u'FileControlBytesPersec', u'FileControlOperationsPersec',
        u'FileDataOperationsPersec', u'FileReadBytesPersec', u'FileReadOperationsPersec',
        u'FileWriteBytesPersec', u'FileWriteOperationsPersec', u'FloatingEmulationsPersec',
        u'Frequency_Object', u'Frequency_PerfTime', u'Frequency_Sys100NS', u'Name',
        u'PercentRegistryQuotaInUse', u'PercentRegistryQuotaInUse_Base', u'Processes',
        u'ProcessorQueueLength', u'SystemCallsPersec', u'SystemUpTime', u'Threads',
        u'Timestamp_Object', u'Timestamp_PerfTime', u'Timestamp_Sys100NS', u'WMIStatus'
    ],
    [
        u'0', u'', u'469922985', u'', u'222849', u'6503221217', u'72494625', u'75272330',
        u'111617810637', u'68676492', u'34750951332', u'6595838', u'0', u'10000000', u'2156247',
        u'10000000', u'', u'250803278', u'-1', u'384', u'0', u'2144858950', u'131983188065000000',
        u'5534', u'131983336220258827', u'31947393930', u'131983372220250000', u'Timeout'
    ], [u'[computer_system]'],
    [
        u'AdminPasswordStatus', u'AutomaticManagedPagefile', u'AutomaticResetBootOption',
        u'AutomaticResetCapability', u'BootOptionOnLimit', u'BootOptionOnWatchDog',
        u'BootROMSupported', u'BootStatus', u'BootupState', u'Caption', u'ChassisBootupState',
        u'ChassisSKUNumber', u'CreationClassName', u'CurrentTimeZone', u'DaylightInEffect',
        u'Description', u'DNSHostName', u'Domain', u'DomainRole', u'EnableDaylightSavingsTime',
        u'FrontPanelResetStatus', u'HypervisorPresent', u'InfraredSupported', u'InitialLoadInfo',
        u'InstallDate', u'KeyboardPasswordStatus', u'LastLoadInfo', u'Manufacturer', u'Model',
        u'Name', u'NameFormat', u'NetworkServerModeEnabled', u'NumberOfLogicalProcessors',
        u'NumberOfProcessors', u'OEMLogoBitmap', u'OEMStringArray', u'PartOfDomain',
        u'PauseAfterReset', u'PCSystemType', u'PCSystemTypeEx', u'PowerManagementCapabilities',
        u'PowerManagementSupported', u'PowerOnPasswordStatus', u'PowerState', u'PowerSupplyState',
        u'PrimaryOwnerContact', u'PrimaryOwnerName', u'ResetCapability', u'ResetCount',
        u'ResetLimit', u'Roles', u'Status', u'SupportContactDescription', u'SystemFamily',
        u'SystemSKUNumber', u'SystemStartupDelay', u'SystemStartupOptions', u'SystemStartupSetting',
        u'SystemType', u'ThermalState', u'TotalPhysicalMemory', u'UserName', u'WakeUpType',
        u'Workgroup', u'WMIStatus'
    ],
    [
        u'3', u'1', u'1', u'1', u'', u'', u'1', u'<array>', u'Normal boot', u'SERG-DELL', u'3',
        u'Notebook', u'Win32_ComputerSystem', u'60', u'0', u'AT/AT COMPATIBLE', u'SERG-DELL',
        u'WORKGROUP', u'0', u'1', u'3', u'0', u'0', u'', u'', u'3', u'', u'Dell Inc.',
        u'XPS 15 9570', u'SERG-DELL', u'', u'1', u'12', u'1', u'', u'<array>', u'0', u'-1', u'2',
        u'2', u'', u'', u'3', u'0', u'3', u'', u'sk', u'1', u'-1', u'-1', u'<array>', u'OK', u'',
        u'XPS', u'087C', u'', u'', u'', u'x64-based PC', u'3', u'34077048832', u'SERG-DELL\\sk',
        u'6', u'WORKGROUP', u'OK'
    ]
]

info_wmi_cpuload_7 = [
    [u'[system_perf]'],
    [
        u'AlignmentFixupsPersec', u'Caption', u'ContextSwitchesPersec', u'Description',
        u'ExceptionDispatchesPersec', u'FileControlBytesPersec', u'FileControlOperationsPersec',
        u'FileDataOperationsPersec', u'FileReadBytesPersec', u'FileReadOperationsPersec',
        u'FileWriteBytesPersec', u'FileWriteOperationsPersec', u'FloatingEmulationsPersec',
        u'Frequency_Object', u'Frequency_PerfTime', u'Frequency_Sys100NS', u'Name',
        u'PercentRegistryQuotaInUse', u'PercentRegistryQuotaInUse_Base', u'Processes',
        u'ProcessorQueueLength', u'SystemCallsPersec', u'SystemUpTime', u'Threads',
        u'Timestamp_Object', u'Timestamp_PerfTime', u'Timestamp_Sys100NS', u'WMIStatus'
    ],
    [
        u'0', u'', u'469922985', u'', u'222849', u'6503221217', u'72494625', u'75272330',
        u'111617810637', u'68676492', u'34750951332', u'6595838', u'0', u'10000000', u'2156247',
        u'10000000', u'', u'250803278', u'-1', u'384', u'0', u'2144858950', u'131983188065000000',
        u'5534', u'131983336220258827', u'31947393930', u'131983372220250000', u'OK'
    ], [u'[computer_system]'],
    [
        u'AdminPasswordStatus', u'AutomaticManagedPagefile', u'AutomaticResetBootOption',
        u'AutomaticResetCapability', u'BootOptionOnLimit', u'BootOptionOnWatchDog',
        u'BootROMSupported', u'BootStatus', u'BootupState', u'Caption', u'ChassisBootupState',
        u'ChassisSKUNumber', u'CreationClassName', u'CurrentTimeZone', u'DaylightInEffect',
        u'Description', u'DNSHostName', u'Domain', u'DomainRole', u'EnableDaylightSavingsTime',
        u'FrontPanelResetStatus', u'HypervisorPresent', u'InfraredSupported', u'InitialLoadInfo',
        u'InstallDate', u'KeyboardPasswordStatus', u'LastLoadInfo', u'Manufacturer', u'Model',
        u'Name', u'NameFormat', u'NetworkServerModeEnabled', u'NumberOfLogicalProcessors',
        u'NumberOfProcessors', u'OEMLogoBitmap', u'OEMStringArray', u'PartOfDomain',
        u'PauseAfterReset', u'PCSystemType', u'PCSystemTypeEx', u'PowerManagementCapabilities',
        u'PowerManagementSupported', u'PowerOnPasswordStatus', u'PowerState', u'PowerSupplyState',
        u'PrimaryOwnerContact', u'PrimaryOwnerName', u'ResetCapability', u'ResetCount',
        u'ResetLimit', u'Roles', u'Status', u'SupportContactDescription', u'SystemFamily',
        u'SystemSKUNumber', u'SystemStartupDelay', u'SystemStartupOptions', u'SystemStartupSetting',
        u'SystemType', u'ThermalState', u'TotalPhysicalMemory', u'UserName', u'WakeUpType',
        u'Workgroup', u'WMIStatus'
    ],
    [
        u'3', u'1', u'1', u'1', u'', u'', u'1', u'<array>', u'Normal boot', u'SERG-DELL', u'3',
        u'Notebook', u'Win32_ComputerSystem', u'60', u'0', u'AT/AT COMPATIBLE', u'SERG-DELL',
        u'WORKGROUP', u'0', u'1', u'3', u'0', u'0', u'', u'', u'3', u'', u'Dell Inc.',
        u'XPS 15 9570', u'SERG-DELL', u'', u'1', u'12', u'1', u'', u'<array>', u'0', u'-1', u'2',
        u'2', u'', u'', u'3', u'0', u'3', u'', u'sk', u'1', u'-1', u'-1', u'<array>', u'OK', u'',
        u'XPS', u'087C', u'', u'', u'', u'x64-based PC', u'3', u'34077048832', u'SERG-DELL\\sk',
        u'6', u'WORKGROUP', u'Timeout'
    ]
]

info_wmi_cpuload_8 = [
    [u'[system_perf]'],
    [
        u'AlignmentFixupsPersec', u'Caption', u'ContextSwitchesPersec', u'Description',
        u'ExceptionDispatchesPersec', u'FileControlBytesPersec', u'FileControlOperationsPersec',
        u'FileDataOperationsPersec', u'FileReadBytesPersec', u'FileReadOperationsPersec',
        u'FileWriteBytesPersec', u'FileWriteOperationsPersec', u'FloatingEmulationsPersec',
        u'Frequency_Object', u'Frequency_PerfTime', u'Frequency_Sys100NS', u'Name',
        u'PercentRegistryQuotaInUse', u'PercentRegistryQuotaInUse_Base', u'Processes',
        u'ProcessorQueueLength', u'SystemCallsPersec', u'SystemUpTime', u'Threads',
        u'Timestamp_Object', u'Timestamp_PerfTime', u'Timestamp_Sys100NS', u'WMIStatus'
    ],
    [
        u'0', u'', u'469922985', u'', u'222849', u'6503221217', u'72494625', u'75272330',
        u'111617810637', u'68676492', u'34750951332', u'6595838', u'0', u'10000000', u'2156247',
        u'10000000', u'', u'250803278', u'-1', u'384', u'0', u'2144858950', u'131983188065000000',
        u'5534', u'131983336220258827', u'31947393930', u'131983372220250000', u'Timeout'
    ], [u'[computer_system]'],
    [
        u'AdminPasswordStatus', u'AutomaticManagedPagefile', u'AutomaticResetBootOption',
        u'AutomaticResetCapability', u'BootOptionOnLimit', u'BootOptionOnWatchDog',
        u'BootROMSupported', u'BootStatus', u'BootupState', u'Caption', u'ChassisBootupState',
        u'ChassisSKUNumber', u'CreationClassName', u'CurrentTimeZone', u'DaylightInEffect',
        u'Description', u'DNSHostName', u'Domain', u'DomainRole', u'EnableDaylightSavingsTime',
        u'FrontPanelResetStatus', u'HypervisorPresent', u'InfraredSupported', u'InitialLoadInfo',
        u'InstallDate', u'KeyboardPasswordStatus', u'LastLoadInfo', u'Manufacturer', u'Model',
        u'Name', u'NameFormat', u'NetworkServerModeEnabled', u'NumberOfLogicalProcessors',
        u'NumberOfProcessors', u'OEMLogoBitmap', u'OEMStringArray', u'PartOfDomain',
        u'PauseAfterReset', u'PCSystemType', u'PCSystemTypeEx', u'PowerManagementCapabilities',
        u'PowerManagementSupported', u'PowerOnPasswordStatus', u'PowerState', u'PowerSupplyState',
        u'PrimaryOwnerContact', u'PrimaryOwnerName', u'ResetCapability', u'ResetCount',
        u'ResetLimit', u'Roles', u'Status', u'SupportContactDescription', u'SystemFamily',
        u'SystemSKUNumber', u'SystemStartupDelay', u'SystemStartupOptions', u'SystemStartupSetting',
        u'SystemType', u'ThermalState', u'TotalPhysicalMemory', u'UserName', u'WakeUpType',
        u'Workgroup', u'WMIStatus'
    ],
    [
        u'3', u'1', u'1', u'1', u'', u'', u'1', u'<array>', u'Normal boot', u'SERG-DELL', u'3',
        u'Notebook', u'Win32_ComputerSystem', u'60', u'0', u'AT/AT COMPATIBLE', u'SERG-DELL',
        u'WORKGROUP', u'0', u'1', u'3', u'0', u'0', u'', u'', u'3', u'', u'Dell Inc.',
        u'XPS 15 9570', u'SERG-DELL', u'', u'1', u'12', u'1', u'', u'<array>', u'0', u'-1', u'2',
        u'2', u'', u'', u'3', u'0', u'3', u'', u'sk', u'1', u'-1', u'-1', u'<array>', u'OK', u'',
        u'XPS', u'087C', u'', u'', u'', u'x64-based PC', u'3', u'34077048832', u'SERG-DELL\\sk',
        u'6', u'WORKGROUP', u'Timeout'
    ]
]

info_msx_info_store_1 = [
    [
        u'AdministrativeRPCrequestsPersec', u'AdminRPCRequests', u'Caption', u'Description',
        u'DirectoryAccessLDAPSearchesPersec', u'Frequency_Object', u'Frequency_PerfTime',
        u'Frequency_Sys100NS', u'JetLogRecordBytesPersec', u'JetLogRecordsPersec',
        u'JetPagesModifiedPersec', u'JetPagesPrereadPersec', u'JetPagesReadPersec',
        u'JetPagesReferencedPersec', u'JetPagesRemodifiedPersec', u'LazyindexescreatedPersec',
        u'LazyindexesdeletedPersec', u'LazyindexfullrefreshPersec',
        u'LazyindexincrementalrefreshPersec', u'MessagescreatedPersec', u'MessagesdeletedPersec',
        u'MessagesopenedPersec', u'MessagesupdatedPersec', u'Name', u'PropertypromotionsPersec',
        u'RPCAverageLatency', u'RPCAverageLatency_Base', u'RPCBytesReceivedPersec',
        u'RPCBytesSentPersec', u'RPCOperationsPersec', u'RPCPacketsPersec', u'RPCRequests',
        u'Timestamp_Object', u'Timestamp_PerfTime', u'Timestamp_Sys100NS'
    ],
    [
        u'13203303', u'0', u'', u'', u'61388', u'0', u'1953125', u'10000000', u'614653228',
        u'12092743', u'49049', u'826', u'312', u'53440863', u'8506178', u'3', u'24', u'3', u'838',
        u'80486', u'23006', u'101226', u'23140', u'_total', u'0', u'1903888', u'3908424', u'1040',
        u'400087174', u'6138327', u'3908424', u'1145789', u'0', u'6743176285319',
        u'130951777565340000'
    ],
]

#.

discovered_wmi_cpuload_result = [(None, None)]


@pytest.mark.parametrize("check_name,info,expected", [
    ('wmi_webservices', info_wmi_timeout, []),
    ('wmi_cpuload', info_wmi_cpuload_1, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_2, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_3, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_4, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_5, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_6, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_7, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_8, discovered_wmi_cpuload_result),
    ('dotnet_clrmemory', [[u'WMItimeout']], []),
])
def test_wmi_cpu_load_discovery(check_name, info, expected):
    check = Check(check_name)
    discovery_result = DiscoveryResult(check.run_discovery(check.run_parse(info)))
    discovery_expected = DiscoveryResult(expected)
    assertDiscoveryResultsEqual(check, discovery_result, discovery_expected)


@pytest.mark.parametrize("check_name,info,expected", [
    ('wmi_webservices', info_wmi_timeout, None),
    ('wmi_cpuload', info_subsection_wmi_timeout, None),
])
def test_wmi_cpuload_timeout_exceptions(check_name, info, expected):
    check = Check(check_name)
    with pytest.raises(MKCounterWrapped):
        CheckResult(check.run_check(None, {}, check.run_parse(info)))


@pytest.mark.parametrize("check_name, expected", [
    ('msexch_isclienttype', [
        (0, 'Average latency: 0.49 ms', [('average_latency', 0.48712422193702626, 40.0, 50.0)]),
        (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60.0, 70.0)]),
    ]),
    ('msexch_isstore', [
        (0, 'Average latency: 0.49 ms', [('average_latency', 0.48712422193702626, 41.0, 51.0)]),
    ]),
])
def test_wmi_msexch_isclienttype_wato_params(check_name, expected):
    check = Check(check_name)
    result = list(
        check.run_check(
            item="_total",
            params={
                'store_latency': (41.0, 51.0),
                'clienttype_latency': (40.0, 50.0),
                'clienttype_requests': (60, 70),
            },
            info=check.run_parse(info_msx_info_store_1),
        ))
    assert result == expected
