 {#
    Essa macro retorna a descrição Matriz / Filial
#}

{% macro get_matriz_filial(identificador_matriz_filial) -%}

    case {{ identificador_matriz_filial }}
        when 1 then 'MATRIZ'
        when 2 then 'FILIAL'
    end

{%- endmacro %}