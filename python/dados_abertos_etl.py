import requests
import numpy as np
import pandas as pd
import tqdm
import argparse

argParser = argparse.ArgumentParser()

argParser.add_argument("-s", "--selector", type=str, help="Identificador dos arquivos para Download")
argParser.add_argument("-p", "--path", type=str, default="../raw_files/", help="Diretório para salvar or arquivos ZIP")

args = argParser.parse_args()
print("args=%s" % args)

headers = {
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

column_name_dict = {
        'Qualificacoes' : ['codigo', 'descricao'],
        'Cnaes' : ['codigo', 'descricao'],
        'Naturezas' : ['codigo', 'descricao'],
        'Municipios' : ['codigo', 'descricao'],
        'Paises' : ['codigo', 'descricao'],
        'Motivos' : ['codigo', 'descricao'],
        'Empresas' : [
                'cnpj_basico',
                'razao_social_nome_empresarial',
                'natureza_juridica',
                'qualificacao_do_responsavel',
                'capital_social_da_empresa',
                'porte_da_empresa',
                'ente_federativo_responsavel',
        ],
        'Simples' : [
                'cnpj_basico',
                'opcao_pelo_simples',
                'data_de_opcao_pelo_simples',
                'data_de_exclusao_do_simples',
                'opcao_pelo_mei',
                'data_de_opcao_pelo_mei',
                'data_de_exclusao_do_mei',
            ],
        'Socios' : [
                'cnpj_basico',
                'identificador_de_socio',
                'nome_do_socio',
                'documento_do_socio',
                'codigo_qualificacao_do_socio',
                'data_de_entrada_sociedade',
                'codigo_pais',
                'documento_representante_legal',
                'nome_do_representante',
                'codigo_qualificacao_do_representante_legal',
                'faixa_etaria',
            ],
        'Estabelecimentos' : [
                'cnpj_basico',
                'cnpj_ordem',
                'cnpj_dv',
                'identificador_matriz_filial',
                'nome_fantasia',
                'situacao_cadastral',
                'data_situacao_cadastral',
                'motivo_situacao_cadastral',
                'nome_da_cidade_no_exterior',
                'pais',
                'data_de_inicio_atividade',
                'cnae_fiscal_principal',
                'cnae_fiscal_secundaria',
                'tipo_de_logradouro',
                'logradouro',
                'numero',
                'complemento',
                'bairro',
                'cep',
                'uf',
                'municipio',
                'ddd_1',
                'telefone_1',
                'ddd_2',
                'telefone_2',
                'ddd_do_fax',
                'fax',
                'correio_eletronico',
                'situacao_especial',
                'data_da_situacao_especial',
            ],
    }

dtypes_dict = {
    'Qualificacoes': {'codigo': np.int32, 'descricao': 'string'},
    'Cnaes': {'codigo': np.int32, 'descricao': 'string'},
    'Naturezas': {'codigo': np.int32, 'descricao': 'string'},
    'Municipios': {'codigo': np.int32, 'descricao': 'string'},
    'Paises': {'codigo': np.int32, 'descricao': 'string'},
    'Motivos' : {'codigo': np.int32, 'descricao': 'string'},
    'Empresas' : {
                'cnpj_basico': 'string',
                'razao_social_nome_empresarial': 'string',
                'natureza_juridica': 'string',
                'qualificacao_do_responsavel': 'string',
                'capital_social_da_empresa': 'string',
                'porte_da_empresa': 'string',
                'ente_federativo_responsavel': 'string',
            },
    'Simples' : {
                'cnpj_basico': 'string',
                'opcao_pelo_simples': 'string',
                'data_de_opcao_pelo_simples': 'string',
                'data_de_exclusao_do_simples': 'string',
                'opcao_pelo_mei': 'string',
                'data_de_opcao_pelo_mei': 'string',
                'data_de_exclusao_do_mei': 'string',
            },
    'Socios' : {
                'cnpj_basico': 'string',
                'identificador_de_socio': 'string',
                'nome_do_socio': 'string',
                'documento_do_socio': 'string',
                'codigo_qualificacao_do_socio': 'string',
                'data_de_entrada_sociedade': 'string',
                'codigo_pais': 'string',
                'documento_representante_legal': 'string',
                'nome_do_representante': 'string',
                'codigo_qualificacao_do_representante_legal': 'string',
                'faixa_etaria': 'string'
            },
    'Estabelecimentos' : {
            'cnpj_basico': np.int32,
            'cnpj_ordem': np.int16,
            'cnpj_dv': np.int16,
            'nome_fantasia': 'string',
            'cnae_fiscal_secundaria': 'string',
            'identificador_matriz_filial': np.int16,
            'motivo_situacao_cadastral': np.int16,
            'nome_da_cidade_no_exterior': 'string',
            'cep': 'string',
            'pais': 'string',
            'situacao_cadastral': np.int16,
            'telefone_1': 'string',
            'ddd_1': 'string',
            'telefone_2': 'string',
            'ddd_2': 'string',
            'fax': 'string',
            'ddd_do_fax': 'string',
            'situacao_especial': 'string',
            'data_da_situacao_especial': 'string'
        },
}

def download_dados_abertos(filename: str, number: int = '', save_path: str = '../raw_files/') -> list:
    """
    Baixa um arquivo ZIP de dados abertos relacionados a CNPJ do site "dadosabertos.rfb.gov.br" e o salva localmente.

    É exibida uma barra de progresso 

    Args:
        filename (str): O nome base do arquivo a ser baixado, podendo ser uma das seguintes opções:
            > Cnaes
            > Empresas
            > Estabelecimentos
            > Motivos
            > Municipios
            > Naturezas
            > Paises
            > Qualificacoes
            > Simples
            > Socios
        number (int, opcional): Um número opcional a ser adicionado ao nome do arquivo, sendo necessário nos casos dos seguintes arquivos:
            > Empresas
            > Estabelecimentos
            > Socios
        save_path (str, opcional): O caminho onde o arquivo ZIP será salvo. O padrão é '../raw_files/'.

    Returns:
        str: A função retorna o nome do arquivo baixado e salvo localmente.

    Example:
        download_dados_abertos('Estabelecimentos', number=1, save_path='/caminho/personalizado/')
        ## Isso baixará o arquivo 'Estabelecimentos1.zip' do site e o salvará em '/caminho/personalizado/'

    """
    url = f'https://dadosabertos.rfb.gov.br/CNPJ/{filename}{number}.zip'
    complete_filename = f'{filename}_{number:02}.zip' if number != '' else f'{filename}.zip'
    
    with open(f'{save_path}/{complete_filename}', 'wb') as f:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))

            # tqdm has many interesting parameters. Feel free to experiment!
            tqdm_params = {
                'desc': url,
                'total': total,
                'miniters': 1,
                'unit': 'B',
                'unit_scale': True,
                'unit_divisor': 1024,
                'dynamic_ncols': True,
            }
            with tqdm.tqdm(**tqdm_params) as pb:
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)
                    
    return complete_filename

