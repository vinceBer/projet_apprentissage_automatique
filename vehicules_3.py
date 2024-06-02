import pandas as pd

def vehicules_2(value):
    if value > 0:
        return 1
    else : 
        return 0    

def occutc(value):
    value = int(value)
    return value
    
def manoeuvre_2(value):
    if value == 22 : #11%
        return 1
    elif value in [7,12,3]: #17%
        return 2
    elif value in [23,25,18,8,2]: #21%
        return 3
    elif value in [11,16,9,26,20]: #23%
        return 4
    elif value in [10,4,24,15]: #28%
        return 5
    elif value in [-1,1,17,21]: #31%
        return 6
    elif value in [19,5]: #35%
        return 7
    elif value == 14 : #39%
        return 8
    elif value in [13,6]: #43%
        return 9
    

def choc_2(value):
    if value == 4: #18%
        return 1
    elif value in [5,6,7,0,8]: #28%
        return 2
    elif value in [1,2,3]: #31%
        return 3
    elif value == 9: #42%
        return 4
    
def obstable_mobile_2(value):
    if value in [2,4] : #26%
        return 1
    elif value in [1]: #29%
        return 2
    elif value in [-1,0,5,6,9]: #41%
        return 3


    # nombre et types d'obstacles mobiles touches par accident
def obstacle_fixe_2(value): # regroupement par catégorie et %age d'accident grave
    if value in [-1,0,1,4]: # 27%
        return 1
    elif value in [14,9,11]:# - de 34%
        return 2
    elif value in [3,12,7,15,5]: # de 41%
        return 3
    elif value in [8,16,6,10]: # de 50%
        return 4
    elif value in [13,2,17]: # 63%
        return 5

def cat_vehicle_3(value): # regroupement par catégorie et %age d'accident grave
    if value in [50,60,42,43]: # - de 15% de chance d'avior un accident grave
        return 1
    elif value in [32,37,40,80,34]:# - de 23%
        return 2
    elif value in [30,1,13,10,7, -1, 0]: # - de 28%
        return 3
    elif value in [3,31,41,2,99,20,38]: # - de 31% 
        return 4
    elif value in [16,15,14,33,17]: # -37% 
        return 5
    elif value in [39,35,21]: # + de 47% 
        return 6
    elif value == 36: # + de 55%
        return 7

def motor(value): 
    value = int(value)
    if value in [2,3]: #17% le - dangereux (hybride/electrique)
        return 1
    elif value in [4,5]: #23% hydrogène et humain
        return 2
    elif value in [1,6]: #26% hydrocarbures/autres
        return 3

# les variables commentées dans cette fonction permettent d'éviter au maximum le "trop de corrélation"

