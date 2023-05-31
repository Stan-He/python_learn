#include <stdio.h>
#include <stdlib.h>
#include <libgen.h>
#include <limits.h>
#include <string.h>
#include <linux/types.h>
#include <fcntl.h>
#include <unistd.h>

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




int main(int argc, char **argv){
	printf("Hellow world\n");
	int ret;
	char *path;
	char *abspath = (char*)calloc(sizeof(char),PATH_MAX);
	char *devname = "ttyACM0";
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


	return 0;

}
