import numpy as np
import subprocess
import os
import time
import matplotlib.pyplot as plt

# настройки
SIZES = [200, 400, 600, 800, 1000, 1200, 1500, 2000]
EXE_PATH = "./matmul.exe" if os.name == "nt" else "./matmul"

def generate_input(size):
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    for name, mat in [("matrixA.txt", A), ("matrixB.txt", B)]:
        with open(name, "w") as f:
            f.write(f"{size}\n")
            np.savetxt(f, mat, fmt='%.4f')
    return A, B

def run_test(size):
    A, B = generate_input(size)
    
    start_time = time.time()
    subprocess.run([EXE_PATH], check=True, capture_output=True)
    end_time = time.time()
    
    cpp_time = (end_time - start_time) * 1000 # время в мс
    
    # верификация
    C_cpp = np.loadtxt("matrixC.txt", skiprows=1)
    C_py = np.dot(A, B)
    
    if not np.allclose(C_cpp, C_py, atol=1e-1):
        print(f"❌ ошибка на размере {size}")
        return None
    
    return cpp_time

def main():
    if not os.path.exists(EXE_PATH):
        print("сначала скомпилируйте c++ код!")
        return

    results = []
    print(f"{'размер':<10} | {'время (мс)':<10}")
    print("-" * 25)

    for size in SIZES:
        t = run_test(size)
        if t is not None:
            print(f"{size:<10} | {t:<10.2f}")
            results.append(t)

    # построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(SIZES, results, marker='o', linestyle='-', color='b', label='фактическое время')
    
    # теоретическая кривая O(n^3) для сравнения
    theoretical = [ (n**3) / (SIZES[0]**3) * results[0] for n in SIZES]
    plt.plot(SIZES, theoretical, linestyle='--', color='r', label='теоретическая сложность O(n^3)')

    plt.title("зависимость времени выполнения от размера матрицы")
    plt.xlabel("размер матрицы (N x N)")
    plt.ylabel("время (мс)")
    plt.grid(True)
    plt.legend()
    plt.savefig("lab1/performance_plot.png") # сохраняем график для отчета
    print("\n✅ график сохранен как performance_plot.png")

if __name__ == "__main__":
    main()