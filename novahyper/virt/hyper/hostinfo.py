# Copyright (c) 2013 dotCloud, Inc.
# Copyright (c) 2015 HyperHQ Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

from oslo_config import cfg

CONF = cfg.CONF


def statvfs():
    hyper_path = CONF.hyper.root_directory
    if not os.path.exists(hyper_path):
        hyper_path = '/'
    return os.statvfs(hyper_path)



def get_disk_usage():
    st = statvfs()
    return {
        'total': st.f_blocks * st.f_frsize,
        'available': st.f_bavail * st.f_frsize,
        'used': (st.f_blocks - st.f_bfree) * st.f_frsize
    }


def get_total_vcpus():
    total_vcpus = 0

    with open('/proc/cpuinfo') as f:
        for ln in f.readlines():
            if ln.startswith('processor'):
                total_vcpus += 1

    return total_vcpus


def get_vcpus_used(containers):
    total_vcpus_used = 0
    for container in containers:
        if isinstance(container, dict):
            total_vcpus_used += container.get('Config', {}).get(
                'CpuShares', 0)

    return total_vcpus_used


def get_memory_usage():
    with open('/proc/meminfo') as f:
        m = f.read().split()
        idx1 = m.index('MemTotal:')
        idx2 = m.index('MemFree:')
        idx3 = m.index('Buffers:')
        idx4 = m.index('Cached:')

        total = int(m[idx1 + 1])
        avail = int(m[idx2 + 1]) + int(m[idx3 + 1]) + int(m[idx4 + 1])

    return {
        'total': total * 1024,
        'used': (total - avail) * 1024
    }


def get_mounts():
    with open('/proc/mounts') as f:
        return f.readlines()
