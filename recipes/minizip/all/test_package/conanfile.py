from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CONAN_MZ_VERSION"] = self.requires["minizip"].ref.version
        if self.options["minizip"].compress:
            cmake.definitions["HAVE_COMPRESS"] = "HAVE_COMPRESS"
        if self.options["minizip"].decompress:
            cmake.definitions["HAVE_DECOMPRESS"] = "HAVE_DECOMPRESS"
        if self.options["minizip"].with_bzip2:
            cmake.definitions["HAVE_BZIP2"] = "HAVE_BZIP2"
        if self.options["minizip"].with_zlib:
            cmake.definitions["HAVE_ZLIB"] = "HAVE_ZLIB"
        if self.options["minizip"].with_lzma:
            cmake.definitions["HAVE_LZMA"] = "HAVE_LZMA"
        if self.options["minizip"].with_zstd:
            cmake.definitions["HAVE_ZSTD"] = "HAVE_ZSTD"
        if self.options["minizip"].compat:
            cmake.definitions["HAVE_COMPAT"] = "HAVE_COMPAT"
        if self.options["minizip"].pkcrypt:
            cmake.definitions["HAVE_PKCRYPT"] = "HAVE_PKCRYPT"
        if self.options["minizip"].wzaes:
            cmake.definitions["HAVE_WZAES"] = "HAVE_WZAES"
        if self.options["minizip"].wzaes or self.options["minizip"].pkcrypt:
            cmake.definitions["HAVE_ENCRYPTION"] = "HAVE_ENCRYPTION"
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path, run_environment=True)
