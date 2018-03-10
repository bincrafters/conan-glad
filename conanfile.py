#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GladConan(ConanFile):
    name = "glad"
    version = "0.1.16a0"
    description = "Multi-Language GL/GLES/EGL/GLX/WGL Loader-Generator based on the official specs."
    url = "https://github.com/bincrafters/conan-glad"
    homepage = "https://github.com/Dav1dde/glad"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "cmake.patch"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "profile": ["compatibility", "core"], # OpenGL profile.
        "api_type": "ANY", # API type like "gl, gles"
        "api_version": "ANY", # API version like "3.2, 4.1", no version means latest
        "extensions": "ANY", # Path to extensions file or comma separated list of extensions, if missing all extensions are included
        "spec": ["gl", "egl", "glx", "wgl"], # Name of the spec
        "no_loader": [True, False] # No loader
    }

    default_options = (
        "shared=False",
        "fPIC=True",
        "profile=compatibility",
        "api_type=gl",
        "api_version=3.2",
        "extensions=",
        "spec=gl",
        "no_loader=False"
    )

    def source(self):
        source_url = "https://github.com/Dav1dde/glad"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Temporary patch, fixed in glad master (support shared lib).
        tools.patch(base_path=extracted_dir, patch_file="cmake.patch")

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

        cmake.definitions["GLAD_PROFILE"] = self.options.profile
        cmake.definitions["GLAD_API"] = "%s=%s" % (self.options.api_type, self.options.api_version)
        cmake.definitions["GLAD_EXTENSIONS"] = self.options.extensions
        cmake.definitions["GLAD_SPEC"] = self.options.spec
        cmake.definitions["GLAD_NO_LOADER"] = self.options.no_loader

        if self.settings.build_type == "Release":
            cmake.definitions["GLAD_GENERATOR"] = "c"
        else:
            cmake.definitions["GLAD_GENERATOR"] = "c-debug"

        cmake.definitions["GLAD_EXPORT"] = True
        cmake.definitions["GLAD_INSTALL"] = True
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        cmake.install()
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("dl")
