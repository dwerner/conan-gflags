from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

class glogConan(ConanFile):
    name = "glog"
    version = "0.3.4"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url="http://github.com/dwerner/conan-glog"
    license="https://www.apache.org/licenses/LICENSE-2.0"
    exports="FindGlog.cmake"
    zip_name = "v%s.tar.gz" % version
    unzipped_name = "glog-%s" % version

    def source(self):
        url = "https://github.com/google/glog/archive/%s" % self.zip_name
        download(url, self.zip_name)
        unzip(self.zip_name)
        os.unlink(self.zip_name)

    def build(self):
        self.run("cd %s && ./configure --prefix=`pwd`/../build && make && make install" % self.unzipped_name)

    def package(self):
        # Copy findglog script into project
        self.copy("FindGlog.cmake", ".", ".")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src="build/include", keep_path=True)

        libdir = "build/lib"
        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)      
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['glog']
