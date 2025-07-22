import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np

def parse_matrix(text):
    try:
        return np.array([[float(num) for num in row.strip().split()] for row in text.strip().split('\n')])
    except:
        messagebox.showerror("Error", "Invalid matrix format. Use space-separated rows.")
        return None

def matrix_operation(op):
    A = parse_matrix(matrix_a_input.get("1.0", tk.END))
    B = parse_matrix(matrix_b_input.get("1.0", tk.END))
    
    if A is None or (op in ['add', 'subtract', 'multiply'] and B is None):
        return

    try:
        if op == 'add':
            result = A + B
            title = "A + B"
        elif op == 'subtract':
            result = A - B
            title = "A - B"
        elif op == 'multiply':
            result = A @ B
            title = "A × B"
        elif op == 'transpose_a':
            result = A.T
            title = "Transpose of A"
        elif op == 'transpose_b':
            result = B.T
            title = "Transpose of B"
        elif op == 'det_a':
            if A.shape[0] != A.shape[1]:
                raise ValueError("Matrix A must be square")
            result = np.linalg.det(A)
            title = "Determinant of A"
        elif op == 'det_b':
            if B.shape[0] != B.shape[1]:
                raise ValueError("Matrix B must be square")
            result = np.linalg.det(B)
            title = "Determinant of B"
        else:
            raise ValueError("Invalid operation")

        show_result(result, title)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_result(result, title):
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, f"📌 {title}:\n\n")
    if isinstance(result, (float, int, np.floating)):
        result_output.insert(tk.END, f"{result:.4f}")
    else:
        formatted = '\n'.join([' '.join([f"{val:.2f}" for val in row]) for row in result])
        result_output.insert(tk.END, formatted)

# GUI Layout
root = tk.Tk()
root.title("🧮 Matrix Operations Tool")
root.geometry("900x600")

# Matrix A Input
tk.Label(root, text="Matrix A (rows space-separated):").grid(row=0, column=0, padx=10, pady=5, sticky='w')
matrix_a_input = scrolledtext.ScrolledText(root, width=40, height=10)
matrix_a_input.grid(row=1, column=0, padx=10, pady=5)

# Matrix B Input
tk.Label(root, text="Matrix B (rows space-separated):").grid(row=0, column=1, padx=10, pady=5, sticky='w')
matrix_b_input = scrolledtext.ScrolledText(root, width=40, height=10)
matrix_b_input.grid(row=1, column=1, padx=10, pady=5)

# Buttons for Operations
ops_frame = tk.Frame(root)
ops_frame.grid(row=2, column=0, columnspan=2, pady=10)

tk.Button(ops_frame, text="➕ Add A + B", command=lambda: matrix_operation('add'), width=18).grid(row=0, column=0, padx=5, pady=5)
tk.Button(ops_frame, text="➖ Subtract A - B", command=lambda: matrix_operation('subtract'), width=18).grid(row=0, column=1, padx=5, pady=5)
tk.Button(ops_frame, text="✖ Multiply A × B", command=lambda: matrix_operation('multiply'), width=18).grid(row=0, column=2, padx=5, pady=5)

tk.Button(ops_frame, text="🔁 Transpose A", command=lambda: matrix_operation('transpose_a'), width=18).grid(row=1, column=0, padx=5, pady=5)
tk.Button(ops_frame, text="🔁 Transpose B", command=lambda: matrix_operation('transpose_b'), width=18).grid(row=1, column=1, padx=5, pady=5)

tk.Button(ops_frame, text="🧮 Determinant |A|", command=lambda: matrix_operation('det_a'), width=18).grid(row=2, column=0, padx=5, pady=5)
tk.Button(ops_frame, text="🧮 Determinant |B|", command=lambda: matrix_operation('det_b'), width=18).grid(row=2, column=1, padx=5, pady=5)

# Result Area
tk.Label(root, text="📋 Result:").grid(row=3, column=0, columnspan=2, sticky='w', padx=10)
result_output = scrolledtext.ScrolledText(root, width=86, height=10)
result_output.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
