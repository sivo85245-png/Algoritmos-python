import csv
import random
from datetime import datetime, timedelta

# Gera 900 registros
qtd = 900
inicio = datetime(2025, 11, 1, 12, 0, 0)

with open("logs_servidor.csv", "w", newline="", encoding="utf-8") as arq:
    escritor = csv.writer(arq)
    escritor.writerow(["timestamp", "ip", "metodo", "rota", "status", "tamanho_bytes"])

    for i in range(qtd):
        momento = inicio + timedelta(seconds=i)
        ip = f"192.168.0.{random.randint(1,255)}"
        metodo = random.choice(["GET", "POST", "PUT", "DELETE"])
        rota = random.choice(["/login", "/logout", "/dashboard", "/api/v1/users", "/api/v1/payments"])
        status = random.choice([200, 201, 404, 500])
        tamanho = random.randint(100, 500000)
        escritor.writerow([momento.isoformat(), ip, metodo, rota, status, tamanho])

print("✅ Arquivo 'logs_servidor.csv' criado com 900 linhas!")
