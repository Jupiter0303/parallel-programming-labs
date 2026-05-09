import numpy as np
import subprocess
import os

def generate_input(size):
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    for name, mat in [("matrixA.txt", A), ("matrixB.txt", B)]:
        with open(name, "w") as f:
            f.write(f"{size}\n")
            np.savetxt(f, mat, fmt='%.8f')
    return A, B

def verify():
    size = 500
    A, B = generate_input(size)
    
    print("запуск c++ программы...")
    exe = "./matmul.exe" if os.name == "nt" else "./matmul"
    subprocess.run([exe], check=True)
    
    # чтение результата (пропускаем только первую строку с N)
    print("чтение результатов...")
    C_cpp = np.loadtxt("matrixC.txt", skiprows=1)
    
    # эталонное умножение
    C_py = np.dot(A, B)
    
    if np.allclose(C_cpp, C_py, atol=1e-1):
        print("✅ верификация пройдена! результаты совпадают.")
    else:
        print("❌ ошибка верификации! результаты сильно различаются.")
        diff = np.abs(C_cpp - C_py).max()
        print(f"максимальное расхождение: {diff}")

if __name__ == "__main__":
    verify()