#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>
#include <mpi.h>

using namespace std;

// функция чтения (только для процесса 0)
void readMatrix(const string& filename, vector<double>& matrix, int& N) {
    ifstream file(filename);
    if (!file.is_open()) return;
    file >> N;
    matrix.resize(N * N);
    for (int i = 0; i < N * N; i++) file >> matrix[i];
}

// функция записи (только для процесса 0)
void writeMatrix(const string& filename, const vector<double>& matrix, int N, double time_ms) {
    ofstream file(filename);
    file << N << "\n" << time_ms << "\n";
    file << fixed << setprecision(4);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) file << matrix[i * N + j] << " ";
        file << "\n";
    }
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int N = 0;
    vector<double> A, B, C;

    // 1. процесс 0 читает данные
    if (rank == 0) {
        readMatrix("matrixA.txt", A, N);
        readMatrix("matrixB.txt", B, N);
    }

    // рассылаем размер всем процессам
    MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // 2. расчет распределения строк (Scatterv позволяет делить не нацело)
    int base_rows = N / size;
    int extra_rows = N % size;

    vector<int> sendcounts(size), displs(size);
    int offset = 0;
    for (int i = 0; i < size; i++) {
        int rows = base_rows + (i < extra_rows ? 1 : 0);
        sendcounts[i] = rows * N;
        displs[i] = offset;
        offset += rows * N;
    }

    int local_rows = base_rows + (rank < extra_rows ? 1 : 0);
    vector<double> local_A(local_rows * N);
    vector<double> local_C(local_rows * N, 0.0);
    if (rank != 0) B.resize(N * N);

    // 3. рассылка данных
    // матрицу B рассылаем целиком всем
    MPI_Bcast(B.data(), N * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    // матрицу A раздаем частями
    MPI_Scatterv(A.data(), sendcounts.data(), displs.data(), MPI_DOUBLE, 
                 local_A.data(), local_rows * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    double start_time = MPI_Wtime();

    // 4. вычисления
    for (int i = 0; i < local_rows; i++) {
        for (int k = 0; k < N; k++) {
            double temp = local_A[i * N + k];
            for (int j = 0; j < N; j++) {
                local_C[i * N + j] += temp * B[k * N + j];
            }
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double end_time = MPI_Wtime();

    // 5. сбор результатов
    if (rank == 0) C.resize(N * N);
    MPI_Gatherv(local_C.data(), local_rows * N, MPI_DOUBLE, 
                C.data(), sendcounts.data(), displs.data(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        double elapsed_ms = (end_time - start_time) * 1000.0;
        writeMatrix("matrixC.txt", C, N, elapsed_ms);
        cout << size << "," << N << "," << elapsed_ms << endl;
    }

    MPI_Finalize();
    return 0;
}