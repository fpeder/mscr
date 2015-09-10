#include <stdio.h>

int findmax(int *input, int H, int W, int *output)
{
    int i, j, idx, max, val, tmp;

    for(i=0; i<H; i++) {

	if (input[i*W] + input[i*W+1] == 0) {
	    output[i] = -1;
	    continue;
	}

	if (input[i*W] > input[i*W+1])
	    output[i] = 0;
	else
	    output[i] = 1;
    }
		

    /* 	for(j=0; j<W; j++) */
    /* 	    tmp += input[i*W + j]; */

    /* 	if(tmp == 0) { */
    /* 	    output[i] = -1; */
    /* 	    continue; */
    /* 	} */

    /* 	for(j=0; j<W; j++) { */
    /* 	    val = input[i*W + j]; */
    /* 	    if(val > max) { */
    /* 		max = val; */
    /* 		idx = j; */
    /* 	    } */
    /* 	} */
    /* 	output[i] = idx; */
    /* } */

    return 1;
}
