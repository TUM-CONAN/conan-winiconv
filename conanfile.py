#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, CMake

class WiniconvConan(ConanFile):
    name = "winiconv"
    version = "0.0.8"
    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "https://gitlab.lan.local/conan/conan-winiconv"
    license = "win_iconv is placed in the public domain."
    description = "iconv implementation using Win32 API to convert."

    def source(self):
        winiconv_name = "winiconv-%s.tar.gz" % self.version
        tools.download("https://github.com/win-iconv/win-iconv/archive/v{0}.tar.gz".format(self.version), winiconv_name)
        tools.unzip(winiconv_name)
        os.unlink(winiconv_name)

    def build(self):
        iconv_source_dir = os.path.join(self.source_folder, "win-iconv-{0}".format(self.version))
        cmake = CMake(self)
        cmake.configure(source_folder=iconv_source_dir)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
