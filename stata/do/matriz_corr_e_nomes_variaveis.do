* =============================================================================
* Matriz de correlações e nomes das variáveis
* =============================================================================

import excel "codigo_python\simulacao_monte_carlo\output\export.xlsx", sheet("dados_todos_mun_pos_sim") firstrow clear

// Socioeconomic variables
label variable sim_mun "IPE Mun"
label variable sim_freg "IPE Freg"

label variable ippcc "IPCC"
label variable rend_mediano "Rendimento mediano"

label variable renda_med "Renda mensal"
label variable desemprego "Taxa de desemprego"
label variable gini "Coeficiente de Gini"

// Population and household variables
label variable resid_estr "Residente estrangeiro"
label variable esc_med_anos "Escolaridade média"
label variable dens_pop "Densidade Populacional"
label variable sobrelot "Sobrelotação"

label variable dim_med_agreg "Dimensão média agregado"
label variable agreg_1 "Agregado 1"
label variable agreg_2 "Agregado 2"
label variable agreg_3 "Agregado 3"
label variable agreg_4 "Agregado 4"
label variable agreg_5 "Agregado 5"
label variable agreg_6 "Agregado 6"
label variable agreg_7 "Agregado 7"
label variable agreg_8 "Agregado 8"
label variable agreg_9_mais "Agregado 9 ou mais"

// Physical variables
label variable temp_med "Temperatura média"
label variable temp_amp "Amplitude térmica"


// Dwelling caracteristics
label variable sem_nec_rep "Reparação desnecessária"
label variable lig_nec_rep "Reparação ligeira"
label variable med_nec_rep "Reparação média"
label variable prof_nec_rep "Reparação profunda"
label variable indice_nec_rep "Índice necessidade reparação"

label variable aloj_x_1919 "Alojamento < 1919"
label variable aloj_1919_1945 "Alojamento 1919-1945"
label variable aloj_1946_1960 "Alojamento 1946-1960"
label variable aloj_1961_1980 "Alojamento 1961-1980"
label variable aloj_1981_1990 "Alojamento 1981-1990"
label variable aloj_1991_2000 "Alojamento 1991-2000"
label variable aloj_2001_2005 "Alojamento 2001-2005"
label variable aloj_2006_2010 "Alojamento 2006-2010"
label variable aloj_2011_2015 "Alojamento 2011-2015"
label variable aloj_2016_2021 "Alojamento 2016-2021"
label variable idade_med_aloj "Idade média alojamento"

label variable propriet_s_enc "Proprietário sem encargos"
label variable propriet_c_enc "Proprietário com encargos"
label variable nao_propriet "Não proprietário"
label variable indice_enc_aloj "Proporção com encargos alojamento"


// Municipality government variables
label variable direita "Direita"
label variable esquerda "Esquerda"
label variable m_absoluta "Maioria absoluta"

drop codigo_municipio
drop distrito
drop municipio
drop nuts_2

order ippcc rend_mediano renda_med desemprego gini resid_estr esc_med_anos dens_pop sobrelot dim_med_agreg agreg_1 agreg_2 agreg_3 agreg_4 agreg_5 agreg_6 agreg_7 agreg_8 agreg_9_mais temp_med temp_amp sem_nec_rep lig_nec_rep med_nec_rep prof_nec_rep indice_nec_rep aloj_x_1919 aloj_1919_1945 aloj_1946_1960 aloj_1961_1980 aloj_1981_1990 aloj_1991_2000 aloj_2001_2005 aloj_2006_2010 aloj_2011_2015 aloj_2016_2021 idade_med_aloj propriet_s_enc propriet_c_enc nao_propriet indice_enc_aloj direita esquerda m_absoluta sim_mun sim_freg

preserve
    describe, replace clear
    list
    export excel using "${user_directory}\stata\output\outros\varnames.xlsx", replace first(var)
restore

correlate

return list
matrix list r(C)

putexcel set "${user_directory}\stata\output\outros\matriz_correlacoes", replace
putexcel A1=matrix(r(C)), names