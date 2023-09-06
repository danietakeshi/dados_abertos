{{ 
    config(
        materialized='table', 
        indexes=[
            {'columns': ['id_cnpj'], 'type': 'hash', 'unique': False},
        ]
    )
}}

with cnae_fiscal_secundaria_aux as 
(
    -- Seleciona os CNPJs cujo campo `cnae_fiscal_secundaria` possui informações
    select
        id_cnpj,
        cnae_fiscal_secundaria
    from {{ ref('ods_estabelecimentos') }}
    where cnae_fiscal_secundaria is not null
),

cnae_fiscal_secundaria_as_list as 
(
    -- Transforma o campo `cnae_fiscal_secundaria` em uma lista e utiliza a função
    -- unnest para transformar essa lista em linhas da tabela
    select 
        id_cnpj,
        unnest(string_split(cnae_fiscal_secundaria, ',')) as cnae_fiscal_secundaria
    from cnae_fiscal_secundaria_aux
)

-- Join com a tabela `ods_cnaes` para pegar as descrições dos CNAEs
select
	cfs.id_cnpj,
	cfs.cnae_fiscal_secundaria,
	oc.descricao descricao_cnae_secundaria
from cnae_fiscal_secundaria_as_list cfs
inner join {{ ref('ods_cnaes') }} oc on oc.codigo = cfs.cnae_fiscal_secundaria