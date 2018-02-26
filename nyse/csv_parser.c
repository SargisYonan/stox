#include "csv_parser.h"
#include <string.h>



size_t CSV_get_filesize(FILE *file_pointer) {
	size_t n = 0;
	FILE *_p = file_pointer;

	fseek(_p, 0L, SEEK_SET);

	for(n = 0; fgetc(_p) != EOF; n++);

	return n;
}

/**
* CSV_open_file - creates a C file pointer to a file path
* IN: file_path - a C-string containing the path of the CSV file to parse
* OUT: a UNIX file pointer to the file path
*	returns NULL if the file could not be opened
**/
FILE *CSV_open_file(char *file_path) {
	FILE *fp = NULL;

	// check to see if memory was allocated to file_path
	if (!file_path) {
		return fp;
	}

	// open the CSV in read only mode
	fp = fopen(file_path, "r");

	return fp;
}

/**
* CSV_close_file - closes the file pointer to the CSV file
* IN: csv_file_pointer - A FILE* pointing to the CSV file
	created in CSV_open_file
* OUT: 0 - csv_file_pointer was not a valid file pointer
	1 - the file was successfully closed
	-1 - the file could not be closed
**/
int CSV_close_file(FILE *csv_file_pointer) {
	if (!csv_file_pointer) {
		return 0;
	}

	if (fclose(csv_file_pointer) == EOF) {
		return -1;
	} else {
		return 1;
	}
}


/**
* CSV_store_to_buffer - stores the file into program memory 
	for faster memory access
* IN: fp - a file pointer to the CSV file to parse
* IN: buffer - an unallocated char* which will point
	to the location of the CSV file in the program memory
* OUT: the size of the CSV file in bytes
* EFFECTS: the file pointer, fp, is reset to the origin
**/

size_t CSV_store_to_buffer(FILE *fp, char *buffer) {
	size_t i = 0;

	// ensuring the whole file will be copied by reseting fp to origin
	fseek(fp, 0L, SEEK_SET);

	// copying file to buffer
	while(buffer[i] != EOF) {
		buffer[++i] = fgetc(fp);
	}

	// resetting fp to the origin
	fseek(fp, 0L, SEEK_SET);

	return i;
}

/** 
* CSV_get_line_size - returns the number of bytes in a 
	line up to the newline or EOF character starting from fp's
	current location
* IN: fp - a pointer to the file opened by CSV_open_file
* OUT: the number of bytes in the line starting from fp
* EFFECTS
**/
size_t CSV_get_line_size(FILE *fp) {
	FILE *_p = fp;
	char c = '\0';
	size_t n = 0;

	c = fgetc(_p);
	while((c != '\n') || (c != EOF)) {
		n++;
		c = fgetc(_p);
	}

	return n;
}

/** 
* CSV_point_to_line - moves fp to the position after the 
	'line_number'ed newline character
* IN: fp - a pointer to the file opened by CSV_open_file
* IN: line_number - the line number of the file to have fp point to
**/
void CSV_point_to_line(FILE *fp, uint64_t line_number) {
	uint64_t n = 0;
	char c = '\0';

	// iterate through each newline from the origin of fp
	rewind(fp);
	for (n = 1; n < line_number; n++) {
		while((c = fgetc(fp)) != '\n');
	}

	// move to next position
	//fgetc(fp);
}

/**
* CSV_create_structure - creates the CSV structure by 
	parsing out the buffer
* IN: fp - a pointer to the allocated CSV file 
* OUT: the CSV structure that was created
**/
CSV_t CSV_create_structure(FILE *fp) {
	char buff[1024];
	int i = 0;

	CSV_t _csv;

	rewind(fp);

	CSV_point_to_line(fp, 2);

	for (i = 0; i < POINTS; i++) {
		memset(_csv.dates[i], '\0', 20);
		fscanf(fp, "%[^,],%lf,%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%[^\n]", _csv.dates[i], &_csv.open[i], _csv.high[i], 
			buff, buff, buff, buff, buff, buff, buff, buff, buff, buff);
		fgetc(fp);
	}

	printf("\n");
	for(i = 0; i < POINTS; i++) {
		printf("%s --> %lf\n", _csv.dates[i], _csv.open[i]);
	}

	printf("%s OPEN PRICES:\n", "NFLX");
	printf("\n\n50 DAY MOVING AVERAGE = %lf\n", CSV_column_moving_average(50, _csv.open));
	printf("200 DAY MOVING AVERAGE = %lf\n\n", CSV_column_moving_average(200, _csv.open));
	return _csv;
}

/**
* CSV_coulumn_moving_average - take an n-point moving average on a dataset
* IN: n - the number of points to take an average of
* IN: dataset - a pointer to a set of data points
* OUT: the n-point rolling average of the dataset
* EFFECTS: at least (n * sizeof double) should be allocated to dataset
* -9999.99 is returned upon a usage error
**/
double CSV_column_moving_average(uint32_t n, double *dataset) {
	double _inc = 0.0;
	uint32_t itor = 0;

	for (itor = 0; itor < n; itor++) {
		_inc += dataset[itor];
	}

	return _inc / n;
}


