#include <stdio.h>
#include <stdlib.h>
#include <libgen.h>
#include <limits.h>
#include <string.h>
#include <linux/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

struct hsc_hdr {
	__u8	header0;
	__u8	header1;
	__u8	len;
	__u8	flag;
	__u8	ret_code;
	__u8	rsvd0;
	__u8	rsvd1;
	__u8	pi;
} __attribute__((packed));


const char *usb_subsys_prefix = "/sys/class/tty";
const char *usb_subsys_post   = "device";


/**
 * read_file - read contents of file into @buffer.
 * @fname:  File name
 * @buffer: Where to save file's contents
 * @bufsz:  Size of @buffer. On success, @bufsz gets decremented by the
 *          number of characters that were writtent to @buffer.
 *
 * Return: The number of characters read. If the file cannot be opened or
 * nothing is read from the file, then this function returns 0.
 */
static size_t read_file(const char * fname, char *buffer, size_t *bufsz)
{
	char   *p;
	FILE   *file;
	size_t len;

	file = fopen(fname, "re");
	if (!file)
		return 0;

	p = fgets(buffer, *bufsz, file);
	fclose(file);

	if (!p)
		return 0;

	 /* Strip unwanted trailing chars */
	len = strcspn(buffer, " \t\n\r");
	*bufsz -= len;

	return len;
}

//设置串口参数
int set_serial_opt(int fd){
	struct termios new_cfg;
	tcgetattr(fd, &new_cfg);
	new_cfg.c_cflag |= (CLOCAL | CREAD);
	cfsetispeed(&new_cfg, B9600);//设置波特率
	cfsetospeed(&new_cfg, B9600);
	new_cfg.c_cflag &= ~CSIZE;    
	new_cfg.c_cflag |= CS8;
	new_cfg.c_cflag &= ~PARENB;    
	new_cfg.c_cflag &= ~CSTOPB;    
	new_cfg.c_cc[VTIME] = 0;    
	new_cfg.c_cc[VMIN] = 0;    
			     
	tcflush(fd,TCIFLUSH);    
	tcsetattr(fd, TCSANOW, &new_cfg); 
	return 0;

}

int uart_send(int fd, struct hsc_hdr *req){
	
	int wr_num;
	int i=0;
	unsigned char buf[1024];
	memcpy(buf, req, sizeof(*req));
	for(i=0;i<sizeof(*req);i++){
		printf("byte%d %x \n",i,buf[i]);
	}
	wr_num = write(fd,buf,sizeof(*req));
	
	printf("uart_send %d bytes\n",wr_num);
	return wr_num;
}

int uart_recv(int fd, struct hsc_hdr *resp){
	
	int nread;
	unsigned char buf[1024];

	nread = read(fd,buf,1024);
	if (nread > 0){
		memcpy(resp, buf, sizeof(*resp));
		printf("resp.ret_code:0x%x\n", resp->ret_code);
	}else{
		printf("error when read uart...\n");
	}
	return 0;


}


int main(int argc, char **argv){
	printf("Hellow world\n");
	int ret;
	char *path;
	char *abspath = (char*)calloc(sizeof(char),PATH_MAX);
	char *devname = "ttyACM0";
	char *devpath = "/dev/ttyACM0";
	ret = asprintf(&path, "%s/%s/%s", usb_subsys_prefix, devname, usb_subsys_post);
	if (ret > 0) {
		printf("error...\n");
	}
	printf("%s\n",path);
	realpath(path,abspath);
	printf("%s\n",abspath);
	dirname(abspath);
	printf("%s\n",abspath);

	//读文件路径准备
	char *pid_path;
	char pid[16];
	asprintf(&pid_path, "%s/%s", abspath, "idProduct");

	//读pid
	int f;
	f=open(pid_path,O_RDONLY);
	read(f, pid, 16);
	printf("pid:%s\n",pid);
	close(f);

	//打开串口
	f = open(devpath,O_RDWR|O_NOCTTY|O_NDELAY);
	if (f<0){
		printf("error in open serial device :%s\n",devpath);
	}
	set_serial_opt(f);

	//初始化
	struct hsc_hdr req_hdr;
	struct hsc_hdr resp_hdr;

	memset(&req_hdr, 0, sizeof(req_hdr));
	memset(&resp_hdr, 0, sizeof(resp_hdr));

	req_hdr.header0 = 0xfd;
	req_hdr.header1 = 0x01;

	uart_send(f, &req_hdr);
	sleep(1);
	uart_recv(f, &resp_hdr);



	close(f);


	return 0;

}
