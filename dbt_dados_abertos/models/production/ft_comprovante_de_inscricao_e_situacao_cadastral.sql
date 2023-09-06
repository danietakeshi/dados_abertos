{{ 
    config(
        materialized='table', 
        indexes=[
            {'columns': ['id_cnpj'], 'type': 'hash', 'unique': True},
        ]
    )
}}

select
	oes.id_cnpj, --Número do CNPJ
	oes.descricao_matriz_filial, --Descrição Matriz / Filial
	oes.data_de_inicio_atividade, --Data de Abertura
	oem.razao_social_nome_empresarial, --Razão Social
	oes.nome_fantasia, --Nome Fantasia,
	oem.descricao_porte_da_empresa, --Porte
	oes.cnae_fiscal_principal, --Código Cnae Principal
	oc.descricao descricao_cnae_fiscal_principal, --Descrição Cnae Principal
	oem.natureza_juridica, --Código Natureza Jurídica
	ona.descricao descricao_natureza_juridica, --Descrição Natureza jurídica
	oes.tipo_de_logradouro  || ' ' || oes.logradouro logradouro, --Logradouro
	oes.numero, --Número
	oes.complemento, --Complemento
	oes.cep, --CEP
	oes.bairro, --Bairro / Distrito
	om.descricao municipio, --Município
	oes.uf, --UF
	oes.correio_eletronico, --Endereço Eletrônico
	'(' || oes.ddd_1 || ') ' || oes.telefone_1 telefone, --Telefone
	oem.ente_federativo_responsavel, --Ente Federativo Responsável
	oes.descricao_situacao_cadastral,  --Situação Cadastral
	oes.data_situacao_cadastral, --Data Situação Cadastal
	omo.descricao motivo_situacao_cadastral, --Motivo da Situação Cadastral
	oes.situacao_especial, --Situação Especial
	oes.data_da_situacao_especial --Data Situação Especial
from {{ ref('ods_estabelecimentos') }} oes
inner join {{ ref('ods_empresas') }} oem on oes.cnpj_basico = oem.cnpj_basico
inner join {{ ref('ods_cnaes') }} oc on oes.cnae_fiscal_principal = oc.codigo
inner join {{ ref('ods_naturezas') }} ona on ona.codigo = oem.natureza_juridica
inner join {{ ref('ods_municipios') }} om on om.codigo = oes.municipio
inner join {{ ref('ods_motivos') }} omo on omo.codigo = oes.motivo_situacao_cadastral 