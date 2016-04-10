#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from distutils.dist import Distribution
from distutils.command.install import install
from distutils.command.install_scripts import install_scripts

import stat
import os
import taemin


class MyDistribution(Distribution):
    def __init__(self, attrs):
        try:
            os.remove("taemin/config.py")
        except:
            pass

        self.conf_files = []
        self.closed_source = os.path.exists("PKG-INFO")
        Distribution.__init__(self, attrs)

class my_install_scripts(install_scripts):
    def initialize_options (self):
        install_scripts.initialize_options(self)
        self.install_data = None

    def finalize_options(self):
        install_scripts.finalize_options(self)
        self.set_undefined_options('install',
                                   ('install_data', 'install_data'))

    def run(self):
        if not self.skip_build:
            self.run_command('build_scripts')

        self.outfiles = []

        self.mkpath(os.path.normpath(self.install_dir))
        ofile, copied = self.copy_file(os.path.join(self.build_dir, 'taemin'), self.install_dir)
        if copied:
            self.outfiles.append(ofile)

class my_install(install):
    def finalize_options(self):
        if self.prefix:
            self.conf_prefix = self.prefix + "/etc/taemin"
        else:
            self.conf_prefix = "/etc/taemin"

        install.finalize_options(self)

    def get_outputs(self):
        tmp = [ self.conf_prefix + "/taemin.yml" ] + install.get_outputs(self)
        return tmp

    def install_conf(self):
        self.mkpath((self.root or "") + self.conf_prefix)
        for file in self.distribution.conf_files:
            dest = (self.root or "") + self.conf_prefix + "/" + os.path.basename(file)
            if os.path.exists(dest):
                dest += "-dist"
            self.copy_file(file, dest)

    def init_config(self):
        config = open("taemin/config.py", "w")
        config.write("conf_dir = '%s'" % os.path.abspath((self.conf_prefix)))
        config.close()

    def run(self):
        os.umask(0o022)
        self.install_conf()
        self.init_config()
        install.run(self)

        os.chmod((self.root or "") + self.conf_prefix, 0o755)

        if not self.dry_run:
            for filename in self.get_outputs():
                if filename.find(".yml") != -1:
                    continue
                mode = os.stat(filename)[stat.ST_MODE]
                mode |= 0o044
                if mode & 0o0100:
                    mode |= 0o011
                os.chmod(filename, mode)

setup(
    name='taemin',

    version=taemin.__version__,

    packages=find_packages(),

    author="Ningirsu",

    description="Un super bot IRC",

    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://github.com/ningirsu/taemin',

    entry_points = {
        'console_scripts': [
            'taemin = taemin.core:taemin',
        ],
    },
    license="MIT",
    scripts=[ "scripts/taemin"],
    conf_files=[ "conf/taemin.yml" ],
    cmdclass={
                 'install': my_install,
                 'install_scripts': my_install_scripts,
    },
    distclass=MyDistribution
)
