# Requisitos
É necessário algum método para aceder à base de dados SQLite. Na elaboração desta dissertação foi utilizada a versão  `DBeaver Community 24.1.3`, disponível em https://dbeaver.io/download/.

# Procedimento
Após estabelecido o acesso à base de dados, é necessário correr o Script.sql para que seja feita a filtragem e o tratamento necessário dos dados de modo a que se obtenha a tabela final utilizada. Esta tabela deve ser exportada para a pasta `output` com o tipo `.csv` e com o nome `main_table`.

Na pasta `output` encontra-se já a tabela exportada para .csv. É recomendado não deixar a pasta `output` vazia pois outras partes do repositório necessitam dos resultados para funcionarem como esperado.

As definições utilizadas para exportar para csv foram:
```
Files settings:
	Write to the single file: No
	Directory: D:\dissertacao\base_de_dados\output
	File name pattern: main_table
	On object data file name conflict: Ask
	On blob value file name conflict: Ask
	Encoding: UTF-8
	Timestamp pattern: yyyyMMddHHmm
	Insert BOM: No
	Compress: No
	Binaries: INLINE
	Encoding: BINARY
CSV settings:
	File extension: csv
	Delimiter: ,
	Row delimiter: default
	Header: top
	Header format: label
	Header case: as is
	Characters escape: quotes
	Quote character: "
	Quote always: disabled
	Quote never: false
	Format numbers: false
```