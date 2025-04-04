create type bandeira_enum as enum ('FARMES', 'EXTRA', 'FARMESLOG', 'MKT');

create table if not exists lojas (
    id uuid primary key default uuid_generate_v4(),
    cnpj varchar(14) unique not null,
    razaosocial varchar(255) not null,
    bandeira bandeira_enum not null,
    validade_certificado date not null,
    telefone varchar(20) not null,
    email varchar(100) not null,
    responsavel varchar(255) not null,
    ativo boolean not null
);

create table if not exists responsaveis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Tabela de Relacionamento Loja x Responsável (M:N)
create table if not exists loja_responsavel (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    loja_id UUID NOT NULL,
    responsavel_id UUID NOT NULL,
    FOREIGN KEY (loja_id) REFERENCES lojas(id) ON DELETE CASCADE,
    FOREIGN KEY (responsavel_id) REFERENCES responsaveis(id) ON DELETE CASCADE,
    UNIQUE(loja_id, responsavel_id)
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";