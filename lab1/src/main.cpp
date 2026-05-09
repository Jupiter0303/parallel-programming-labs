#include <iostream>
#include <vector>

using namespace std;

int main()
 {
    int N = 100;
    vector<double> A(N * N, 1.0);
    vector<double> B(N * N, 2.0);
    vector<double> C(N * N, 0.0);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i * N + j] += A[i * N + k] * B[k * N + j];
            }
        }
    }

    return 0;
}