#!/usr/bin/env python3
"""
Verification que l'export a réussi en vérifiant les données dans Neo4j
"""
import os
import dotenv
from py2neo import Graph

dotenv.load_dotenv(override=True)

neo4j_server = os.environ["TPBDD_NEO4J_SERVER"]
neo4j_user = os.environ["TPBDD_NEO4J_USER"]
neo4j_password = os.environ["TPBDD_NEO4J_PASSWORD"]

graph = Graph(neo4j_server, auth=(neo4j_user, neo4j_password))

print("=" * 70)
print("VÉRIFICATION DE L'EXPORT NEO4J")
print("=" * 70)

# Nombre de films
result = list(graph.run("MATCH (f:Film) RETURN COUNT(f) as count"))
film_count = result[0]["count"] if result else 0
print(f"\n📊 Nombre de nœuds Film: {film_count:,}")

# Nombre d'artistes
result = list(graph.run("MATCH (a:Artist) RETURN COUNT(a) as count"))
artist_count = result[0]["count"] if result else 0
print(f"👥 Nombre de nœuds Artist: {artist_count:,}")

# Nombre total de relations
result = list(graph.run("MATCH ()-[r]->() RETURN COUNT(r) as count"))
rel_count = result[0]["count"] if result else 0
print(f"🔗 Nombre total de relations: {rel_count:,}")

# Détail par type de relation
print("\n📋 Relations par type:")
for rel_type in ["ACTED_IN", "DIRECTED", "PRODUCED", "COMPOSED"]:
    result = list(graph.run(f"MATCH ()-[r:{rel_type}]->() RETURN COUNT(r) as count"))
    count = result[0]["count"] if result else 0
    print(f"   {rel_type}: {count:,}")

# Exemple de film
print("\n📽️ Exemple de film:")
result = list(graph.run("MATCH (f:Film) LIMIT 1 RETURN f"))
if result:
    film = result[0]["f"]
    print(f"   ID: {film['idFilm']}")
    print(f"   Titre: {film['primaryTitle']}")
    print(f"   Année: {film['startYear']}")

# Exemple d'artiste avec relations
print("\n🎬 Exemples d'artistes avec leurs relations:")
result = list(graph.run("""
    MATCH (a:Artist)-[r]->(f:Film)
    RETURN a.primaryName as name, type(r) as rel_type, f.primaryTitle as film_title
    LIMIT 3
"""))

for record in result:
    print(f"   {record['name']} --[{record['rel_type']}]--> {record['film_title']}")

print("\n" + "=" * 70)
print("✅ VÉRIFICATION TERMINÉE - Les données sont bien dans Neo4j!")
print("=" * 70)
