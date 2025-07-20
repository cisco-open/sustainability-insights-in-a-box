# Copyright 2024 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from pyats import topology
import logging
from utils.secrets import decrypt

class SSH_Connection:

    def __init__(self, task_config):
        """
        SSH CLI connection provider
        uses PyATS
        """
        self._connection = None
        self._task_config = task_config
        self._name = task_config['device']['name']
        self._type = task_config['device']['connection']
        self._device_config = self._task_config['device']

    def connect(self):
        """
        Overrides baseclass connect() method
        opens SSH connection to device specified using PyATS
        Parameters:
            None, uses connection details from task_config 
        Results:
            True: if connection attempt is successful
            False otherwise
        """
        testbed_config = {
            "devices": {
                self._name: {
                    "credentials": {
                        "default": {
                            "username": self._device_config['username'],
                            "password": self._device_config['password']
                        }
                    },
                    "connections": {
                        "cli": {
                            "ip": self._device_config['address'],
                            "port": self._device_config['port'],
                            "protocol": self._device_config['connection'],
                            # Set default ssh options value as some devices will not work without specifying one
                            "ssh_options": "-o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa"
                        }
                    },
                    "os": self._device_config['os_type']
                }
            }
        }
        # Insert optional ssh_options
        if 'ssh_options' in self._device_config:
            testbed_config['devices'][self._name]['connections']['cli']['ssh_options'] = self._device_config['ssh_options']
        logging.debug(testbed_config)

        # Insert decrypted password
        testbed_config['devices'][self._name]['credentials']['default']['password'] = decrypt(
            self._device_config['password'], self._device_config['key'])
        # DO NOT log decrypted password!

        testbed = topology.loader.load(testbed_config)
        self._connection = testbed.devices[self._name]

        try:
            self._connection.connect(log_stdout = False,
                                     goto_enable = False,
                                     init_exec_commands=['terminal length 0'],
                                     init_config_commands=[],
                                     connection_timeout=self._device_config['timeout'])
        except:
            self._connection = None
            return False
        
        logging.debug(self._connection)
        return True

    def execute(self, commands):
        """
        Executes given CLI commands on the connected device
        Parameters:
            commands: Device specific CLI commands to run
        Returns:
            Dictionary of command run results
            On failure to run any command, only that specific command result is set to empty
            But if any exception is encountered at any time, None is returned
        """
        if self._connection is None:
            return None

        try:
            timeout = self._device_config['timeout']
            result = {}
            for cmd in commands.keys():
                
                # first, try running the given command
                logging.info(f"{self._name} Running command {commands[cmd]}")
                try:
                    result[cmd] = self._connection.execute(command=commands[cmd], timeout = timeout)
                    logging.debug(result[cmd])
                except:
                    logging.error(
                        f"{self._name} Failed to run command {commands[cmd]}")
                    result[cmd] = ""

                # if that failed, and is an admin command, try alternate form without admin
                if (commands[cmd][0:6] == "admin ") and self._is_empty_show_result(result[cmd]):
                    new_cmd = commands[cmd][6:]
                    logging.info(
                        f"{self._name} Running alternate command {new_cmd}")
                    try:
                        result[cmd] = self._connection.execute(command = new_cmd, timeout = timeout)
                        logging.debug(result[cmd])
                    except:
                        logging.error(f"Failed to run command {new_cmd}")
            logging.debug(result)
            return result
        except:
            logging.error(
                f"{self._name} Failed to run commands")
            return None

    def disconnect(self):
        """
        Overrides baseclass disconnect() method
        Disconnects from the device and cleans up
        called by connector component
        Parameters:
            None
        Returns:
            None
        """
        if self._connection is not None:
            logging.info(f"{self._name} Disconnecting from device")
            self._connection.disconnect()
        self._connection = None

    def _is_empty_show_result(self, show_result):
        """
        Checks if the show command result is empty, typically for "admin show ..." form
        Parameters:
            show_result (string): show command result
        Returns:
            True: if result contains warnings and no meaningful data

        """
        show_result = show_result.lower()
        if len(show_result) < 150:
            return True
        if ("warning" in show_result and "deprecated" in show_result):
            return True
        return False
