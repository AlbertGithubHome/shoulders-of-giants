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
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family      = AF_INET;
    server_addr.sin_port        = htons(8899);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    bind(listen_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    listen(listen_fd, 10);

    printf("<server>server[ip:%s, port:%d] is running...\n", "127.0.0.1", 8899);

    socklen_t len = sizeof(server_addr);
    int client_fd = accept(listen_fd, (struct sockaddr *)&server_addr, &len);

    while(1)
    {
        char recv_buffer[2048] = {0};
        int ret = recv(client_fd, recv_buffer, sizeof(recv_buffer) - 1, 0);
        printf("ret is %d\n", ret);

        if (ret == 0)
        {
            ret = send(client_fd, recv_buffer, strlen(recv_buffer), 0);
            printf("after client close fd, send ret is %d\n", ret);
            break;
        }
        else if (ret < 0)
            break;

        //getchar();
        //close(client_fd);
        
    }

    close(listen_fd);
    return 0;
}