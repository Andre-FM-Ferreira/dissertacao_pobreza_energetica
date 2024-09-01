import numpy as np
from data_check import data_check
import pandas as pd
from scipy.stats import ttest_ind
import xlwings as xw

simulate_mun = True
simulate_par = True
test_if_simulations_differ = True
export_data = True

rng = np.random.default_rng(12345)
main_df = pd.read_csv("base_de_dados\\output\\main_table.csv", delimiter=",").dropna()

def adjust_columns(excel_file):    
    with xw.App(visible=False) as app:
        wb = xw.Book(excel_file)
        for sheet in range(len(wb.sheets)):
            ws = wb.sheets[sheet]
            ws.autofit()
        wb.save()
        wb.close()

if simulate_mun or simulate_par:
    municipalities_df = main_df["codigo_municipio"].copy().drop_duplicates()
    
    code_to_name_dict = {}
    for cod_mun in municipalities_df:
        df = main_df[main_df["codigo_municipio"] == cod_mun]
        name = df["municipio"].iloc[0]
        
        code_to_name_dict[cod_mun] = name
    
    # Simulation at municipality level
    if simulate_mun:
        df_dict_mun = {}
        count = 0

        print("\nStarting municipality-level simulation...")
        for cod_mun in municipalities_df:
            count += 1
            
            single_mun_df = main_df[main_df["codigo_municipio"] == cod_mun]
            mun_cons_mean = single_mun_df["kwh_cpe_med_mes"].mean()
            mun_cons_std = single_mun_df["kwh_cpe_med_mes"].std()
            
            simulation = rng.normal(mun_cons_mean, mun_cons_std, size=10_000_000)
            
            median = np.median(simulation)
            
            a1 = simulation[simulation <= median*0.5].shape[0] / simulation.shape[0] * 100
            
            mun_name = code_to_name_dict[cod_mun]
            df_dict_mun[cod_mun] = [mun_name, mun_cons_mean, mun_cons_std, median, a1]
            print(f"Finished {count}/{len(municipalities_df)} municipalities - municipality level")
            
        sim_df_mun = pd.DataFrame().from_dict(df_dict_mun).transpose().reset_index().rename(columns={
            "index": "codigo_municipio",
            0: "municipio",
            1: "cons_medias",
            2: "cons_desvio_padrao", 
            3: "mediana", 
            4: "sim_mun",
            })
        
        print("\n Saving simulation at municipality level to csv in output folder")
        sim_df_mun.to_csv("codigo_python\\simulacao_monte_carlo\\output\\sim_mun_10_mill.csv", index=False)

    # Simulation at parish level
    if simulate_par:
        df_dict_parish = {}
        count = 0

        print("\nStarting parish-level simulation...")
        for cod_mun in municipalities_df:
            count += 1
            
            single_mun_df = main_df[main_df["codigo_municipio"] == cod_mun]
            parishes_df = single_mun_df["codigo_freguesia"].copy().drop_duplicates()
            
            mun_cons_std = single_mun_df["kwh_cpe_med_mes"].std()
            
            means = []
            for cod_par in parishes_df:
                single_par_df = single_mun_df[single_mun_df["codigo_freguesia"] == cod_par]
                par_cons_mean = single_par_df["kwh_cpe_med_mes"].iloc[0]
                means.append(par_cons_mean)
            
            sim = rng.normal(means, mun_cons_std, size=(1_000_000, len(means))).flatten()
            
            median = np.median(sim)
            sim = np.array(sim)
            a1 = sim[sim <= median*0.5].shape[0] / sim.shape[0] * 100
            
            mun_name = code_to_name_dict[cod_mun]
            df_dict_parish[cod_mun] = [mun_name, means, mun_cons_std, median, a1]
            print(f"Finished {count}/{len(municipalities_df)} municipalities - parish level")
            
        sim_df_par = pd.DataFrame().from_dict(df_dict_parish).transpose().reset_index().rename(columns={
            "index": "codigo_municipio",
            0: "municipio",
            1: "cons_medias",
            2: "cons_desvio_padrao", 
            3: "mediana", 
            4: "sim_freg",
            })

        print("\n Saving simulation at parish level to csv in output folder")
        sim_df_par.to_csv("codigo_python\\simulacao_monte_carlo\\output\\sim_freg_1_mill.csv", index=False)

# Test whether there is a significant difference between simulations and data
# Through a Welch's t-test (doesn't assume equal variance)
if test_if_simulations_differ:
    print("\nTesting if simulations are statistically different...")
    df_mun = pd.read_csv("codigo_python\\simulacao_monte_carlo\\output\\sim_mun_10_mill.csv").dropna()
    df_par = pd.read_csv("codigo_python\\simulacao_monte_carlo\\output\\sim_freg_1_mill.csv").dropna()
    
    test_sim_mun_vs_freg = ttest_ind(df_mun["sim_mun"], df_par["sim_freg"], equal_var=False)    
    test_median_mun_vs_freg = ttest_ind(df_mun["mediana"], df_par["mediana"], equal_var=False)
    
    file = open("codigo_python\\simulacao_monte_carlo\\output\\significancia_simulacao.txt", "w", encoding='utf-8')
    file.write("Teste da estatística t de Welch (não assume à priori que as variâncias são iguais):")
    file.write(f"\n\n\tHipótese nula - a percentagem de indivíduos com consumo energético abaixo de 50% da mediana é idêntica nas simulações ao nível do município e ao nível da freguesia:\n\t\t{test_sim_mun_vs_freg}")    
    file.write(f"\n\n\tHipótese nula - a mediana nas simulações ao nível do município e ao nível da freguesia é idêntica:\n\t\t{test_median_mun_vs_freg}")

