#include <date/date.h>
#include <iostream>
#include <cstdlib>

using namespace date;

int main(int, char**) {
    const auto t = std::chrono::system_clock::now();
    std::cout << "Now: " << t << std::endl;
    return EXIT_SUCCESS;
}