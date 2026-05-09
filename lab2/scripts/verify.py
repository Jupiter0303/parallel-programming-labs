import numpy as np
import subprocess
import os
import time
import matplotlib.pyplot as plt
import csv

SIZES = [200, 400, 800, 1200, 1600, 2000]
THREADS = [1, 2, 4, 8]
EXE_PATH = "./matmul_omp.exe"

def generate_input(size):
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    for name, mat in [("matrixA.txt", A), ("matrixB.txt", B)]:
        with open(name, "w") as f:
            f.write(f"{size}\n")
            np.savetxt(f, mat, fmt='%.4f')
    return A, B

def main():
    results = [] # тут будем хранить {size, threads, time}

    for size in SIZES:
        print(f"\n--- Тест размера {size}x{size} ---")
        A, B = generate_input(size)
        
        for t in THREADS:
            # передаем количество потоков через переменную окружения
            env = os.environ.copy()
            env["OMP_NUM_THREADS"] = str(t)
            
            proc = subprocess.run([EXE_PATH], env=env, capture_output=True, text=True)
            res_threads, res_size, time_ms = proc.stdout.strip().split(',')
            time_ms = float(time_ms)
            
            print(f"  Потоков: {t} | Время: {time_ms:.2f} мс")
            results.append({"size": size, "threads": t, "time": time_ms})

    # сохраняем в CSV
    with open("lab2/results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["size", "threads", "time"])
        writer.writeheader()
        writer.writerows(results)

    # построение графиков
    # 1. график времени
    plt.figure(figsize=(10, 6))
    for t in THREADS:
        subset = [r for r in results if r["threads"] == t]
        plt.plot([r["size"] for r in subset], [r["time"] for r in subset], marker='o', label=f'Threads: {t}')
    plt.title("Время выполнения vs Размер матрицы")
    plt.xlabel("Размер N")
    plt.ylabel("Время (мс)")
    plt.legend()
    plt.grid(True)
    plt.savefig("lab2/plot_time.png")

    # 2. график ускорения (Speedup)
    plt.figure(figsize=(10, 6))
    for size in SIZES:
        t1_time = next(r["time"] for r in results if r["size"] == size and r["threads"] == 1)
        speedup = [t1_time / r["time"] for r in results if r["size"] == size]
        plt.plot(THREADS, speedup, marker='s', label=f'Size: {size}')
    
    plt.plot(THREADS, THREADS, '--', color='gray', label='Идеальное ускорение')
    plt.title("Ускорение S = T1 / Tn")
    plt.xlabel("Число потоков")
    plt.ylabel("Ускорение")
    plt.legend()
    plt.grid(True)
    plt.savefig("lab2/plot_speedup.png")

if __name__ == "__main__":
    main()