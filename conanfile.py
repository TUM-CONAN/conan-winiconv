#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, CMake

class WiniconvConan(ConanFile):
    name = "winiconv"
    upstream_version = "0.0.8"
    package_revision = "-r2"
    version = "{0}{1}".format(upstream_version, package_revision)

    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "https://git.ircad.fr/conan/conan-winiconv"
    license = "win_iconv is placed in the public domain."
    description = "iconv implementation using Win32 API to convert."

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        self.requires("common/1.0.0@sight/stable")

    def source(self):
        winiconv_name = "winiconv-%s.tar.gz" % self.upstream_version
        tools.download("https://github.com/win-iconv/win-iconv/archive/v{0}.tar.gz".format(self.upstream_version), winiconv_name)
        tools.unzip(winiconv_name)
        os.unlink(winiconv_name)

    def build(self):
        #Import common flags and defines
        import common
        iconv_source_dir = os.path.join(self.source_folder, "win-iconv-{0}".format(self.upstream_version))
        cmake = CMake(self)
        
        #Set common flags
        cmake.definitions["CMAKE_C_FLAGS"] = common.get_c_flags()
        cmake.definitions["CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        
        cmake.configure(source_folder=iconv_source_dir)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
