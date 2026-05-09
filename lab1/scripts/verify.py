import numpy as np
import os

# функция генерации случайных матриц
def generate_input(size):
    print(f"Генерация матриц размером {size}x{size}...")
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    
    with open("matrixA.txt", "w") as f:
        f.write(f"{size}\n")
        np.savetxt(f, A, fmt='%.4f')
        
    with open("matrixB.txt", "w") as f:
        f.write(f"{size}\n")
        np.savetxt(f, B, fmt='%.4f')

if __name__ == "__main__":
    generate_input(500)