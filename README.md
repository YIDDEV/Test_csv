# Test_csv
## 01. Acquisition et Agrégation des Données
Le notebook `01_data_understanding.ipynb` est dédié à la compréhension de la structure des données brutes et à leur transformation vers un format utilisable pour la modélisation de Machine Learning.

#### Objectif Principal
Créer un jeu de données journalier structuré et cohérent (test_dataset.csv), en consolidant l'ensemble des données hétérogènes (séries temporelles des capteurs, journaux d'activité et rapports subjectifs) pour tous les participants. Ce fichier agrégé sert de base unique pour toutes les étapes de prétraitement et de modélisation futures.

#### Méthodologie Clés
##### Exploration par Source : 
Comprendre la granularité et la nature de chaque source de données (Fréquence Cardiaque au niveau minute, Sommeil, Activité, Blessures, Rapports Subjectifs).

##### Définition de la Granularité Cible : 
L'analyse des performances et des blessures étant réalisée sur une base quotidienne, toutes les données ont été agrégées pour obtenir une ligne par participant et par jour.

##### Agrégation Intelligente :
Fréquence Cardiaque (HR) : Calcul de métriques statistiques clés (Moyenne, Maximum, Écart-type, Percentiles P10/P90) pour résumer l'activité cardiaque sur 24 heures.

Activité : Utilisation de la somme des durées, des pas et des calories pour les métriques d'effort physique.

Fusion : Alignement et fusion finale de toutes les métriques et rapports (Fitbit, SRPE, Blessures) sur la colonne date.

#### Résultat Livré
Le notebook génère et exporte le fichier ../data/agregation/test_dataset.csv. Ce dataset est la matrice de travail finale, où chaque ligne représente l'état complet d'un athlète à une date donnée, prêt pour le nettoyage des valeurs manquantes et le développement des modèles.

***

## 02. Traitement et Classification des Images Alimentaires

Le notebook `02_food_images.ipynb`vise à extraire des informations nutritionnelles des photos de repas prises par les participants, malgré les défis inhérents à la reconnaissance d'images alimentaires.

### Objectif

Développer un pipeline pour :
1.  Extraire la date de la prise de vue des images (via métadonnées **EXIF** en priorité).
2.  Classifier les aliments présents sur les photos à l'aide d'un modèle pré-entraîné (ResNet-Food101).
3.  Estimer une valeur calorique journalière pour chaque participant.

### Pipeline et Méthodologie

#### Extraction des Métadonnées (Date et Heure)
* **Priorité EXIF :** La date et l'heure de prise de vue sont extraites des métadonnées EXIF (Tag `DateTimeOriginal`) pour garantir une attribution temporelle précise.

#### Classification et Estimation Calorique
* **Modèle Utilisé :** Un modèle **ResNet-Food101** pré-entraîné a été utilisé pour classer les images dans 101 catégories alimentaires.
* **Estimation :** Une valeur calorique moyenne est attribuée à la classe prédite. L'approche est agrégée au niveau journalier pour capturer une **tendance de consommation**.

### Limites de l'Approche

Les résultats de classification des aliments fournis par le modèle ResNet-Food101 présentent un manque de précision notable. Une fiabilité acceptable n'est observée que pour les prédictions associées à un score de confiance élevé, bien qu'il y ait des exceptions où même ces prédictions restent erronées.

Cette tâche est complexe pour un modèle générique, compte tenu de la forte variabilité des cuisines (inter-culturelle et inter-régionale) et de la difficulté à l'estimation précise des portions et des calories à partir d'une image.

Cette problématique souligne la spécialisation nécessaire, typiquement maîtrisée par des startup comme Nutrify (Brisbane, Australie), qui se concentrent spécifiquement sur la reconnaissance alimentaire contextuelle.

## 03. Variables Cibles et Prétraitement

Le notebook `03_data_presentation.ipynb` finalise la préparation des données en appliquant les corrections de types, en gérant les valeurs manquantes de manière stratégique et en construisant les variables cibles spécifiques pour la modélisation.

### Objectif Principal

Rendre le jeu de données `test_dataset.csv` complet, propre, et structuré avec les variables cibles complexes, prêtes pour l'entraînement des modèles de prédiction.

### Méthodologie

#### 1. Correction des Types et Gestion des Manquants

* **Correction des Types :** Application d'une conversion stricte en `int` (entier) pour les colonnes de compte (pas, minutes, scores) et conversion de la `date` en type `datetime`.
* **Imputation Logique :** Utilisée pour les séries temporelles physiologiques (ex: `resting_hr_day`), combinant l'imputation par la dernière valeur connue (`ffill`) et l'**Interpolation Linéaire** pour maintenir la continuité.

#### 2. Cible 1 : Indice de Performance (Régression)

* **Normalisation :** Toutes les composantes (étapes, sommeil, FC repos, humeur) sont mises à l'échelle (MinMaxScaler) pour garantir l'équité des poids.
* **Construction :** Un indice composé (`Performance_Index`) est créé en agrégeant des indicateurs d'effort et de récupération, basé sur la littérature sportive avec des pondérations pour refléter l'importance relative de chaque facteur.

#### 3. Cible 2 : Risque de Blessure (Classification)

* **Fenêtre Temporelle :** La variable cible binaire (`injury_next_7d`) est créée pour indiquer si une blessure survient dans les **sept jours suivants** le jour d'observation (`J+1` à `J+7`).
* **Méthode :** Utilisation d'une fenêtre glissante (`rolling max` après un décalage `shift(-1)`) pour attribuer le statut de risque (1) à tous les jours précédant l'événement de blessure.
* **Problématique :** La distribution de cette variable révèle un fort **déséquilibre des classes** (minorité de jours de blessures)
