#!/bin/bash

if [ -d "raw_files" ]; then
  echo "Folder raw_files exists"
else
  echo "Creating Folder raw_files..."
  mkdir raw_files
fi

if [ -d "parquet_files" ]; then
  echo "Folder parquet_files exists"
else
  echo "Creating Folder parquet_files..."
  mkdir parquet_files
fi

if [ -d "database" ]; then
  echo "Folder database exists"
else
  echo "Creating Folder parquet_files..."
  mkdir database
fi

cd python
python3 dados_abertos_etl.py -s "Qualificacoes"
python3 dados_abertos_etl.py -s "Cnaes"
python3 dados_abertos_etl.py -s "Naturezas"
python3 dados_abertos_etl.py -s "Municipios"
python3 dados_abertos_etl.py -s "Paises"
python3 dados_abertos_etl.py -s "Motivos"
python3 dados_abertos_etl.py -s "Empresas"
python3 dados_abertos_etl.py -s "Simples"
python3 dados_abertos_etl.py -s "Socios"
python3 dados_abertos_etl.py -s "Estabelecimentos"

cd ../dbt_dados_abertos
dbt run --vars "is_test_run: false"
