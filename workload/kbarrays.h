
static size_t array_alloc_size = 1001;

/* 'Dynamic' array for storing msg/req times */
typedef struct 
{
  float *record;
  unsigned long *start_ts;
  size_t used;
  size_t size;
} Array;
static void initArray(Array *a, size_t array_size) 
{
    a->record = (float *)malloc(array_size * sizeof(float));
    if (!a->record && array_size != 0){
        printf("ERROR: Unable to initialize records array.\n");
        exit(0);
    }
    a->start_ts = (unsigned long *)malloc(array_size * sizeof(unsigned long));
    if (!a->start_ts && array_size != 0){
        printf("ERROR: Unable to initialize start_ts array.\n");
        exit(0);
    }
    a->used = 0;
    a->size = array_size;
}
static void insertArray(Array *a, size_t index, float element, double ts) 
{
    if (index < a->size){
        a->record[index] = element;
	a->start_ts[index] = (unsigned long) ts;
	a->used++;
        return;
    }
    else {
        a->record = (float *)realloc(a->record, (a->size+array_alloc_size) * sizeof(float));
        if (!a->record){
            printf("ERROR: Unable to grow records array from %d to %d bytes.\n", a->size, a->size+array_alloc_size);
            exit(0);
        }
        a->start_ts = (unsigned long *)realloc(a->start_ts, (a->size+array_alloc_size) * sizeof(unsigned long));
        if (!a->start_ts){
            printf("ERROR: Unable to grow start_ts array from %d to %d bytes.\n", a->size, a->size+array_alloc_size);
            exit(0);
        }
        a->size += array_alloc_size;
    }
    a->record[index] = element;
    a->start_ts[index] = (unsigned long) ts;
    a->used++;
}
static void freeArray(Array *a) 
{
  free(a->record);
  free(a->start_ts);
  a->record = NULL;
  a->start_ts = NULL;
  a->used = 0;
  a->size = 0;
}

static void printArray(FILE* outfile, Array *a, int start, int stop)
{
	int i;
	for(i = start; i < stop; i++)
	{
		if(i > start)
			fprintf(outfile, ",");
		fprintf(outfile, "%lu:%.0f", a->start_ts[i], a->record[i]);
	}
}
