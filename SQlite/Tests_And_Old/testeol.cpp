#include <iostream>

void show_bytes(uint8_t* ptr, int len) {
    for (int i = 0; i < len; i++) {
        std::cout << +*(ptr+i) << " ";
    }
    std::cout << "\n";
}

int main() {
    uint8_t a[] = "\n";
    std::cout << sizeof(a) << "\n";
    show_bytes(&a[0], sizeof(a) / sizeof(char));
    char b[] = "b";
    b[0] = static_cast<uint8_t>(10); // 
    std::cout << "hi" << b << "hi2";
}