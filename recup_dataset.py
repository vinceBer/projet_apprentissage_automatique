import pandas as pd
import os
import chardet
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Fonction pour détecter l'encodage d'un fichier
def detecter_encodage(fichier):
    with open(fichier, 'rb') as f:
        result = chardet.detect(f.read(100000))  # Lire les premiers 100000 octets pour deviner l'encodage
    return result['encoding']

def recuperer_train():
    # je me suis aperçu que certains fichier avaient des séparations en ' , ' et les autres en ' ; ' donc on règle le problème comme ci-dessous
    chemin_base = 'TRAIN/BAAC-Annee-'
    virgule = ['caracteristiques_2010.csv', 'lieux_2010.csv', 'usagers_2010.csv' , 'vehicules_2010.csv', 'caracteristiques_2011.csv', 'lieux_2011.csv', 'usagers_2011.csv', 'vehicules_2011.csv']

    # Initialiser un dictionnaire pour stocker les DataFrames
    dataframes = {}

    # parcourir tous les dossiers pour récupérer toutes les colonnes
    for i in range(2010,2023):
        chemin_dossier = chemin_base+str(i)+'/'
        fichiers = os.listdir(chemin_dossier)

            # Charger chaque fichier CSV dans un DataFrame et l'ajouter au dictionnaire
        for fichier in fichiers:
            # Construire le chemin complet du fichier
            chemin_complet = os.path.join(chemin_dossier, fichier)

            # Détecter l'encodage du fichier
            encodage = detecter_encodage(chemin_complet)

            # Lire le fichier CSV avec l'encodage détecté
            if fichier in virgule :
                df = pd.read_csv(chemin_complet, on_bad_lines='skip', encoding=encodage, sep =',')
            else :
                df = pd.read_csv(chemin_complet, on_bad_lines='skip', encoding=encodage, sep =';')

            # Utiliser le nom du fichier sans l'extension '.csv' comme clé dans le dictionnaire
            cle = fichier.replace('.csv', '')
            dataframes[cle] = df
            
    return dataframes

def merge_c_v_l_u(dataframes):
    # comme ceci, j'essaie de former un grand tableau pour chacune des catégories
    # Initialiser des listes pour stocker les DataFrames de chaque type
    caracteristiques = []
    lieux = []
    vehicules = []
    usagers = []

    # Parcourir les clés du dictionnaire de DataFrames
    for nom_dataframe in dataframes.keys():
        # Vérifier le type de DataFrame et l'ajouter à la liste correspondante
        if nom_dataframe.startswith('caracteristiques'):
            caracteristiques.append(dataframes[nom_dataframe])
        elif nom_dataframe.startswith('lieux'):
            lieux.append(dataframes[nom_dataframe])
        elif nom_dataframe.startswith('vehicules'):
            vehicules.append(dataframes[nom_dataframe])
        elif nom_dataframe.startswith('usagers'):
            usagers.append(dataframes[nom_dataframe])

    # Concaténer tous les DataFrames dans chaque liste pour former un seul DataFrame
    caracteristiques_merged = pd.concat(caracteristiques, ignore_index=True)
    lieux_merged = pd.concat(lieux, ignore_index=True)
    vehicules_merged = pd.concat(vehicules, ignore_index=True)
    usagers_merged = pd.concat(usagers, ignore_index=True)

    # Afficher les premières lignes de chaque DataFrame résultant
    #print("Caractéristiques merged:")
    #print(caracteristiques_merged.head())

    #print("\nLieux merged:")
    #print(lieux_merged.head())

    #print("\nVéhicules merged:")
    #print(vehicules_merged.head())

    #print("\nUsagers merged:")
    #print(usagers_merged.head())
    return caracteristiques_merged, lieux_merged, vehicules_merged, usagers_merged