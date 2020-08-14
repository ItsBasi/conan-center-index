from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class KokkosConan(ConanFile):
    name = "kokkos"
    description = "Kokkos Core implements a programming model in C++ for writing "
    "performance portable applications targeting all major HPC platforms."
    topics = ("conan", "kokkos", "HPC")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/kokkos/kokkos"
    license = "BSD-3-Clause"
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    _cmake = None

    requires = (
        "pthreads4w/3.0.0",
    )
    
    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        print("")

    def configure(self):
        print("")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        self.run("git clone file:///D:/Repositories/kokkos " + self._source_subfolder)
        self.run("git -C " + self._source_subfolder + " checkout conan-patches/3.1.01")
        #tools.get(**self.conan_data["sources"][self.version])
        #extracted_dir = self.name + "-" + self.version
        #os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["Kokkos_ENABLE_PTHREAD"] = True
            self._cmake.definitions["Kokkos_ENABLE_LIBDL"] = False
            self._cmake.definitions["Kokkos_ENABLE_PROFILING"] = False
            self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        #for patch in self.conan_data["patches"][self.version]:
        #    tools.patch(base_path=self._source_subfolder, **patch)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses",
                  src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
