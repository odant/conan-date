# Test for HowardHinnant/date Conan package
# Dmitriy Vetutnev, ODANT, 2018


project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)


enable_testing()


# Conan imported targets

add_executable(test_tz_CONAN_PKG test_tz.cpp)
target_link_libraries(test_tz_CONAN_PKG CONAN_PKG::date)
set_target_properties(test_tz_CONAN_PKG
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_tz_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_tz_CONAN_PKG
)

add_executable(test_custom_clock_CONAN_PKG test_custom_clock.cpp)
target_link_libraries(test_custom_clock_CONAN_PKG CONAN_PKG::date)
set_target_properties(test_custom_clock_CONAN_PKG
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_custom_clock_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_custom_clock_CONAN_PKG
)
