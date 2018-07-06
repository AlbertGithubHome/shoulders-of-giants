#define __CLIENT__
#include "common.h"

// IO多路复用select
void start_select(int client_fd);
// fd变化处理函数
void handle_fd_changed(fd_set *p_read_set, fd_set *p_error_set, int client_fd, char *buffer);
// 处理读数据
void do_read(int fd, int client_fd, char *buffer);
// 处理服务器断开连接
void do_disconnect(int fd);

int main(int argc, char *argv[])
{
    // 创建客户端套接字
    int client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (-1 == client_fd)
    {
        printf("<client>create client socket error!\n");
        exit(1);
    }

    // 设置服务器IP和Port
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr    = inet_addr(SERVER_IP);
    //inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    // 开始连接
    if (-1 == connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)))
    {
        printf("<client>connect server error!\n");
        exit(1);
    }
    else
    {
        printf("<client>client[%d] connect server success!\n", client_fd);
    }

    // 开启IO多路复用
    start_select(client_fd);

    close(client_fd);
    return 0;
}

void start_select(int client_fd)
{
    char buffer[BUFFER_SIZE] = {0};
    int ready_count;
    fd_set read_set;
    fd_set error_set;

    while(true)
    {
        // 清空原描述符
        FD_ZERO(&read_set);
        FD_ZERO(&error_set);

        FD_SET(STDIN_FILENO, &read_set);
        FD_SET(STDIN_FILENO, &error_set);
        FD_SET(client_fd, &read_set);
        FD_SET(client_fd, &error_set);

        // linux 版本的第一参数应该为检测描述符中最大的一个加1
        ready_count = select(client_fd + 1, &read_set, NULL, &error_set, NULL);
        if (ready_count > 0)
        {
            handle_fd_changed(&read_set, &error_set, client_fd, buffer);
        }
    }
}

void handle_fd_changed(fd_set *p_read_set, fd_set *p_error_set, int client_fd, char *buffer)
{
    if (FD_ISSET(client_fd, p_read_set))
    {
        do_read(client_fd, client_fd, buffer);
    }
    else if (FD_ISSET(client_fd, p_error_set))
    {
        do_disconnect(client_fd);
    }

    if (FD_ISSET(STDIN_FILENO, p_read_set))
    {
        do_read(STDIN_FILENO, client_fd, buffer);
    }
}

void do_read(int fd, int client_fd, char *buffer)
{
    //printf("do read[%d]\n", fd);
    int read_count = read(fd, buffer, BUFFER_SIZE);
    //int read_count = recv(fd, buffer, BUFFER_SIZE, MSG_NOSIGNAL);// 返回-1
    if (-1 == read_count)
    {
        //printf("accept error[%d] %s\n", errno, strerror(errno));
        printf("<client>read server msg error!\n");
        close(fd);
        exit(1);
    }
    else if (0 == read_count)
    {
        printf("<client>client[%d] close, no data!\n", fd);
        printf("<client>server closed, client to exit!\n");
        close(fd);
        exit(1);
    }
    else
    {
        //printf("my msg: %s", buffer);
        buffer[read_count] = '\0';
        if (fd == STDIN_FILENO)
        {
            int write_count = send(client_fd, buffer, strlen(buffer), MSG_NOSIGNAL);
            if (-1 == write_count)
            {
                printf("<client>client[%d] write error!\n", client_fd);
                close(client_fd);
                exit(1);
            }
        }
        else
        {
            printf("<client>receive server response:%s", buffer);
        }
    }
}

void do_disconnect(int fd)
{
    printf("<server>client[%d] disconnect!\n", fd);
    close(fd);
    exit(1);
}
