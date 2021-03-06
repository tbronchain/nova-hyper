#!/bin/bash
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# This script is executed inside gate_hook.sh

INSTALLDIR=${INSTALLDIR:-/opt/stack}
source $INSTALLDIR/devstack/functions-common
LOGDIR=/opt/stack/logs

#todo: check
#if is_ubuntu; then
# Find and collect docker daemon logs
sudo find /var/log/ -name "hyper*" -print -exec sudo cp {} $LOGDIR \;
#elif is_fedora; then
#  # fetch the docker logs from the journal
#  sudo journalctl _SYSTEMD_UNIT=docker.service | sudo tee -a $LOGDIR/docker.service.log > /dev/null
#  sudo journalctl _SYSTEMD_UNIT=docker.socket | sudo tee -a $LOGDIR/docker.socket.log > /dev/null
#fi

# Copy logs from the hyperdb
sudo mkdir -p $LOGDIR/hyper.db/
sudo find /var/lib/hyper/hyper.db/ -name "*.log" -print -exec sudo cp {} $LOGDIR/hyper.db/ \;
