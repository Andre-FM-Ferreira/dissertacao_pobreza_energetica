# Introdução
Este repositório contém os dados e procedimentos para replicar integralmente os resultados utilizados na elaboração da dissertação com o título `A DIMENSÃO DA POBREZA ENERGÉTICA NOS MUNICÍPIOS EM PORTUGAL E OS SEUS DETERMINANTES` para a Faculdade de Economia do Porto no ano letivo 2023/2024, da autoria de André Filipe Martins Ferreira e orientado pela Exma. Sra. Professora Maria Isabel Mota.

A dissertação tem como objetivos:
- analisar a incidência da pobreza energética em Portugal ao nível do município e
- identificar os principais fatores explicativos dos padrões observados.

O disponibilizado neste repositório permite:
1. Analisar a base de dados utilizada de acordo com os dados disponíveis no momento da elaboração da dissertação;
2. Replicar o tratamento dos dados;
3. Analisar e replicar a extração e categorização dos dados das Legislativas 2021 disponibilizados pelo Ministério da Administração Interna;
4. Analisar e replicar as simulações de Monte-Carlo;
5. Analisar e replicar as regressões lineares e a matriz de correlações.

# Guia do repositório
Este repositório está estruturado da seguinte forma:
```
base_de_dados
    |----- output
    |----- outros_dados
    |----- db.db
    |----- README.md
    |----- Script.sql
codigo_python
    |----- legislativas_2021
    |----- simulacao_monte_carlo
    |----- README.md
stata
    |----- do
    |----- output
    |----- README.md
.gitignore
README.md
requirements.txt
```

As pastas: `base_de_dados`, `codigo_python` e `stata` são as subdivisões por ferramentas utilizadas. Em cada uma das pastas está um `README.md` para informar sobre os requisitos e os procedimentos.

O ficheiro `requirements.txt` é necessário por causa do código executado em python e é onde estão identificadas as bibliotecas necessárias.

# Requisitos
- Base de dados - É necessário algum método para aceder à base de dados SQLite. Na elaboração desta dissertação foi utilizada a versão  `DBeaver Community 24.1.3`, disponível em https://dbeaver.io/download/.

- Código Python - É necessário instalar o Python previamente, disponível em https://www.python.org/downloads/. Foi utilizada a versão `3.12.4` na elaboração desta dissertação.

- Stata - A versão do Stata utilizada foi a versão 17.0.

- Microsoft Office Excel.

# Procedimentos
- [Base de dados](base_de_dados/README.md)
- [Código Python](codigo_python/README.md)
- [Stata](stata/README.md)