def traitement_vehicules_2(df_v):

    vehi_df =df_v.groupby('Num_Acc').size().reset_index(name='nb_vehi')#vehi_df = df_v[['Num_Acc']].drop_duplicates()#

    # plus il y a de personnes dans un transport en commun plus il y a de chances d'avoir un accident grave
    # plus il y a de personnes dans un transport en commun plus il y a de chances d'avoir un accident grave
    df_v['occutc'] =df_v['occutc'].fillna(round(df_v['occutc'].mean())) # remplace les na pour la moyenne
    df_v['occutc'] =df_v['occutc'].apply(occutc)
    
    sum_occutc = df_v.groupby('Num_Acc')['occutc'].sum()
    vehi_df['sum_occutc'] = vehi_df['Num_Acc'].map(sum_occutc)
    
    # tous les moteurs n'ont pas la même proba de créer un accident grave
    df_v['motor'] = df_v['motor'].replace(-1,0)
    df_v['motor'] = df_v['motor'].fillna(round(df_v['motor'].mean()))# la moyenne sont les vehicules hydrocarbures (ce qui est le plus utilisé en france)
    df_v['motor'] = df_v['motor'].replace(0,round(df_v['motor'].mean()))

    counts_motor_1 = df_v[(df_v['motor'] == 1)].groupby('Num_Acc')['motor'].count()
    vehi_df['motor_1'] = vehi_df['Num_Acc'].map(counts_motor_1)
    vehi_df['motor_1'] = vehi_df['motor_1'].fillna(0) # si il n'y a pas de moteur de tel ou tel type
    
    counts_motor_2 = df_v[(df_v['motor'] == 2)].groupby('Num_Acc')['motor'].count()
    vehi_df['motor_2'] = vehi_df['Num_Acc'].map(counts_motor_2)
    vehi_df['motor_2'] = vehi_df['motor_2'].fillna(0)
    
    counts_motor_3 = df_v[(df_v['motor'] == 3)].groupby('Num_Acc')['motor'].count()
    vehi_df['motor_3'] = vehi_df['Num_Acc'].map(counts_motor_3)
    vehi_df['motor_3'] = vehi_df['motor_3'].fillna(0)

    #df_v['catv'] = df_v['catv'].apply(cat_vehicle_2)
    df_v['catv'] = df_v['catv'].apply(cat_vehicle_3)

    counts_catv_1 = df_v[(df_v['catv'] == 1)].groupby('Num_Acc')['catv'].count()
    vehi_df['nb_catv_1'] = vehi_df['Num_Acc'].map(counts_catv_1)
    vehi_df['nb_catv_1'] = vehi_df['nb_catv_1'].fillna(0)

    counts_catv_2 = df_v[(df_v['catv'] == 2)].groupby('Num_Acc')['catv'].count()
    vehi_df['nb_catv_2'] = vehi_df['Num_Acc'].map(counts_catv_2)
    vehi_df['nb_catv_2'] = vehi_df['nb_catv_2'].fillna(0)

    counts_catv_3 = df_v[(df_v['catv'] == 3)].groupby('Num_Acc')['catv'].count()
    vehi_df['nb_catv_3'] = vehi_df['Num_Acc'].map(counts_catv_3)
    vehi_df['nb_catv_3'] = vehi_df['nb_catv_3'].fillna(0)

    counts_catv_4 = df_v[(df_v['catv'] == 4)].groupby('Num_Acc')['catv'].count()
    vehi_df['nb_catv_4'] = vehi_df['Num_Acc'].map(counts_catv_4)
    vehi_df['nb_catv_4'] = vehi_df['nb_catv_4'].fillna(0)
    
    counts_catv_5 = df_v[(df_v['catv'] == 5)].groupby('Num_Acc')['catv'].count()
    vehi_df['nb_catv_5'] = vehi_df['Num_Acc'].map(counts_catv_5)
    vehi_df['nb_catv_5'] = vehi_df['nb_catv_5'].fillna(0)

    counts_catv_6 = df_v[(df_v['catv'] == 4)].groupby('Num_Acc')['catv'].count()
    vehi_df['nb_catv_6'] = vehi_df['Num_Acc'].map(counts_catv_6)
    vehi_df['nb_catv_6'] = vehi_df['nb_catv_6'].fillna(0)
    
    counts_catv_7 = df_v[(df_v['catv'] == 4)].groupby('Num_Acc')['catv'].count()
    vehi_df['nb_catv_7'] = vehi_df['Num_Acc'].map(counts_catv_7)
    vehi_df['nb_catv_7'] = vehi_df['nb_catv_7'].fillna(0)

    # nombre de type d'objects fixes touches par accidents
    df_v['obs'] = df_v['obs'].fillna(-1)
    df_v['obs'] = df_v['obs'].apply(obstacle_fixe_2)

    counts_obs_1 = df_v[(df_v['obs'] == 1)].groupby('Num_Acc')['obs'].count()
    vehi_df['obs_1'] = vehi_df['Num_Acc'].map(counts_obs_1)
    vehi_df['obs_1'] = vehi_df['obs_1'].fillna(0)

    counts_obs_2 = df_v[(df_v['obs'] == 2)].groupby('Num_Acc')['obs'].count()
    vehi_df['obs_2'] = vehi_df['Num_Acc'].map(counts_obs_2)
    vehi_df['obs_2'] = vehi_df['obs_2'].fillna(0)

    counts_obs_3 = df_v[(df_v['obs'] == 3)].groupby('Num_Acc')['obs'].count()
    vehi_df['obs_3'] = vehi_df['Num_Acc'].map(counts_obs_3)
    vehi_df['obs_3'] = vehi_df['obs_3'].fillna(0)
    
    ### ajouté pour obstacle fixe 2
    counts_obs_4 = df_v[(df_v['obs'] == 4)].groupby('Num_Acc')['obs'].count()
    vehi_df['obs_4'] = vehi_df['Num_Acc'].map(counts_obs_4)
    vehi_df['obs_4'] = vehi_df['obs_4'].fillna(0)
    
    counts_obs_5 = df_v[(df_v['obs'] == 5)].groupby('Num_Acc')['obs'].count()
    vehi_df['obs_5'] = vehi_df['Num_Acc'].map(counts_obs_5)
    vehi_df['obs_5'] = vehi_df['obs_5'].fillna(0)
    ####
    
    
    # nombre de type d'objects mobiles touches par accidents
    df_v['obsm'] = df_v['obsm'].fillna(-1)
    df_v['obsm'] = df_v['obsm'].apply(obstable_mobile_2)

    counts_obsm_1 = df_v[(df_v['obsm'] == 1)].groupby('Num_Acc')['obsm'].count()
    vehi_df['obsm_1'] = vehi_df['Num_Acc'].map(counts_obsm_1)
    vehi_df['obsm_1'] = vehi_df['obsm_1'].fillna(0)

    counts_obsm_2 = df_v[(df_v['obsm'] == 2)].groupby('Num_Acc')['obsm'].count()
    vehi_df['obsm_2'] = vehi_df['Num_Acc'].map(counts_obsm_2)
    vehi_df['obsm_2'] = vehi_df['obsm_2'].fillna(0)

    counts_obsm_3 = df_v[(df_v['obsm'] == 3)].groupby('Num_Acc')['obsm'].count()
    vehi_df['obsm_3'] = vehi_df['Num_Acc'].map(counts_obsm_3)
    vehi_df['obsm_3'] = vehi_df['obsm_3'].fillna(0)
    
    # nombre d'obstacle touchés de la caté 1
    df_v['choc']= df_v['choc'].fillna(-1)
    df_v['choc']= df_v['choc'].apply(choc_2) 

    counts_choc_1 = df_v[(df_v['choc'] == 1)].groupby('Num_Acc')['choc'].count()
    vehi_df['choc_1'] = vehi_df['Num_Acc'].map(counts_choc_1)
    vehi_df['choc_1'] = vehi_df['choc_1'].fillna(0)

    counts_choc_2 = df_v[(df_v['choc'] == 2)].groupby('Num_Acc')['choc'].count()
    vehi_df['choc_2'] = vehi_df['Num_Acc'].map(counts_choc_2)
    vehi_df['choc_2'] = vehi_df['choc_2'].fillna(0)

    counts_choc_3 = df_v[(df_v['choc'] == 3)].groupby('Num_Acc')['choc'].count()
    vehi_df['choc_3'] = vehi_df['Num_Acc'].map(counts_choc_3)
    vehi_df['choc_3'] = vehi_df['choc_3'].fillna(0)

    counts_choc_4 = df_v[(df_v['choc'] == 4)].groupby('Num_Acc')['choc'].count()
    vehi_df['choc_4'] = vehi_df['Num_Acc'].map(counts_choc_4)
    vehi_df['choc_4'] = vehi_df['choc_4'].fillna(0)
    
    # nombre d'obstacle touchés par catégorie
    df_v['manv'] =df_v['manv'].fillna(-1)
    df_v['manv'] =df_v['manv'].replace(0,-1)
    
    df_v['manv'] =df_v['manv'].apply(manoeuvre_2)
    
    counts_manv_1 = df_v[(df_v['manv'] == 1)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_1'] = vehi_df['Num_Acc'].map(counts_manv_1)
    vehi_df['manv_1'] = vehi_df['manv_1'].fillna(0)

    counts_manv_2 = df_v[(df_v['manv'] == 2)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_2'] = vehi_df['Num_Acc'].map(counts_manv_2)
    vehi_df['manv_2'] = vehi_df['manv_2'].fillna(0)

    counts_manv_3 = df_v[(df_v['manv'] == 3)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_3'] = vehi_df['Num_Acc'].map(counts_manv_3)
    vehi_df['manv_3'] = vehi_df['manv_3'].fillna(0)

    counts_manv_4 = df_v[(df_v['manv'] == 4)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_4'] = vehi_df['Num_Acc'].map(counts_manv_4)
    vehi_df['manv_4'] = vehi_df['manv_4'].fillna(0)

    counts_manv_5 = df_v[(df_v['manv'] == 5)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_5'] = vehi_df['Num_Acc'].map(counts_manv_5)
    vehi_df['manv_5'] = vehi_df['manv_5'].fillna(0)
    
    
    #### ajout ###
    counts_manv_6 = df_v[(df_v['manv'] == 6)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_6'] = vehi_df['Num_Acc'].map(counts_manv_6)
    vehi_df['manv_6'] = vehi_df['manv_6'].fillna(0)
    
    counts_manv_7 = df_v[(df_v['manv'] == 7)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_7'] = vehi_df['Num_Acc'].map(counts_manv_7)
    vehi_df['manv_7'] = vehi_df['manv_7'].fillna(0)
    
    counts_manv_8 = df_v[(df_v['manv'] == 8)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_8'] = vehi_df['Num_Acc'].map(counts_manv_8)
    vehi_df['manv_8'] = vehi_df['manv_8'].fillna(0)
    
    counts_manv_9 = df_v[(df_v['manv'] == 9)].groupby('Num_Acc')['manv'].count()
    vehi_df['manv_9'] = vehi_df['Num_Acc'].map(counts_manv_9)
    vehi_df['manv_9'] = vehi_df['manv_9'].fillna(0)
    
    return vehi_df
