#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cuda_runtime.h>

using namespace std;

// классическое cuda-ядро для умножения матриц
__global__ void matMulKernel(const double* A, const double* B, double* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        double sum = 0.0;
        for (int k = 0; k < N; k++) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

void readMatrix(const string& filename, vector<double>& matrix, int& N) {
    ifstream file(filename);
    if (!file.is_open()) return;
    file >> N;
    matrix.resize(N * N);
    for (int i = 0; i < N * N; i++) file >> matrix[i];
}

void writeMatrix(const string& filename, const vector<double>& matrix, int N, float time_ms) {
    ofstream file(filename);
    file << N << "\n" << time_ms << "\n";
    file << fixed << setprecision(4);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) file << matrix[i * N + j] << " ";
        file << "\n";
    }
}

int main(int argc, char* argv[]) {
    int N;
    vector<double> h_A, h_B;
    
    // считываем размер блока
    int blockSize = (argc > 1) ? atoi(argv[1]) : 16; //по  умолчанию 16

    readMatrix("matrixA.txt", h_A, N);
    readMatrix("matrixB.txt", h_B, N);
    if (h_A.empty()) return 1;

    vector<double> h_C(N * N);
    size_t bytes = N * N * sizeof(double);

    // выделение памяти на видеокарте
    double *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    // копирование данных с процессора на видеокарту
    cudaMemcpy(d_A, h_A.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), bytes, cudaMemcpyHostToDevice);

    // настройка сетки потоков
    dim3 threads(blockSize, blockSize);
    dim3 blocks((N + blockSize - 1) / blockSize, (N + blockSize - 1) / blockSize);

    // замер времени с помощью cuda-событий
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);
    matMulKernel<<<blocks, threads>>>(d_A, d_B, d_C, N);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float ms = 0;
    cudaEventElapsedTime(&ms, start, stop);

    // копирование результата обратно на процессор
    cudaMemcpy(h_C.data(), d_C, bytes, cudaMemcpyDeviceToHost);

    writeMatrix("matrixC.txt", h_C, N, ms);

    // вывод данных для парсинга скриптом: блок,размер,время
    cout << blockSize << "," << N << "," << ms << endl;

    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    cudaEventDestroy(start); cudaEventDestroy(stop);

    return 0;
}