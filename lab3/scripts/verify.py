import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt

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
        print(f"Размер {size}...")
        generate_input(size)
        
        for p in PROCS:
            # З
            #запуск через mpiexec
            cmd = ["mpiexec", "-n", str(p), EXE_PATH]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            
            # читаем результат из stdout
            res_p, res_size, time_ms = proc.stdout.strip().split(',')
            time_ms = float(time_ms)
            results[p].append(time_ms)
            print(f"  Процессов: {p} | Время: {time_ms:.2f} мс")

    # график ускорения
    plt.figure(figsize=(10, 6))
    for p in PROCS:
        plt.plot(SIZES, results[p], marker='o', label=f'{p} процессов')
    plt.title("MPI: Время выполнения")
    plt.legend()
    plt.grid(True)
    plt.savefig("lab3/mpi_plot.png")
    print("✅ График сохранен в lab3/mpi_plot.png")

if __name__ == "__main__":
    main()