# Travaux Pratiques Base de Données Azure SQL - Partie 1

## Yannis Andre & Trystan Aubertin

## Exercice 0: Décrivez les tables et les attributs

### Schéma de la base de données

```
tArtist ──────┬───── tJob ─────── tFilm ───── tFilmGenre ───── tGenre
              │
          (N:N)
```

### Description des tables et attributs

#### TABLE 1: tArtist (82,046 lignes)

**Attributs:**
- `idArtist` (nvarchar, NOT NULL) - Identifiant unique de l'artiste
- `primaryName` (nvarchar, NOT NULL) - Nom principal de l'artiste
- `birthYear` (smallint, NULLABLE) - Année de naissance de l'artiste

**Description:** Contient les informations sur tous les artistes (acteurs, réalisateurs, producteurs, etc.) avec leur identifiant unique et leur année de naissance.

---

#### TABLE 2: tFilm (14,294 lignes)

**Attributs:**
- `idFilm` (nvarchar, NOT NULL) - Identifiant unique du film
- `primaryTitle` (nvarchar, NOT NULL) - Titre principal du film
- `startYear` (smallint, NULLABLE) - Année de sortie du film
- `runtimeMinutes` (smallint, NULLABLE) - Durée du film en minutes

**Description:** Contient les informations sur les films avec leur titre, l'année de sortie et la durée.

---

#### TABLE 3: tJob (148,444 lignes)

**Attributs:**
- `idArtist` (nvarchar, NOT NULL) - Identifiant de l'artiste (FK vers tArtist)
- `category` (nvarchar, NULLABLE) - Rôle/catégorie de l'artiste (acteur, réalisateur, producteur, etc.)
- `idFilm` (nvarchar, NULLABLE) - Identifiant du film (FK vers tFilm)

**Description:** Table de jonction (N:N) qui établit les relations entre les artistes et les films, avec le rôle/responsabilité de chaque artiste dans chaque film.

---

#### TABLE 4: tFilmGenre (20,529 lignes)

**Attributs:**
- `idFilm` (nvarchar, NOT NULL) - Identifiant du film (FK vers tFilm)
- `idGenre` (nvarchar, NULLABLE) - Identifiant du genre (FK vers tGenre)

**Description:** Associe les films à leurs genres (une relation N:N entre films et genres).

---

#### TABLE 5: tGenre (0 lignes)

**Attributs:**
- `idGenre` (nvarchar, NOT NULL) - Identifiant unique du genre
- `genre` (nvarchar, NULLABLE) - Nom du genre

**Description:** Définition des genres disponibles (table actuellement vide ou non populée).

---

## Exercice 1 (¼ pt): Visualisez l'année de naissance de l'artiste Kavin Dave

### Approche
Projection sur les attributs `primaryName` et `birthYear` de la table `tArtist`, en filtrant sur le nom de l'artiste 'Kavin Dave'.

### Requête SQL
```sql
SELECT primaryName, birthYear 
FROM tArtist 
WHERE primaryName = 'Kavin Dave';
```

### Résultat
| primaryName | birthYear |
|-------------|-----------|
| Kavin Dave  | 1984      |

### Interprétation
Kavin Dave est né en **1984**.

---

## Exercice 2 (¼ pt): Comptez le nombre d'artistes présents dans la base de données

### Approche
Agrégation `COUNT(*)` sur la table `tArtist` pour compter le nombre total d'artistes.

### Requête SQL
```sql
SELECT COUNT(*) as nombre_artistes 
FROM tArtist;
```

### Résultat
| nombre_artistes |
|-----------------|
| 82046           |

### Interprétation
Il y a **82,046 artistes** au total dans la base de données.

---

## Exercice 3 (¼ pt): Trouvez les noms des artistes nés en 1960, affichez ensuite leur nombre

### Approche
Projection sur l'attribut `primaryName` de la table `tArtist`, en filtrant sur l'année de naissance = 1960, puis compter les résultats.

### Requête SQL
```sql
SELECT primaryName 
FROM tArtist 
WHERE birthYear = 1960 
ORDER BY primaryName;
```

### Résultats (liste partielle)
- A.M. Rathnam
- Adriana Altaras
- Alfonso de Vilallonga
- Amira Ghazalla
- Anders Palm
- ... (affichage partiel)
- Walter Werzowa

### Nombre total
**203 artistes** nés en 1960.

---

## Exercice 4 (1 pt): Trouvez l'année de naissance la plus représentée parmi les acteurs (sauf 0!), et combien d'acteurs sont nés cette année

### Approche
Jointure entre `tArtist` et `tJob`, filtrage sur la catégorie `'acted in'`, exclusion des années 0, puis groupement par `birthYear` et comptage des occurrences.

### Requête SQL
```sql
SELECT TOP 1 a.birthYear, COUNT(*) as count_actors
FROM tArtist a
INNER JOIN tJob j ON a.idArtist = j.idArtist
WHERE j.category = 'acted in' AND COALESCE(a.birthYear, 0) != 0
GROUP BY a.birthYear
ORDER BY count_actors DESC;
```

### Résultat
| birthYear | count_actors |
|-----------|--------------|
| 1978      | 555          |

### Interprétation
L'année de naissance la plus représentée parmi les acteurs est **1978**, avec **555 acteurs** nés cette année.

---

## Exercice 5 (½ pt): Trouvez les artistes ayant joué dans plus d'un film

### Approche
Utilisation d'une sous-requête pour identifier les artistes qui ont un `COUNT(DISTINCT idFilm) > 1` dans la table `tJob`.

