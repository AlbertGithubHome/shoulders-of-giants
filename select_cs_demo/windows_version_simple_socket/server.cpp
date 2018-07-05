#include <stdio.h>
#include <stdlib.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")

int main(int argc, char * argv[])
{
	WSADATA wsaData;
	WORD wVersionRequested = MAKEWORD(2, 2);
	WSAStartup(wVersionRequested, &wsaData);
	int listen_fd = socket(AF_INET, SOCK_STREAM, 0);

	// 设置服务器IP和Port
	struct sockaddr_in server_addr;
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family		= AF_INET;
	server_addr.sin_port		= htons(8899);
	server_addr.sin_addr.s_addr	= INADDR_ANY;

	bind(listen_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
	listen(listen_fd, 10);

	printf("<server>server[ip:%s, port:%d] is running...\n", "127.0.0.1", 8899);

	int len = sizeof(server_addr);
	int client_id = accept(listen_fd, (struct sockaddr *)&server_addr, &len);

	while(1)  
	{  
		char szRecvBuf[50001] = {0};  
		int iRet = recv(client_id, szRecvBuf, sizeof(szRecvBuf)-1, 0);  
		printf("iRet is %d\n", iRet);	

		getchar();	
		closesocket(client_id);
	} 
	
	closesocket(listen_fd);
	return 0;
}