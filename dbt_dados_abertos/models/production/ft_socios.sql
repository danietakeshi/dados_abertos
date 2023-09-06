{{ 
    config(
        materialized='table', 
        indexes=[
            {'columns': ['cnpj_basico'], 'type': 'hash', 'unique': False},
        ]
    )
}}

select
	os.cnpj_basico,
	os.descricao_identificador_de_socio,
	os.nome_do_socio,
	oq.descricao,
	os.data_de_entrada_sociedade,
	os.descricao_faixa_etaria 
from {{ ref('ods_socios') }} os
inner join {{ ref('ods_qualificacoes') }} oq on os.codigo_qualificacao_do_socio = oq.codigo