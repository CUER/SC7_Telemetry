#include <stdint.h>
#include <cstring>
#include <iostream>

#define SEND_DATA_LEN 4

float send_data[] = {3,4,5,6};
uint8_t send_buffer[4*SEND_DATA_LEN + 1]; //assuming sizeof(float)=4

// dummy declarations to get rid of disgusting squiggly red lines
void HAL_UART_Transmit(int* uart_object, uint8_t* ptr, int len, int timeout);
int huart;

void show_bytes(uint8_t* ptr, int len) {
    for (int i = 0; i < len; i++) {
        std::cout << +*(ptr+i) << " ";
    }
    std::cout << "\n";
}

int main() {
    if (sizeof(float) != 4) {
        // send error message
        return 1;
    }
    memcpy(send_buffer, send_data, 4*SEND_DATA_LEN);
    send_buffer[4*SEND_DATA_LEN] = 10;

    show_bytes(send_buffer, 4*SEND_DATA_LEN+1);
    // HAL_UART_Transmit(&huart, send_buffer, sizeof(send_buffer) / 4, 100);

    // HAL send command, set start pointer as reinterpret_cast<uint8_t*>(send_buffer)
    // HAL send command, EOL byte
}