import os
import mysql.connector
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

conexao = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

if not all([host, port, user, password, database]):
    raise ValueError("conexão com o banco falhou")

# query SQL
sql = """
SELECT * FROM digital_wallet_transactions;
"""

df = pd.read_sql_query(sql, conexao)


#tratamento 
colunas_numericas = ["product_amount", "transaction_fee", "cashback", "loyalty_points"]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")


df = df.dropna()
df = df.drop_duplicates(subset=["transaction_id"])


df["product_amount"] = df["product_amount"].round(2)
df["transaction_fee"] = df["transaction_fee"].round(2)
df["cashback"] = df["cashback"].round(2)

conexao.close()


#salvar relatório
stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

df.to_excel(f"relatorio_wallet_analytics_{stamp}.xlsx", index=False)
df.to_csv(f"relatorio_wallet_analytics_{stamp}.csv", index=False, encoding="utf-8")

print("\nRelatório gerado com sucesso.")
