/* 
   @author: Ahmed Amokrane
   A SocketCAN example that prints the content of received CAN packets on an interface (physical or virtual)
   Similar kind of functioning as candump
*/
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <ctype.h>
#include <net/if.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>


int soc; //The CAN socket that will be used

int open_port(const char *port)
{
    //Open the TCP port
    struct ifreq ifr;
    struct sockaddr_can addr;
    /* open socket */
    soc = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if(soc < 0)
    {
        return (-1);
    }
    addr.can_family = AF_CAN;
    strcpy(ifr.ifr_name, port);
    if (ioctl(soc, SIOCGIFINDEX, &ifr) < 0)
    {
        return (-1);
    }
    addr.can_ifindex = ifr.ifr_ifindex;
    fcntl(soc, F_SETFL, O_NONBLOCK);
    if (bind(soc, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        return (-1);
    }
    return 0;
}

void read_port()
{
    /*This reads a packet from the CAN Socket*/
    struct can_frame frame_rd;
    int recvbytes = 0;
    int i;
    while(1)
    {
        struct timeval timeout = {10, 10}; //Timeout after 10 seconds if the port is not active
        fd_set readSet;
        FD_ZERO(&readSet);
        FD_SET(soc, &readSet);
        if (select((soc + 1), &readSet, NULL, NULL, &timeout) >= 0)
        {
            if (FD_ISSET(soc, &readSet))
            {
                recvbytes = read(soc, &frame_rd, sizeof(struct can_frame));
                if(recvbytes)
                {	
                    printf("\n***\nNew frame received\n Arbitraion_ID = %lX, dlc = %d, data = ", (unsigned long)frame_rd.can_id,frame_rd.can_dlc);
                    for(i=0; i<frame_rd.can_dlc; i++)
                    	printf("%X", frame_rd.data[i]);
                }
            }
            else
            	break;
        }
    }
}



int main(void)
{
    open_port("vcan0");
    read_port();
    return 0;
}
