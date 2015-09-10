#include <stdio.h>
#include <stdint.h>

int blocketize(uint8_t *input, int M1, int N1,
	       uint8_t *output, int M2, int N2,
	       int w, int h, int sx, int sy)
{
    int i, j, y, x;
    int a, b;

    for (i=0, a=0; i<M1-h+1; i+=sy) {
	for (j=0; j<N1-w+1; j+=sx) {

	    for (y=0, b=0; y<w; y++) {
	    	for (x=0; x<w; x++) {
		    output[a*N2 + b] = input[(i+y)*N1 + j + x];
		    b++;
	    	}
	    }
	    a++;
	}
    }

    return 1;
}