# Export main table
if export_data:
    print("\nExporting data to excel in output folder...")
    
    no_export_columns = ["distrito", "municipio", "freguesia", "codigo_municipio", "codigo_freguesia"]
    export_columns = []

    for col in main_df.columns:
        if col not in no_export_columns:
            export_columns.append(col)

    df_mun = pd.read_csv("codigo_python\\simulacao_monte_carlo\\output\\sim_mun_10_mill.csv")
    df_par = pd.read_csv("codigo_python\\simulacao_monte_carlo\\output\\sim_freg_1_mill.csv")
    
    with pd.ExcelWriter("codigo_python\\simulacao_monte_carlo\\output\\export.xlsx") as writer:        
        
        # Make sure that NAs are removed from dataframes
        dropped_mun = []
        
        temp_mun = df_mun[["municipio", "codigo_municipio", "cons_medias", "cons_desvio_padrao", "mediana", "sim_mun"]] #, "mun_porcento_acima_2x_mediana"]]
        temp_mun_na = temp_mun[temp_mun["cons_desvio_padrao"].isna()]
        
        for cod_mun in temp_mun_na["codigo_municipio"]:
            if cod_mun not in dropped_mun:
                dropped_mun.append(cod_mun)
        
        temp_par = df_par[["municipio", "codigo_municipio", "cons_medias", "cons_desvio_padrao", "mediana", "sim_freg"]] #, "freg_porcento_acima_2x_mediana"]]
        temp_par_na = temp_par[temp_par["cons_desvio_padrao"].isna()]
        
        for cod_mun in temp_par_na["codigo_municipio"]:
            if cod_mun not in dropped_mun:
                dropped_mun.append(cod_mun)
        
        for cod_mun in dropped_mun:
            main_df = main_df.drop(main_df[main_df.codigo_municipio == cod_mun].index)
            temp_mun = temp_mun.drop(temp_mun[temp_mun.codigo_municipio == cod_mun].index)
            temp_par = temp_par.drop(temp_par[temp_par.codigo_municipio == cod_mun].index)
        
        # Add describe sheet to excel
        describe_df = main_df.copy().drop(columns=["freguesia", "codigo_freguesia", "kwh_cpe_med_mes", "kwh_med_mes", "pontos_med_mes"])
        
        describe_df2 = pd.DataFrame()
        cols_list = ["municipio", "codigo_municipio", "freguesia", "codigo_freguesia", "kwh_med_mes", "pontos_med_mes", "kwh_cpe_med_mes"]
        
        for col in cols_list:
            describe_df2[col] = main_df[col]
        
        describe_df = pd.merge(describe_df, temp_mun[["codigo_municipio", 
                                                     "sim_mun",
                                                     ]], on="codigo_municipio", how='left')
       
        describe_df = pd.merge(describe_df, temp_par[["codigo_municipio", 
                                                     "sim_freg",
                                                     ]], on="codigo_municipio", how='left')
        
        
        # Remove duplicate municipalities
        describe_df = describe_df.drop_duplicates()
        describe_df2 = describe_df2.drop_duplicates()
        full_data_mun = describe_df
        
        # Export data describe and full data
        describe_df = describe_df.describe()
        describe_df2 = describe_df2.describe()
        
        # Overwrite describe data that is not interpretable
        indexes = ["mean", "std", "25%", "50%", "75%"]
        for i in indexes:
            describe_df["codigo_municipio"] = describe_df["codigo_municipio"].astype(object)            
            describe_df["nuts_2"] = describe_df["nuts_2"].astype(object)

            describe_df.at[i, "codigo_municipio"] = str("irrelevante")            
            describe_df.at[i, "nuts_2"] = str("irrelevante")
        
        describe_df.to_excel(writer, sheet_name="describe")
        describe_df2.to_excel(writer, sheet_name="describe_var_dep")
        
        full_data_mun.to_excel(writer, sheet_name="dados_todos_mun_pos_sim", index=False)
        
        # Export simulation-only data
        temp_mun.to_excel(writer, sheet_name="sim_municipio", index=False)
        temp_par.to_excel(writer, sheet_name="sim_freguesia", index=False)

        # Add separate sheets for all relevant columns in data
        for col in export_columns:
            if col == "kwh_cpe_med_mes":
                temp_df = main_df[["municipio", "freguesia", "codigo_municipio", "codigo_freguesia", col]].copy()
                col = "energia_cpe_mes"
            else:
                temp_df = main_df[["municipio", "codigo_municipio", col]].copy().drop_duplicates()
                
            for cod_mun in dropped_mun:
                temp_df = temp_df.drop(temp_df[temp_df.codigo_municipio == cod_mun].index)  
            
            temp_df.to_excel(writer, sheet_name=col, index=False)
        
    adjust_columns("codigo_python\\simulacao_monte_carlo\\output\\export.xlsx")
    print("\nChecking data...")
        
    data_check(main_df)  


print("\nFinished.")

