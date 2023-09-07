# Coletando e Transformando Dados Abertos com Pandas, DuckDB, dbt e Streamlit

---

Este repositório tem como objetivo demonstrar como é possível utilizar os dados abertos disponíveis no site https://dadosabertos.rfb.gov.br/CNPJ para construir um App de consulta de CNPJ.

Para rodar todos os scripts as seguintes dependências são necessárias:
1. Python 3.x com as dependências listadas no arquivo requirements.txt;
ˋˋˋbash
pip install -r requirements.txt
ˋˋˋ
2. dbt;
3. pastas com o nome 'raw_files', 'parquet_files' e 'database' na raiz do diretório 'dados_abertos';

Nos computadores Windows basta rodar o arquivo 'download_data.bat', que irá criar os diretórios, efetuar o download e transformação dos dados e criação da base de dados.

## Documentação do Script `download_data.bat`

Este script em lote (batch) tem como objetivo configurar a estrutura de diretórios necessária e executar o processo de Extração, Transformação e Carregamento (ETL) de dados a partir de arquivos brutos para um banco de dados DuckDB. O script é projetado para uso em ambientes Windows.

### Estrutura de Diretórios

O script verifica a existência de três diretórios principais e, se eles não existirem, os cria. Esses diretórios são:

1. `raw_files`: Este diretório é usado para armazenar arquivos brutos que serão processados durante o ETL.

2. `parquet_files`: Este diretório é usado para armazenar os arquivos Parquet gerados durante o processo de ETL.

3. `database`: Este diretório é usado para armazenar o banco de dados DuckDB resultante do ETL.

### Execução do ETL

Após criar os diretórios necessários, o script muda para o diretório `python` e executa o script Python `dados_abertos_etl.py` várias vezes, cada vez especificando uma tabela específica para extração e transformação. As tabelas processadas incluem:

- Qualificações
- Cnaes
- Naturezas
- Municípios
- Países
- Motivos
- Empresas
- Simples
- Sócios
- Estabelecimentos

Cada execução do `dados_abertos_etl.py` extrai os dados brutos correspondentes, executa transformações específicas para a tabela e, em seguida, carrega os dados transformados em arquivos Parquet no diretório `parquet_files`.

Após a conclusão do ETL, o script muda para o diretório `dbt_dados_abertos` e executa o comando `dbt run` para processar e modelar os dados usando o DBT (Data Build Tool). O parâmetro `--vars "is_test_run: false"` é passado para indicar que esta não é uma execução de teste.

## Documentação do Script Python para Download e Conversão de Dados Abertos

Este é um script Python que permite baixar arquivos ZIP de dados abertos relacionados a CNPJ do site "dadosabertos.rfb.gov.br" e convertê-los em arquivos Parquet usando chunks. A documentação abaixo descreve as funcionalidades e uso deste script.

### Requisitos

Para executar este script, você deve ter os seguintes requisitos:

1. Python 3.x instalado no seu sistema.
2. As bibliotecas Python `requests`, `numpy`, `pyarrow`, `fastparquet`, `pandas`, `tqdm`, e `argparse` devem estar instaladas. Você pode instalá-las usando o `pip` da seguinte forma:

```bash
pip install requests numpy pandas tqdm argparse pyarrow fastparquet
```

### Uso do Script

O script oferece duas principais funções: `download_dados_abertos` e `csv_to_parquet`.

#### Função `download_dados_abertos`

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

##### Exemplo de Uso

```python
download_dados_abertos('Estabelecimentos', number=1, save_path='/caminho/personalizado/')
# Isso baixará o arquivo 'Estabelecimentos1.zip' do site e o salvará em '/caminho/personalizado/'
```

#### Função `csv_to_parquet`

A função `csv_to_parquet` converte um arquivo CSV (possivelmente dentro de um ZIP) em vários arquivos Parquet usando chunks. Ela lê o arquivo CSV baixado do diretório especificado por `save_path` e salva os dados em múltiplos arquivos Parquet com chunks. Aqui estão os parâmetros da função:

- `filename` (str): O nome do arquivo CSV a ser convertido, localizado em `save_path`.
- `selector` (str): Nome do seletor utilizado para baixar os dados e selecionar o nome das colunas e os tipos de dados para leitura.
- `number` (int, opcional): Um número opcional a ser adicionado ao nome do arquivo. É necessário nos casos dos seguintes arquivos: Empresas, Estabelecimentos, Socios.
- `save_path` (str, opcional): O diretório onde o arquivo CSV está localizado. Padrão: '../raw_files/'.

##### Exemplo de Uso

