# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# run
if __name__ == "__main__":
    # load data
    data_dict = {}
    for i in range(2000,2025+1):
        df = pd.read_csv(f'wine_data_{i}.csv')
        data_dict[str(i)] = df
    
    # concatenation
    df = pd.concat(data_dict).reset_index(drop=True)

    # transform contries
    df = df[df["Country"].str.match(r"^_{3,4}")]
    df["Country"] = df["Country"].str.replace(r"^_{3,4}", "", regex=True)

    # transform types
    df['Type'] = df['Type'].str.replace(r"^_+", "", regex=True)

    # type hierarchies
    df['Type_2'] = df[df['Type_Level'] == 2]['Type']
    df['Type_3'] = df[df['Type_Level'] == 3]['Type']
    df['Type_4'] = df[df['Type_Level'] == 4]['Type']

    # parent maps
    # aop tranquilles
    aop_tranquilles_less_15 = [
        "Alsace blanc <= 15° (1)",
        "Alsace blanc < 13° (2)",
        "Beaujolais rouge et rosé <= 15° (1)",
        "Beaujolais rouge et rosé < 13° (2)",
        "Bordeaux <= 15° (1)",
        "Bordeaux < 13° (2)",
        "Bourgogne <= 15° (1)",
        "Bourgogne < 13° (2)",
        "Val de Loire <= 15° (1)",
        "Val de Loire < 13° (2)",
        "Côtes du Rhône rouge et rosé <=15° (1)",
        "Côtes du Rhône rouge et rosé < 13° (2)",
        "Languedoc-Roussillon rouge et rosé <= 15° (1)",
        "Languedoc-Roussillon rouge et rosé < 13° (2)",
        "Autres appellations tranquilles non détaillés ( <= 15°) (1)",
        "Autres appellations tranquilles non détaillés (<= 15°) (1)",
        "Autres appellations tranquilles < 13° (2)",
        "Appellations tranquilles > 13° (2)",
        "Complément Vallée du Rhône"
    ]
    aop_tranquilles_less_15_dict = {typ: "AOP tranquilles <= 15°" for typ in aop_tranquilles_less_15} # 4->3

    aop_tranquilles = {
        "AOP tranquilles <= 15°": "AOP tranquilles",
        "AOP tranquilles > 15° (y c. blancs)": "AOP tranquilles"
    } # 3->2

    # champagne
    vins_tranquilles = {
        "Vins tranquilles sans IG avec mention du cépage (1)" : "Vins tranquilles sans IG (1)",
        "Vins tranquilles sans IG sans mention du cépage (1)" : "Vins tranquilles sans IG (1)"
    } # 4->3

    vins_igp_tranquilles = {
        "Vins tranquilles sans IG (1)" : "Vins IGP et sans IG tranquilles",
        "Vins IGP tranquilles (1)" : "Vins IGP et sans IG tranquilles"
    } # 3->2

    # Vins effervescents hors Champagne
    eff_hors_champage = [
        "Vins Mousseux et pétillants AOP (1)",
        "Vins Mousseux et pétillants non AOP et AOP, jusqu'en 2009 (2)",
        "Vins Mousseux et pétillants IGP (y c. rosé) <=2L (1)",
        "Vins Mousseux et pétillants de cépage sans IG (y c. rosé) <=2L (1)",
        "Vins Mousseux et pétillants sans IG sans mention du cépage (y c. rosé) <=2L (1)",
        "Pétillants >2L (1)"
    ]

    eff_hors_champage_dict = {typ : "Vins effervescents hors Champagne" for typ in eff_hors_champage} # 3->2

    # concat parentmaps
    dict_4_3 = aop_tranquilles_less_15_dict | vins_tranquilles

    dict_3_2 = aop_tranquilles | vins_igp_tranquilles | eff_hors_champage_dict

    # apply parentmaps
    df['Type_3'] = df['Type'].replace(dict_4_3)
    df['Type_2'] = df['Type_3'].replace(dict_3_2)

    # save data
    df.to_csv('data_v2.csv')
