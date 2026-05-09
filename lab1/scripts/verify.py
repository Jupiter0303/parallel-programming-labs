import numpy as np
import subprocess
import os
import time

# генерация входных данных
def generate_input(size):
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    for name, mat in [("matrixA.txt", A), ("matrixB.txt", B)]:
        with open(name, "w") as f:
            f.write(f"{size}\n")
            np.savetxt(f, mat, fmt='%.4f')
    return A, B

# проверка результата
def verify():
    size = 500
    A, B = generate_input(size)
    
    # запуск скомпилированной программы C++
    print("Запуск C++ программы...")
    exe = "./matmul.exe" if os.name == "nt" else "./matmul"
    subprocess.run([exe], check=True)
    
    # загрузка результата C++
    with open("matrixC.txt", "r") as f:
        f.readline() # пропуск N
        f.readline() # пропуск строки со временем
        C_cpp = np.loadtxt(f)
    
    # эталонное умножение NumPy
    C_py = np.dot(A, B)
    
    # сравнение
    if np.allclose(C_cpp, C_py, atol=1e-2):
        print("✅ Верификация пройдена! Результаты совпадают.")
    else:
        print("❌ Ошибка верификации!")

if __name__ == "__main__":
    verify()