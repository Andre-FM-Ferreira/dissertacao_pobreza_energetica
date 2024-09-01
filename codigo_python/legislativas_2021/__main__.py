from playwright.sync_api import sync_playwright, Playwright
import pandas as pd

def check_code(municipality_code):
    municipality_code = str(municipality_code)
    if len(municipality_code) == 3:
        municipality_code = "0" + municipality_code
        
    return municipality_code

def get_link(municipality_code):
    site_link = "https://www.eleicoes.mai.gov.pt/autarquicas2021/resultados/territorio-nacional?local=LOCAL-"
    
    municipality_code = check_code(municipality_code)
    site_link = site_link + municipality_code + "00"
    
    return site_link
    
def run(playwright: Playwright):
    # Get municipality codes
    mun_df = pd.read_csv("base_de_dados\\outros_dados\\lista_municipios.csv", delimiter=",")
    mun_df = mun_df[["designacao", "dicofre"]]
    municipality_codes = mun_df["dicofre"].copy().drop_duplicates().to_list()
    
    # If not direita or esquerda, then independente
    direita = ["PSD", "CDS", "CH", "JPP"]
    esquerda = ["PS", "PCP", "B.E"]
    
    # Columns that the dataframe will have - requires initial values
    columns = {"codigo_municipal": ["0"], "municipio": ["aaa"], "partido": ["a"], 
               "percentagem_votos": ["1"], "numero_votos": ["1"], 
               "presidentes": ["0"], "maiorias_absolutas": ["0"], "numero_mandatos": ["1"], 
               "orientacao": ["aa"]}
    
    main_df = pd.DataFrame()
    
    # Open browser
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    
    # Get data for municipality codes
    for municipality_code in municipality_codes:
        # Access link
        link = get_link(municipality_code)
        page.goto(link)
        
        # Click details and get all tables
        page.get_by_text("Detalhes").click()
        rows = page.locator('tbody')

        # For each table found
        for i in range(rows.count()):
            # Insert municipality code and name to dataframe
            temp_df = pd.DataFrame(columns)
            temp_df.iloc[0, 0] = municipality_code
            
            name = mun_df["designacao"].loc[mun_df["dicofre"] == municipality_code]
            temp_df.iloc[0, 1] = name.values[0]
            
            # Each table comes out all at once, so split it
            text = rows.nth(i).inner_text()
            text = text.split()
            
            # And group up data appropriately
            group_amount = 6
            splits = [text[i:i+group_amount] for i in range(0,len(text), group_amount)]
            
            # Save only the results of the winning political party
            for index, value in enumerate(splits[0]):                
                temp_df.iloc[0, index+2] = str(value)
            
            # Classify whether the winning political party is left, right or independent
            if any(political_party in temp_df["partido"][0] for political_party in direita):
                temp_df.loc[0, "orientacao"] = "direita"
            elif any(political_party in temp_df["partido"][0] for political_party in esquerda):
                temp_df.loc[0, "orientacao"] = "esquerda"
            else:
                temp_df.loc[0, "orientacao"] = "independente"
            
            # Add to main dataframe
            if len(main_df.index) == 0:
                main_df = temp_df
            else:
                main_df = pd.concat([main_df, temp_df], ignore_index=True, join="inner")

        # Drop latest row with non-relevant info (blank and null votes - comes as a separate table)
        main_df = main_df.drop(len(main_df)-1)
        
        # Print progress
        print(f"Municipalities done: {len(main_df)}/{len(municipality_codes)}")
    
    # Special cases - one list per case
    info = [[908,"Manteigas","MANTEIGAS 2030","34,14","758","1","0", "2", "independente"]]
    
    for i, special_case in enumerate(info):
        row_index = main_df.loc[main_df["codigo_municipal"] == special_case[0]].index[0]
        for j, new_info in enumerate(special_case):
            main_df.iloc[row_index, j] = new_info
    
    # Replace dots and commas according to computer usage
    main_df["numero_votos"] = main_df["numero_votos"].str.replace('.', '')
    main_df["percentagem_votos"] = main_df["percentagem_votos"].str.replace(',', '.')    
    
    # Convert text to float where needed
    main_df["numero_votos"] = pd.to_numeric(main_df["numero_votos"])
    main_df["percentagem_votos"] = pd.to_numeric(main_df["percentagem_votos"])
    main_df["presidentes"] = pd.to_numeric(main_df["presidentes"])
    main_df["maiorias_absolutas"] = pd.to_numeric(main_df["maiorias_absolutas"])
    main_df["numero_mandatos"] = pd.to_numeric(main_df["numero_mandatos"])
    
    # Create dummy variables
    main_df["dummy_direita"] = main_df["orientacao"].apply(lambda x: 1 if x == "direita" else 0)
    main_df["dummy_esquerda"] = main_df["orientacao"].apply(lambda x: 1 if x == "esquerda" else 0)

    # Export
    main_df.to_csv("codigo_python\\legislativas_2021\\output\\partidos_vencedores.csv", index=False, encoding='utf-8')
    main_df.to_excel("codigo_python\\legislativas_2021\\output\\partidos_vencedores.xlsx", index=False)
    
    # Close browser and stop
    browser.close()
    playwright.stop

with sync_playwright() as playwright:
    run(playwright)