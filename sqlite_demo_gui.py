import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time

# Setup database from JSON file
def setup_db():
    with open('data/products.json') as f:
        products = json.load(f)
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS products")
    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            price REAL
        )
    ''')
    c.executemany("INSERT INTO products VALUES (:id, :name, :description, :price)", products)
    conn.commit()
    conn.close()

# Search function
def search_products():
    keyword = entry.get().strip()
    if not keyword:
        messagebox.showwarning("Input Required", "Please enter a keyword to search.")
        return
    start = time.time()
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    like_keyword = f"%{keyword}%"
    c.execute("SELECT * FROM products WHERE description LIKE ?", (like_keyword,))
    results = c.fetchall()
    conn.close()
    elapsed = time.time() - start
    display_results(results, f"Search results for '{keyword}' (Time: {elapsed:.4f} sec):")

# View all function
def view_all():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    results = c.fetchall()
    conn.close()
    display_results(results, "All products:")

# Output display function
def display_results(results, header):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, header + "\n\n")
    if results:
        for row in results:
            output_box.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}, Price: ₹{row[3]}\n")
    else:
        output_box.insert(tk.END, "No results found.")

# Initialize GUI
setup_db()
root = tk.Tk()
root.title("SQLite vs Elasticsearch - Demo GUI")
root.geometry("700x500")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

label = ttk.Label(frame, text="Enter keyword to search in product descriptions:")
label.pack()

entry = ttk.Entry(frame, width=50)
entry.pack(pady=5)

btn_frame = ttk.Frame(frame)
btn_frame.pack()

search_btn = ttk.Button(btn_frame, text="Search", command=search_products)
search_btn.grid(row=0, column=0, padx=5)

view_all_btn = ttk.Button(btn_frame, text="View All", command=view_all)
view_all_btn.grid(row=0, column=1, padx=5)

output_box = tk.Text(frame, wrap=tk.WORD, height=20)
output_box.pack(fill=tk.BOTH, expand=True)

root.mainloop()
