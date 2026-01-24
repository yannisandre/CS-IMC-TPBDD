# Partie 4: Requêtes Cypher Neo4j

## Yannis Andre && Trystan Aubertin

### Schéma de la base de données neo4j
(Artist {idArtist, primaryName, birthYear})
  -[:ACTED_IN|DIRECTED|PRODUCED|COMPOSED]->
(Film {idFilm, primaryTitle, startYear, runtimeMinutes})

### **Exercice 1** (¼ pt): Ajouter une personne et vérifier la création
**Requête Cypher:**
```cypher
CREATE (p:Artist {
    idArtist: 'tt' + randomUUID(),
    primaryName: 'Yannis Andre',
    birthYear: 2003
})
RETURN p.primaryName as name, p.birthYear as birthYear
```
La requête crée un nœud `Artist` avec un identifiant random, le nom et l'année de naissance, puis renvoie ces deux attributs pour vérifier l'insert.

**Réponse:** 'Yannis Andre' (née en 2003) a été créée et le nœud existe maintenant dans la base neo4j.

---

### **Exercice 2** (¼ pt): Ajouter un film
**Requête Cypher:**
```cypher
CREATE (f:Film {
    idFilm: 'film_' + randomUUID(),
    primaryTitle: "L'histoire de mon 20 au cours Infrastructure de donnees",
    startYear: 2026,
    runtimeMinutes: 90,
})
RETURN f
```
La requête insère un nœud `Film` avec un identifiant unique, le titre, l'année ainsi que la durée et  retourne le titre et l'année pour confirmer la création.

**Réponse:** Le film "L'histoire de mon 20 au cours Infrastructure de donnees" a été créé en 2026, il dure 90 minutes.

---

### **Exercice 3** (½ pt): Ajouter la relation ACTED_IN
**Requête Cypher:**
```cypher
MATCH (p:Artist {primaryName: 'Yannis Andre'})
MATCH (f:Film {primaryTitle: "L'histoire de mon 20 au cours Infrastructure de donnees"})
CREATE (p)-[r:ACTED_IN]->(f)
RETURN p.primaryName as actor, f.primaryTitle as film
```
La requête trouve l'artiste "Yannis Andre" et le film "L'histoire de mon 20 au cours Infrastructure de donnees" par leur `primaryName`, elle crée ensuite la relation `ACTED_IN` entre les deux. Elle affiche ensuite les deux noeuds pour confirmation

**Réponse:** La relation ACTED_IN a été créée entre Yannis Andre et le film.

---

