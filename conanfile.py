from conans import ConanFile, CMake, tools
import os

class clpConan(ConanFile):
    name = "Clp"
    version = "1.17.5"
    description = "Open-Source Linear Programming Solver"
    license = "Eclipse Public License - v1.0"
    author = "Michael Gardner mhgardner@unr.edu"
    url = "https://github.com/coin-or/Clp"
    settings = {"os": ["Linux", "Macos"], "build_type": None, "compiler": None, "arch": ["x86_64"]}
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    build_policy = "missing"

    # Custom attributes
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _install_subfolder = "install_subfolder"
    
    def source(self):
       git = tools.Git(folder=self._build_subfolder)
       git.clone("https://github.com/shellshocked2003/Coin-Clp.git", "master")
    
    def build(self):
        # Build using coinbrew script        
        if self.options.shared:
            self.run(self._build_subfolder + "/coinbrew.sh build Clp:releases/1.17.5 --test --verbosity 2 --prefix=" + self._install_subfolder)
        else:
            self.run(self._build_subfolder + "/coinbrew.sh build Clp:releases/1.17.5 --fully-static --test --verbosity 2 --prefix=" + self._install_subfolder)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy("*.h", dst="include", src=self._install_subfolder + "/include")
        self.copy("*.hpp", dst="include", src=self._install_subfolder + "/include")        
        self.copy("*.tcc", dst="include", src=self._install_subfolder + "/include")

        self.copy("*.dll", dst="bin", src=self._install_subfolder + "/bin")
        self.copy("*.lib", dst="lib", src=self._install_subfolder + "/lib")
        self.copy("*.so", dst="lib", src=self._install_subfolder + "/lib")
        self.copy("*.dylib", dst="lib", src=self._install_subfolder + "/lib")
        self.copy("*.a", dst="lib", src=self._install_subfolder + "/lib")
        self.copy("*.la", dst="lib", src=self._install_subfolder + "/lib")        

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ['include']
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        # Add to path so shared objects can be found        
        if self.options.shared:
            self.env_info.PATH.append(os.path.join(self.package_folder, "lib"))
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))                        
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
            self.env_info.DYLD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
