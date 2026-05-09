#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>


using namespace std;

//чтение матрицы из файла
void readMatrix(const string& filename, vector<double>& matrix, int& N) {
    ifstream file(filename);
    file >> N;
    matrix.resize(N * N);
    for (int i = 0; i < N * N; i++) file >> matrix[i];
}

//запись матрицы в файл
void writeMatrix(const string& filename, const vector<double>& matrix, int N) {
    ofstream file(filename);
    file << N << "\n";
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) file << matrix[i * N + j] << " ";
        file << "\n";
    }
}


int main()
 {
     int N;
    vector<double> A, B, C;
    
    try {
        readMatrix("matrixA.txt", A, N);
        readMatrix("matrixB.txt", B, N);
        C.assign(N * N, 0.0);

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                for (int k = 0; k < N; k++) {
                    C[i * N + j] += A[i * N + k] * B[k * N + j];
                }
            }
        }

        writeMatrix("matrixC.txt", C, N);
    } catch (...) {
        return 1;
    }
    return 0;
}