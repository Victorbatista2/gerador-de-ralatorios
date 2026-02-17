import os
import sqlite3
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# carregar .env
load_dotenv()

DB_PATH = os.getenv("DB_PATH")

if not DB_PATH:
    raise ValueError("Banco de dados não encontrado")

# SQL relatório músicas por artista
sql = """
SELECT
    ar.Name AS artista,
    COUNT(t.TrackId) AS total_musicas
FROM Artist ar
JOIN Album al ON al.ArtistId = ar.ArtistId
JOIN Track t ON t.AlbumId = al.AlbumId
GROUP BY ar.ArtistId
ORDER BY total_musicas DESC
LIMIT 20;
"""

# conectar
con = sqlite3.connect(DB_PATH)

# executar
df = pd.read_sql_query(sql, con)

con.close()

# salvar relatório
stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

df.to_excel(f"relatorio_musicas_por_artista_{stamp}.xlsx", index=False)
df.to_csv(f"relatorio_musicas_por_artista_{stamp}.csv", index=False, encoding="utf-8")

print("\nRelatório gerado com sucesso.")
