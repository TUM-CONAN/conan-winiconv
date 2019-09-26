#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from conans import ConanFile, tools, CMake


class WiniconvConan(ConanFile):
    name = "winiconv"
    upstream_version = "0.0.8"
    package_revision = "-r3"
    version = "{0}{1}".format(upstream_version, package_revision)

    generators = "cmake"
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url = "https://git.ircad.fr/conan/conan-winiconv"
    license = "win_iconv is placed in the public domain."
    description = "iconv implementation using Win32 API to convert."
    source_subfolder = "source_subfolder"
    short_paths = True

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        self.requires("common/1.0.1@sight/stable")

    def source(self):
        tools.get("https://github.com/win-iconv/win-iconv/archive/v{0}.tar.gz".format(self.upstream_version))
        os.rename("win-iconv-" + self.upstream_version, self.source_subfolder)

    def build(self):
        # Import common flags and defines
        import common

        # Generate Cmake wrapper
        common.generate_cmake_wrapper(
            cmakelists_path='CMakeLists.txt',
            source_subfolder=self.source_subfolder,
            build_type=self.settings.build_type
        )

        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
