{{ config(materialized='table') }}

select
    codigo,
    descricao
from {{ source('external_source', 'Cnaes') }}