```python
csv_to_parquet('Estabelecimentos_01.zip', selector='Estabelecimentos', number=2, save_path='/caminho/do/arquivo/')
# Converte o arquivo 'Estabelecimentos_01.zip' em arquivos Parquet.
# Os arquivos resultantes são divididos em chunks de 100000 linhas e são salvos no diretório '/caminho/do/arquivo/'.
```

### Execução do Script

Para executar o script, utilize o seguinte comando no terminal:

```bash
python dados_abertos_etl.py -s "Estabelecimentos" -p "Caminho/Personalizado/"
```

- `-s` ou `--selector`: Especifique o nome do arquivo a ser baixado e convertido.
- `-p` ou `--path` (opcional): Especifique o caminho personalizado onde os arquivos serão salvos. Se não fornecido, o padrão é '../raw_files/'.

Certifique-se de que o script esteja na mesma pasta em que você deseja que os arquivos ZIP sejam salvos e onde deseja que os arquivos Parquet sejam gerados. Certifique-se também de que o diretório de saída exista.

### Observações

- Os arquivos CSV baixados são lidos com base nas colunas e tipos de dados definidos nos dicionários `column_name_dict` e `dtypes_dict` de acordo com o seletor escolhido.
- Para os arquivos Empresas, Estabelecimentos e Socios, o script faz o download de até 10 arquivos diferentes, adicionando números ao nome do arquivo. Certifique-se de que os arquivos correspondentes estejam disponíveis no site "dadosabertos.rfb.gov.br".

Este script simplifica o processo de download e conversão de dados abertos relacionados a CNPJ para o formato Parquet, facilitando análises subsequentes dos dados.

## Documentação do processo em dbt para criação do banco de dados em DuckDB

### Requisitos

Para executar este processo você precisa:
1. dbt-core
2. dbt-duckdb

### Uso dos scripts

ˋˋˋbash
dbt run --vars "is_test_run: false"
ˋˋˋ

Obs.: Utilizando somente o código ˋdbt runˋ irá criar a base com a restrição de 1000 registros em algumas bases.

### Descrição

O dbt é uma ferramenta de transformação de dados e modelagem que permite que você trabalhe com dados em um ambiente de análise de dados. O arquivo 'schema.yml' define como os dados serão extraídos dos arquivos parquet, transformados e carregados no banco de dados em DuckDB salvo no diretório database. Aqui está um resumo do que esse arquivo dbt faz:

1. **Definição das Fontes de Dados:**
   - O arquivo começa definindo as fontes de dados em "sources". As fontes estão localizadas em arquivos Parquet no diretório "../parquet_files/".
   - As tabelas de dados a serem carregadas incluem: Paises, Estabelecimentos, Empresas, Simples, Socios, Municipios, Naturezas, Qualificacoes, Cnaes e Motivos.

2. **Definição dos Modelos:**
   - O arquivo define vários modelos no bloco "models". Cada modelo corresponde a uma tabela que será construída ou transformada no seu ambiente de análise.
   
   **Exemplos de Modelos:**
   
   - `ods_paises`: Este modelo representa uma tabela de mapeamento com os nomes dos países e seus códigos. Ele possui colunas como "codigo" e "descricao" e realiza testes de unicidade e não nulidade nessas colunas.
   
   - `ods_estabelecimentos`: Este modelo representa uma tabela que contém informações sobre estabelecimentos, incluindo detalhes sobre CNPJ, situação cadastral, endereço, etc.
   
   - `ods_empresas`: Este modelo contém informações sobre empresas, incluindo dados como razão social, natureza jurídica e porte da empresa.

   - `ods_socios`: Este modelo contém informações sobre os sócios das empresas, incluindo detalhes sobre nome, CPF ou CNPJ, qualificação, etc.

   - `ods_municipios`: Este modelo representa uma tabela de mapeamento com os nomes dos municípios e seus códigos.

   - `ods_qualificacoes`, `ods_cnaes`, `ods_motivos`: Esses modelos são tabelas de mapeamento semelhantes para qualificações, CNAEs e motivos, respectivamente.

   - `ft_cnaes_secundarias_as_list`: Uma visão que contém códigos CNAE secundários e suas descrições como uma lista por CNPJ.

   - `ft_socios`: Uma visão que contém informações dos sócios e suas qualificações.

   - `ft_comprovante_de_inscricao_e_situacao_cadastral`: Tabela que contém informações do Comprovante de Inscrição e de Situação Cadastral.

3. **Descrição e Testes:**
   - Cada modelo tem uma descrição que descreve o que a tabela contém.
   - As colunas em cada modelo têm descrições que explicam o que cada coluna representa.
   - Alguns modelos também especificam testes para garantir a qualidade dos dados, como verificar a unicidade e a não nulidade das colunas.


