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
    raise ValueError("conexão com o banco de dados falhou")

# query SQL
sql = """
SELECT
    transaction_id,
    user_id,
    transaction_date,
    product_category,
    product_name,
    merchant_name,
    product_amount,
    transaction_fee,
    cashback,
    loyalty_points,
    payment_method,
    transaction_status,
    merchant_id,
    device_type,
    location
FROM digital_wallet_transactions;
"""

# executar
df = pd.read_sql_query(sql, conexao)

conexao.close()

# salvar relatório
stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

df.to_excel(f"relatorio_wallet_analytics_{stamp}.xlsx", index=False)
df.to_csv(f"relatorio_wallet_analytics_{stamp}.csv", index=False, encoding="utf-8")

print("\nRelatório gerado com sucesso.")
