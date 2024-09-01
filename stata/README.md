# Requisitos
A versão do Stata utilizada foi a versão 17.0.

# Procedimento
Na pasta `do`, no ficheiro `main.do`, é necessário inserir o caminho para este repositório. Não deve ser inserido o caminho para a pasta `stata` deste repositório, mas sim para a pasta geral.

Para inserir o caminho, deverá substituir-se:
```bash
global user_directory "C:\path\to\your\directory"
```

Para, por exemplo:
```bash
global user_directory "D:\dissertacao"
```

Posteriormente, deve ser corrido o ficheiro `main.do` no Stata. Este ficheiro automaticamente altera o ambiente em que o Stata irá executar o código para o adequado. Ao longo do código, irão ser executados os restantes do-files e os resultados irão para a pasta `output`.

Na pasta `output` estão 3 pastas:
- `log` onde irá ser guardado o ficheiro `log.txt` com todo o código executado;
- `regressoes` onde irão ser guardados os resultados das regressões lineares;
- `outros` onde irá ser guardada a matriz de correlações (`matriz_correlacoes.xlsx`) e um ficheiro com as variáveis e as respetivas `labels` usadas no stata (`varnames.xlsx`).