{{ config(materialized='table') }}

select 
    cnpj_basico,
    opcao_pelo_simples,
    {{ get_opcao_simples('opcao_pelo_simples') }} as descricao_opcao_pelo_simples,
    case 
      when data_de_opcao_pelo_simples = '00000000' then null
      else cast(strptime(data_de_opcao_pelo_simples, '%Y%m%d') as date)
    end as data_de_opcao_pelo_simples,
    case 
      when data_de_exclusao_do_simples = '00000000' then null
      else cast(strptime(data_de_exclusao_do_simples, '%Y%m%d') as date)
    end as data_de_exclusao_do_simples,
    opcao_pelo_mei,
    {{ get_opcao_simples('opcao_pelo_mei') }} as descricao_opcao_pelo_mei,
    case 
      when data_de_opcao_pelo_mei = '00000000' then null
      else cast(strptime(data_de_opcao_pelo_mei, '%Y%m%d') as date)
    end as data_de_opcao_pelo_mei,
    case 
      when data_de_exclusao_do_mei = '00000000' then null
      else cast(strptime(data_de_exclusao_do_mei, '%Y%m%d') as date)
    end as data_de_exclusao_do_mei,
from {{ source('external_source', 'Simples') }}

-- dbt build --model ods_simples.sql --vars 'is_test_run: true'
{% if var('is_test_run', default=true) %}

  limit 1000

{% endif %}