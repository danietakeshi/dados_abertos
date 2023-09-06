 {#
    Essa macro retorna a descrição do porte da Empresa
#}

{% macro get_porte_empresa(porte_da_empresa) -%}

    case {{ porte_da_empresa }}
        when 0 then 'NÃO INFORMADO'
        when 1 then 'MICRO EMPRESA'
        when 3 then 'EMPRESA DE PEQUENO PORTE'
        when 5 then 'DEMAIS'
    end

{%- endmacro %}