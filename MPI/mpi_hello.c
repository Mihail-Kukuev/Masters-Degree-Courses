#include <mpi.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {

    int p;
    int myrank;
    int str_size = 100;
    char str[str_size];
    int tag = 10;
    MPI_Status status;

    MPI_Init(&argc, &argv);

    MPI_Comm_size(MPI_COMM_WORLD, &p);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    if (myrank != 0) {
        sprintf(str, "Hello from process %d", myrank);
        MPI_Send(str, (int) strlen(str) + 1, MPI_CHAR, 0, tag, MPI_COMM_WORLD);
    }
    else {
        char **responses = malloc(p * sizeof(char *));

        int count, source;
        for (int i = 1; i < p; i++) {
            MPI_Probe(MPI_ANY_SOURCE, tag, MPI_COMM_WORLD, &status);
            MPI_Get_count(&status, MPI_CHAR, &count);

            source = status.MPI_SOURCE;
            responses[source] = malloc(count * sizeof(char));

            MPI_Recv(responses[source], count, MPI_CHAR, source, tag, MPI_COMM_WORLD, &status);

            printf("Received message from process %d\n", source);
        }

        printf("\nResult:\n");
        for (int i = 1; i < p; ++i) {
            printf("%s\n", responses[i]);
        }

        for (int i = 1; i < p; ++i) {
            free(responses[i]);
        }
        free(responses);
    }

    MPI_Finalize();
    return 0;
}
