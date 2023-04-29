#include <iostream>

void show_bytes(uint8_t* ptr, int len) {
    for (int i = 0; i < len; i++) {
        std::cout << +*(ptr+i) << " ";
    }
    std::cout << "\n";
}

int main() {
    uint8_t buffer[] = {0,0,0,0,0,0};
    std::cout << sizeof(float);
    float float1 = 12.0;
    float float2 = 13.0;
    float float3 = 14.0;

    // buffer[3] = float1;
    show_bytes(buffer, 24);
}