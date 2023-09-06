{{ config(materialized='table') }}

select 
    cnpj_basico,
    cnpj_ordem,
    cnpj_dv,
    lpad(cnpj_basico, 8, '0') || lpad(cnpj_ordem, 4, '0') || lpad(cnpj_dv, 2, '0') id_cnpj,
    identificador_matriz_filial,
    {{ get_matriz_filial('identificador_matriz_filial') }} as descricao_matriz_filial,
    nome_fantasia,
    situacao_cadastral,
    {{ get_situacao_cadastral('situacao_cadastral') }} as descricao_situacao_cadastral,
    case 
        when data_situacao_cadastral = 0 then null
        when data_situacao_cadastral = 2021221 then cast(strptime('20221221', '%Y%m%d') as date)
        else cast(strptime(data_situacao_cadastral, '%Y%m%d') as date)
    end data_situacao_cadastral,
    motivo_situacao_cadastral,
    nome_da_cidade_no_exterior,
    pais,
    case 
        when data_de_inicio_atividade = 0 then null
        when data_de_inicio_atividade = 2021221 then cast(strptime('20221221', '%Y%m%d') as date)
        else cast(strptime(data_de_inicio_atividade, '%Y%m%d') as date)
    end data_de_inicio_atividade,
    cnae_fiscal_principal,
    cnae_fiscal_secundaria,
    tipo_de_logradouro,
    logradouro,
    numero,
    complemento,
    bairro,
    cep,
    uf,
    municipio,
    ddd_1,
    telefone_1,
    ddd_2,
    telefone_2,
    ddd_do_fax,
    fax,
    correio_eletronico,
    situacao_especial,
    cast(strptime(data_da_situacao_especial, '%Y%m%d') as date) data_da_situacao_especial
from {{ source('external_source', 'Estabelecimentos') }}

-- dbt build --model ods_estabelecimentos.sql --vars 'is_test_run: true'
{% if var('is_test_run', default=true) %}

  limit 1000

{% endif %}