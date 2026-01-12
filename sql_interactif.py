import os
import dotenv
import pyodbc

dotenv.load_dotenv(override=True)

server = os.environ["TPBDD_SERVER"]
database = os.environ["TPBDD_DB"]
username = os.environ["TPBDD_USERNAME"]
password = os.environ["TPBDD_PASSWORD"]
driver = os.environ["ODBC_DRIVER"]

conn_str = (
    f"DRIVER={driver};"
    f"SERVER=tcp:{server};"
    f"PORT=1433;"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

print("Connexion à Azure SQL...")
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
print("✔️ Connecté\n")

print("Prompt SQL interactif (exit / quit pour quitter)")
print("---------------------------------------------")

while True:
    try:
        query = input("sql> ").strip()

        if query.lower() in ("exit", "quit"):
            break

        if not query:
            continue

        cursor.execute(query)

        # Si la requête retourne des résultats
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

            print(" | ".join(columns))
            print("-" * 40)

            for row in rows:
                print(" | ".join(str(v) for v in row))
        else:
            conn.commit()
            print("✔️ Requête exécutée")

    except Exception as e:
        print("❌ Erreur :", e)

cursor.close()
conn.close()
print("Connexion fermée.")