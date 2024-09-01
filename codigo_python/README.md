# Introdução
Foram utilizados dois módulos separados. 

O primeiro módulo é o `legislativas_2021` que acede ao website do Ministério da Administração Interna para as legislativas de 2021, extrai os resultados e classifica-os de acordo com o partido vencedor entre direita, esquerda e independente (explícito nas linhas 73 a 79).

O segundo módulo é o `simulacao_monte_carlo` que calcula as simulações de Monte-Carlo utilizadas na dissertação como Índices de Pobreza Energética.

# Requisitos
É necessário instalar o Python previamente, disponível em https://www.python.org/downloads/. Foi utilizada a versão `3.12.4` na elaboração desta dissertação.
É necessário ter também o Microsoft Office Excel instalado.

# Procedimento - primeira vez
Abrir a linha de comandos na pasta global deste repositório e executar os seguintes comandos:

```bash
# Create environment
python -m venv .venv
# Activate environment
.\.venv\Scripts\activate
# Install requirements
pip install -r requirements.txt
# Install playwright
playwright install
```

# Procedimento geral
Após a instalação dos requisitos, para correr qualquer código python é necessário abrir a linha de comandos na pasta global deste repositório e executar o comando:

```bash
# Activate environment
.\.venv\Scripts\activate
```

# Correr o código
## Módulo - legislativas_2021
Para executar o módulo `legislativas_2021`, após ativado o ambiente virtual (procedimento geral), deverá correr-se na linha de comandos:
```bash
python codigo_python\legislativas_2021\__main__.py
```

## Módulo - simulacao_monte_carlo
No começo do ficheiro `__main__.py` (linhas 7 a 10) estão variáveis para determinar o que deve ser executado:

```bash
simulate_mun = True
simulate_par = True
test_if_simulations_differ = True
export_data = True
```

Caso não seja pretendido correr alguma das partes do código, na respetiva parte deverá substituir-se `True` por `False`.

Para executar o módulo `simulacao_monte_carlo`, após ativado o ambiente virtual (procedimento geral), deverá correr-se na linha de comandos:
```bash
python codigo_python\simulacao_monte_carlo\__main__.py
```

# Resultados
Em cada módulo tem a pasta `output` onde são gravados os resultados da execução dos módulos. Uma nova execução dos módulos irá substituir estes ficheiros.

É recomendado não deixar as pastas `output` vazias pois outras partes do repositório necessitam dos resultados para funcionarem como esperado.
