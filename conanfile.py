# HowardHinnant/date Conan package
# Dmitriy Vetutnev, ODANT 2018


from conans import ConanFile, CMake, tools


class DateConan(ConanFile):
    name = "date"
    version = "3.0.0+0"
    license = "MIT License https://raw.githubusercontent.com/HowardHinnant/date/master/LICENSE.txt"
    description = "A date and time library based on the C++11/14/17 <chrono> header "
    url = "https://github.com/odant/conan-date"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86_64", "x86", "mips", "armv7"]
    }
    options = {
        "with_unit_tests": [False, True],
    }
    default_options = "with_unit_tests=False"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "tzdata/*", "build.patch", "fix_check_stdc++17.patch"
    no_copy_source = True
    build_policy = "missing"
    build_type = None

    def configure(self):
        # Only C++11
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")

    def source(self):
        tools.patch(patch_file="build.patch")
        tools.patch(patch_file="fix_check_stdc++17.patch")

    def build(self):
        self.build_type = "RelWithDebInfo" if self.settings.build_type == "Release" else "Debug"
        cmake = CMake(self, build_type=self.build_type)
        cmake.verbose = True
        #
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE:BOOL"] = "ON"
        cmake.definitions["BUILD_SHARED_LIBS:BOOL"] = "OFF"
        #
        cmake.definitions["USE_SYSTEM_TZ_DB:BOOL"] = "OFF"
        cmake.definitions["USE_TZ_DB_IN_DOT:BOOL"] = "OFF"
        cmake.definitions["ENABLE_DATE_TESTING:BOOL"] = "ON" if self.options.with_unit_tests else "OFF"
        cmake.definitions["BUILD_TZ_LIB:BOOL"] = "ON"
        #
        cmake.configure()
        cmake.build()
        if self.options.with_unit_tests:
            cmake.build(target="testit")
            if self.settings.os == "Windows":
                self.run("ctest --build-config %s" % self.build_type)
            else:
                self.run("ctest")

    def package(self):
        self.copy("*.h", dst="include", src="src/include", keep_path=True)
        self.copy("libdate-tz.a", dst="lib", src="lib", keep_path=False)
        self.copy("date-tz.lib", dst="lib", src="lib", keep_path=False)
        self.copy("date-tz.pdb", dst="lib", src="lib", keep_path=False)
        self.copy("date-tz.pdb", dst="lib", src="src/date-tz.dir/%s" % self.build_type, keep_path=False)
        self.copy("*", dst="tzdata", src="tzdata", keep_path=False)

    def package_id(self):
        self.info.options.with_unit_tests = "any"

    def package_info(self):
        self.cpp_info.libs = ["date-tz"]
        if self.settings.os != "Windows":
            self.cpp_info.libs.extend(["pthread"])
        self.cpp_info.defines = [
            "USE_OS_TZDB=0",
            "HAS_REMOTE_API=0",
            "AUTO_DOWNLOAD=0"
        ]
