from conans import ConanFile, CMake, tools
import os

required_conan_version = ">=1.36.0"

class MsgpackCConan(ConanFile):
    name = "msgpack-c"
    description = "MessagePack implementation for C"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/msgpack/msgpack-c"
    topics = ("msgpack", "message-pack", "serialization")
    license = "BSL-1.0"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    settings = "os", "arch", "build_type", "compiler"
    options = {
        "fPIC": [True, False],
        "shared": [True, False],
    }
    default_options = {
        "fPIC": True,
        "shared": False,
    }

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
            destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["MSGPACK_ENABLE_SHARED"] = self.options.shared
        self._cmake.definitions["MSGPACK_ENABLE_STATIC"] = not self.options.shared
        self._cmake.definitions["MSGPACK_32BIT"] = self.settings.arch == "x86"
        self._cmake.definitions["MSGPACK_BUILD_EXAMPLES"] = False
        self._cmake.definitions["MSGPACK_BUILD_TESTS"] = False
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE_1_0.txt", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.filenames["cmake_find_package"] = "msgpack-c"
        self.cpp_info.filenames["cmake_find_package_multi"] = "msgpack-c"
        self.cpp_info.set_property("cmake_file_name", "msgpack-c")
        self.cpp_info.names["cmake_find_package"] = "msgpack"
        self.cpp_info.names["cmake_find_package_multi"] = "msgpack"
        self.cpp_info.set_property("cmake_target_name", "msgpack")
        self.cpp_info.components["msgpack"].names["cmake_find_package"] = "msgpack-c"
        self.cpp_info.components["msgpack"].names["cmake_find_package_multi"] = "msgpack-c"
        self.cpp_info.components["msgpack"].set_property("cmake_target_name", "msgpack-c")
        self.cpp_info.components["msgpack"].set_property("pkg_config_name", "msgpack")
        self.cpp_info.components["msgpack"].libs = ["msgpackc"]