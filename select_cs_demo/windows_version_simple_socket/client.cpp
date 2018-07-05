#include <stdio.h>
#include <stdlib.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")

int main(int argc, char *argv[])
{
	WSADATA wsaData;
	WORD wVersionRequested = MAKEWORD(2, 2);
	WSAStartup(wVersionRequested, &wsaData);
	int client_fd = socket(AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in server_addr;
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(8899);
	server_addr.sin_addr.s_addr	= inet_addr("127.0.0.1");

	connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));

	while(1)
	{
		char szSendBuf[64] = {0};
		for(unsigned int i = 0; i < 64; i++)
		{
			szSendBuf[i] = 'a';	
		}

		int iRet = send(client_fd, szSendBuf, sizeof(szSendBuf) , 0); 
		printf("send size is %d, iRet is %d\n", sizeof(szSendBuf), iRet);
		getchar();
	}

	closesocket(client_fd);
	return 0;
}