# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Erik Johnson (erik@saltstack.com)`
    tests.integration.states.npm
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
# Import Python libs
from __future__ import absolute_import
from distutils.version import LooseVersion

# Import Salt Testing libs
from salttesting import skipIf
from salttesting.helpers import destructiveTest, ensure_in_syspath
ensure_in_syspath('../../')

# Import salt libs
import integration
import salt.utils
import salt.modules.cmdmod as cmd

MAX_NPM_VERSION = '5.0.0'


@skipIf(salt.utils.which('npm') is None, 'npm not installed')
class NpmStateTest(integration.ModuleCase, integration.SaltReturnAssertsMixIn):

    @destructiveTest
    def test_npm_installed_removed(self):
        '''
        Basic test to determine if NPM module was successfully installed and
        removed.
        '''
        ret = self.run_state('npm.installed', name='pm2')
        self.assertSaltTrueReturn(ret)
        ret = self.run_state('npm.removed', name='pm2')
        self.assertSaltTrueReturn(ret)

    @destructiveTest
    def test_npm_install_url_referenced_package(self):
        '''
        Determine if URL-referenced NPM module can be successfully installed.
        '''
        ret = self.run_state('npm.installed', name='request/request#v2.81.1')
        self.assertSaltTrueReturn(ret)
        ret = self.run_state('npm.removed', name='git://github.com/request/request')
        self.assertSaltTrueReturn(ret)

    @destructiveTest
    def test_npm_installed_pkgs(self):
        '''
        Basic test to determine if NPM module successfully installs multiple
        packages.
        '''
        ret = self.run_state('npm.installed', name=None, pkgs=['pm2', 'grunt'])
        self.assertSaltTrueReturn(ret)

    @skipIf(salt.utils.which('npm') and LooseVersion(cmd.run('npm -v')) >= LooseVersion(MAX_NPM_VERSION),
            'Skip with npm >= 5.0.0 until #41770 is fixed')
    @destructiveTest
    def test_npm_cache_clean(self):
        '''
        Basic test to determine if NPM successfully cleans it's cached packages.
        '''
        ret = self.run_state('npm.cache_cleaned', name=None, force=True)
        self.assertSaltTrueReturn(ret)


if __name__ == '__main__':
    from integration import run_tests
    run_tests(NpmStateTest)
