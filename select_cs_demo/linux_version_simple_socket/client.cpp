#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <sys/epoll.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char *argv[])
{
    int client_fd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family      = AF_INET;
    server_addr.sin_port        = htons(8899);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));

    while(1)
    {
        char senf_buffer[64] = "this is client message!";
        int ret = send(client_fd, senf_buffer, strlen(senf_buffer), 0);
        printf("1:send size is %d, ret is %d\n", strlen(senf_buffer), ret);

        // close(client_fd);
        // ret = recv(client_fd, senf_buffer, sizeof(senf_buffer) - 1, 0);
        // printf("after client close fd, client receive ret is %d\n", ret);

        // ret = send(client_fd, senf_buffer, strlen(senf_buffer), 0);
        // printf("2:send size is %d, ret is %d\n", strlen(senf_buffer), ret);
        getchar();
    }

    close(client_fd);
    return 0;
}