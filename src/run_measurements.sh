#! /bin/bash

set -o xtrace

MEASUREMENTS=10
ITERATIONS=4

INITIAL_SIZE=16
INITIAL_THREADS=1

SIZE=$INITIAL_SIZE
NUM_THREADS=$INITIAL_THREADS
NAMES=('mandelbrot_seq' 'mandelbrot_seq_io' 'mandelbrot_pth' 'mandelbrot_omp')
THREAD_ITERATIONS=(1 1 6 6)

make
rm -rf results
mkdir results

K=0
for NAME in ${NAMES[@]}; do
    mkdir results/$NAME

    for((j=1; j<=${THREAD_ITERATIONS[K]}; j++)); do

        export OMP_NUM_THREADS=$NUM_THREADS;
        export PTH_NUM_THREADS=$NUM_THREADS;

        for ((i=1; i<=$ITERATIONS; i++)); do
                perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $NUM_THREADS>> full.log 2>&1
                perf stat -r $MEASUREMENTS ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $NUM_THREADS>> seahorse.log 2>&1
                perf stat -r $MEASUREMENTS ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $NUM_THREADS>> elephant.log 2>&1
                perf stat -r $MEASUREMENTS ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $NUM_THREADS>> triple_spiral.log 2>&1
                SIZE=$(($SIZE * 2))
        done

        SIZE=$INITIAL_SIZE
        NUM_THREADS=$(($NUM_THREADS * 2))
    done

    K=$(($K + 1))
    SIZE=$INITIAL_SIZE
    NUM_THREADS=$INITIAL_THREADS

    mv *.log results/$NAME
done
rm output_seq.ppm
