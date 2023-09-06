{{ config(materialized='table') }}

select 
    cnpj_basico,
    razao_social_nome_empresarial,
    natureza_juridica,
    qualificacao_do_responsavel,
    capital_social_da_empresa,
    porte_da_empresa,
    {{ get_porte_empresa('porte_da_empresa') }} as descricao_porte_da_empresa,
    ente_federativo_responsavel
from {{ source('external_source', 'Empresas') }}
where razao_social_nome_empresarial is not null

-- dbt build --model ods_empresas.sql --vars 'is_test_run: true'
{% if var('is_test_run', default=true) %}

  limit 1000

{% endif %}