#ifndef _CSV_PARSER_H_
#define _CSV_PARSER_H_

#include <stdio.h>
#include <stdlib.h>
#include "stox_csv.h"

struct CSV {
	char dates[POINTS][20];
	double open[POINTS];
	char high[POINTS][20];
};
typedef struct CSV CSV_t;

/**
* CSV_open_file - creates a C file pointer to a file path
* IN: file_path - a string containing the path of the CSV file to parse
* OUT: a UNIX file pointer to the file path
**/
FILE *CSV_open_file(char *file_path);

/**
* CSV_get_filesize - returns the size (in bytes) of the CSV file
	without moving the file pointer address passed in
* IN: file_pointer - the file pointer returned by CSV_open_file
* OUT: the size in bytes of the CSV file
**/
size_t CSV_get_filesize(FILE *file_pointer);


/**
* CSV_coulumn_moving_average - take an n-point moving average on a dataset
* IN: n - the number of points to take an average of
* IN: dataset - a pointer to a set of data points
* OUT: the n-point rolling average of the dataset
* EFFECTS: at least (n * sizeof double) should be allocated to dataset
* -9999.99 is returned upon a usage error
**/
double CSV_column_moving_average(uint32_t n, double *dataset);

/**
* CSV_close_file - closes the file pointer to the CSV file
* IN: csv_file_pointer - A FILE* pointing to the CSV file
	created in CSV_open_file
* OUT: 0 - csv_file_pointer was not a valid file pointer
	1 - the file was successfully closed
	-1 - the file could not be closed
**/
int CSV_close_file(FILE *csv_file_pointer);

/**
* CSV_store_to_buffer - stores the file into program memory 
	for faster memory access
* IN: fp - a file pointer to the CSV file to parse
* IN: buffer - an unallocated char* which will point
	to the location of the CSV file in the program memory
* OUT: the size of the CSV file in bytes
* EFFECTS: the file pointer, fp, is reset to the origin
**/
size_t CSV_store_to_buffer(FILE *fp, char *buffer);

/** 
* CSV_point_to_line - moves fp to the position after the 
	'line_number'ed newline character
* IN: fp - a pointer to the file opened by CSV_open_file
* IN: line_number - the line number of the file to have fp point to
**/
void CSV_point_to_line(FILE *fp, uint64_t line_number);

/** 
* CSV_get_line_size - returns the number of bytes in a 
	line up to the newline or EOF character starting from fp's
	current location
* IN: fp - a pointer to the file opened by CSV_open_file
* OUT: the number of bytes in the line starting from fp
**/
size_t CSV_get_line_size(FILE *fp);

/**
* CSV_create_structure - creates the CSV structure by 
	parsing out the buffer
* IN: fp - a pointer to the allocated CSV file 
* OUT: the CSV structure that was created
**/
CSV_t CSV_create_structure(FILE *fp);

#endif