def csv_to_parquet(filename: str, selector: str, number: int = '', save_path: str = '../raw_files/') -> None:
    """
    Converte um arquivo CSV (possivelmente dentro de um ZIP) em vários arquivos Parquet usando chunks.

    Esta função lê o arquivo CSV baixado do diretório especificado por save_path, e salva os dados em
    múltiplos arquivos Parquet com chunks.

    Args:
        filename (str): O nome do arquivo CSV a ser convertido, localizado em save_path.
        selector (str): Nome do seletor utilizado para baixar os dados e selecionar o nome das colunas e
        os tipos de dados para leitura.
        number (int, opcional): Um número opcional a ser adicionado ao nome do arquivo, sendo necessário
        nos casos dos seguintes arquivos:
            > Empresas
            > Estabelecimentos
            > Socios
        save_path (str, opcional): O diretório onde o arquivo CSV está localizado. Padrão: '../raw_files/'.

    Returns:
        None

    Example:
        >>> csv_to_parquet('Estabelecimentos_01.zip', selector='Estabelecimentos', number=2, save_path='/caminho/do/arquivo/')
        Converte o arquivo 'Estabelecimentos_01.zip' em arquivos Parquet.
        Os arquivos resultantes são divididos em chunks de 100000 linhas e são salvos no
        diretório '/caminho/do/arquivo/'.
    """
    complete_filename = f'{number:02}_{selector}' if number != '' else f'{selector}'
    count=0
    
    for chunck in pd.read_csv(f'{save_path}/{filename}', sep=';', encoding='latin1', names=column_name_dict[selector], chunksize=100000, dtype=dtypes_dict[selector]):
        count += 1
        print(f'Getting chunck number {count}')
        chunck.to_parquet(f'../parquet_files/{complete_filename}_{count:02}.parquet')


if __name__ == '__main__':
    seletor = args.selector
    file_path = args.path
    
    if seletor in ['Empresas', 'Estabelecimentos', 'Socios']:
        for i in range(10):
            file = download_dados_abertos(seletor, i, file_path)
            csv_to_parquet(file, seletor, i, file_path)
    else:  
        file = download_dados_abertos(seletor)
        csv_to_parquet(file, seletor)

