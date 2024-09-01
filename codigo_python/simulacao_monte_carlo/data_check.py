import pandas as pd

def data_check(main_df):
    municipalities_in_df = main_df["codigo_municipio"].copy().drop_duplicates().to_list()
    parishes_in_df = main_df["codigo_freguesia"].copy().drop_duplicates().to_list()

    # Get municipalities
    
    mun_df = pd.read_csv("base_de_dados\\outros_dados\\lista_municipios.csv", delimiter=",")
    mun_df = mun_df[["designacao", "dicofre"]]
    mun_df_continent = mun_df.loc[mun_df["dicofre"] < 3101]
    possible_municipalities = mun_df_continent["dicofre"].copy().drop_duplicates().to_list()

    # Check if any municipality is missing
    missing_municipalities = []
    extra_municipalities = []
    for index, code in enumerate(possible_municipalities):
        name = mun_df_continent.loc[mun_df_continent["dicofre"] == code, "designacao"].iloc[0]
        if (code not in municipalities_in_df):
            missing_municipalities.append(name)

    # Check if there are any extra municipalities
    for index, code in enumerate(municipalities_in_df):
        if (code not in possible_municipalities):
            extra_municipalities.append(str(code))


    # Get parishes
    par_df = pd.read_csv("base_de_dados\\outros_dados\\lista_freguesias.csv", delimiter=",")
    par_df = par_df[["freguesia", "dicofre"]]
    max_index = par_df['dicofre'].loc[lambda x: x=="310101"].index.to_list()[0]
    par_df_continent = par_df[:max_index]
    possible_parishes = par_df_continent["dicofre"].copy().drop_duplicates().to_list()

    # Check if any parish is missing
    missing_parishes = []
    extra_parishes = []
    for index, code in enumerate(possible_parishes):
        name = par_df_continent.loc[par_df_continent["dicofre"] == code, "freguesia"].iloc[0]
        if (code not in parishes_in_df):
            missing_parishes.append(name)

    #Check if there are any extra parishes
    for index, code in enumerate(parishes_in_df):
        if (code not in possible_parishes):
            extra_parishes.append(str(code))
    
    
    missing_par_codes = []
    for index, code in enumerate(possible_parishes):
        fcode = par_df_continent.loc[par_df_continent["dicofre"] == code, "dicofre"].iloc[0]
        if (code not in parishes_in_df):
            missing_par_codes.append(fcode)
    
    missing_mun_codes = []
    for index, code in enumerate(possible_municipalities):
        fcode = mun_df_continent.loc[mun_df_continent["dicofre"] == code, "dicofre"].iloc[0]
        if (code not in municipalities_in_df):
            missing_mun_codes.append(fcode)    
    
    missing_par_not_in_missing_mun = pd.DataFrame({'code': missing_par_codes})
    for index, code in enumerate(missing_mun_codes):
        code = str(code)
        if len(code) < 4:
            code = "0" + code
        
        for ifreg, freg_code in enumerate(missing_par_codes):  
            freg_code = str(freg_code)
            if code in (freg_code[0:4]):
                missing_par_not_in_missing_mun = missing_par_not_in_missing_mun.loc[missing_par_not_in_missing_mun['code'] != freg_code]
    
    missing_par_not_in_missing_mun = missing_par_not_in_missing_mun['code'].values.tolist()
    par_names = []     
    for par, code in enumerate(possible_parishes):
        name = par_df_continent.loc[par_df_continent["dicofre"] == code, "freguesia"].iloc[0]
        
        if code == '011304':
            pass
        
        if (code in missing_par_not_in_missing_mun):
            par_names.append(name)
            
    file = open("codigo_python\\simulacao_monte_carlo\\output\\dados_em_falta.txt", "w", encoding='utf-8')

    missing_municipalities.sort()
    missing_parishes.sort()
    extra_municipalities.sort()
    extra_parishes.sort()
    par_names.sort()
    
    delimiter = "; "
    file.write("Verificação dos dados:")
    file.write(f"\n\n\tDados têm {len(municipalities_in_df)}/{len(possible_municipalities)} municípios - faltam {len(possible_municipalities)-len(municipalities_in_df)} município(s) ({round((len(possible_municipalities)-len(municipalities_in_df))/len(possible_municipalities)*100, 3)}%)")
    file.write(f"\n\n\tDados têm {len(parishes_in_df)}/{len(possible_parishes)} freguesias - faltam {len(possible_parishes)-len(parishes_in_df)} freguesia(s) ({round((len(possible_parishes)-len(parishes_in_df))/len(possible_parishes)*100, 3)}%)")
    file.write(f"\n\n\tMunicípios em falta: {delimiter.join(missing_municipalities)}")
    file.write(f"\n\n\tMunicípios a mais (por possíveis erros nos dados): {delimiter.join(extra_municipalities)}")
    file.write(f"\n\n\tFreguesias em falta: {delimiter.join(missing_parishes)}")
    file.write(f"\n\n\tFreguesias a mais (por possíveis erros nos dados): {delimiter.join(extra_parishes)}")
    file.write(f"\n\n\tFreguesias em falta não incluídas nos municípios em falta: {delimiter.join(par_names)}")

    print("\n Data check: ")
    print(f"\n\tData has {len(municipalities_in_df)}/{len(possible_municipalities)} municipalities - missing {len(possible_municipalities)-len(municipalities_in_df)} municipality(ies) ({round((len(possible_municipalities)-len(municipalities_in_df))/len(possible_municipalities)*100, 3)}%)")
    print(f"\n\tData has {len(parishes_in_df)}/{len(possible_parishes)} parishes - missing {len(possible_parishes)-len(parishes_in_df)} parish(es) ({round((len(possible_parishes)-len(parishes_in_df))/len(possible_parishes)*100, 3)}%)")
    print(f"\n\tMissing municipalities: {missing_municipalities}")
    print(f"\n\tExtra municipalities: {extra_municipalities}")
    print(f"\n\tMissing parishes: {missing_parishes}")
    print(f"\n\tExtra parishes: {extra_parishes}")
    print(f"\n\tMissing parishes not in missing municipalities: {par_names}")