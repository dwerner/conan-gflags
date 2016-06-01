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
    license="https://www.apache.org/licenses/LICENSE-2.0"
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
        self.run("cmake %s/%s %s" % (self.conanfile_directory, self.unzipped_name, cmake.command_line))
        self.run("cmake -DCMAKE_CXX_FLAGS=\"-D_GLIBCXX_USE_CXX11_ABI=0\" --build . %s" % cmake.build_config)

    def package(self):
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