## Documentação do Aplicativo de Pesquisa de CNPJ com Streamlit

Este documento descreve o código Python que cria um aplicativo web para pesquisar informações de empresas com base no número de CNPJ. O aplicativo utiliza a biblioteca Streamlit para criar uma interface de usuário interativa e consulta um banco de dados DuckDB local para recuperar informações sobre as empresas.

### Visão Geral

O aplicativo foi desenvolvido para permitir que os usuários obtenham informações detalhadas sobre empresas brasileiras com base em seus números de CNPJ (Cadastro Nacional da Pessoa Jurídica). Ele oferece uma interface amigável onde os usuários podem inserir um CNPJ e, ao clicar no botão "Pesquisar", o aplicativo exibirá informações relevantes sobre a empresa correspondente.

### Requisitos

- Python 3.x
- Bibliotecas Python: Streamlit, DuckDB, streamlit-lottie, requests

### Funcionalidades

#### Carregamento da Animação Lottie

O aplicativo começa carregando uma animação Lottie de uma URL. Isso é feito usando a função `load_lottieurl`, que faz uma solicitação HTTP para a URL especificada e retorna o conteúdo JSON da animação.

```python
# Carregue o arquivo JSON da animação Lottie
lottie_search = load_lottieurl('https://lottie.host/f6530fed-b976-477c-abe0-c10a125d114c/x6QlRKooX2.json')
```

#### Conexão ao Banco de Dados DuckDB

O aplicativo se conecta a um banco de dados DuckDB localizado em um arquivo chamado `dados_abertos.duckdb`. Isso permite que o aplicativo consulte dados sobre empresas.

```python
# Conectar ao banco de dados DuckDB
conn = duckdb.connect(database='../database/dados_abertos.duckdb')
```

#### Funções de Pesquisa

O aplicativo define três funções para realizar consultas no banco de dados DuckDB:

- `pesquisar_cnpj`: Pesquisa informações de uma empresa com base no CNPJ fornecido.
- `pesquisar_cnaes`: Pesquisa as atividades econômicas secundárias de uma empresa com base no CNPJ.
- `pesquisar_socios`: Pesquisa os sócios de uma empresa com base no CNPJ.

#### Interface do Aplicativo

O aplicativo utiliza o Streamlit para criar uma interface de usuário interativa. Ele inclui um título e um campo de entrada de texto onde o usuário pode inserir um CNPJ.

```python
# Interface do Aplicativo
st.title("Procurar CNPJ no DuckDB")

# Input do usuário para inserir o CNPJ
cnpj_input = st.text_input("Digite o CNPJ que deseja pesquisar:")
```

#### Pesquisa do CNPJ

Quando o usuário clica no botão "Pesquisar", o código verifica se um CNPJ válido foi inserido. Se um CNPJ válido foi inserido, o aplicativo executa consultas no banco de dados DuckDB para obter informações sobre a empresa com base no CNPJ. As informações recuperadas são exibidas no aplicativo, incluindo detalhes sobre a empresa, endereço, natureza jurídica, situação cadastral, situação especial e atividades econômicas.

```python
# Pesquisa do CNPJ
if st.button("Pesquisar"):
    if cnpj_input:
        resultado = pesquisar_cnpj(cnpj_input)
        if not resultado.empty:
            # Exibir informações da empresa
            # ...
        else:
            st.warning("CNPJ não encontrado.")
    else:
        st.warning("Por favor, insira um CNPJ válido.")
```

#### Fechamento da Conexão

Após concluir as consultas, o aplicativo fecha a conexão com o banco de dados DuckDB.

```python
# Fechar a conexão com o banco de dados DuckDB
conn.close()
```

### Uso

Para usar o aplicativo, siga estas etapas:

1. Certifique-se de que você possui todos os requisitos listados acima instalados em seu ambiente Python.

2. Execute o script Python fornecido. Isso iniciará o aplicativo Streamlit localmente.

3. No navegador, acesse a URL fornecida pelo Streamlit para interagir com o aplicativo.

4. Insira um número de CNPJ válido no campo de pesquisa e clique no botão "Pesquisar". As informações da empresa serão exibidas na interface.

### Considerações Finais

Este aplicativo oferece uma maneira conveniente de pesquisar informações detalhadas sobre empresas brasileiras com base em seus CNPJs. Ele pode ser usado para consulta rápida e acesso a dados empresariais relevantes.

Para obter informações atualizadas sobre empresas, certifique-se de que o banco de dados DuckDB esteja atualizado com os dados mais recentes.
