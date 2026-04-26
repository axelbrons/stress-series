# Stress-Series : Analyse Prédictive du Stress Académique par Signaux Physiologiques et Apprentissage Automatique

Ce projet de recherche propose une méthodologie objective pour la mesure et l'anticipation du stress en milieu scolaire. En s'appuyant sur l'acquisition de signaux biomédicaux et des algorithmes d'apprentissage supervisé, ce pipeline vise à identifier les états de surcharge mentale pour prévenir les risques de burn-out et de décrochage académique.

---

## 1. Dispositif Expérimental et Instrumentation

### 1.1 Matériel (Hardware)
L'acquisition des données a été réalisée via la plateforme **BITalino (R)evolution**, utilisant les capteurs suivants :
*   **Électrocardiogramme (ECG) :** Mesure de l'activité électrique cardiaque via des électrodes thoraciques.
*   **Activité Électrodermale (EDA) :** Mesure de la conductance cutanée via des capteurs placés sur les phalanges proximale et distale de l'index et du majeur.

### 1.2 Logiciels et Bibliothèques
*   **Acquisition :** OpenSignals (BLUE).
*   **Traitement du signal :** Environnement Python avec intégration de la bibliothèque **NeuroKit2** pour le filtrage et l'extraction de primitives physiologiques.

### 1.3 Protocole de Recherche
L'étude a été conduite sur un échantillon d'étudiants avec une fréquence d'échantillonnage de **1000 Hz**. Le protocole a été structuré en trois phases distinctes de 5 minutes afin de discriminer les réponses physiologiques :
1.  **Phase de Repos (Baseline) :** Établissement de l'état physiologique de référence.
2.  **Phase de Stress Cognitif :** Induction d'une charge mentale élevée via des tâches de mémorisation sous contrainte temporelle et des parties d'échecs en format "Bullet".
3.  **Phase d'Effort Physique :** Activité motrice intense servant de groupe contrôle pour valider la capacité du modèle à distinguer l'activation sympathique due au stress de celle due à l'exercice physique.

---

## 2. Pipeline de Traitement des Données

Le signal brut subit une série de transformations pour aboutir à un vecteur de caractéristiques exploitable par les modèles :

*   **Segmentation (Windowing) :** Découpage du signal en fenêtres disjointes de 30 secondes ($T=30s$).
*   **Extraction de Caractéristiques (Feature Engineering) :**
    *   **ECG :** Fréquence cardiaque moyenne (`HR_Mean`), variabilité de la fréquence cardiaque (`HRV_RMSSD`, `HRV_pNN50`).
    *   **EDA :** Conductance tonique moyenne (`EDA_Mean`), nombre de pics de sudation (`SCR_Peaks`), amplitude moyenne des réponses (`SCR_Amplitude_Mean`).
*   **Normalisation :** Application d'un **Z-score intra-sujet** pour corriger la variabilité inter-individuelle et se concentrer sur les variations relatives.

---

## 3. Modélisation et Validation

### 3.1 Méthodologie d'Évaluation
Afin de prévenir les biais liés à l'autocorrélation temporelle des signaux d'un même individu (*data leakage*), les modèles ont été validés par une méthode **LOGO (Leave-One-Group-Out)**. Cette approche garantit que les tests sont effectués sur des sujets dont les données n'ont jamais été présentées au modèle lors de l'entraînement.

### 3.2 Résultats Comparatifs
Les performances ont été évaluées selon les métriques de précision (Accuracy) et de score F1 :

| Modèle | F1-Score |
| :--- | :---: |
| Régression Logistique / SVM | 64.66% - 70.99% |
| Random Forest | 82.91% |
| XGBoost | 84.26% |
| **CatBoost** | **88.15%** |

### 3.3 Analyse du Modèle Retenu
Le modèle **CatBoost** a été sélectionné pour sa robustesse face au surapprentissage (overfitting) grâce à l'utilisation d'arbres de décision symétriques.
*   **Efficacité :** Le modèle atteint une Accuracy de 88.14%, avec une sensibilité de 100% sur la classe "Stress".
*   **Interprétabilité :** L'analyse de l'importance des variables identifie la conductance cutanée tonique (`EDA_Mean`) comme le prédicteur majeur (66.8% de poids décisionnel), confirmant la pertinence de l'EDA comme biomarqueur du stress cognitif.

---

## 4. Affiliations et Équipe de Recherche

Ce projet s'inscrit dans le cadre de la **Mineure Recherche (ING4)** au sein de l'**ECE École d'ingénieurs** / Laboratoire **LYRIDS** (Année universitaire 2025/2026).

*   **Étudiants chercheurs :** Axel Bröns, Anas Boutaleb, Omar El Alami El Fellousse.
*   **Encadrement scientifique :** Guilherme Medeiros Machado, Aakash Soni, Faiza Belbachir.

**Contact :** axelbrons@edu.ece.fr
