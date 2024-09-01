* =============================================================================
* Regressões para as subamostras do IPCC
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

encode nuts_3, gen(nnuts_3)

local i=1

local l_or_h = ""
preserve

// Dependent variable
foreach d_var in "sim_mun" "sim_freg" {	
	foreach ipcc in "80" "85" "90" "95" "100" {	
		foreach low_or_high in "0" "1" {
			if `low_or_high' == 0 {
				local l_or_h = "low"
				keep if ippcc <= `ipcc'
			}
			
			if `low_or_high' == 1 {
				local l_or_h = "high"
				keep if ippcc > `ipcc'
			}
			
			regress `d_var' ippcc temp_med, vce(robust)
			eststo R_`l_or_h'_`ipcc'_`i'
			local ++i

			regress `d_var' rend_mediano temp_med, vce(robust)
			eststo R_`l_or_h'_`ipcc'_`i'
			local ++i
			
			regress `d_var' ippcc dim_med_agreg temp_med indice_enc_aloj, vce(robust)
			eststo R_`l_or_h'_`ipcc'_`i'
			local ++i
			
			regress `d_var' rend_mediano dim_med_agreg temp_med indice_enc_aloj, vce(robust)
			eststo R_`l_or_h'_`ipcc'_`i'
			local ++i
			
			regress `d_var' ippcc renda_med desemprego gini resid_estr esc_med_anos dens_pop sobrelot dim_med_agreg temp_med temp_amp indice_nec_rep idade_med_aloj indice_enc_aloj direita esquerda m_absoluta, vce(robust)
			eststo R_`l_or_h'_`ipcc'_`i'
			local ++i
			
			regress `d_var' rend_mediano renda_med desemprego gini resid_estr esc_med_anos dens_pop sobrelot dim_med_agreg temp_med temp_amp indice_nec_rep idade_med_aloj indice_enc_aloj direita esquerda m_absoluta, vce(robust)
			eststo R_`l_or_h'_`ipcc'_`i'
			local ++i
			
			local i=1
			restore, preserve
		}
	}
	
	estout using "${user_directory}\stata\output\regressoes\temp_`d_var'.csv", cells(b(star fmt(%9.3f)) & p(par)) starlevels( * 0.10 ** 0.05 *** 0.01) order(ippcc rend_mediano renda_med desemprego gini resid_estr esc_med_anos dens_pop sobrelot dim_med_agreg temp_med temp_amp indice_nec_rep idade_med_aloj indice_enc_aloj direita esquerda m_absoluta) stats(N F p r2 r2_a rmse, labels("Obs." "Estatística F" "Prob > F" "R-quadrado" "R-quadrado ajustado" "Raíz Erro-Quadrado Médio")) legend label collabels(none) varlabels(_cons Constante) replace
	unicode convertfile "${user_directory}\stata\output\regressoes\temp_`d_var'.csv" "${user_directory}\stata\output\regressoes\ipcc_`d_var'.csv", dstencoding(Windows-1252) replace
	erase "${user_directory}\stata\output\regressoes\temp_`d_var'.csv"
	eststo clear
	local i=1
}