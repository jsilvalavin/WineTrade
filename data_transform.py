import pandas as pd

# transform function
def data_transform(df, save_csf = False, save_name = "unnamed.csv"):
    # select columns
    data = df[[
    'ANNREF',
    'D_0015_DIM2_LIB',
    'D_0015_DIM3_LIB',
    'D_0015_DIM5_LIB',
    'N027_LIB',
    'N053_LIB',
    'VALEUR',
    ]]
    # rename columns
    rename_dict = {
    "ANNREF" : "Year",
    "D_0015_DIM2_LIB": "Type",
    "D_0015_DIM3_LIB": "Color",
    "D_0015_DIM5_LIB": "Country",
    "N027_LIB": "Exchange",
    "N053_LIB": "Period",
    "VALEUR": "Value"
    }
    data = data.rename(columns=rename_dict)
    # hierarchy
    data["Type_Level"] = data["Type"].str.extract(r'^(_+)', expand=False).str.len().fillna(0).astype(int)
    data["Country_Level"] = data["Country"].str.extract(r'^(_+)', expand=False).str.len().fillna(0).astype(int)

    data['Period_Level'] = None
    data['Period_Level'][data['Period']=='Total annuel'] = 0
    data['Period_Level'][~(data['Period']=='Total annuel')] = 1

    data['Color_Level'] = None
    data['Color_Level'][data['Color']=='Total couleurs'] = 0
    data['Color_Level'][~(data['Color']=='Total couleurs')] = 1

    data['Exchange_Type'] = None
    data['Exchange_Type'][data['Exchange']=='Exportation (volume)'] = 'Exportation'
    data['Exchange_Type'][data['Exchange']=='Exportation (valeur)'] = 'Exportation'
    data['Exchange_Type'][data['Exchange']=='Importation (volume)'] = 'Importation'
    data['Exchange_Type'][data['Exchange']=='Importation (valeur)'] = 'Importation'

    data['Exchange_Measure'] = None
    data['Exchange_Measure'][data['Exchange']=='Exportation (volume)'] = 'Volume'
    data['Exchange_Measure'][data['Exchange']=='Exportation (valeur)'] = 'Valeur'
    data['Exchange_Measure'][data['Exchange']=='Importation (volume)'] = 'Volume'
    data['Exchange_Measure'][data['Exchange']=='Importation (valeur)'] = 'Valeur'

    if save_csf:
        data.to_csv(save_name, index=False)

    return data

# transform loop
if __name__ == "__main__":
    for i in range(10):
        df = pd.read_csv(f"FDS_D_0015_200{i}.csv", sep=";",encoding="utf-8")
        data_transform(df, True, f"wine_data_200{i}.csv")
for i in range(10, 26):
        df = pd.read_csv(f"FDS_D_0015_20{i}.csv", sep=";",encoding="utf-8")
        data_transform(df, True, f"wine_data_20{i}.csv")