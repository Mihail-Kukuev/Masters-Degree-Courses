#include <mpi.h>
#include <iostream>
#include <cmath>

void print_matrix(const double *matrix, const int n) {
    printf("\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%.1f\t", matrix[i * n + j]);
        }
        printf("\n");
    }
}

void init_matrix(double *matrix, const int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double randNr = (rand() % 100);
            matrix[i * n + j] = randNr;
        }
    }
}

void multiply(const double *a, const double *b, double *c, int n) {
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            for (int j = 0; j < n; j++) {
                c[i * n + j] += a[i * n + k] * b[k * n + j];
            }
        }
    }
}

int main(int argc, char *argv[]) {
    double *A, *B, *C, *C_correct, *a, *b, *c, *a_temp;
    int N, n, p, my_rank, my_col_rank, my_row_rank;
    MPI_Comm comm, row_comm, col_comm;
    MPI_Datatype block_type;
    MPI_Status status;
    MPI_Request request1, request2;

    if (argc < 2) {
        printf("Too few arguments");
        exit(1);
    }

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &p);

    sscanf(argv[1], "%d", &N);
    int q = (int) sqrt(p);
    if (q * q != p || N / p * p != N) {
        printf("Wrong argument, dimension should be a square of number and divides by processors number");
        exit(1);
    }
    n = N / q;
    MPI_Type_vector(n, n, N, MPI_DOUBLE, &block_type);
    MPI_Type_commit(&block_type);

    int dimensions[2] = {q, q}, periods[2] = {1, 1}, reorder = 1;
    MPI_Cart_create(MPI_COMM_WORLD, 2, dimensions, periods, reorder, &comm);
    MPI_Comm_rank(comm, &my_rank);

    int my_coords[2];
    MPI_Cart_coords(comm, my_rank, 2, my_coords);

    int rows_free_coords[] = {false, true};
    int cols_free_coords[] = {true, false};
    MPI_Cart_sub(comm, rows_free_coords, &row_comm);
    MPI_Comm_rank(row_comm, &my_row_rank);
    MPI_Cart_sub(comm, cols_free_coords, &col_comm);
    MPI_Comm_rank(col_comm, &my_col_rank);

    if (my_rank == 0) {
        A = new double[N * N];
        B = new double[N * N];
        C = new double[N * N];
        C_correct = new double[N * N];

        srand(time(nullptr));
        init_matrix(A, N);
        init_matrix(B, N);
        /*printf("Matrix A\n");
        print_matrix(A, N);
        printf("\nMatrix B\n");
        print_matrix(B, N);*/
    }

    a = new double[N * N];
    b = new double[N * N];
    c = new double[N * N];
    a_temp = new double[N * N];
    
    int p_rank, p_coords[2];
    int a_tag = 11, b_tag = 22;
    if (my_rank == 0) {
        for (int i = 0; i < q; i++) {
            for (int j = 0; j < q; j++) {
                p_coords[0] = i;
                p_coords[1] = j;
                int start_index = i * N * n + j * n;
                MPI_Cart_rank(comm, p_coords, &p_rank);
                MPI_Isend(&A[start_index], 1, block_type, p_rank, a_tag, comm, &request1);
                MPI_Isend(&B[start_index], 1, block_type, p_rank, b_tag, comm, &request2);
                //free requests
            }
        }
    }

    MPI_Irecv(a, n * n, MPI_DOUBLE, 0, a_tag, comm, &request1);
    MPI_Irecv(b, n * n, MPI_DOUBLE, 0, b_tag, comm, &request2);
    MPI_Wait(&request1, &status);
    MPI_Wait(&request2, &status);

    b_tag = 33;
    double *a_mul;
    for (int step = 0; step < q; step++) {
        int root = (my_col_rank + step) % q;
        a_mul = (root == my_row_rank) ? a : a_temp;
        MPI_Bcast(a_mul, n * n, MPI_DOUBLE, root, row_comm);

        if (step > 0) {
            MPI_Wait(&request2, &status);
        }
        MPI_Isend(b, n * n, MPI_DOUBLE, (my_col_rank - 1 + q) % q, b_tag, col_comm, &request1);
        multiply(a_mul, b, c, n);

        if (step < q-1) {
//            MPI_Sendrecv_replace(b, n * n, MPI_DOUBLE, (my_col_rank - 1 + q) % q, b_tag, (my_col_rank + 1) % q, b_tag, col_comm, &status);
            MPI_Irecv(b, n * n, MPI_DOUBLE, (my_col_rank + 1) % q, b_tag, col_comm, &request2);
        }
    }

    int c_tag = 44;
    MPI_Isend(c, n * n, MPI_DOUBLE, 0, c_tag, comm, &request1);

    if (my_rank == 0) {
        for (int i = 0; i < p; i++) {
            MPI_Probe(MPI_ANY_SOURCE, c_tag, comm, &status);
            p_rank = status.MPI_SOURCE;
            MPI_Cart_coords(comm, p_rank, 2, p_coords);

            MPI_Recv(&C[p_coords[0] * N * n + p_coords[1] * n], 1, block_type, p_rank, c_tag, comm, &status);
        }

        multiply(A, B, C_correct, N);
        bool result = std::equal(C, C + N * N, C_correct);
        if (result)
            printf("Right answer\n");
        else
            printf("Wrong answer\n");

        /*printf("matrix C");
        print_matrix(C, N);
        printf("correct matrix C");
        print_matrix(C_correct, N);*/
    }

    MPI_Wait(&request1, &status);

    if (my_rank == 0) {
        delete[] A;
        delete[] B;
        delete[] C;
        delete[] C_correct;
    }
    delete[] a;
    delete[] a_temp;
    delete[] b;
    delete[] c;
    MPI_Comm_free(&row_comm);
    MPI_Comm_free(&col_comm);
    MPI_Comm_free(&comm);
    MPI_Finalize();
    return 0;
}
