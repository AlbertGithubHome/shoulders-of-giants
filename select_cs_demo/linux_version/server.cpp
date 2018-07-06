#define __SERVER__
#include "common.h"

// IO多路复用select
void start_select(int listen_fd);
// fd变化处理函数
void handle_fd_changed(int *fd_array, fd_set *p_read_set, fd_set *p_error_set, int listen_fd, char *buffer);
// 处理新的客户端接入
void do_accpet(int *fd_array, int listen_fd);
// 处理读数据
void do_read(int *fd_array, int fd, char *buffer);
// 处理客户端断开连接
void do_disconnect(int *fd_array, int fd);
// 改变fd集合
void operate_fd_changed(int *fd_array, int fd, bool is_add);

int main(int argc, char * argv[])
{
    // 创建服务器套接字
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (-1 == listen_fd)
    {
        printf("<server>create server listen socket error!\n");
        exit(1);
    }

    /*一个端口释放后会等待两分钟之后才能再被使用, SO_REUSEADDR是让端口释放后立即就可以被再次使用。*/
    int reuse = 1;
    if (-1 == setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, (const char*)&reuse, sizeof(reuse)))
    {
        printf("<server>setsockopt option SO_REUSEADDR failed!\n");
        exit(1);
    }

    // 设置服务器IP和Port
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family        = AF_INET;
    server_addr.sin_port        = htons(SERVER_PORT);
    //server_addr.sin_addr.s_addr    = INADDR_ANY;   // 可以阻挡其它IP连接进来inet_addr("127.0.0.1");
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);



    // 绑定套接字
    if (-1 == bind(listen_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)))
    {
        printf("<server>bind server socket error!\n");
        exit(1);
    }

    // 监听套接字
    listen(listen_fd, LISTEN_NUM);
    printf("<server>server[ip:%s, port:%d] is running...\n", SERVER_IP, SERVER_PORT);

    // 开始select版本IO多路复用
    start_select(listen_fd);

    close(listen_fd);
    return 0;
}

void start_select(int listen_fd)
{
    int fd_array[FD_MAX_SIZE];
    char buffer[BUFFER_SIZE] = {0};
    int ready_count;
    fd_set read_set;
    fd_set error_set;
    int max_fd;

    for (int index = 0; index < FD_MAX_SIZE; ++index) 
    { 
        fd_array[index] = -1; 
    }

    // 首先添加listen_fd
    fd_array[0] = listen_fd;
    while(true)
    {
        // 清空原描述符
        FD_ZERO(&read_set);
        FD_ZERO(&error_set);
        max_fd = -1;
        for (int index = 0; index < FD_MAX_SIZE; ++index)
        {
            if (fd_array[index] > 0)
            {
                FD_SET(fd_array[index], &read_set);
                FD_SET(fd_array[index], &error_set);
                if (fd_array[index] > max_fd)
                    max_fd = fd_array[index];
            }
        }

        // linux 版本的第一参数应该为检测描述符中最大的一个加1
        ready_count = select(max_fd + 1, &read_set, NULL, &error_set, NULL);
        if (ready_count > 0)
        {
            handle_fd_changed(fd_array, &read_set, &error_set, listen_fd, buffer);
        }
    }
}


void handle_fd_changed(int *fd_array, fd_set *p_read_set, fd_set *p_error_set, int listen_fd, char *buffer)
{
    for (int index = 0; index < FD_MAX_SIZE; index++)
    {
        const int socket_fd = fd_array[index];
        if (socket_fd <= 0)
            continue;

        if (FD_ISSET(socket_fd, p_read_set))
        {
            if (socket_fd == listen_fd)
                do_accpet(fd_array, socket_fd);
            else
                do_read(fd_array, socket_fd, buffer);
        }
        else if (FD_ISSET(socket_fd, p_error_set))
        {
            do_disconnect(fd_array, socket_fd);
        }
    }
}

void do_accpet(int *fd_array, int listen_fd)
{
    struct sockaddr_in client_addr;
    int client_addr_len = sizeof(client_addr);
    int client_fd = accept(listen_fd, (struct sockaddr*)&client_addr, (socklen_t*)&client_addr_len);
    if (-1 == client_fd)
    {
        printf("<server>accpet client error!\n");
        printf("%s\n", strerror(errno)); 
    }
    else
    {
        printf("<server>accept a new client[%d]: %s:%d\n", client_fd, inet_ntoa(client_addr.sin_addr), client_addr.sin_port);
        operate_fd_changed(fd_array, client_fd, true);
    }
}

void do_read(int *fd_array, int fd, char *buffer)
{
    int read_count = recv(fd, buffer, BUFFER_SIZE, MSG_NOSIGNAL);
    if (-1 == read_count)
    {
        printf("<server>read client [%d] msg error!\n", fd);
        close(fd);
        operate_fd_changed(fd_array, fd, false);
    }
    else if (0 == read_count)
    {
        printf("<server>client [%d] close, no data!\n", fd);
        close(fd);
        operate_fd_changed(fd_array, fd, false);
    }
    else
    {
        // 收到消息后反馈到客户端
        buffer[read_count] = '\0';
        printf("<server>receive client[%d] message, size = %d, content is : %s", fd, strlen(buffer), buffer);
        int write_count = send(fd, buffer, strlen(buffer), MSG_NOSIGNAL);
        if (-1 == write_count)
        {
            printf("<server>response to client[%d] error!\n", fd);
            close(fd);
            operate_fd_changed(fd_array, fd, false);
        }
    }
}

void do_disconnect(int *fd_array, int fd)
{
    printf("<server>client[%d] disconnect!\n", fd);
    close(fd);
    operate_fd_changed(fd_array, fd, false);
}

void operate_fd_changed(int *fd_array, int fd, bool is_add)
{
    for (int index = 0; index < FD_MAX_SIZE; ++index) 
    { 
        if (is_add && fd_array[index] < 0)
        {
            fd_array[index] = fd;
            break;
        }
        else if(!is_add && fd_array[index] == fd)
        {
            fd_array[index] = -1;
            break;
        }
    }
}