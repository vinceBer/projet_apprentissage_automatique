import numpy as np
import pandas as pd

def map_hour(hour_str):
    hour = int(hour_str)
    if hour < 100:
        return 0
    else:
        return hour // 100
    
def heure_group(value):
    value = int(value)
    if value in [1,2,3,4,5]: #" plus dangereux"
        return 4
    if value in [0,6,22,23]:#" 2ème dangereux"
        return 3
    if value in [7,10,11,14,15,16,17,18,19,20,21]: # 3ème plus dangereux
        return 2
    if value in [8,9,12,13]: # - dangereux
        return 1
    
def luminosite(value):
    value =int(value)
    if value in [-1,1,5]: # 29%
        return 1
    elif value in [2,4]:#33%
        return 2
    elif value ==3:#46%
        return 3
    else :
        return 1
    
def intersection(value):
    value = int(value)
    if value in [5,7]: # 14%
        return 1
    if value in [2,3,4,6]: #25%
        return 2
    elif value in [-1,0,1,8,9]: #34%
        return 3
    
def atmospherique(value):
    value = int(value)
    if value == 2: #35%
        return 1
    elif value in [1,3,8]: #41%
        return 2
    elif value in [4,9]: #50%
        return 3
    elif value in [5,6,7]: #60%
        return 4
    else :
        return 1
    
def collision(value):
    value = int(value)
    if value in [2,4]: #20%
        return 1
    elif value in [-1,3]: #25%
        return 2
    elif value in [5,6,7]: #37%
        return 3
    elif value == 1: #40%
        return 4
    else :
        return 3
    
def formatter_an(an):
    if len(str(an)) == 4:  # Si le nombre comporte 4 chiffres
        return int(str(an)[-2:])  # Garder les deux derniers chiffres
    else:
        return an  # Sinon, ne rien changer
        
def agglo(value):
    value = int(value)
    if value ==1: # 59%
        return 1
    elif value == 2: # 31%
        return 2
    else :
        return 1
    

def mois(value): # il faudra peut-être regrouper 1 et 2
    value = int(value)
    if value in [1,2,3,10,11,12]: # 39% d'accident graves
        return 1 
    if value in [4,5,6,9]: # - de 41%
        return 2 
    if value in [7,8]: # + de 46% d'accient grave
        return 3
    else : # om remplit les inconnues par là où il y a le plus d'accident
        return 1    

def group_departement(value):
    if value == '2A' or value == '2B':
        value = 2
        
    value = int(value)
    
    if value not in [971,972,973,974,975,976,977,978,988]:# départements outre-mer
        value = str(value)
        if len(value) > 2:
            value = value[0:2]
    #else :
    #    value = 970
    
    value = int(value)
    return value
    
def dep_2(value):
    if value == 75: #8%
        return 1
    elif value == 92: #12%
        return 2
    elif value == 94: #15%
        return 3
    elif value in [91,976]:#20%
        return 4
    elif value in [95,69,13,93]:#25%
        return 5
    elif value in [95,69,13,93]:#25%
        return 6
    elif value in [54,87,64,33,67,49]:
        return 7
    elif value in [5,6,974,35,975,78,31,60,37]:#29%
        return 8
    elif value in [56,972,29,973,17]:#34
        return 9
    elif value in [66,2,11,63,77,76,42,50,45,80,51]: #37%
        return 10
    elif value in [19,36,1,59,65,9,86,90,14,34,988,20]:#40%
        return 11
    elif value in [22,58,44,26,72,10,68,7,57,18,4,30,83,25,41,27,38,971,28,74,71,62]:#45%
        return 12
    elif value in [3,21,89,79,52,8]:#48%
        return 13
    elif value in [55,978,73,61,12,16,85,47,15,88,81,84,32,70,43,40,977]:#51%
        return 14
    elif value in [24,46,82,98,48,53,39,23]:#le reste%
        return 15
    
        
def traitement_caracteristiques(df_c):
    # je me suis aperçu que l'heure était parfois défifnie
    df_progre = df_c[['Num_Acc']]
    
    df_progre['an'] = df_c['an'].apply(formatter_an)
    
    df_progre['mois'] = df_c['mois'].fillna(-1)
    df_progre['mois'] = df_progre['mois'].apply(mois)
    #df_progre['mois'] = df_progre['mois'].replace(2,1)
    
    #df_progre['mois'] = df_c['mois'].fillna(-1)
    #dummy_mois = pd.get_dummies(df_progre['mois'], prefix='mois')
    #df_progre = df_progre.drop(columns=['mois'], axis=1)
    # Concaténer les variables fictives avec le DataFrame d'origine
    #df_progre = pd.concat([df_progre, dummy_mois], axis=1)
    
    df_progre['dep'] = df_c['dep'].apply(group_departement)
    #df_progre['dep'] = df_progre['dep'].apply(dep)
    df_progre['dep'] = df_progre['dep'].apply(dep_2)

    df_progre['heure']= df_c['hrmn'].fillna(-1)
    df_progre['heure']= df_progre['heure'].apply(lambda x: x.replace(':', '') if ':' in str(x) else x)
    df_progre['heure'] = df_progre['heure'].apply(map_hour)
    df_progre['heure_g'] = df_progre['heure'].apply(heure_group)

    dummy_heure = pd.get_dummies(df_progre['heure_g'], prefix='heure_g')
    df_progre = df_progre.drop(columns=['heure_g','heure'], axis=1)
    # Concaténer les variables fictives avec le DataFrame d'origine
    df_progre = pd.concat([df_progre, dummy_heure], axis=1)


    df_progre['lum'] = df_c['lum'].fillna(-1)
    df_progre['lum'] = df_progre['lum'].apply(luminosite)
    #dummy_lum = pd.get_dummies(df_progre['lum'], prefix='lum')
    #df_progre = df_progre.drop(columns=['lum'], axis=1)
    # Concaténer les variables fictives avec le DataFrame d'origine
    #df_progre = pd.concat([df_progre, dummy_lum], axis=1)

    df_progre['int'] = df_c['int'].fillna(-1)
    df_progre['int'] = df_progre['int'].apply(intersection)

    df_progre['atm'] = df_c['atm'].fillna(-1)
    df_progre['atm'] = df_progre['atm'].apply(atmospherique)

    df_progre['col'] = df_c['col'].fillna(-1)
    df_progre['col'] = df_progre['col'].apply(collision)
    
    df_progre['agg'] = df_c['agg'].fillna(-1)
    df_progre['agg'] = df_progre['agg'].apply(agglo)
    
    df_progre = df_progre.drop(columns=['heure_g_2'])

    return df_progre