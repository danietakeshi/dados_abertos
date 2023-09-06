 {#
    Essa macro retorna a descrição da identificação do Sócio
#}

{% macro get_identificador_socio(identificador_de_socio) -%}

    case {{ identificador_de_socio }}
        when 1 then 'PESSOA JURÍDICA'
        when 2 then 'PESSOA FÍSICA'
        when 3 then 'ESTRANGEIRO'
    end

{%- endmacro %}