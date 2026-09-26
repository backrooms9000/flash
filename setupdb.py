'''
setupdb.py
Faz o reset e o setup inicial do banco de dados SELite quando necessário.
PERIGO! Use isso somente em "devtime".
'''

import sqlite3

# Abre (ou cria) o banco de dados
connection = sqlite3.connect("database.db")

# Lê o arquivo SQL modelador do banco de dados
with open("database.sql", "r", encoding="utf-8") as file:
    sql = file.read()

# Executa todo o script SQL
connection.executescript(sql)

# Fecha a conexão
connection.close()

# Feedback
print("Banco de dados preparado com sucesso!")