// The part of Code was adapted from the "rapl_plot" program
// by Vince Weaver

/** 
 * @author  W
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
//#include <omp.h>
#include <time.h>
#include <sys/time.h>

#include "papi.h"

#define NUM_EVENTS 6
 

int stap4rapl(long p0,long p1,long d0,long d1){
	//fprintf(stderr,"stap4rapl() running\n");
	//fprintf(stderr,"%ld \n",p0);
	//x=0;
	//return x;
}


char events[NUM_EVENTS][BUFSIZ]={
	"PACKAGE_ENERGY:PACKAGE0",
	"PACKAGE_ENERGY:PACKAGE1",
	"DRAM_ENERGY:PACKAGE0",
	"DRAM_ENERGY:PACKAGE1",
	"PP0_ENERGY:PACKAGE0",
	"PP0_ENERGY:PACKAGE1",
};


int main (int argc, char **argv)
{

	int retval,cid,rapl_cid=-1,numcmp;
	int EventSet = PAPI_NULL;
	long long values[NUM_EVENTS];
	const PAPI_component_info_t *cmpinfo = NULL;
	//double start_time,before_time,after_time;
	//double elapsed_time,total_time;


	/* PAPI Initialization */
	retval = PAPI_library_init( PAPI_VER_CURRENT );
	if ( retval != PAPI_VER_CURRENT ) {
		fprintf(stderr,"PAPI_library_init failed\n");
		exit(1);
	}

	numcmp = PAPI_num_components();

	for(cid=0; cid<numcmp; cid++) {

		if ( (cmpinfo = PAPI_get_component_info(cid)) == NULL) {
			fprintf(stderr,"PAPI_get_component_info failed\n");
			exit(1);
		}

		if (strstr(cmpinfo->name,"rapl")) {
			rapl_cid=cid;
			printf("Found rapl component at cid %d\n", rapl_cid);

			if (cmpinfo->num_native_events==0) {
				fprintf(stderr,"No rapl events found\n");
				exit(1);
			}
			break;
		}
	}

	/* Component not found */
	if (cid==numcmp) {
		fprintf(stderr,"No rapl component found\n");
		exit(1);
	}


	/* Create EventSet */
	retval = PAPI_create_eventset( &EventSet );
	if (retval != PAPI_OK) {
		fprintf(stderr,"Error creating eventset!\n");
	}
int i;
	for( i=0;i<NUM_EVENTS;i++) {

		retval = PAPI_add_named_event( EventSet, events[i] );
		if (retval != PAPI_OK) {
			fprintf(stderr,"Error adding event %s\n",events[i]);
		}
	}

	retval = PAPI_start( EventSet);
	while(1) {
		usleep(1001);//1000us=1ms
		retval = PAPI_stop( EventSet, values);
		//if (retval != PAPI_OK) {
		//	fprintf(stderr, "PAPI_start() failed\n");
		//}

		retval = PAPI_start( EventSet);
		stap4rapl(values[0],values[1],values[2],values[3]);
	}

	return 0;
}