### Requête SQL
```sql
SELECT a.primaryName
FROM tArtist a
WHERE a.idArtist IN (
    SELECT idArtist FROM tJob 
    WHERE idFilm IS NOT NULL
    GROUP BY idArtist
    HAVING COUNT(DISTINCT idFilm) > 1
)
ORDER BY a.primaryName;
```

### Résumé des résultats

**Nombre total:** 12,266 artistes ayant joué dans plus d'un film

**Premiers artistes trouvés:**
- 2Kun
- 9m88
- A Deshon Parks
- A Toi
- A$AP Rocky
- A.R. Murugadoss
- A.R. Rahman
- ... et beaucoup d'autres

---

## Exercice 6 (½ pt): Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière

### Approche
Groupement par `idArtist` dans la table `tJob` et filtrage sur `HAVING COUNT(DISTINCT category) > 1` pour trouver ceux avec plusieurs catégories.

### Requête SQL
```sql
SELECT a.primaryName
FROM tArtist a
WHERE a.idArtist IN (
    SELECT idArtist FROM tJob
    GROUP BY idArtist
    HAVING COUNT(DISTINCT category) > 1
)
ORDER BY a.primaryName;
```

### Résumé des résultats

**Nombre total:** 5,985 artistes ayant eu plusieurs responsabilités

**Exemples d'artistes trouvés:**
- A Ram Lakhan
- A. Balakrishnan
- A. Tamilselvan
- A.M. Figliano
- A.M. Nonnis
- Aamir Khan
- Aanand L. Rai
- ... et beaucoup d'autres

### Interprétation
Ces artistes ont occupé **plusieurs postes différents** au cours de leur carrière (ex: acteur ET réalisateur, producteur ET acteur, etc.)

---

## Exercice 7 (¾ pt): Trouver le nom du ou des film(s) ayant le plus d'acteurs

### Approche
Jointure entre `tFilm` et `tJob` en filtrant sur `category = 'acted in'`, puis groupement par film pour compter les acteurs.

### Requête SQL
```sql
SELECT TOP 10 f.primaryTitle, COUNT(*) as num_actors
FROM tFilm f
INNER JOIN tJob j ON f.idFilm = j.idFilm
WHERE j.category = 'acted in'
GROUP BY f.idFilm, f.primaryTitle
ORDER BY num_actors DESC;
```

### Résumé des résultats

**Nombre maximum d'acteurs:** 36 acteurs

**Film(s) ayant le plus d'acteurs:**
- **Heidi - Rescue of the Lynx** (36 acteurs)

### Interprétation
Le film **"Heidi - Rescue of the Lynx"** est le film avec le plus grand nombre d'acteurs dans la base de données, avec **36 acteurs différents** ayant participé au film.

---

## Exercice 8 (1 pt): Montrez les artistes ayant eu plusieurs responsabilités dans un même film

### Approche
Jointure triple entre `tArtist`, `tJob` et `tFilm`, puis groupement par artiste et film pour compter les catégories distinctes.

### Requête SQL
```sql
SELECT a.primaryName, f.primaryTitle, COUNT(DISTINCT j.category) as num_roles
FROM tArtist a
JOIN tJob j ON a.idArtist = j.idArtist
JOIN tFilm f ON j.idFilm = f.idFilm
GROUP BY a.idArtist, a.primaryName, f.idFilm, f.primaryTitle
HAVING COUNT(DISTINCT j.category) > 1
ORDER BY a.primaryName, f.primaryTitle;
```

### Résumé des résultats

**Nombre total de cas:** 6,218 cas (artiste-film) avec plusieurs responsabilités

**Exemples de cas trouvés:**

1. [Redacted] - Ivan: Across the River (2 rôles)
2. A Ram Lakhan - Abhimanyu - A Revenge Story (2 rôles)
3. A. Balakrishnan - Thiruk Kural (2 rôles)
4. A. Tamilselvan - Thotram (2 rôles)
5. A.M. Figliano - The Blood Orange (2 rôles)
6. A.M. Nonnis - Red Wins (2 rôles)
7. Aalok Kumar - Drishyantar (2 rôles)
8. Aamir Khan - Sitaare Zameen Par (2 rôles)
9. Aanand L. Rai - Tere Ishk Mein (2 rôles)
10. Aarjun Verma - Inteqam pyaar ka (3 rôles)
11. Aaron Benham - Bleed Like Me (2 rôles)
12. Aaron Brookner - Nova 78' (2 rôles)
13. Aaron Crocker - Poison Tree (2 rôles)
14. Aaron Dobson - Raw File (2 rôles)
15. Aaron Dylan Kearns - Intravenus (3 rôles)
... et 6,203 autres cas

### Interprétation
Ces artistes ont occupé **plusieurs postes différents DANS LE MÊME FILM**. Par exemple, Aarjun Verma a occupé **3 responsabilités différentes** dans le film "Inteqam pyaar ka" (ex: acteur ET réalisateur ET producteur, ou d'autres combinaisons).

---

## Résumé des résultats

| Exercice | Résultat |
|----------|----------|
| **1** | Kavin Dave est né en 1984 |
| **2** | 82,046 artistes au total |
| **3** | 203 artistes nés en 1960 |
| **4** | 1978 est l'année la plus représentée (555 acteurs) |
| **5** | 12,266 artistes ont joué dans plus d'un film |
| **6** | 5,985 artistes ont eu plusieurs responsabilités |
| **7** | "Heidi - Rescue of the Lynx" avec 36 acteurs |
| **8** | 6,218 cas d'artistes avec plusieurs rôles dans le même film |
