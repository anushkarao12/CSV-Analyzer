import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load and prepare data
df = pd.read_csv('train.csv')
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt']
target = 'SalePrice'
data = df[features + [target]].dropna()
X = data[features]
y = data[target]

# Train model
model = LinearRegression()
model.fit(X, y)

# GUI Application
def predict_price():
    try:
        # Get values from entry boxes
        input_data = [
            int(entry_quality.get()),
            int(entry_area.get()),
            int(entry_garage.get()),
            int(entry_basement.get()),
            int(entry_bath.get()),
            int(entry_year.get())
        ]
        df_input = pd.DataFrame([input_data], columns=features)
        predicted_price = model.predict(df_input)[0]
        result_label.config(text=f"Predicted Price: ${predicted_price:,.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")

# Main window
root = tk.Tk()
root.title("House Price Predictor")
root.geometry("400x400")
root.resizable(False, False)

# Form fields
tk.Label(root, text="Overall Quality (1-10):").pack(pady=5)
entry_quality = tk.Entry(root)
entry_quality.pack()

tk.Label(root, text="Living Area (sq ft):").pack(pady=5)
entry_area = tk.Entry(root)
entry_area.pack()

tk.Label(root, text="Garage Capacity (cars):").pack(pady=5)
entry_garage = tk.Entry(root)
entry_garage.pack()

tk.Label(root, text="Total Basement Area (sq ft):").pack(pady=5)
entry_basement = tk.Entry(root)
entry_basement.pack()

tk.Label(root, text="Full Bathrooms:").pack(pady=5)
entry_bath = tk.Entry(root)
entry_bath.pack()

tk.Label(root, text="Year Built:").pack(pady=5)
entry_year = tk.Entry(root)
entry_year.pack()

# Predict button
tk.Button(root, text="Predict Price", command=predict_price, bg="blue", fg="white").pack(pady=20)

# Result
result_label = tk.Label(root, text="Predicted Price: ", font=("Arial", 12))
result_label.pack(pady=10)

# Start GUI
root.mainloop()
