import pandas as pd
    
def situation_3(value):
    value = int(value)
    if value in [5,6]: #23%
        return 1
    elif value in [0,1,2]: #38%
        return 2
    elif value in [-1,4,8]: #54%
        return 3
    elif value == 3: #62%
        return 4
    else :
        return 2
    
def plan_2(value):
    value = int(value)
    if value in [-1,0,1]: #37%
        return 1
    elif value in [2,3,4]: #56%
        return 2
    else:
        return 1
    
def prof_3(value):
    if value == 1: #38%
        return 1
    if value == 2: #48%
        return 2
    else :
        return 3 #54%
    
def vosp_3(value):
    value = int(value)
    if value in [1]: #29%
        return 1
    elif value in [2,3]: #32%
        return 2
    elif value in [-1,0]: #43%
        return 3
    
def nbv(value):
    if value =='#ERREUR':
        value = -1
    value = int(value)
    if value == 2:
        return 2
    elif value in [1,3,4,5]: 
        return 1
    else :
        return -1

def d_nbv(value):
    if value =='#ERREUR':
        value = -1
    value = int(value)
    return value
    
def d_nbv2(value):
    if value == 6 :
        return 1
    else :
        return value
    
    
def circ_2(value):
    if value == 1: #24%
        return 1
    elif value in [-1,0,3,4]: #34%
        return 2
    elif value == 2 : #48%
        return 3
    else :
        return 2

def catr_2(value):
    if value == 4: # 28%
        return 1
    elif value in [1,7]: # %30
        return 2
    elif value in [6,2,9,5]:# 45%
        return 3
    elif value ==  3: # 60%
        return 4
    
def latpc(value):
    value= str(value)
    value = value.replace(',','.')
    value = float((value))
    #value = int((value))
    #print(value)
    return value
    
    
def surface(value):
    if value in [-1,1,2,8]: # - de 41%
        return 1
    elif value in [3,4,5,6,7,9]: # + de 57% d'accidents graves
        return 2   
    
def infrastructure_2(value):
    if value == 1: # -de 22% des cas sont dangereux
        return 1
    elif value in [3,8]: # ~ 33%
        return 2
    elif value in [9,6,0,-1,4,5]: #  de 41%
        return 3
    elif value ==2: # de 44%
        return 4
    elif value ==7: #  de 57%
        return 5
    
def traitement_lieux(df_l):
    # je supprime les variables que je ne compte pas utiliser
    df_l = df_l[['Num_Acc','situ','plan','prof','vosp','nbv','circ','catr', 'surf','infra','vma']]#df_l.drop(columns=['vma', 'Unnamed: 0','env1','infra','surf', 'larrout','lartpc','voie', 'v1','v2', 'pr','pr1'])
    
    ##### ce que je viens d'ajouter
    #df_l['lartpc'] = df_l['lartpc'].apply(latpc)
    #df_l['lartpc'] = df_l['lartpc'].round()
    
    df_l['surf'] = df_l['surf'].fillna(-1)
    df_l['surf'] = df_l['surf'].replace(0,-1)
    df_l['surf'] = df_l['surf'].apply(surface)
    
    df_l['infra'] = df_l['infra'].fillna(-1)
    #df_l['infra'] = df_l['infra'].apply(infrastructure)
    df_l['infra'] = df_l['infra'].apply(infrastructure_2)
    ####
    
    # situations
    df_l['situ'] =df_l['situ'].fillna(-1)
    #df_l['situ'] =df_l['situ'].apply(situation)
    #df_l['situ'] =df_l['situ'].apply(situation_2)
    df_l['situ'] =df_l['situ'].apply(situation_3)
    #one hot encoding de situation
    #dummy_situ = pd.get_dummies(df_l['situ'], prefix='plan')
    #df_l = df_l.drop(columns=['situ'], axis=1)
    #df_l = pd.concat([df_l, dummy_situ], axis=1)
    
    # plan
    df_l['plan'] = df_l['plan'].fillna(-1)
    #df_l['plan'] = df_l['plan'].apply(plan)
    df_l['plan'] = df_l['plan'].apply(plan_2)
    #one hot encoding de situation
    #dummy_plan = pd.get_dummies(df_l['plan'], prefix='plan')
    #df_l = df_l.drop(columns=['plan'], axis=1)
    #df_l = pd.concat([df_l, dummy_plan], axis=1)
    
    # prof
    df_l['prof'] = df_l['prof'].fillna(-1)
    #df_l['prof'] = df_l['prof'].apply(prof)  
    #df_l['prof'] = df_l['prof'].apply(prof_2)
    df_l['prof'] = df_l['prof'].replace(0,-1)
    df_l['prof'] = df_l['prof'].apply(prof_3)
    #one hot encoding de prof
    #dummy_prof = pd.get_dummies(df_l['prof'], prefix='prof')
    #df_l = df_l.drop(columns=['prof'], axis=1)
    #df_l = pd.concat([df_l, dummy_prof], axis=1)
    
    # vosp
    df_l['vosp'] = df_l['vosp'].fillna(-1)
    #df_l['vosp'] = df_l['vosp'].apply(vosp)
    df_l['vosp'] = df_l['vosp'].apply(vosp_3)#(vosp_2)
    #one hot encoding de prof
    #dummy_vosp = pd.get_dummies(df_l['vosp'], prefix='vosp')
    #df_l = df_l.drop(columns=['vosp'], axis=1)
    #df_l = pd.concat([df_l, dummy_vosp], axis=1)
    
    # nbv
    df_l['nbv'] = df_l['nbv'].fillna(-1)
    #df_l['nbv'] = df_l['nbv'].apply(nbv)
    #df_l['nbv'] = df_l['nbv'].apply(d_nbv)
    
    df_l['nbv'] = df_l['nbv'].apply(d_nbv)
    df_l['nbv'] = df_l['nbv'].replace(-1,2)
    df_l['nbv'] = df_l['nbv'].apply(d_nbv2)
    #one hot encoding de nbv
    #dummy_nbv = pd.get_dummies(df_l['nbv'], prefix='nbv')
    #df_l = df_l.drop(columns=['nbv'], axis=1)
    #df_l = pd.concat([df_l, dummy_nbv], axis=1)
    
    # circ
    df_l['circ'] = df_l['circ'].fillna(-1)
    #df_l['circ'] = df_l['circ'].apply(circ)
    #df_l['circ'] = df_l['circ'].apply(circ_2)
    df_l['circ'] = df_l['circ'].replace(0,-1)
    df_l['circ'] = df_l['circ'].apply(circ_2)
    #one hot encoding de circ
    #dummy_circ = pd.get_dummies(df_l['circ'], prefix='circ')
    #df_l = df_l.drop(columns=['circ'], axis=1)
    #df_l = pd.concat([df_l, dummy_circ], axis=1)
    
    # catr
    df_l['catr'] = df_l['catr'].fillna(-1)
    #df_l['catr'] = df_l['catr'].apply(catr)
    df_l['catr'] = df_l['catr'].apply(catr_2)
    #one hot encoding de circ
    #dummy_circ = pd.get_dummies(df_l['catr'], prefix='catr')
    #df_l = df_l.drop(columns=['catr'], axis=1)
    #df_l = pd.concat([df_l, dummy_circ], axis=1)
    
    return df_l