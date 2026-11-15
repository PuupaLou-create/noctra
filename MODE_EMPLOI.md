# NOCTRA — Mode d’emploi

## Mise en ligne gratuite
1. Décompressez le ZIP.
2. Sur GitHub, créez un dépôt public (par exemple `noctra`).
3. Envoyez **le contenu du dossier NOCTRA_Magazine**, pas le dossier parent, à la racine du dépôt (Add file → Upload files → Commit changes).
4. Dans Settings → Pages → Build and deployment, choisissez Deploy from a branch, branche `main`, dossier `/ (root)`, puis Save.
5. Le site sera disponible à `https://VOTRE-PSEUDO.github.io/noctra/` après publication. Si vous utilisez un autre nom de dépôt, l’adresse change.

## Publier un article
1. Dans `data/articles.json`, ajoutez un objet à la liste. Attention aux virgules entre objets.
2. Créez `articles/mon-article.html` avec le même `slug` que dans l’index.
3. Écrivez votre article en HTML simple (`<p>`, `<h2>`, `<a>`, `<img>`, etc.).
4. Envoyez les deux fichiers modifiés sur GitHub. La page d’accueil et la recherche se mettront à jour automatiquement.

### Exemple de fiche d'article
```json
{
  "slug": "mon-article",
  "title": "Titre de mon article",
  "category": "Archives",
  "date": "2026-11-15",
  "excerpt": "Résumé de deux lignes.",
  "tags": ["histoire", "archives"],
  "readingMinutes": 5,
  "published": true
}
```
Rubriques : `Archives`, `Data`, `Arts`, `Enquêtes`, `Laboratoire`.

### Images
Placez les fichiers dans `assets/images/`, puis dans votre article :
```html
<figure><img src="assets/images/mon-image.jpg" alt="Description"><figcaption>Source et crédit.</figcaption></figure>
```
**Attention :** depuis `article.html`, les chemins des images doivent commencer par `assets/images/` (pas `../assets/`).

## Important
- Le nom **NOCTRA** est provisoire : remplacez-le dans les pages HTML si vous choisissez un autre nom.
- L’article « Bienvenue » est une démonstration, pas une recherche historique.
- La recherche couvre titres, résumés et tags, pas le texte intégral.
- Les statistiques de fréquentation ne sont pas encore activées : elles nécessitent un service externe.
- Le site est statique, sans base de données, sans frais d’hébergement sur GitHub Pages (dépôt public).
- Ne publiez pas de données personnelles ou de documents protégés sans autorisation.
