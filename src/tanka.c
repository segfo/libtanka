#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

// compile
// gcc -m32 tanka.c -o tanka32

typedef	void (*TANKA)();
int	main(){
	int	ret;
	char	*buf;

	buf = (char*)malloc(256*sizeof(char));
	read(1,buf,255);
	((TANKA)buf)();
	free(buf);
	// 短歌を読むとレジスタ壊す場合があるので、そのまま終了。
	exit(0);
	return	0;
}

