# conan-gflags

[Conan.io](https://conan.io) package for gflags library

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py
    
## Upload packages to server

    $ conan upload gflags/2.1.2@dwerner/testing --all
    
## Reuse the packages

### Basic setup

    $ conan install gflags/2.1.2@dwerner/testing
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    gflags/2.1.2@dwerner/testing

    [options]
    gflags:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
