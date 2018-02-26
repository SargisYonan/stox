// main.c

#include "csv_parser.h"
#include "stox_csv.h"


int main (void) {
	FILE *csv_file = NULL;
	size_t n = 0;
	char curl_buff[1024];
	char filename[16];
char ticker_string[10] = "AAPL";

	sprintf(filename, "%s.csv", ticker_string);
	sprintf(curl_buff, "curl https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?api_key=%s > %s", ticker_string, API_KEY, filename);
	printf("%s\n", curl_buff);
	system(curl_buff);

	csv_file = CSV_open_file(filename);
	printf("\n\nBYTES = %zu", n);

	CSV_create_structure(csv_file);

	return 1;
}
