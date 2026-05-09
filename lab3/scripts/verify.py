import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt

# настройки эксперимента
SIZES = [200, 400, 800, 1200, 1600, 2000]
PROCS = [1, 2, 4, 8]
EXE_PATH = "matmul_mpi.exe"

def generate_input(size):
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    for name, mat in [("matrixA.txt", A), ("matrixB.txt", B)]:
        with open(name, "w") as f:
            f.write(f"{size}\n")
            np.savetxt(f, mat, fmt='%.4f')
    return A, B

def main():
    results = {p: [] for p in PROCS}

    for size in SIZES:
        print(f"\nТестирование размера {size}x{size}...")
        generate_input(size)
        
        for p in PROCS:
            cmd = ["mpiexec", "-n", str(p), EXE_PATH]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            try:
                # парсим вывод c++ (size,procs,time)
                _, _, time_ms = proc.stdout.strip().split(',')
                time_ms = float(time_ms)
                results[p].append(time_ms)
                print(f"  Процессов: {p} | Время: {time_ms:.2f} мс")
            except:
                print(f"  ❌ Ошибка на {p} процессах")
                results[p].append(None)

    # построение графиков
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 1. график времени
    for p in PROCS:
        ax1.plot(SIZES, results[p], marker='o', label=f'{p} проц.')
    ax1.set_title("Зависимость времени выполнения от N")
    ax1.set_xlabel("Размер матрицы (N)")
    ax1.set_ylabel("Время (мс)")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)

    # 2. график ускорения - Speedup -  S = T1 / Tp
    for i, size in enumerate(SIZES):
        t1 = results[1][i]
        if t1:
            speedup = [t1 / results[p][i] if results[p][i] else 0 for p in PROCS]
            ax2.plot(PROCS, speedup, marker='s', label=f'N={size}')
    
    ax2.plot(PROCS, PROCS, '--', color='gray', label='Идеал')
    ax2.set_title("Коэффициент ускорения (Speedup)")
    ax2.set_xlabel("Количество процессов")
    ax2.set_ylabel("S = T1 / Tp")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig("lab3/analysis_plot.png", dpi=150)
    print("\n✅ Анализ завершен. Графики сохранены в lab3/analysis_plot.png")

if __name__ == "__main__":
    main()