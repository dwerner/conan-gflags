from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

class gflagsConan(ConanFile):
    name = "gflags"
    version = "2.1.2"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url="http://github.com/dwerner/conan-gflags"
    license="https://github.com/gflags/gflags/blob/master/COPYING.txt"
    exports="FindGflags.cmake"
    zip_name = "v%s.tar.gz" % version
    unzipped_name = "gflags-%s" % version

    def source(self):
        url = "https://github.com/gflags/gflags/archive/%s" % self.zip_name
        download(url, self.zip_name)
        unzip(self.zip_name)
        os.unlink(self.zip_name)

    def build(self):
        cmake = CMake(self.settings)
        c1 ="cmake -DCMAKE_CXX_FLAGS=\"-D_GLIBCXX_USE_CXX11_ABI=0 -std=c++0x\" %s/%s %s" % (self.conanfile_directory, self.unzipped_name, cmake.command_line)
        self.run(c1)
        c2 = "cmake --build . %s" % cmake.build_config
        self.run(c2)
        

    def package(self):

        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copy findgflags script into project
        self.copy("FindGflags.cmake", ".", ".")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src="include", keep_path=True)

        libdir = "lib"
        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)      
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['gflags']
