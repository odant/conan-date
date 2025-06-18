# HowardHinnant/date Conan package
# Dmitriy Vetutnev, ODANT 2018


from conan import ConanFile, tools
import os

class DateConan(ConanFile):
    name = "date"
    version = "3.0.4+0"
    license = "MIT License https://raw.githubusercontent.com/HowardHinnant/date/master/LICENSE.txt"
    description = "A date and time library based on the C++11/14/17 <chrono> header "
    url = "https://github.com/odant/conan-date"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "ninja": [True, False],
        "with_unit_tests": [False, True],
    }
    default_options = {
        "ninja": True,
        "with_unit_tests": False
    }
    exports_sources = "src/*", "tzdata/*", "build.patch", "fix.patch"
    no_copy_source = True
    build_policy = "missing"
    package_type = "static-library"
    
    def layout(self):
        tools.cmake.cmake_layout(self, src_folder="src")

    def build_requirements(self):
        if self.options.ninja:
            self.tool_requires("ninja/[>=1.12.1]")

    def configure(self):
        # Only C++11
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")

    def source(self):
        tools.files.patch(self, patch_file="build.patch")
        tools.files.patch(self, patch_file="fix.patch")
        
    def generate(self):
        benv = tools.env.VirtualBuildEnv(self)
        benv.generate()
        renv = tools.env.VirtualRunEnv(self)
        renv.generate()
        if tools.microsoft.is_msvc(self):
            vc = tools.microsoft.VCVars(self)
            vc.generate()
        deps = tools.cmake.CMakeDeps(self)    
        deps.generate()
        cmakeGenerator = "Ninja" if self.options.ninja else None
        tc = tools.cmake.CMakeToolchain(self, generator=cmakeGenerator)
        if self.settings.os != "Windows":
            tc.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        tc.variables["BUILD_SHARED_LIBS"] = "OFF"
        #
        tc.variables["USE_SYSTEM_TZ_DB"] = "OFF"
        tc.variables["USE_TZ_DB_IN_DOT"] = "OFF"
        tc.variables["ENABLE_DATE_TESTING"] = "ON" if self.options.with_unit_tests else "OFF"
        tc.variables["MANUAL_TZ_DB"] = "ON"
        tc.variables["BUILD_TZ_LIB"] = "ON"
        tc.generate()

    def build(self):
        cmake = tools.cmake.CMake(self)
        cmake.configure()
        cmake.build()
        if self.options.with_unit_tests:
            cmake.build(target="testit")
            if self.settings.os == "Windows":
                self.run("ctest --build-config %s" % self.build_type)
            else:
                self.run("ctest")

    def package(self):
        tools.files.copy(self, "*.h", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"), keep_path=True)
        tools.files.copy(self, "libdate-tz.a", dst=os.path.join(self.package_folder, "lib"), src=self.build_folder, keep_path=False)
        tools.files.copy(self, "*/libdate-tz.a", dst=os.path.join(self.package_folder, "lib"), src=self.build_folder, keep_path=False)
        tools.files.copy(self, "date-tz.lib", dst=os.path.join(self.package_folder, "lib"), src=self.build_folder, keep_path=False)
        tools.files.copy(self, "*/date-tz.lib", dst=os.path.join(self.package_folder, "lib"), src=self.build_folder, keep_path=False)
        tools.files.copy(self, "date-tz.pdb", dst=os.path.join(self.package_folder, "bin"), src=self.build_folder, keep_path=False)
        tools.files.copy(self, "*/date-tz.pdb", dst=os.path.join(self.package_folder, "bin"), src=self.build_folder, keep_path=False)
        tools.files.copy(self, "*", dst=os.path.join(self.package_folder, "tzdata"), src=os.path.join(self.export_sources_folder, "tzdata"), keep_path=False)

    def package_id(self):
        self.info.options.with_unit_tests = "any"
        self.info.options.ninja = "any"

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "date")
        self.cpp_info.set_property("cmake_target_name", "date::date")
        self.cpp_info.libs = ["date-tz"]
        if self.settings.os != "Windows":
            self.cpp_info.system_libs.extend(["pthread"])
        self.cpp_info.defines = [
            "USE_OS_TZDB=0",
            "HAS_REMOTE_API=0",
            "AUTO_DOWNLOAD=0"
        ]
