import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

def criar_tabela():
    conn = sqlite3.connect("imc_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            peso REAL,
            altura REAL,
            imc REAL,
            classificacao TEXT
        )
    """)
    conn.commit()
    conn.close()

def inserir_registro(peso, altura, imc, classificacao):
    conn = sqlite3.connect("imc_database.db")
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO registros (data, peso, altura, imc, classificacao)
        VALUES (?, ?, ?, ?, ?)
    """, (data_atual, peso, altura, imc, classificacao))
    conn.commit()
    conn.close()

def obter_registros():
    conn = sqlite3.connect("imc_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros")
    registros = cursor.fetchall()
    conn.close()
    return registros

def exibir_historico():
    registros = obter_registros()
    historico_window = tk.Toplevel(root)
    historico_window.title("Histórico de IMC")

    tree = ttk.Treeview(historico_window, columns=("ID", "Data", "Peso", "Altura", "IMC", "Classificação"))
    tree.heading("#0", text="ID")
    tree.column("#0", width=30, anchor="center")
    tree.heading("#1", text="Data")
    tree.column("#1", width=120, anchor="center")
    tree.heading("#2", text="Peso")
    tree.column("#2", width=70, anchor="center")
    tree.heading("#3", text="Altura")
    tree.column("#3", width=70, anchor="center")
    tree.heading("#4", text="IMC")
    tree.column("#4", width=70, anchor="center")
    tree.heading("#5", text="Classificação")
    tree.column("#5", width=150, anchor="center")

    for registro in registros:
        tree.insert("", tk.END, values=registro)

    tree.pack(padx=10, pady=10)

def calcular_imc():
    try:
        peso = float(entry_peso.get())
        altura_cm = float(entry_altura.get())
        
        if peso <= 0 or altura_cm <= 0:
            resultado.set("Insira valores válidos para peso e altura.")
            return
        
        # Converter altura para metros (de centímetros para metros)
        altura_m = altura_cm / 100
        imc = peso / (altura_m ** 2)
        classificacao = classificar_imc(imc)

        resultado.set(f"Seu IMC é: {imc:.2f}\nClassificação: {classificacao}")

        inserir_registro(peso, altura_cm, imc, classificacao)

    except ValueError:
        resultado.set("Insira valores numéricos válidos.")

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    elif 30 <= imc < 34.9:
        return "Obesidade Grau I"
    elif 35 <= imc < 39.9:
        return "Obesidade Grau II"
    elif imc >= 40:
        return "Obesidade Grau III"

root = tk.Tk()
root.title("Calculadora IMC")

resultado = tk.StringVar()

label_peso = ttk.Label(root, text="Peso (kg):")
label_altura = ttk.Label(root, text="Altura (cm):")
entry_peso = ttk.Entry(root)
entry_altura = ttk.Entry(root)
button_calcular = ttk.Button(root, text="Calcular", command=calcular_imc)
button_historico = ttk.Button(root, text="Histórico", command=exibir_historico)
label_resultado = ttk.Label(root, textvariable=resultado)

label_peso.grid(row=0, column=0, padx=10, pady=5)
label_altura.grid(row=1, column=0, padx=10, pady=5)
entry_peso.grid(row=0, column=1, padx=10, pady=5)
entry_altura.grid(row=1, column=1, padx=10, pady=5)
button_calcular.grid(row=2, column=0, pady=10)
button_historico.grid(row=2, column=1, pady=10)
label_resultado.grid(row=3, column=0, columnspan=2, pady=5)

criar_tabela()

root.mainloop()