### **Exercice 4** (½ pt): Ajouter deux professeurs comme réalisateurs
**Requête Cypher:**
```cypher
-- Création des professeurs
MERGE (p1:Artist {
    idArtist: 'prof_' + randomUUID(),
    primaryName: 'Luc Vo Van',
    birthYear: 2015
})

MERGE (p2:Artist {
    idArtist: 'prof_' + randomUUID(),
    primaryName: 'Thierry Rapatout',
    birthYear: 2022
})

-- Ajout des relations DIRECTED
MATCH (p:Artist)
WHERE p.primaryName IN ['Thierry Rapatout', 'Luc Vo Van']
MATCH (f:Film {primaryTitle: "L'histoire de mon 20 au cours Infrastructure de donnees"})
CREATE (p)-[r:DIRECTED]->(f)
RETURN p.primaryName as director, f.primaryTitle as film
```
Les deux blocs `MERGE` permettent de garantir la présence des artistes (ça les crée s'ils sont absents). Les `MATCH` récupèrent ces artistes ainsi que le film cible, `CREATE` ajoute une relation `DIRECTED` pour chacun avant de retourner les couples réalisateur/film.

**Réponse:** Deux professeurs ont été créés et ajoutés comme réalisateurs du film "l'histoire de mon 20 au cours Infrastructure de donnees":
- Thierry Rapatout (né 2022)
- Luc Vo Van (né 2015)
(les dates sont volontairement flatteuses, ne nous remerciez pas)

---

### **Exercice 5** (½ pt): Nicole Kidman et son année de naissance
**Requête Cypher:**
```cypher
MATCH (a:Artist {primaryName: 'Nicole Kidman'})
RETURN a.primaryName as name, a.birthYear as birthYear
```
Le `MATCH` recherche le nœud `Artist` portant comme `primaryName` Nicole Kidman donné, et renvoie son nom et son année de naissance pour vérifier la présence de l'information.

**Réponse:** Nicole Kidman est née en 1967.

---

### **Exercice 6** (½ pt): Visualiser l'ensemble des films
**Requête Cypher:**
```cypher
MATCH (f:Film)
RETURN f.primaryTitle as titre, f.startYear as annee, f.runtimeMinutes as duree
ORDER BY f.startYear DESC
```
Liste tous les nœuds `Film`, retourne le titre, année ainsi que la durée, et trie le résultat par année décroissante (du plus récent au plus ancien)

**Réponse:** 
- **14,294 films** sont dans la base de données

---

### **Exercice 7** (½ pt): Artistes nés en 1963
**Requête Cypher:**
```cypher
MATCH (a:Artist)
WHERE a.birthYear = 1963
RETURN count(*)
```
On filtre les artistes sur l'année de naissance 1963, ensuite on compte le nombre de nœuds.

**Réponse:** 
- 222 artistes sont nés en 1963 selon les données actuelles la la bdd

---

### **Exercice 8** (1 pt): Ensemble des acteurs qui ont joué dans plus d'un film.
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH a.idArtist as artistId, a.primaryName as actor, COUNT(DISTINCT f) as film_count
WHERE film_count > 1
RETURN artistId, actor, film_count
ORDER BY film_count DESC, actor
```
On parcours les relations `ACTED_IN` on agrège ensuitepar artiste pour compter les films distincts, on filtre ceux qui en ont plus d'un film puis on retourne l'id le nom et le nombre de films joués par l'artiste.

**Réponse:** 
- **8,595 acteurs** ont joué dans plus d'1 film

- **Top 5 des acteurs les plus prolifiques:**
  1. Yogi Babu - 22 films
  2. Eric Roberts - 20 films
  3. Achyuth Kumar - 17 films
  4. Redin Kingsley - 16 films
  5. Rudy Ledbetter - 15 films

---

### **Exercice 9** (1 pt): Artistes ayant eu plusieurs responsabilités au cours de leur carrière
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[r:ACTED_IN|DIRECTED|PRODUCED|COMPOSED]->(f:Film)
WITH a.idArtist as artistId, a.primaryName as artist, COUNT(DISTINCT type(r)) as role_count, 
     COLLECT(DISTINCT type(r)) as roles
WHERE role_count > 1
RETURN artistId, artist, role_count, roles
ORDER BY role_count DESC, artist
```
La requête récupère toutes les relations (jeu, réalisation, production, composition), elle compte ensuite le nombre de rôles distincts par artiste et filtre ceux ayant plus d'un rôle. Elle renvoie ainsi l'artiste suivi de la liste des rôles qu'il a occupé.

**Réponse:** 
- **5,985 artistes** ont eu plusieurs responsabilités

- **Top 5 des plus polyvalents (tous avec 4 rôles différents):**
  1. Abbey Abimbola - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  2. Adam Baranello - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  3. Adam Kritzer - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  4. Alec Vrancken - ACTED_IN, DIRECTED, PRODUCED, COMPOSED
  5. Alex Engel - ACTED_IN, DIRECTED, PRODUCED, COMPOSED

---

### **Exercice 10** (1 pt): Artistes avec plusieurs responsabilités dans un même film
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[r:ACTED_IN|DIRECTED|PRODUCED|COMPOSED]->(f:Film)
WITH a.idArtist as artistId, a.primaryName as artist, f.idFilm as filmId, f.primaryTitle as film, 
     COUNT(DISTINCT type(r)) as role_count, COLLECT(DISTINCT type(r)) as roles
WHERE role_count > 1
RETURN artistId, artist, filmId, film, role_count, roles
ORDER BY role_count DESC, artist, film
```
On compte les rôles distincts d'un artiste pour chaque film, on garde uniquement ceux ayant plus d'un rôle sur un même film, puis on retourne les données : (l'artiste, le film , la  liste des rôles cumulés.

**Réponse:**

- **6,218 cas** d'artistes avec plusieurs responsabilités dans un même film

- **Exemples:**
  1. Abbey Abimbola - 4 rôles dans 'Buaya Barat #AbgNakTambahSatuLagi' (ACTED_IN, DIRECTED, PRODUCED, COMPOSED)
  2. Adam Baranello - 4 rôles dans 'Night' (ACTED_IN, DIRECTED, PRODUCED, COMPOSED)
  3. Alexandre Astier - 4 rôles dans 'Kaamelott - Deuxième volet: Partie 1' (ACTED_IN, DIRECTED, PRODUCED, COMPOSED)

---

### **Exercice 11** (2 pt): Film(s) avec le plus d'acteurs (acteurs principaux)
**Requête Cypher:**
```cypher
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH f, COUNT(DISTINCT a) as actor_count
WITH MAX(actor_count) as max_count
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH f.idFilm as filmId, f.primaryTitle as film, f.startYear as annee, COUNT(DISTINCT a) as actor_count, max_count
WHERE actor_count = max_count
RETURN filmId, film, annee, actor_count
ORDER BY film, annee
```
La requête calcule d'abord pour chaque film le nombre distincts d'acteurs elle extrait ensuite le maximum global du nombre d'acteurs dans un film. Enfin elle refiltre les films pour ne garder que ceux qui matchent ce nombre maximum d'acteurs.

**Réponse:** 

- **Nombre maximum d'acteurs: 10**

- **Films avec le plus d'acteurs:** 4600 films ayant 10 acteurs (la base n'a extrait visiblement que 10 acteurs principaux maximum par film)

---

## Version Gremlin (Cosmos DB) 

Les résultats étant plus ou moins les mêmes, nous avons cette fois omis de préciser les réponse des requêtes pour nous concentrer sur l'explication de ces dernières.

### **Exercice 1**: Ajouter une personne et vérifier la création
**Requête Gremlin:**
```gremlin
g.addV('Artist').
  property('id', 'nm14585625').
  property('pk', 1).
  property('primaryName', 'Yannis Andre').
  property('birthYear', 2003).
  valueMap()
```
Crée un sommet `Artist` avec un identifiant unique, la partition key, et renvoie ses propriétés pour vérification.

La requête suivante : 

```
g.V().hasLabel('Artist').has('primaryName', 'Yannis Andre').count()
```

renvoie bien 1, ce qui prouve que l'artiste a bien été crée.

---

### **Exercice 2**: Ajouter un film
**Requête Gremlin:**
```gremlin
g.addV('Film').
  property('id', 'tt45827598').
  property('pk', 2).
  property('primaryTitle', "L'histoire de mon 20 au cours Infrastructure de donnees").
  property('startYear', 2024).
  property('runtimeMinutes', 90).
  valueMap()
```
Insère un sommet `Film` avec identifiant (random mais unique), partition key, titre, année et durée, puis renvoie ses propriétés.

La requête suivante : 

```
g.V().hasLabel('Film').has('id', "t45827598").count()
```

renvoie 1 ce qui atteste de la création du film.

---

### **Exercice 3**: Ajouter la relation ACTED_IN
**Requête Gremlin:**
```gremlin
g.V().hasLabel('Artist').has('id', 'nm14585625').as('p').
  V().hasLabel('Film').has('id', 'tt45827598').as('f').
  addE('ACTED_IN').from('p').to('f').
  select('p', 'f').by('primaryName').by('primaryTitle')
```
Relie l'artiste et le film trouvés, puis retourne les deux noms pour contrôle.

---

### **Exercice 4**: Ajouter deux professeurs comme réalisateurs
**Requête Gremlin:**
```gremlin
// ajout des artsites
g.addV('Artist').
  property('id', 'nm99991').
  property('pk', 1).
  property('primaryName', 'Luc Vo Van').
  property('birthYear', 2015).
  valueMap()

g.addV('Artist').
  property('id', 'nm99992').
  property('pk', 1).
  property('primaryName', 'Thierry Rapatout').
  property('birthYear', 2022).
  valueMap()

// ajout des relations directed
g.V().hasLabel('Artist').has('id', within('nm99991', 'nm99992')).as('p').
  V().hasLabel('Film').has('id', 'tt45827598').as('f').
  addE('DIRECTED').from('p').to('f').
  select('p', 'f').by('primaryName').by('primaryTitle')
```

On garantit la présence  des deux artistes (avec partition key et ids uniques) puis on crée une relation `DIRECTED` vers le film.

---

### **Exercice 5** : Nicole Kidman et son année de naissance
```gremlin
g.V().hasLabel('Artist').has('primaryName', 'Nicole Kidman').valueMap('primaryName', 'birthYear')
```
Récupère et affiche le nom et l'année de naissance de Nicole Kidman.

---

### **Exercice 6**: Visualiser l'ensemble des films
```gremlin
g.V().hasLabel('Film').
  order().by('startYear', decr).
  project('titre', 'annee', 'duree').
    by(coalesce(values('primaryTitle'), constant('N/A'))).
    by(coalesce(values('startYear'), constant('N/A'))).
    by(coalesce(values('runtimeMinutes'), constant('N/A')))
```
Liste les films avec titre, année et durée triés par année décroissante. On utilise `coalesce()` pour gérer les films qui ont certains champs non définis.

---

### **Exercice 7**: Artistes nés en 1963
**Requête Gremlin:**
```gremlin
g.V().hasLabel('Artist').has('birthYear', 1963).count()
```
Compte les artistes dont l'année de naissance est 1963.

---

### **Exercice 8**: Acteurs qui ont joué dans plus d'un film
**Requête Gremlin:**
```gremlin
g.V().hasLabel('Artist').
  where(outE('acted in').count().is(gt(1))).
  order().by(outE('acted in').count(), decr).
  project('actor', 'film_count').
    by(values('primaryName')).
    by(outE('acted in').count()).
  limit(5)
```
Filtre d'abord les artistes ayant plus d'une relation "acted in", trie par nombre de films décroissant **avant la projection**, puis retourne les 5 premiers avec le nom et le nombre de films.

---

### **Exercice 9**: Artistes ayant plusieurs responsabilités
**Requête Gremlin:**
```gremlin
g.V().hasLabel('Artist').
  where(outE('acted in', 'directed', 'produced', 'composed').label().dedup().count().is(gt(1))).
  order().by(outE('acted in', 'directed', 'produced', 'composed').label().dedup().count(), decr).
  project('artist', 'role_count', 'roles').
    by(values('primaryName')).
    by(outE('acted in', 'directed', 'produced', 'composed').label().dedup().count()).
    by(outE('acted in', 'directed', 'produced', 'composed').label().dedup().fold()).
  limit(5)
```
Filtre les artistes ayant plusieurs rôles distincts, trie par nombre de rôles décroissant **avant la projection**, puis retourne les détails des 5 premiers.

---

### **Exercice 10**: Artistes avec plusieurs responsabilités dans un même film
**Requête Gremlin:**
```gremlin
g.V().hasLabel('Artist').as('a').
  outE('acted in', 'directed', 'produced', 'composed').as('e').
  inV().hasLabel('Film').as('f').
  group().by(select('a', 'f')).by(select('e').label().dedup().fold()).
  unfold().
  where(select(values).count(local).is(gt(1))).
  project('artist', 'film', 'role_count', 'roles').
    by(select(keys).select('a').values('primaryName')).
    by(select(keys).select('f').values('primaryTitle')).
    by(select(values).count(local)).
    by(select(values))
```
Regroupe les arêtes par paire artiste/film, filtre ceux ayant plusieurs rôles, puis retourne les détails (nom artiste, titre film, nombre de rôles et liste des rôles).

---

### **Exercice 11**: Film(s) avec le plus d'acteurs
**Requête Gremlin:**
```gremlin
g.V().hasLabel('Film').
  order().by(inE('acted in').count(), decr).
  limit(1).
  project('film', 'annee', 'actor_count').
    by(coalesce(values('primaryTitle'), constant('N/A'))).
    by(coalesce(values('startYear'), constant('N/A'))).
    by(inE('acted in').count())
```
Groupe les films par nombre d'arêtes "acted in" entrantes (le nombre d'acteurs) puis trie de manière décroissante pour extraire le groupe avec le maximum, enfin on  retourne les infos des films avec ce maximum.

---

