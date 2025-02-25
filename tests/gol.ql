; Attempt at Game Of Life

#define GRID_SIZE 32
#define ARR_START 0x8000
#define RNG_SEED 0x1234

load RNG_SEED
store $_rand

subr random
    load $_rand
    mul 20077
    add 12345
    store $_rand
    return


halt
