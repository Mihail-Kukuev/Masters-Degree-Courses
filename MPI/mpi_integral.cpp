#include <mpi.h>
#include <cmath>
using namespace std;

double f(double x) {
    return x * x;
}

int main(int argc, char **argv) {
    int p, r, n;
    int myrank;
    int tag = 10;
    MPI_Status status;
    const int EXIT_CODE = -1;
    double a = 0;
    double b = 1;

    MPI_Init(&argc, &argv);

    MPI_Comm_size(MPI_COMM_WORLD, &p);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    sscanf(argv[1], "%d", &n);
    sscanf(argv[2], "%d", &r);

    double h = (b - a) / n;
    int block_index;
    
    if (myrank == 0) {
        block_index = 0;
        for (int i = 1; i < p; ++i) {
            MPI_Send(&block_index, 1, MPI_INT, i, tag, MPI_COMM_WORLD);
            block_index++;
        }

        int received_sums = 0;
        int blocks_count = (int) ceil(n * 1.0 / r);
        double sum, result = 0;

        while (received_sums < blocks_count) {
            MPI_Recv(&sum, 1, MPI_DOUBLE, MPI_ANY_SOURCE, tag, MPI_COMM_WORLD, &status);

            if (block_index < blocks_count) {
                MPI_Send(&block_index, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD);
                block_index++;
            }
            else {
                MPI_Send(&EXIT_CODE, 1, MPI_INT, status.MPI_SOURCE, tag, MPI_COMM_WORLD);
            }

            result += sum;
            received_sums++;
        }

        result *= h;
        printf("Result: %f\n", result);

        double second_derivative = 2;
        double e = second_derivative * n * pow(h, 3) / 12;
        double correct_answer = 1. / 3;
        printf("Precision:\n%.12f\n", e);
        printf("Norm:\n%.12f\n", fabs(correct_answer - result));
    }
    else {
        while (true) {
            MPI_Recv(&block_index, 1, MPI_INT, 0, tag, MPI_COMM_WORLD, &status);

            if (block_index == EXIT_CODE)
                break;

            double left_bound = a + (b-a) * (block_index * r) / n;
            double right_bound = fmin(left_bound + (b-a) * r / n, b);
            double sum = f(left_bound) / 2;

            double x;
            int intervals = (int) round((right_bound - left_bound) * n / (b-a));
            for (int i = 1; i < intervals; ++i) {
                x = left_bound + (b-a) * i / n;
                sum += f(x);
            }
            sum += f(right_bound) / 2;

            MPI_Send(&sum, 1, MPI_DOUBLE, 0, tag, MPI_COMM_WORLD);
        }
    }

    MPI_Finalize();
    return 0;
}
