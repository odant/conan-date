# HowardHinnant/date Conan package
# Dmitriy Vetutnev, ODANT 2018

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory(src)
