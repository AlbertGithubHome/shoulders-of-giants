#include "myadd.h"
#include "mysub.h"
#include <iostream>

int main() {
    std::cout << "happy birthday!" << std::endl;
    std::cout << "519 + 1 = " << add(519, 1) << std::endl;
    std::cout << "1320 - 6 = " << sub(1320, 6) << std::endl;
    return 0;
}