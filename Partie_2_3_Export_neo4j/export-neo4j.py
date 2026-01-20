import os

import dotenv
import pyodbc
from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships, merge_relationships
from py2neo.data import Node

# la librairie py2neo est une sorte d'api permettant de manipuler une base de données Neo4j depuis Python (allant de la connexion à l'éxécution de requêtes Cypher en passant par la création de nœuds et de relations)


# on charge les variables d'environnement depuis le fichier .env (qui contient les infos de connexion à la base neo4j et sql server)
dotenv.load_dotenv(override=True)

server = os.environ["TPBDD_SERVER"]
database = os.environ["TPBDD_DB"]
username = os.environ["TPBDD_USERNAME"]
password = os.environ["TPBDD_PASSWORD"]
driver= os.environ["ODBC_DRIVER"]

neo4j_server = os.environ["TPBDD_NEO4J_SERVER"]
neo4j_user = os.environ["TPBDD_NEO4J_USER"]
neo4j_password = os.environ["TPBDD_NEO4J_PASSWORD"]


#on se connecte à la base Neo4j
graph = Graph(neo4j_server, auth=(neo4j_user, neo4j_password))

BATCH_SIZE = 10000

print("Deleting existing nodes and relationships...")
graph.run("MATCH ()-[r]->() DELETE r")
graph.run("MATCH (n:Artist) DETACH DELETE n")
graph.run("MATCH (n:Film) DETACH DELETE n")

# on assure les contraintes d'unicité sur les identifiants
print("Ensuring uniqueness constraints...")
try:
    graph.run("CREATE CONSTRAINT artist_id_unique IF NOT EXISTS FOR (a:Artist) REQUIRE a.idArtist IS UNIQUE")
except Exception:
    try:
        graph.run("CREATE CONSTRAINT ON (a:Artist) ASSERT a.idArtist IS UNIQUE")
    except Exception:
        print("Artist uniqueness constraint exists or could not be created")

try:
    graph.run("CREATE CONSTRAINT film_id_unique IF NOT EXISTS FOR (f:Film) REQUIRE f.idFilm IS UNIQUE")
except Exception:
    try:
        graph.run("CREATE CONSTRAINT ON (f:Film) ASSERT f.idFilm IS UNIQUE")
    except Exception:
        print("Film uniqueness constraint exists or could not be created")

# on se connecte à la base SQL Server et on exporte les données vers Neo4j
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    cursor = conn.cursor()

    # Films
    exportedCount = 0
    cursor.execute("SELECT COUNT(1) FROM TFilm")
    totalCount = cursor.fetchval()
    cursor.execute("SELECT idFilm, primaryTitle, startYear, runtimeMinutes FROM TFilm")
    while True:
        importData = []
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break

        i = 0
        for row in rows:
            # on crée un objet Node avec comme label Film et les propriétés adéquates
            n = Node("Film", idFilm=row[0], primaryTitle=row[1], startYear=row[2], runtimeMinutes=row[3])
            importData.append(n)
            i += 1

        try:
            # on utilise la fonction create_nodes pour insérer les nœuds en batch (batch de 10000 ici)
            create_nodes(graph.auto(), importData, labels={"Film"})
            exportedCount += len(rows)
            print(f"{exportedCount}/{totalCount} title records exported to Neo4j")
        except Exception as error:
            print(error)

    # Artists
    # on fait la même chose pour les artistes
    exportedCount = 0
    cursor.execute("SELECT COUNT(1) FROM tArtist")
    totalCount = cursor.fetchval()
    cursor.execute("SELECT idArtist, primaryName, birthYear FROM tArtist")
    while True:
        importData = []
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break

        for row in rows:
            n = Node("Artist", idArtist=row[0], primaryName=row[1], birthYear=row[2])
            importData.append(n)

        try:
            create_nodes(graph.auto(), importData, labels={"Artist"})
            exportedCount += len(rows)
            print(f"{exportedCount}/{totalCount} artist records exported to Neo4j")
        except Exception as error:
            print(error)

    try:
        # on crée des index pour accélérer les recherches par idFilm et idArtist dans Neo4j
        print("Indexing Film nodes...")
        try:
            graph.run("CREATE INDEX ON :Film(idFilm)")
        except:
            try:
                graph.run("CREATE INDEX FOR (f:Film) ON (f.idFilm)")
            except:
                print("Index on Film already exists or could not be created")
        
        print("Indexing Name (Artist) nodes...")
        try:
            graph.run("CREATE INDEX ON :Artist(idArtist)")
        except:
            try:
                graph.run("CREATE INDEX FOR (a:Artist) ON (a.idArtist)")
            except:
                print("Index on Artist already exists or could not be created")
    except Exception as error:
        print(error)
    except Exception as error:
        print(error)


    # Relationships
    # et enfin on crée les relations entre artistes et films de la même manière
    # on utilise DISTINCT pour éviter les doublons (idArtist, category, idFilm)
    exportedCount = 0
    cursor.execute("SELECT COUNT(*) FROM (SELECT DISTINCT idArtist, category, idFilm FROM tJob) as distinct_jobs")
    totalCount = cursor.fetchval()
    cursor.execute(f"SELECT DISTINCT idArtist, category, idFilm FROM tJob")
    while True:
        importData = { "acted in": [], "directed": [], "produced": [], "composed": [] }
        batch_seen = set()  # pour dédupliquer après normalisation (idArtist, idFilm, category)
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break

        for row in rows:
            cat = (row[1] or "").strip().lower()
            if cat in importData:
                key = (row[0], row[2], cat)
                if key in batch_seen:
                    continue
                relTuple = (row[0], {}, row[2])
                importData[cat].append(relTuple)
                batch_seen.add(key)
            else:
                # catégorie inconnue: on ignore
                continue

        try:
            for cat in importData:
                if importData[cat]:
                    # Remplacer les espaces par des _ pour nommer les types de relation
                    rel_type = cat.replace(" ", "_").upper()
                    try:
                        merge_relationships(
                            graph.auto(),
                            importData[cat],
                            rel_type,
                            start_node_key=("Artist", "idArtist"),
                            end_node_key=("Film", "idFilm")
                        )
                    except Exception:
                        # fallback si merge_relationships indisponible
                        create_relationships(
                            graph.auto(),
                            importData[cat],
                            rel_type,
                            start_node_key=("Artist", "idArtist"),
                            end_node_key=("Film", "idFilm")
                        )
            exportedCount += sum(len(v) for v in importData.values())
            print(f"{exportedCount}/{totalCount} relationships exported to Neo4j")
        except Exception as error:
            print(error)
