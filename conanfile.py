#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "glad"
    version = "0.1.16a0"
    url = "https://github.com/p-groarke/conan-glad"
    description = "Multi-Language GL/GLES/EGL/GLX/WGL Loader-Generator based on the official specs."

    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "profile": ["compatibility", "core"], # OpenGL profile.
        "api_type": "ANY", # API type like "gl, gles"
        "api_version": "ANY", # API version like "3.2, 4.1", no version means latest
        "extensions": "ANY", # Path to extensions file or comma separated list of extensions, if missing all extensions are included
        "spec": ["gl", "egl", "glx", "wgl"], # Name of the spec
        "no_loader": [True, False] # No loader
    }

    default_options = (
        "profile=compatibility",
        "api_type=gl",
        "api_version=3.2",
        "extensions=",
        "spec=gl",
        "no_loader=False"
    )

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        source_url = "https://github.com/Dav1dde/glad"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)


    def build(self):
        cmake = CMake(self)
        cmake.definitions["GLAD_PROFILE"] = self.options.profile
        cmake.definitions["GLAD_API"] = "%s=%s" % (self.options.api_type, self.options.api_version)
        cmake.definitions["GLAD_EXTENSIONS"] = self.options.extensions
        cmake.definitions["GLAD_SPEC"] = self.options.spec
        cmake.definitions["GLAD_NO_LOADER"] = self.options.no_loader
        cmake.definitions["GLAD_GENERATOR"] = "c"
        cmake.definitions["GLAD_EXPORT"] = True
        cmake.definitions["GLAD_INSTALL"] = True
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
