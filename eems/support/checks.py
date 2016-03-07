# -*- coding: utf-8 -*-
"""
Checks module provides functions to check sensor requirements.
"""

import logging


class Check(object):
    def __init__(self):
        """Public class *Check* provides functions to validate system
        configuration enabling DS18B20 sensors.

        :return:
            Returns an object providing the public functions *w1_config* and
            *w1_modules*.
        """
        self.logger = logging.getLogger(__name__)
        self.dir_modules = '/etc/modules'
        self.dir_config = '/boot/config.txt'
        self.flag = {'w1-therm': False,
                     'w1-gpio': False}

    def w1_config(self):
        """Public function *w1_config* checks the config.txt file for the
        entry *dtoverlay=w1-gpio*.

        :return:
            Returns *True* if check passed. Otherwise *False*.
        """
        return self.__w1_config()

    def __w1_config(self, quiet=None):
        """Private function *__w1_config* checks the config.txt file for the
        entry *dtoverlay=w1-gpio*.

        :param quiet:
            Expects the boolean *True* or *None*. If *quiet=True*, all outputs
            of the function *w1_config* are disabled.
        :return:
            Returns *True* if check passed. Otherwise *False*.
        """
        if quiet is True:
            self.logger.disabled = True
        try:
            with open(self.dir_config, 'r') as config_file:
                config = config_file.readlines()
        except IOError as e:
            self.logger.error('{}'.format(e))
        else:
            check = [c for c in config if c.strip('\n')[:17] ==
                     'dtoverlay=w1-gpio']
            if len(check) == 0:
                self.logger.error('Config.txt check failed: "dtoverlay=w1-gpio"'
                             ' is not set')
                self.logger.info('Please use the command script <sudo eems '
                            'prepare> to prepare "/boot/config.txt"')
                return False
            else:
                self.logger.info('Config.txt check ok: "dtoverlay=w1-gpio" is set')
                return True

    def w1_modules(self):
        """Public function *w1_modules* checks the file */etc/modules* for the
        entries *w1-therm* and *w1-gpio*.

        :return:
            Returns *True* if check passed. Otherwise returns *False*.
        """
        return self.__w1_modules()

    def __w1_modules(self, quiet=None):
        """Private function *__w1_modules* checks the file */etc/modules* for the
        entries *w1-therm* and *w1-gpio*.

        :param quiet:
            Expects the boolean *True* or *None*. If *quiet=True*, all outputs
            of the function *w1_modules* are disabled.
        :return:
            Returns *True* if check passed. Otherwise returns *False*.
        """
        if quiet is True:
            self.logger.disabled = True
        try:
            with open(self.dir_modules, 'r') as modules_file:
                modules = modules_file.readlines()
        except IOError as e:
            self.logger.error('{}'.format(e))
        else:
            check_therm = [c for c in modules if c.strip('\n') == 'w1-therm']
            check_gpio = [c for c in modules if c.strip('\n') == 'w1-gpio']
            if len(check_therm) == 1:
                self.logger.info('Module check ok: "w1-therm" is set')
                self.flag['w1-therm'] = True
            else:
                self.logger.error('Module check failed: "w1-therm" is not set')
            if len(check_gpio) == 1:
                self.logger.info('Module check ok: "w1-gpio" is set')
                self.flag['w1-gpio'] = True
            else:
                self.logger.error('Module check failed: "w1-gpio" is not set')
            if self.flag['w1-therm'] is True and self.flag['w1-gpio'] is True:
                return True
            else:
                self.logger.info('Please use the command script <sudo eems '
                            'prepare> to prepare "/etc/modules"')
                return False

    def w1_prepare(self):
        """Public function *prepare* modifies the files */boot/config.txt* and
        */etc/modules* to enable DS18B20 functionality. Function requires *sudo*
        rights!!!

        :return:
            Returns *None*.
        """
        if self.__w1_config(quiet=True) is False:
            self.logger.disabled = False
            try:
                with open(self.dir_config, 'a') as config_file:
                    config_file.write('dtoverlay=w1-gpio\n')
            except IOError as e:
                self.logger.error('{}'.format(e))
            else:
                self.logger.info('Config.txt has been prepared successfully')
        else:
            self.logger.disabled = False

        if self.__w1_modules(quiet=True) is False:
            self.logger.disabled = False
            try:
                if self.flag['w1-therm'] is False:
                    with open(self.dir_modules, 'a') as modules_file:
                        modules_file.write('w1-therm\n')
                if self.flag['w1-gpio'] is False:
                    with open(self.dir_modules, 'a') as modules_file:
                        modules_file.write('w1-gpio\n')
            except IOError as e:
                self.logger.error('{}'.format(e))
            else:
                self.logger.info('Modules have been prepared successfully')
        else:
            self.logger.disabled = False
