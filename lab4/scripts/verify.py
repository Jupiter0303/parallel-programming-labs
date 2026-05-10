import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt

# параметры тестирования
SIZES = [400, 800, 1200, 1600, 2000]
BLOCK_SIZES = [8, 16, 32]
EXE_PATH = "./matmul_cuda.exe"

def generate_input(size):
    # генерация случайных матриц
    print(f"генерация данных для N={size}...", end=" ", flush=True)
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    for name, mat in [("matrixA.txt", A), ("matrixB.txt", B)]:
        with open(name, "w") as f:
            f.write(f"{size}\n")
            np.savetxt(f, mat, fmt='%.4f')
    print("готов.")
    return A, B

def main():
    if not os.path.exists(EXE_PATH):
        return

    # словарь для хранения результатов {размер_блока: [времена_для_разных_N]}
    results = {bs: [] for bs in BLOCK_SIZES}

    for size in SIZES:
        generate_input(size)
        
        for bs in BLOCK_SIZES:
            #запуск скомпилированной программы с передачей размера блока
            # передаем bs как аргумент командной строки
            proc = subprocess.run([EXE_PATH, str(bs)], capture_output=True, text=True)
            
            try:
                output = proc.stdout.strip().split(',')
                if len(output) == 3:
                    time_ms = float(output[2])
                    results[bs].append(time_ms)
                    print(f"  блок {bs}x{bs} | время ядра: {time_ms:.4f} мс")
                else:
                    print(f"  ошибка вывода программы: {proc.stdout}")
            except Exception as e:
                print(f"  ошибка при обработке блока {bs}: {e}")

    # построение графика
    plt.figure(figsize=(10, 6))
    for bs in BLOCK_SIZES:
        plt.plot(SIZES, results[bs], marker='o', label=f'блок {bs}x{bs}')
    
    plt.title("производительность CUDA: влияние размера блока и размерности N")
    plt.xlabel("размер матрицы (N)")
    plt.ylabel("время выполнения ядра (мс)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig("lab4/cuda_performance.png")
    print("\n✅ все тесты завершены!")
    print("📊 график сохранен как lab4/cuda_performance.png")

if __name__ == "__main__":
    main()