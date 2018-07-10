#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define BUFF_SIZE 1024

enum e_ip_version
{
    e_ipv4 = 0,
    e_ipv6 = 1, 
};

int main(int argc, char *argv[])  
{
    int ip_version = e_ipv4;
    int listen_num = 10;
    int listen_port = 8899;

    int listen_fd, client_fd;
    socklen_t socklen;
    char buffer[BUFF_SIZE] = {0};
  
    struct sockaddr_in server_addrin;   // IPv4
    struct sockaddr_in6 server_addrin6; // IPv6

    if (argv[1])
        ip_version = atoi(argv[1]);

    if (ip_version != e_ipv4)
        ip_version = e_ipv6;
 
    if (ip_version == e_ipv4)
        listen_fd = socket(PF_INET, SOCK_STREAM, 0);     // IPv4
    else
        listen_fd = socket(PF_INET6, SOCK_STREAM, 0);    // IPv6

    if (listen_fd == -1)
    {
        printf("create socket error\n");
        exit(1);
    }
    else
        printf("socket created success, listen fd =%d\n", listen_fd);

    if (ip_version == e_ipv4)
    {
        memset(&server_addrin, 0, sizeof(server_addrin));
        server_addrin.sin_family = AF_INET;             // IPv4
        server_addrin.sin_port = htons(listen_port);    // IPv4
        server_addrin.sin_addr.s_addr = INADDR_ANY;     // IPv4
        //server_addrin.sin_addr.s_addr = inet_addr(argv[3]); // IPv4  
    }
    else
    {
        memset(&server_addrin6, 0, sizeof(server_addrin6));
        server_addrin6.sin_family = AF_INET6;           // IPv6
        server_addrin6.sin6_port = htons(listen_port);  // IPv6
        server_addrin6.sin6_addr = in6addr_any;         // IPv6
        //inet_pton(AF_INET6, argv[3], &server_addrin.sin6_addr);  // IPv6  
    }

    int bind_ret = -1;
    if (ip_version == e_ipv4)
        bind_ret = bind(listen_fd, (struct sockaddr *)&server_addrin, sizeof(struct sockaddr_in));    // IPv4
    else
        bind_ret = bind(listen_fd, (struct sockaddr *)&server_addrin6, sizeof(struct sockaddr_in6))   // IPv6

    if (bind_ret == -1)
    {
        printf("bind socket error\n");
        exit(1);
    }
  
    if (listen(listen_fd, listen_num) == -1)
    {
        perror("listen socket error\n");
        exit(1);
    }
    printf("begin listen port = %d, max connection = %d\n", listen_port, listen_num);

    socklen = sizeof(struct sockaddr);
    if (ip_version == e_ipv4)
    {
        if ((client_fd = accept(listen_fd, (struct sockaddr *)&server_addrin, &socklen)) == -1)
        {
            perror("accept connection error\n");
            exit(errno);
        } else  
            printf("server: got connection from %s, port = %d, client_fd = %d\n", 
                inet_ntoa(server_addrin.sin_addr), ntohs(server_addrin.sin_port), client_fd); // IPv4  
    }
    else
    {
        if ((client_fd = accept(listen_fd, (struct sockaddr *)&server_addrin6, &socklen)) == -1)
        {
            perror("accept connection error\n");
            exit(errno);
        } else  
            printf("server: got connection from %s, port = %d, client_fd = %d\n", 
                inet_ntop(AF_INET6, &server_addrin6.sin6_addr, buffer, sizeof(buffer)), sockaddr_in6.sin6_port, client_fd); // IPv6  
    }

    memset(buffer, 0, sizeof(buffer));
    strcpy(buffer, "you can tell me something about you!\n");
    /* send message to client */
    socklen = send(client_fd, buffer, strlen(buffer), 0);
    if (socklen < 0)
    {
        printf("send message to client failed! error msg is '%s'\n", strerror(errno));
        exit(errno);
    }

    while (1) {
        /* receive message from client */
        socklen = recv(client_fd, buffer, BUFF_SIZE, 0);
        buffer[socklen] = '\0';
        if (len > 0)
            printf("receive message from client success, content is '%s'", buffer);
        else
            printf("receive message from client failed, exit because of '%s'", strerror(errno));
    }

    close(listen_fd);
    return 0;
}  