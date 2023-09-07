import streamlit as st
import duckdb
from streamlit_lottie import st_lottie
import requests


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Carregue o arquivo JSON da animação Lottie
lottie_search = load_lottieurl('https://lottie.host/f6530fed-b976-477c-abe0-c10a125d114c/x6QlRKooX2.json')

# Conectar ao banco de dados DuckDB
conn = duckdb.connect(database='../database/dados_abertos.duckdb')

# Função para pesquisar CNPJ
def pesquisar_cnpj(cnpj):
    query = f"SELECT * FROM dados_abertos.main.ft_comprovante_de_inscricao_e_situacao_cadastral WHERE id_cnpj = '{cnpj}'"
    result = conn.execute(query).df()
    return result

# Função para pesquisar CNAEs Secundárias
def pesquisar_cnaes(cnpj):
    query = f"SELECT * FROM dados_abertos.main.ft_cnaes_secundarias_as_list WHERE id_cnpj = '{cnpj}'"
    result = conn.execute(query).df()
    return result

# Função para pesquisar Sócios
def pesquisar_socios(cnpj):
    query = f"SELECT * FROM dados_abertos.main.ft_socios WHERE cnpj_basico = '{cnpj[:8]}'"
    result = conn.execute(query).df()
    return result

def formatar_cnpj(cnpj):
    # Inserir os pontos e barras no CNPJ formatado
    cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

    return cnpj_formatado

# Exiba a animação no aplicativo Streamlit
st_lottie(lottie_search, width=300, height=300)

# Configurações do Streamlit
st.title("Procurar CNPJ no DuckDB")

# Input do usuário para inserir o CNPJ
cnpj_input = st.text_input("Digite o CNPJ que deseja pesquisar:")

if st.button("Pesquisar"):
    if cnpj_input:
        resultado = pesquisar_cnpj(cnpj_input)
        if not resultado.empty:
            st.success("CNPJ encontrado!")

            # Formatar a saída como um comprovante de situação cadastral
            st.header("Dados da Empresa:")
            st.write(f"CNPJ: {formatar_cnpj(resultado['id_cnpj'].values[0])}")
            st.write(f"Razão Social: {resultado['razao_social_nome_empresarial'].values[0]}")
            st.write(f"Nome Fantasia: {resultado['nome_fantasia'].values[0]}")
            st.write(f"Matriz / Filial: {resultado['descricao_matriz_filial'].values[0]}")
            st.write(f"Data início de Atividade: {str(resultado['data_de_inicio_atividade'].values[0])[:10]}")
            st.write(f"Porte da Empresa: {resultado['descricao_porte_da_empresa'].values[0]}")
            
            st.header("Endereço:")
            st.write(f"Logradouro: {resultado['logradouro'].values[0]}")
            st.write(f"Número: {resultado['numero'].values[0]}")
            st.write(f"Complemento: {resultado['complemento'].values[0]}")
            st.write(f"Bairro: {resultado['bairro'].values[0]}")
            st.write(f"Cidade: {resultado['municipio'].values[0]}")
            st.write(f"Estado: {resultado['uf'].values[0]}")
            st.write(f"CEP: {resultado['cep'].values[0]}")
            st.write(f"Telefone: {resultado['telefone'].values[0]}")
            st.write(f"Email: {resultado['correio_eletronico'].values[0]}")

            st.header("Natureza Jurídica:")
            st.write(f"{resultado['natureza_juridica'].values[0]} : {resultado['descricao_natureza_juridica'].values[0]}")

            st.header("Situação Cadastral:")
            st.write(f"Situação: {resultado['descricao_situacao_cadastral'].values[0]}")
            st.write(f"Data da Situação: {str(resultado['data_situacao_cadastral'].values[0])[:10]}")
            st.write(f"Motivo da Situação: {resultado['motivo_situacao_cadastral'].values[0]}")

            st.header("Situação Especial:")
            st.write(f"{resultado['situacao_especial'].values[0]} : {str(resultado['data_da_situacao_especial'].values[0])[:10]}")

            st.header("Atividade Econômica Principal:")
            st.write(f"Código CNAE Principal: {resultado['cnae_fiscal_principal'].values[0]}")
            st.write(f"Descrição CNAE Principal: {resultado['descricao_cnae_fiscal_principal'].values[0]}")

            cnaes = pesquisar_cnaes(cnpj_input)
            if not cnaes.empty:
                st.header("Atividades Econômicas Secundárias:")

                for cnpj, codigo, descricao in cnaes.values.tolist():
                    st.write(f"{codigo} - {descricao}")

            socios = pesquisar_socios(cnpj_input)
            if not socios.empty:
                st.header("Sócios:")

                for cnpj_basico, descricao_identificador_de_socio, nome_do_socio, descricao, data_de_entrada_sociedade, descricao_faixa_etaria in socios.values.tolist():
                    st.write(f"{nome_do_socio} ({descricao_identificador_de_socio}) - {descricao} - {descricao_faixa_etaria}")
            
        else:
            st.warning("CNPJ não encontrado.")
    else:
        st.warning("Por favor, insira um CNPJ válido.")

# Fechar a conexão com o banco de dados DuckDB
conn.close()
