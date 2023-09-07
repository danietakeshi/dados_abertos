# Coletando e Transformando Dados Abertos com Pandas, DuckDB, dbt e Streamlit

---

Este repositório tem como objetivo demonstrar como é possível utilizar os dados abertos disponíveis no site https://dadosabertos.rfb.gov.br/CNPJ para construir um App de consulta de CNPJ.

# Documentação do Script Python para Download e Conversão de Dados Abertos

Este é um script Python que permite baixar arquivos ZIP de dados abertos relacionados a CNPJ do site "dadosabertos.rfb.gov.br" e convertê-los em arquivos Parquet usando chunks. A documentação abaixo descreve as funcionalidades e uso deste script.

## Requisitos

Para executar este script, você deve ter os seguintes requisitos:

1. Python 3.x instalado no seu sistema.
2. As bibliotecas Python `requests`, `numpy`, `pandas`, `tqdm`, e `argparse` devem estar instaladas. Você pode instalá-las usando o `pip` da seguinte forma:

```bash
pip install requests numpy pandas tqdm argparse
```

## Uso do Script

O script oferece duas principais funções: `download_dados_abertos` e `csv_to_parquet`.

### Função `download_dados_abertos`

A função `download_dados_abertos` é usada para baixar arquivos ZIP de dados abertos do site "dadosabertos.rfb.gov.br" e salvá-los localmente. Ela também exibe uma barra de progresso durante o download. Aqui estão os parâmetros da função:

- `filename` (str): O nome base do arquivo a ser baixado, podendo ser uma das seguintes opções:
    - Qualificacoes
    - Cnaes
    - Naturezas
    - Municipios
    - Paises
    - Motivos
    - Empresas
    - Simples
    - Socios
    - Estabelecimentos
- `number` (int, opcional): Um número opcional a ser adicionado ao nome do arquivo. É necessário nos casos dos seguintes arquivos: Empresas, Estabelecimentos, Socios.
- `save_path` (str, opcional): O caminho onde o arquivo ZIP será salvo. O padrão é '../raw_files/'.

#### Exemplo de Uso

```python
download_dados_abertos('Estabelecimentos', number=1, save_path='/caminho/personalizado/')
# Isso baixará o arquivo 'Estabelecimentos1.zip' do site e o salvará em '/caminho/personalizado/'
```

### Função `csv_to_parquet`

A função `csv_to_parquet` converte um arquivo CSV (possivelmente dentro de um ZIP) em vários arquivos Parquet usando chunks. Ela lê o arquivo CSV baixado do diretório especificado por `save_path` e salva os dados em múltiplos arquivos Parquet com chunks. Aqui estão os parâmetros da função:

- `filename` (str): O nome do arquivo CSV a ser convertido, localizado em `save_path`.
- `selector` (str): Nome do seletor utilizado para baixar os dados e selecionar o nome das colunas e os tipos de dados para leitura.
- `number` (int, opcional): Um número opcional a ser adicionado ao nome do arquivo. É necessário nos casos dos seguintes arquivos: Empresas, Estabelecimentos, Socios.
- `save_path` (str, opcional): O diretório onde o arquivo CSV está localizado. Padrão: '../raw_files/'.

#### Exemplo de Uso

```python
csv_to_parquet('Estabelecimentos_01.zip', selector='Estabelecimentos', number=2, save_path='/caminho/do/arquivo/')
# Converte o arquivo 'Estabelecimentos_01.zip' em arquivos Parquet.
# Os arquivos resultantes são divididos em chunks de 100000 linhas e são salvos no diretório '/caminho/do/arquivo/'.
```

## Execução do Script

Para executar o script, utilize o seguinte comando no terminal:

```bash
python dados_abertos_etl.py -s "Estabelecimentos" -p "Caminho/Personalizado/"
```

- `-s` ou `--selector`: Especifique o nome do arquivo a ser baixado e convertido.
- `-p` ou `--path` (opcional): Especifique o caminho personalizado onde os arquivos serão salvos. Se não fornecido, o padrão é '../raw_files/'.

Certifique-se de que o script esteja na mesma pasta em que você deseja que os arquivos ZIP sejam salvos e onde deseja que os arquivos Parquet sejam gerados. Certifique-se também de que o diretório de saída exista.

## Observações

- Os arquivos CSV baixados são lidos com base nas colunas e tipos de dados definidos nos dicionários `column_name_dict` e `dtypes_dict` de acordo com o seletor escolhido.
- Para os arquivos Empresas, Estabelecimentos e Socios, o script faz o download de até 10 arquivos diferentes, adicionando números ao nome do arquivo. Certifique-se de que os arquivos correspondentes estejam disponíveis no site "dadosabertos.rfb.gov.br".

Este script simplifica o processo de download e conversão de dados abertos relacionados a CNPJ para o formato Parquet, facilitando análises subsequentes dos dados.

