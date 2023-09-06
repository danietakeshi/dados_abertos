 {#
    Essa macro retorna a descrição da faixa etária do Sócio
#}

{% macro get_faixa_etaria(faixa_etaria) -%}

    case {{ faixa_etaria }}
        when 1 then '0 a 12 anos'
        when 2 then '13 a 20 anos'
        when 3 then '21 a 30 anos'
        when 4 then '31 a 40 anos'
        when 5 then '41 a 50 anos'
        when 6 then '51 a 60 anos'
        when 7 then '61 a 70 anos'
        when 8 then '71 a 80 anos'
        when 9 then 'Maiores de 80 anos'
        when 0 then 'Não se aplica'
    end

{%- endmacro %}