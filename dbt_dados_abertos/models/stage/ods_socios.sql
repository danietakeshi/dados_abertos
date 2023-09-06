{{ config(materialized='table') }}

select 
    cnpj_basico,
    identificador_de_socio,
    {{ get_identificador_socio('identificador_de_socio') }} as descricao_identificador_de_socio,
    nome_do_socio,
    documento_do_socio,
    codigo_qualificacao_do_socio,
    cast(strptime(data_de_entrada_sociedade, '%Y%m%d') as date) as data_de_entrada_sociedade,
    codigo_pais,
    documento_representante_legal,
    nome_do_representante,
    codigo_qualificacao_do_representante_legal,
    faixa_etaria,
    {{ get_faixa_etaria('faixa_etaria') }} as descricao_faixa_etaria
from {{ source('external_source', 'Socios') }}

-- dbt build --model ods_socios.sql --vars 'is_test_run: true'
{% if var('is_test_run', default=true) %}

  limit 1000

{% endif %}