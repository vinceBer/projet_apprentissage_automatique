import pandas as pd

def gravite(value):
    if value in [2,3]:
        return 1
    elif value in [1,4]:
        return 0
    else :
        return -1
    
def femme_homme_conduit(value):
    if value >= 1:
        return 1
    else : 
        return 0

def trajet(value):
    if value in [-1,0]:
        return -1
    else :
        return value 
    
def trajet_2(value):
    if value > 0:
        return 1
    else : 
        return 0    
    
def loc_pieton(value):
    if value == 0 : # pas de pieton (= pas trop de danger)
        return 1
    if value in [2,3,4,5,7,8,9]: # pieton "protégé" (trottroir, refuge,...)
        return 2
    if value in [1,6,7]: # pieton loin d'un passage pieton(il attend pas pour traverser) ou pas "protégé"=accotement
        return 3
    
def etat_pi(value):
    if value in [-1,0]: # sans pieton
        return 1
    elif value in [1,2,3]: # pieton seul ou accompagne
        return 2
    
def avec_sans(value):
    if value > 0:
        return 2
    else :
        return 1   
    

def traitement_usagers_2(usagers_merged,test =False):
    #on fait un nouveau df avec simplement le nb_personne par accident
    new_df = usagers_merged[['Num_Acc']].drop_duplicates() #usagers_merged.groupby('Num_Acc').size().reset_index(name='nb_pers')
    
    # Calcul des occurrences de chaque Num_Acc
    counts = usagers_merged.groupby('Num_Acc').size()
    new_df['nb_pers'] = usagers_merged['Num_Acc'].map(counts)
    
    
    #on définit la "gravité d'un accident 0 ou 1"
    if test==False :
        usagers_merged['grave'] = usagers_merged['grav'].apply(gravite)
    
    # on remplace les na par -1 = inconnue
    usagers_merged['place'] = usagers_merged['place'].fillna(-1)
    
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    #counts_pieton = usagers_merged[usagers_merged['place'] == 10].groupby('Num_Acc')['place'].count()
    #new_df['nb_pietons'] = new_df['Num_Acc'].map(counts_pieton)
    #new_df['nb_pietons']= new_df['nb_pietons'].fillna(0)
    
    #new_df['est_pieton']= new_df['nb_pietons'].apply(trajet_2)
    
    # on compte le nombre de personne à l'avant (à l'avant les accident sont plus grave qu'a l'arrière)
    counts_avant = usagers_merged[(usagers_merged['place'] == 1) | (usagers_merged['place'] == 6) | (usagers_merged['place'] == 1)].groupby('Num_Acc')['place'].count()
    new_df['nb_place_avant'] = new_df['Num_Acc'].map(counts_avant)
    new_df['nb_place_avant'] = new_df['nb_place_avant'].fillna(0)
    
    #new_df['est_a_l_avant'] = new_df['nb_place_avant'].apply(trajet_2)
    
    # on compte le nombre de personne à l'arrière
    counts_arriere = usagers_merged[(usagers_merged['place'] == 4) | (usagers_merged['place'] == 5) | (usagers_merged['place'] == 3)].groupby('Num_Acc')['place'].count()
    new_df['nb_place_arriere'] = new_df['Num_Acc'].map(counts_arriere)
    new_df['nb_place_arriere'] = new_df['nb_place_arriere'].fillna(0)
    
    #new_df['est_a_l_arriere']= new_df['nb_place_arriere'].apply(trajet_2)
    
    # nombre de personne au "centre du véhicule"
    counts_milieu = usagers_merged[(usagers_merged['place'] == 7) | (usagers_merged['place'] == 8) | (usagers_merged['place'] == 9)].groupby('Num_Acc')['place'].count()
    new_df['nb_place_milieu'] = new_df['Num_Acc'].map(counts_milieu)
    new_df['nb_place_milieu'] = new_df['nb_place_milieu'].fillna(0)
    #new_df['est_au_milieu']= new_df['nb_place_milieu'].apply(trajet_2)
    
    # nombre de femme au volant au moment de l'accident
    counts_femme_conduit = usagers_merged[(usagers_merged['place'] == 1) & (usagers_merged['sexe'] == 2)].groupby('Num_Acc')['place'].count()
    new_df['nb_fem_cond'] = new_df['Num_Acc'].map(counts_femme_conduit)
    new_df['nb_fem_cond'] = new_df['nb_fem_cond'].fillna(0)
    
    # nombre de femmes au volant au moment de l'accident
    counts_homme_conduit = usagers_merged[(usagers_merged['place'] == 1) & (usagers_merged['sexe'] == 1)].groupby('Num_Acc')['place'].count()
    new_df['nb_hom_cond'] = new_df['Num_Acc'].map(counts_homme_conduit)
    new_df['nb_hom_cond'] = new_df['nb_hom_cond'].fillna(0)
    
    #booléen si oui ou un homme ou femm était au volant
    #new_df['fe_cond'] = new_df['nb_fem_cond'].apply(femme_homme_conduit)
    #new_df['ho_cond'] = new_df['nb_hom_cond'].apply(femme_homme_conduit)
    
    
    ### partie qui ne fonctionne plus
    
    
    # age moyen par accident grave. On s'attend à ce que un certain age il y ait plus de jeune ou de vieux conducteus qui aient des accidents
    #new_df['moyenne_an_nais'] = usagers_merged.groupby('Num_Acc')['an_nais'].mean()
    #new_df['moyenne_an_nais']= new_df['moyenne_an_nais'].fillna(new_df['moyenne_an_nais'].mean)
    # Calculer l'âge moyen par accident
    df = usagers_merged.groupby('Num_Acc')['an_nais'].mean().reset_index()
    df = df.rename(columns={'an_nais': 'moyenne_an_nais'})

    # Remplacer les valeurs manquantes par la moyenne globale de l'âge
    moyenne_globale = df['moyenne_an_nais'].mean()
    df['moyenne_an_nais'] = df['moyenne_an_nais'].fillna(moyenne_globale)
    new_df = pd.merge(new_df, df, on='Num_Acc', how='inner')
    
    
    ###
    
    
    # on remplace les valeurs inconnues par -1
    usagers_merged['trajet'] = usagers_merged['trajet'].fillna(-1)
    usagers_merged['trajet'] = usagers_merged['trajet'].apply(trajet)

    # le nombre de personnes qui fiasaient le trajet domicile/travail au moment de l'accident
    counts_dom_trav = usagers_merged[(usagers_merged['trajet'] == 1) ].groupby('Num_Acc')['trajet'].count()
    new_df['nb_dom_trav'] = new_df['Num_Acc'].map(counts_dom_trav)
    new_df['nb_dom_trav'] = new_df['nb_dom_trav'].fillna(0)
    
        
    # le nombre de personnes qui fiasaient le trajet domicile/ecole au moment de l'accident
    counts_dom_eco= usagers_merged[(usagers_merged['trajet'] == 2) ].groupby('Num_Acc')['trajet'].count()
    new_df['nb_dom_eco'] = new_df['Num_Acc'].map(counts_dom_eco)
    new_df['nb_dom_eco'] = new_df['nb_dom_eco'].fillna(0)

    # le nombre de personnes qui faisait leurs achat au moment de l'accident
    counts_achat= usagers_merged[(usagers_merged['trajet'] == 3) ].groupby('Num_Acc')['trajet'].count()
    new_df['nb_achat'] = new_df['Num_Acc'].map(counts_achat)
    new_df['nb_achat'] = new_df['nb_achat'].fillna(0)

    # le nombre de personnes qui faisait un trajet professionel au moment de l'accident
    counts_prof= usagers_merged[(usagers_merged['trajet'] == 4) ].groupby('Num_Acc')['trajet'].count()
    new_df['nb_prof'] = new_df['Num_Acc'].map(counts_prof)
    new_df['nb_prof'] = new_df['nb_prof'].fillna(0)

    # le nombre de personnes qui faisait un trajet "loisir" au moment de l'accident
    counts_loisir= usagers_merged[(usagers_merged['trajet'] == 5) ].groupby('Num_Acc')['trajet'].count()
    new_df['nb_loisir'] = new_df['Num_Acc'].map(counts_loisir)
    new_df['nb_loisir'] = new_df['nb_loisir'].fillna(0)

    # si oui ou non il y avait une personne qui faisait tel ou tel trajet au moment de l'accident
    #new_df['dom_trav'] = new_df['nb_dom_trav'].apply(trajet_2)
    #new_df['dom_eco'] = new_df['nb_dom_eco'].apply(trajet_2)
    #new_df['dep_prof'] = new_df['nb_prof'].apply(trajet_2)
    #new_df['dep_loisir'] = new_df['nb_loisir'].apply(trajet_2)
    
    
    #### a ajouter maintenant
    # catu
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    usagers_merged['catu'] = usagers_merged['catu'].replace(4,1)
    
    counts_pieton = usagers_merged[usagers_merged['catu'] == 3].groupby('Num_Acc')['catu'].count()
    new_df['nb_piets'] = new_df['Num_Acc'].map(counts_pieton)
    new_df['nb_piets']= new_df['nb_piets'].fillna(0)


    # ne pas utiliser pieton de catu (le remplacer par la catégorie existante)
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    counts_pass = usagers_merged[usagers_merged['catu'] == 2].groupby('Num_Acc')['catu'].count()
    new_df['nb_passagers'] = new_df['Num_Acc'].map(counts_pass)
    new_df['nb_passagers']= new_df['nb_passagers'].fillna(0)



    # ne pas utiliser pieton de catu (le remplacer par la catégorie existante)
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    counts_conduc = usagers_merged[usagers_merged['catu'] == 1].groupby('Num_Acc')['catu'].count()
    new_df['nb_conducteurs'] = new_df['Num_Acc'].map(counts_conduc)
    new_df['nb_conducteurs']= new_df['nb_conducteurs'].fillna(0)
    
    
    # loc_pie
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    #counts_pas_pi = usagers_merged[usagers_merged['loc_pie'] == 1].groupby('Num_Acc')['loc_pie'].count()
    #new_df['nb_pas_piets'] = new_df['Num_Acc'].map(counts_pas_pi)
    #new_df['nb_pas_piets']= new_df['nb_pas_piets'].fillna(0)


    # ne pas utiliser pieton de catu (le remplacer par la catégorie existante)
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    usagers_merged['locp'] = usagers_merged['locp'].fillna(-1)
    usagers_merged['locp'] = usagers_merged['locp'].replace(-1,0)
    usagers_merged['loc_pie'] = usagers_merged['locp'].apply(loc_pieton)
    
    counts_pi_pro = usagers_merged[usagers_merged['loc_pie'] == 2].groupby('Num_Acc')['catu'].count()
    new_df['nb_pie_prot'] = new_df['Num_Acc'].map(counts_pi_pro)
    new_df['nb_pie_prot']= new_df['nb_pie_prot'].fillna(0) # même si les pietons sont sur le trotoire (ex) plus il y a de pietons plus il y a de risques 



    # ne pas utiliser pieton de catu (le remplacer par la catégorie existante)
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    counts_ss_pro = usagers_merged[usagers_merged['loc_pie'] == 3].groupby('Num_Acc')['catu'].count()
    new_df['nb_ss_prot'] = new_df['Num_Acc'].map(counts_ss_pro)
    new_df['nb_ss_prot']= new_df['nb_ss_prot'].fillna(0) # plus il y a de pietons sans protection plus il y a de risques

    
    # etatp
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    usagers_merged['etatp'] = usagers_merged['etatp'].fillna(-1)
    usagers_merged['etatp'] = usagers_merged['etatp'].apply(etat_pi)
    counts_pas_pi = usagers_merged[usagers_merged['etatp'] == 1].groupby('Num_Acc')['etatp'].count()
    new_df['etatp_sans'] = new_df['Num_Acc'].map(counts_pas_pi)
    new_df['etatp_sans']= new_df['etatp_sans'].fillna(0)
    new_df['etatp_sans_2']= new_df['etatp_sans'].apply(avec_sans)
    new_df = new_df.drop(columns=['etatp_sans']) # plus il y a de pietons non accompagné plus le danger est grand

    # ne pas utiliser pieton de catu (le remplacer par la catégorie existante)
    #on compte le nombre de pieton par accident car si des pieton = accident grave
    #counts_pi_pro = usagers_merged[usagers_merged['etatp'] == 2].groupby('Num_Acc')['etatp'].count()
    #new_df['etatp_avec'] = new_df['Num_Acc'].map(counts_pi_pro)
    #new_df['etatp_avec']= new_df['etatp_avec'].fillna(0) # qu'il y ait 1 pieton accompagné de 1 ou plusiuers plus cela ne change rien
    #nv_df['etatp_avec_2']= nv_df['etatp_avec'].apply(avec_sans)

    #### fin ajout maintennat
        
    if test==False :
        # on récupère si un accident est grave ou pas
        grave_1 = usagers_merged[usagers_merged['grave'] == 1]
        has_grave = grave_1['Num_Acc'].nunique(dropna=False) > 0
        has_grave = pd.Series(has_grave, index=grave_1['Num_Acc'].unique())
        new_df['grave'] = new_df['Num_Acc'].map(has_grave)
        new_df['grave'] = new_df['grave'].fillna(0)#==0
        new_df['grave'] = new_df['grave'].astype(int)

    #new_df = new_df.drop(columns=['nb_hom_cond','nb_fem_cond','nb_place_avant','nb_place_arriere','nb_place_milieu','nb_dom_trav','nb_achat','nb_prof','nb_loisir','nb_dom_eco'])
    
    return new_df