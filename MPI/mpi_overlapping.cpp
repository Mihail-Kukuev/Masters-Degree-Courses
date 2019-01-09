#include <mpi.h>
#include <random>
#include <iostream>

using namespace std;

void print_lines(int** a, int lines, int columns) {
    for (int i = 1; i < lines; ++i) {
        for (int j = 0; j < columns; ++j) {
            cout << a[i][j] << "\t";
        }
        cout << endl;
    }
}

int main(int argc, char **argv) {
    int p, r, N1, N2;
    int myrank;
    int tag = 10;
    MPI_Status status;
    MPI_Request request1 = MPI_REQUEST_NULL, request2 = MPI_REQUEST_NULL;

    MPI_Init(&argc, &argv);

    MPI_Comm_size(MPI_COMM_WORLD, &p);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    sscanf(argv[1], "%d", &N1);
    sscanf(argv[2], "%d", &N2);
    sscanf(argv[3], "%d", &r);

    int lines_ceil = (N1 + (p-1))/ p;
    int lines_number = min(lines_ceil, N1 - myrank * lines_ceil) + 1;

    auto *memory = new int[lines_number * N2];
    auto **a = new int *[lines_number];

    for (int i = 0; i < lines_number; ++i) {
        a[i] = &memory[i * N2];
    }
    
    srand(time(NULL));

    for (int jb = 0; jb < N2; jb += r) {
        int block_size = min(r, N2 - jb);

        if (myrank == 0) {
            for(int j=0; j < jb + block_size; j++) {
                a[0][j] = (rand() % 100);
            }
        }
        else {
            if (jb == 0) {
                MPI_Irecv(a[0] + jb, block_size, MPI_INT, myrank - 1, tag, MPI_COMM_WORLD, &request1);
            }

            MPI_Wait(&request1, &status);
            if (jb + r < N2) {
                MPI_Irecv(a[0] + jb + r, block_size, MPI_INT, myrank - 1, tag, MPI_COMM_WORLD, &request1);
            }
        }

        for (int i = 1; i < lines_number; ++i) {
            for (int j = jb; j < jb + block_size; ++j) {
                a[i][j] = a[i-1][j] + 1;
            }
        }

        if (myrank < p - 1) {
            if (request2 != MPI_REQUEST_NULL)
                MPI_Wait(&request2, &status);
            MPI_Isend(a[lines_number - 1] + jb, block_size, MPI_INT, myrank + 1, tag, MPI_COMM_WORLD, &request2);
        }
    }
    MPI_Wait(&request2, &status);

    int print_code = 1;
    if (myrank != 0) {
        MPI_Recv(&print_code, 1, MPI_INT, myrank - 1, tag, MPI_COMM_WORLD, &status);
    }
    printf("Results for %d process:\n", myrank);
    print_lines(a, lines_number, N2);
    if (myrank < p - 1) {
        MPI_Send(&print_code, 1, MPI_INT, myrank + 1, tag, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}
