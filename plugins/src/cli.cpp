// plugins/src/cli.cpp
#include "plugins.h"
#include <iostream>

int main(int argc, char *argv[]) {
    quark::Plugins::smoke_test();

    std::cout << "Command-line arguments:" << std::endl;
    for (int i = 0; i < argc; ++i) {
        std::cout << "  " << argv[i] << std::endl;
    }

    return 0;
}
