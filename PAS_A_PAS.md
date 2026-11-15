# NOCTRA — Guide de publication

## 1. Mettre à jour le site déjà en ligne
Ce ZIP est une mise à jour de ton dépôt GitHub `noctra`.
- Décompresse le ZIP.
- Dans le dépôt GitHub, utilise **Add file → Upload files** pour ajouter les nouveaux fichiers.
- Pour les fichiers qui existent déjà, GitHub peut proposer leur remplacement par glisser-déposer si tu conserves les mêmes chemins. Vérifie attentivement les chemins avant de valider.
- Clique sur **Commit changes**.
- GitHub Pages republiera automatiquement le site. Tu n'as pas besoin de créer un autre dépôt.

## 2. Écrire un article sans coder
- Ouvre `https://puupalou-create.github.io/noctra/studio.html` une fois la mise à jour publiée.
- Remplis le titre, la catégorie, la date, le résumé et les mots-clés.
- Rédige ton article dans la zone de texte. Les boutons permettent le gras, l'italique, les titres, liens et images.
- **Important** : avant de publier, récupère la version la plus récente de `data/articles.json` sur GitHub (ouvre le fichier puis clique sur **Download raw file**) et importe-la dans le Studio. Cela évite d'écraser les fiches d'articles déjà publiées.
- Clique sur **Télécharger les 2 fichiers**. Le navigateur téléchargera `identifiant.html` et `articles.json`.
- Sur GitHub, place le fichier HTML dans le dossier `articles/`.
- Remplace le fichier `data/articles.json` par le nouveau `articles.json`. Le chemin final doit rester `data/articles.json`.
- Valide les modifications avec **Commit changes**. Le nouvel article apparaîtra sur le site après publication.
- Pour les images locales, envoie-les aussi dans `assets/images/`. Dans le Studio, indique `assets/images/nom.jpg`.

## 3. Statistiques de fréquentation
- Crée un compte sur `https://www.goatcounter.com/` (gratuit pour usage non commercial, selon conditions du fournisseur).
- Choisis un identifiant de site.
- Édite `assets/js/config.js` sur GitHub :
  `window.NOCTRA_GOATCOUNTER = "ton-identifiant";`
- Enregistre. Les visites commenceront à être mesurées après la mise à jour.
- Consulte `https://ton-identifiant.goatcounter.com/` pour le tableau de bord.
- Avant configuration, **aucune statistique n'est enregistrée par ce module**.
- Vérifie les règles de confidentialité applicables et informe tes lecteurs de l'outil utilisé.

## Notes importantes
- Le Studio est public et accessible aux visiteurs, mais il **ne peut pas modifier ton dépôt GitHub** : seuls les comptes autorisés peuvent publier.
- Le bouton « Enregistrer un brouillon » stocke le texte dans le navigateur utilisé. Il ne remplace pas une sauvegarde.
- L'éditeur repose sur la mise en forme native du navigateur et peut nécessiter des retouches pour les mises en page complexes.
- Ne colle pas de code provenant de sources non fiables. Vérifie les droits des images et indique les sources de tes recherches.
- La recherche du site porte sur les titres, résumés et mots-clés, pas le texte intégral.
