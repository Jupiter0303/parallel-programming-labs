#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <chrono>

using namespace std;

// чтение матрицы из файла
void readMatrix(const string& filename, vector<double>& matrix, int& N) {
    ifstream file(filename);
    if (!file.is_open()) return;
    file >> N;
    matrix.resize(N * N);
    for (int i = 0; i < N * N; i++) file >> matrix[i];
}

// запись только чисел в файл для надежной верификации
void writeMatrix(const string& filename, const vector<double>& matrix, int N) {
    ofstream file(filename);
    file << N << "\n";
    // устанавливаем высокую точность вывода
    file << fixed << setprecision(8); 
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            file << matrix[i * N + j] << " ";
        }
        file << "\n";
    }
}

int main() {
    int N;
    vector<double> A, B, C;
    
    readMatrix("matrixA.txt", A, N);
    readMatrix("matrixB.txt", B, N);
    if (A.empty() || B.empty()) return 1;

    C.assign(N * N, 0.0);

    auto start = chrono::high_resolution_clock::now();

    for (int i = 0; i < N; i++) {
        for (int k = 0; k < N; k++) {
            double temp = A[i * N + k];
            for (int j = 0; j < N; j++) {
                C[i * N + j] += temp * B[k * N + j];
            }
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double, milli> elapsed = end - start;

    writeMatrix("matrixC.txt", C, N);

    // выводим время в консоль, а не в файл
    cout << "расчет окончен. время: " << elapsed.count() << " мс" << endl;
    return 0;
}