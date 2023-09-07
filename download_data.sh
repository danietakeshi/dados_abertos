#!/bin/bash

if [ -d "raw_files" ]; then
  echo "Folder exists"
else
  echo "Creating Folder raw_files..."
  mkdir raw_files
fi

if [ -d "parquet_files" ]; then
  echo "Folder exists"
else
  echo "Creating Folder parquet_files..."
  mkdir parquet_files
fi

cd python
python dados_abertos_etl.py -s "Qualificacoes"
python dados_abertos_etl.py -s "Cnaes"
python dados_abertos_etl.py -s "Naturezas"
python dados_abertos_etl.py -s "Municipios"
python dados_abertos_etl.py -s "Paises"
python dados_abertos_etl.py -s "Motivos"
python dados_abertos_etl.py -s "Empresas"
python dados_abertos_etl.py -s "Simples"
python dados_abertos_etl.py -s "Socios"
python dados_abertos_etl.py -s "Estabelecimentos"

cd ../dbt_dados_abertos
dbt run --vars "is_test_run: false"