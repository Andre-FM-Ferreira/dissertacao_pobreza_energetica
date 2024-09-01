* =============================================================================
* Configurações: Inserir abaixo o caminho para a pasta global do repositório
* Exemplo: "D:\repositorio"
* =============================================================================

global user_directory "C:\path\to\your\directory"

* =============================================================================
* Fim das configurações
* =============================================================================

ssc install estout

cd "$user_directory"

log using "stata\output\log\log.txt", replace text

do "stata\do\matriz_corr_e_nomes_variaveis.do"
do "stata\do\regressoes_base.do"
do "stata\do\regressoes_desagregados.do"
do "stata\do\regressoes_ipcc_subamostras.do"
do "stata\do\regressoes_nuts_subamostras.do"

log close