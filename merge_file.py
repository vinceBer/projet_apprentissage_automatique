import pandas as pd
def tout_merge(usagers_merged_lignes_uniques_v2, vehicules_merged_v3, lieux_merged_v2, caracteristiques_merged_v2):
    
    df_final  = pd.merge(caracteristiques_merged_v2, lieux_merged_v2, on='Num_Acc', how='inner')
    
    df_final = pd.merge(df_final, usagers_merged_lignes_uniques_v2, on='Num_Acc', how='inner')

    df_final = pd.merge(df_final, vehicules_merged_v3, on='Num_Acc', how='inner')
    
    df_final = df_final.fillna(-1)
    
    
    return df_final