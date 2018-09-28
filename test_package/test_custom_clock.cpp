//#include <date/date.h>
#include <date/tz.h>
#include <iostream>
#include <cstdlib>


#include <chrono>

namespace oda {

struct Clock
{
    using rep = int64_t;
    using period = std::nano; // 1 tick equal 1ns
    using duration = std::chrono::duration<rep, period>;
    using time_point = std::chrono::time_point<std::chrono::system_clock, duration>;

    static constexpr bool is_steady = false;

    static time_point now() noexcept {
        const auto ticks = getTicks();
        return time_point{duration{ticks}};
    }

private:
    static int64_t getTicks() noexcept;
};

} // namespace oda

using date::operator<<;

int main(int, char**) {
    const auto tSys = std::chrono::system_clock::now();
    std::cout << "std::chrono::system_clock::now(): " << tSys << std::endl;

    const auto tOda = oda::Clock::now();
    std::cout << "oda::Clock::now(): " << tOda << std::endl;

    date::set_install("tzdata_dir");
    date::reload_tzdb();
    const auto t = date::make_zoned(date::current_zone(), tOda);
    std::cout << "Date/time with current TZ: " << t << std::endl;

    return EXIT_SUCCESS;
}


#ifdef _WIN32 // Windows implementation

#ifndef WIN32_LEAN_AND_MEAN
#   define WIN32_LEAN_AND_MEAN
#endif
#include <Windows.h>

namespace oda {

static constexpr int64_t epoch = 116444736000000000LL;
int64_t Clock::getTicks() noexcept {
    FILETIME ft;
    ::GetSystemTimeAsFileTime(&ft);
    const int64_t winTicks = (static_cast<int64_t>(ft.dwHighDateTime) << 32) + static_cast<int64_t>(ft.dwLowDateTime);
    return (winTicks - epoch) * 100LL;
}

} // namespace oda
#endif // _WIN32
