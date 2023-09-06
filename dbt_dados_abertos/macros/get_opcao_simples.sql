 {#
    Essa macro retorna a descrição da opção Simples / MEI
#}

{% macro get_opcao_simples(opcao) -%}

    case {{ opcao }}
        when 'S' then 'SIM'
        when 'N' then 'NÃO'
        ELSE 'OUTROS'
    end

{%- endmacro %}