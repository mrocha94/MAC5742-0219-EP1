#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>

#define CHUNK 20

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int num_pthreads;

double c_x_min;
double c_x_max;
double c_y_min;
double c_y_max;

double pixel_width;
double pixel_height;

int iteration_max = 200;

int image_size;

int i_x_max;
int i_y_max;
int image_buffer_size;
int current_pixel;

void init(int argc, char *argv[]){
    if(argc < 6){
        printf("usage: ./mandelbrot_pth c_x_min c_x_max c_y_min c_y_max image_size\n");
        printf("examples with image_size = 11500:\n");
        printf("    Full Picture:         ./mandelbrot_pth -2.5 1.5 -2.0 2.0 11500\n");
        printf("    Seahorse Valley:      ./mandelbrot_pth -0.8 -0.7 0.05 0.15 11500\n");
        printf("    Elephant Valley:      ./mandelbrot_pth 0.175 0.375 -0.1 0.1 11500\n");
        printf("    Triple Spiral Valley: ./mandelbrot_pth -0.188 -0.012 0.554 0.754 11500\n");
        exit(0);
    }
    else{
        sscanf(argv[1], "%lf", &c_x_min);
        sscanf(argv[2], "%lf", &c_x_max);
        sscanf(argv[3], "%lf", &c_y_min);
        sscanf(argv[4], "%lf", &c_y_max);
        sscanf(argv[5], "%d", &image_size);

        i_x_max           = image_size;
        i_y_max           = image_size;
        image_buffer_size = image_size * image_size;

        pixel_width       = (c_x_max - c_x_min) / i_x_max;
        pixel_height      = (c_y_max - c_y_min) / i_y_max;
        num_pthreads    = atoi(getenv("PTH_NUM_THREADS"));

    };
};

void *compute_mandelbrot_thread(void *pthreadid) {
    double z_x;
    double z_y;
    double z_x_squared;
    double z_y_squared;
    double escape_radius_squared = 4;

    int iteration;
    int i_x;
    int i_y;

    double c_x;
    double c_y;
    int i_k;

    int i;

    while(1){
        pthread_mutex_lock(&mutex);
        i_k = current_pixel;
        current_pixel += CHUNK;
        pthread_mutex_unlock(&mutex);

        for (i = 0; i < CHUNK; i++) {
            if (i_k >= i_y_max * i_x_max) pthread_exit(NULL);

            i_y = i_k / i_x_max;
            c_y = c_y_min + i_y * pixel_height;
            if(fabs(c_y) < pixel_height / 2){
                c_y = 0.0;
            }

            i_x = i_k % i_x_max;
            c_x         = c_x_min + i_x * pixel_width;

            z_x         = 0.0;
            z_y         = 0.0;

            z_x_squared = 0.0;
            z_y_squared = 0.0;

            for(iteration = 0;
                iteration < iteration_max && \
                ((z_x_squared + z_y_squared) < escape_radius_squared);
                iteration++){
                z_y         = 2 * z_x * z_y + c_y;
                z_x         = z_x_squared - z_y_squared + c_x;

                z_x_squared = z_x * z_x;
                z_y_squared = z_y * z_y;
            }
            i_k++;
        }
    }
}

void compute_mandelbrot(){
    pthread_t *threads;
    int i;
    int error_code;

    threads = (pthread_t *) malloc(sizeof(pthread_t) * num_pthreads);
    current_pixel = 0;

    // cria as pthread
    for (i = 0; i < num_pthreads; i++) {
        error_code = pthread_create(&threads[i], NULL, compute_mandelbrot_thread, NULL);
        if (error_code){
            printf("ERROR pthread_create(): %d\n", error_code);
            exit(-1);
        }
    }

    // espera todas as threads terminarem
    for(i = 0; i < num_pthreads; i++) {
        error_code = pthread_join(threads[i], NULL);
        if (error_code) {
            printf("ERROR; return code from pthread_join() is %d\n", error_code);
            exit(-1);
        }
    }
    pthread_mutex_destroy(&mutex);
};

int main(int argc, char *argv[]){
    init(argc, argv);
    compute_mandelbrot();
    return 0;
};
