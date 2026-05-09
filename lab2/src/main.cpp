#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <omp.h>

using namespace std;

// функция чтения
void readMatrix(const string& filename, vector<double>& matrix, int& N) {
    ifstream file(filename);
    if (!file.is_open()) return;
    file >> N;
    matrix.resize(N * N);
    for (int i = 0; i < N * N; i++) file >> matrix[i];
}

// функция записи
void writeMatrix(const string& filename, const vector<double>& matrix, int N) {
    ofstream file(filename);
    file << N << "\n" << fixed << setprecision(8); 
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) file << matrix[i * N + j] << " ";
        file << "\n";
    }
}

int main(int argc, char* argv[]) {
    int N;
    vector<double> A, B, C;
    
    // получаем количество потоков из переменной окружения или аргумента
    int num_threads = 1;
    if (char* env_t = getenv("OMP_NUM_THREADS")) {
        num_threads = atoi(env_t);
    } else if (argc > 1) {
        num_threads = atoi(argv[1]);
    }
    omp_set_num_threads(num_threads);

    readMatrix("matrixA.txt", A, N);
    readMatrix("matrixB.txt", B, N);
    if (A.empty() || B.empty()) return 1;

    C.assign(N * N, 0.0);

    // замер времени с помощью функций OpenMP
    double start_time = omp_get_wtime();

    // параллельный блок
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        for (int k = 0; k < N; k++) {
            double temp = A[i * N + k];
            for (int j = 0; j < N; j++) {
                C[i * N + j] += temp * B[k * N + j];
            }
        }
    }

    double end_time = omp_get_wtime();
    double elapsed_ms = (end_time - start_time) * 1000.0;

    writeMatrix("matrixC.txt", C, N);

    // вывод для парсинга питоном: потоки,размер,время
    cout << num_threads << "," << N << "," << elapsed_ms << endl;

    return 0;
}