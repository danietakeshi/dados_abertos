 {#
    Essa macro retorna a descrição da situação Cadastral
#}

{% macro get_situacao_cadastral(situacao_cadastral) -%}

    case {{ situacao_cadastral }}
        when 1 then 'NULA'
        when 2 then 'ATIVA'
        when 3 then 'SUSPENSA'
        when 4 then 'INAPTA'
        when 8 then 'BAIXADA'
    end

{%- endmacro %}