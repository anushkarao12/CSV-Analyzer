import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize app
root = tk.Tk()
root.title("Universal CSV Analyzer")
root.geometry("800x600")

df = None  # global dataframe

# Output area
output_box = scrolledtext.ScrolledText(root, width=100, height=20, font=("Consolas", 10))
output_box.pack(pady=10)

# Function to load CSV
def load_csv():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        df = pd.read_csv(file_path)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"✅ Loaded: {file_path}\n\n")
        output_box.insert(tk.END, df.head().to_string(index=False))
        update_column_options()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Show basic stats
def show_stats():
    if df is not None:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "📊 Basic Statistics:\n\n")
        output_box.insert(tk.END, df.describe().to_string())
    else:
        messagebox.showerror("Error", "No CSV loaded")

# Show null values
def show_nulls():
    if df is not None:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "🧾 Missing Value Count:\n\n")
        output_box.insert(tk.END, df.isnull().sum().to_string())
    else:
        messagebox.showerror("Error", "No CSV loaded")

# Show columns
def show_columns():
    if df is not None:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "📁 Column Names:\n\n")
        output_box.insert(tk.END, "\n".join(df.columns))
    else:
        messagebox.showerror("Error", "No CSV loaded")

# Correlation heatmap
def show_heatmap():
    if df is not None:
        num_df = df.select_dtypes(include=np.number)
        corr = num_df.corr()
        fig, ax = plt.subplots()
        cax = ax.matshow(corr, cmap='coolwarm')
        fig.colorbar(cax)
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
        plt.yticks(range(len(corr.columns)), corr.columns)
        for (i, j), val in np.ndenumerate(corr.values):
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')
        plt.title("Correlation Heatmap", pad=20)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", "No CSV loaded")

# Scatter plot
def plot_scatter():
    x_col = x_col_combo.get()
    y_col = y_col_combo.get()
    if df is not None and x_col in df.columns and y_col in df.columns:
        plt.scatter(df[x_col], df[y_col], alpha=0.7, color='teal')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Scatter Plot: {x_col} vs {y_col}')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", "Invalid column selection")

# Bar plot
def plot_bar():
    col = bar_col_combo.get()
    if df is not None and col in df.columns:
        counts = df[col].value_counts().head(10)
        counts.plot(kind='bar', color='coral')
        plt.title(f'Bar Plot of {col}')
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", "Invalid column selection")

# Update column dropdowns
def update_column_options():
    if df is not None:
        cols = list(df.columns)
        x_col_combo['values'] = cols
        y_col_combo['values'] = cols
        bar_col_combo['values'] = cols

# Top Buttons
tk.Button(root, text="📂 Load CSV", command=load_csv, bg="lightgreen", width=15).pack(pady=5)

frame1 = tk.Frame(root)
frame1.pack(pady=5)

tk.Button(frame1, text="🧮 Show Stats", command=show_stats, width=15).pack(side=tk.LEFT, padx=5)
tk.Button(frame1, text="🕳 Show Nulls", command=show_nulls, width=15).pack(side=tk.LEFT, padx=5)
tk.Button(frame1, text="🗂 Show Columns", command=show_columns, width=15).pack(side=tk.LEFT, padx=5)
tk.Button(frame1, text="📊 Heatmap", command=show_heatmap, width=15).pack(side=tk.LEFT, padx=5)

# Scatter Plot Controls
tk.Label(root, text="📈 Scatter Plot: X vs Y").pack(pady=5)
frame2 = tk.Frame(root)
frame2.pack()

x_col_combo = ttk.Combobox(frame2, state='readonly', width=20)
x_col_combo.pack(side=tk.LEFT, padx=5)
y_col_combo = ttk.Combobox(frame2, state='readonly', width=20)
y_col_combo.pack(side=tk.LEFT, padx=5)
tk.Button(frame2, text="Plot", command=plot_scatter).pack(side=tk.LEFT, padx=5)

# Bar Plot Controls
tk.Label(root, text="📊 Bar Plot (Top 10 categories):").pack(pady=5)
frame3 = tk.Frame(root)
frame3.pack()

bar_col_combo = ttk.Combobox(frame3, state='readonly', width=20)
bar_col_combo.pack(side=tk.LEFT, padx=5)
tk.Button(frame3, text="Plot", command=plot_bar).pack(side=tk.LEFT, padx=5)

# Run app
root.mainloop()
