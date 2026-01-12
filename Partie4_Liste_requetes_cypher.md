# Partie 4: Requêtes Cypher Neo4j

## Yannis Andre && Trystan Aubertin

### **Exercice 1** (¼ pt): Ajouter une personne et vérifier la création
**Requête Cypher:**
```cypher
CREATE (p:Artist {
    nconst: 'tt' + randomUUID(),
    primaryName: 'Gabriel Martin',
    birthYear: 1995
})
RETURN p.primaryName as name, p.birthYear as birthYear
```
**Réponse:** La personne 'Gabriel Martin' (née en 1995) a été créée et le nœud existe maintenant dans la base de données.

---

### **Exercice 2** (¼ pt): Ajouter un film
**Requête Cypher:**
```cypher
CREATE (f:Film {
    tconst: 'film_' + randomUUID(),
    primaryTitle: "L'histoire de mon 20 au cours Infrastructure de donnees",
    startYear: 2024,
    runtimeMinutes: 90,
    genres: 'Documentary'
})
RETURN f.primaryTitle as titre, f.startYear as annee
```
**Réponse:** Le film "L'histoire de mon 20 au cours Infrastructure de donnees" a été créé en 2024, avec une durée de 90 minutes (Documentary).

---

### **Exercice 3** (½ pt): Ajouter la relation ACTED_IN
**Requête Cypher:**
```cypher
MATCH (p:Artist {primaryName: 'Gabriel Martin'})
MATCH (f:Film {primaryTitle: "L'histoire de mon 20 au cours Infrastructure de donnees"})
CREATE (p)-[r:ACTED_IN]->(f)
RETURN p.primaryName as actor, f.primaryTitle as film
```
**Réponse:** La relation ACTED_IN a été créée entre Gabriel Martin et le film.

---

### **Exercice 4** (½ pt): Ajouter deux professeurs comme réalisateurs
**Requête Cypher:**
```cypher
-- Création des professeurs
MERGE (p1:Artist {
    nconst: 'prof_' + randomUUID(),
    primaryName: 'Dr. Antoine Dupont',
    birthYear: 1965
})

MERGE (p2:Artist {
    nconst: 'prof_' + randomUUID(),
    primaryName: 'Prof. Marie Leclerc',
    birthYear: 1972
})

-- Ajout des relations DIRECTED
MATCH (p:Artist)
WHERE p.primaryName IN ['Dr. Antoine Dupont', 'Prof. Marie Leclerc']
MATCH (f:Film {primaryTitle: "L'histoire de mon 20 au cours Infrastructure de donnees"})
CREATE (p)-[r:DIRECTED]->(f)
RETURN p.primaryName as director, f.primaryTitle as film
```
**Réponse:** Deux professeurs ont été créés et ajoutés comme réalisateurs:
- Dr. Antoine Dupont (né 1965)
- Prof. Marie Leclerc (née 1972)

---

### **Exercice 5** (½ pt): Nicole Kidman et son année de naissance
**Requête Cypher:**
```cypher
MATCH (a:Artist {primaryName: 'Nicole Kidman'})
RETURN a.primaryName as name, a.birthYear as birthYear
```
**Réponse:** Nicole Kidman a été trouvée dans la base de données (l'année de naissance n'est pas disponible dans les données actuelles).

---

### **Exercice 6** (½ pt): Visualiser l'ensemble des films
**Requête Cypher:**
```cypher
MATCH (f:Film)
RETURN f.primaryTitle as titre, f.startYear as annee, f.runtimeMinutes as duree
ORDER BY f.startYear DESC
```
**Réponse:** 
- **Total: 14,164 films** dans la base de données
- Les films sont classés par année décroissante (du plus récent au plus ancien)

---

### **Exercice 7** (½ pt): Artistes nés en 1963
**Requête Cypher:**
```cypher
MATCH (a:Artist)
WHERE a.birthYear = 1963
RETURN a.primaryName as name, a.birthYear as birthYear
ORDER BY a.primaryName
```
**Réponse:** 
- **Nombre d'artistes nés en 1963: 0**
- Aucun artiste avec cette année de naissance dans les données actuelles

---

### **Exercice 8** (1 pt): Acteurs ayant joué dans plusieurs films
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH a.primaryName as actor, COUNT(DISTINCT f) as film_count
WHERE film_count > 1
RETURN DISTINCT actor, film_count
ORDER BY film_count DESC, actor
```
**Réponse:** 
- **Total: 8,766 acteurs** ont joué dans plus d'1 film
- **Top 5 des acteurs les plus prolifiques:**
  1. Yogi Babu - 22 films
  2. Eric Roberts - 20 films
  3. Achyuth Kumar - 17 films
  4. Redin Kingsley - 16 films
  5. Rudy Ledbetter - 15 films

---

### **Exercice 9** (1 pt): Artistes avec plusieurs responsabilités
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[r:ACTED_IN|DIRECTED|PRODUCED|COMPOSED]->(f:Film)
WITH a.primaryName as artist, COUNT(DISTINCT type(r)) as role_count, 
     COLLECT(DISTINCT type(r)) as roles
WHERE role_count > 1
RETURN artist, role_count, roles
ORDER BY role_count DESC, artist
```
**Réponse:** 
- **Total: 6,149 artistes** ont eu plusieurs responsabilités
- **Top 5 des plus polyvalents (tous avec 4 rôles différents):**
  1. Abbey Abimbola - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  2. Adam Baranello - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  3. Adam Kritzer - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  4. Alec Vrancken - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  5. Alex Engel - ACTED_IN, DIRECTED, PRODUCED, COMPOSED

---

### **Exercice 10** (1 pt): Artistes avec plusieurs responsabilités dans UN MÊME film
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[r:ACTED_IN|DIRECTED|PRODUCED|COMPOSED]->(f:Film)
WITH a.primaryName as artist, f.primaryTitle as film, 
     COUNT(DISTINCT type(r)) as role_count, COLLECT(DISTINCT type(r)) as roles
WHERE role_count > 1
RETURN artist, film, role_count, roles
ORDER BY role_count DESC, artist, film
```
**Réponse:** 
- **Total: 6,259 cas** d'artistes avec plusieurs responsabilités dans un même film
- **Exemples:**
  1. Abbey Abimbola - 4 rôles dans 'Buaya Barat #AbgNakTambahSatuLagi' (ACTED_IN, DIRECTED, PRODUCED, COMPOSED)
  2. Adam Baranello - 4 rôles dans 'Night' (ACTED_IN, DIRECTED, PRODUCED, COMPOSED)
  3. Alexandre Astier - 4 rôles dans 'Kaamelott - Deuxième volet: Partie 1' (ACTED_IN, DIRECTED, PRODUCED, COMPOSED)

---

### **Exercice 11** (2 pt): Film(s) avec le plus d'acteurs
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH f.primaryTitle as film, COUNT(DISTINCT a) as actor_count
WITH MAX(actor_count) as max_count
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH f.primaryTitle as film, COUNT(DISTINCT a) as actor_count, max_count
WHERE actor_count = max_count
RETURN film, actor_count
ORDER BY film
```
**Réponse:** 
- **Nombre maximum d'acteurs: 30**
- **Film avec le plus d'acteurs:** 'Trapped' (30 acteurs)

---

