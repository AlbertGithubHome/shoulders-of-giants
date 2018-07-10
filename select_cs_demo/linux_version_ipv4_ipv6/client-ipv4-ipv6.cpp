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
    int listen_port = 8899;

    int client_fd;
    socklen_t socklen;
    char buffer[BUFF_SIZE] = {0};

    struct sockaddr_in server_addrin;   // IPv4
    struct sockaddr_in6 server_addrin6; // IPv6

    if (argv[1])
        ip_version = atoi(argv[1]);

    if (ip_version != e_ipv4)
        ip_version = e_ipv6;

    if (ip_version == e_ipv4)
        client_fd = socket(PF_INET, SOCK_STREAM, 0);     // IPv4
    else
        client_fd = socket(PF_INET6, SOCK_STREAM, 0);    // IPv6

    if (client_fd == -1)
    {
        printf("create client socket error\n");
        exit(1);
    }
    else
        printf("socket created success, client fd =%d\n", client_fd);


    if (ip_version == e_ipv4)
    {
        memset(&server_addrin, 0, sizeof(server_addrin));
        server_addrin.sin_family = AF_INET;             // IPv4
        server_addrin.sin_port = htons(listen_port);    // IPv4
        server_addrin.sin_addr.s_addr = INADDR_ANY;     // IPv4
        if (inet_aton(argv[2], (struct in_addr *) &server_addrin.sin_addr.s_addr) == 0) // IPv4
        {
            printf("convert server ip failed, error msg is '%s'\n", strerror(errno));
            exit(errno);
        } 
    }
    else
    {
        memset(&server_addrin6, 0, sizeof(server_addrin6));
        server_addrin6.sin_family = AF_INET6;           // IPv6
        server_addrin6.sin6_port = htons(listen_port);  // IPv6
        server_addrin6.sin6_addr = in6addr_any;         // IPv6
        if (inet_pton(AF_INET6, argv[2], &server_addrin6.sin6_addr) < 0 ) // IPv6
        {
            printf("convert server ip failed, error msg is '%s'\n", strerror(errno));
            exit(errno);
        }
    }

    if (ip_version == e_ipv4)
    {
        if (connect(client_fd, (struct sockaddr *) &server_addrin, sizeof(server_addrin)) == 0) // IPv4
        {
            printf("connect server failed, error msg is '%s'\n", strerror(errno));
            exit(errno);
        } 
    }
    else
    {
        if (connect(client_fd, (struct sockaddr *) &server_addrin6, sizeof(server_addrin6)) < 0 ) // IPv6
        {
            printf("connect server failed, error msg is '%s'\n", strerror(errno));
            exit(errno);
        }
    }

    /* receive message from server */
    socklen = recv(client_fd, buffer, MAXBUF, 0);
    buffer[socklen] = '\0';
    if (socklen > 0)  
        printf("receive message from server success, content is '%s'", buffer);
    else
        printf("receive message from server failed, error msg is '%s'", strerror(errno));

    int num = 0;
    while(1)
    {
        getchar();
        sprintf(buffer, "%d\n", ++num);
        socklen = send(client_fd, buffer, strlen(buffer), 0)
        if (socklen < 0)
        {
            printf("send message to server failed, error msg is '%s'\n", strerror(errno));
            exit(errno);
        }
    }

    close(client_fd);
    return 0;
}