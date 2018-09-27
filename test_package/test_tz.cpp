// Test for HowardHinnant/date Conan package
// Dmitriy Vetutnev, ODANT, 2018


#include <date/tz.h>
#include <iostream>
#include <cstdlib>


int main(int, char**) {
    date::set_install("tzdata_dir");
    date::reload_tzdb();
    const auto t = date::make_zoned(date::current_zone(), std::chrono::system_clock::now());
    std::cout << "Date/time with current TZ: " << t << std::endl;
    return EXIT_SUCCESS;
}