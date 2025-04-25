import pandas as pd
import psycopg2
import openpyxl

arquivo = 'xxx.xlsx'
tabela = 'lojas'
DB_CONFIG = {
    'host': 'x',
    'port': x,
    'dbname': 'x',
    'user': 'x',
    'password': 'x'
}

df = pd.read_excel(arquivo, dtype={'cnpj': str, 'telefone': str})

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

for _, row in df.iterrows():
    cnpj = str(row['cnpj']).replace('.', '').replace('-', '').replace('/', '')
    cnpj = cnpj.split('E')[0].replace(',', '').replace(' ', '').zfill(14)

    telefone = str(row['telefone']).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
    telefone = telefone.split('E')[0].replace(',', '').zfill(10)

    try:
        cursor.execute(f"""
            INSERT INTO {tabela} (
                cnpj, razaosocial, bandeira, validade_certificado,
                telefone, email, responsavel, ativo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cnpj) DO NOTHING
        """, (
            cnpj, row['razaosocial'], row['bandeira'],
            row['validade_certificado'], telefone,
            row['email'], row['responsavel'], row['ativo']
        ))
    except Exception as e:
        print(f"Erro ao inserir {cnpj}: {e}")
        conn.rollback()

conn.commit()
cursor.close()
conn.close()
print("Dados inseridos com sucesso!")
