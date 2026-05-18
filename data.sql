-- =========================================
-- BANCO: BIBLIOTECA
-- MODELAGEM COMPLETA
-- =========================================

-- =========================
-- TABELA: USUARIOS
-- =========================
-- Armazena os usuários do sistema

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,       -- Identificador único
    nome VARCHAR(100) NOT NULL,          -- Nome do usuário
    email VARCHAR(100) UNIQUE NOT NULL,  -- Email único
    endereco TEXT,                       -- Endereço (opcional)
    telefone VARCHAR(20)                 -- Telefone (opcional)
);

-- =========================
-- TABELA: EDITORA
-- =========================
-- Representa editoras dos livros

CREATE TABLE editora (
    id_editora SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- =========================
-- TABELA: AUTOR
-- =========================
-- Representa autores dos livros

CREATE TABLE autor (
    id_autor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- =========================
-- TABELA: LIVROS
-- =========================
-- Armazena os livros da biblioteca

CREATE TABLE livros (
    id_livro SERIAL PRIMARY KEY,
    nome_livro VARCHAR(255) NOT NULL,
    id_editora INTEGER,

    -- Relacionamento com editora
    CONSTRAINT fk_editora
        FOREIGN KEY (id_editora)
        REFERENCES editora(id_editora)
        ON DELETE SET NULL
);

-- =========================
-- TABELA: LIVRO_AUTOR
-- =========================
-- Relação N:N entre livros e autores

CREATE TABLE livro_autor (
    id_livro INTEGER,
    id_autor INTEGER,

    -- Chave primária composta
    PRIMARY KEY (id_livro, id_autor),

    -- Relacionamentos
    CONSTRAINT fk_livro
        FOREIGN KEY (id_livro)
        REFERENCES livros(id_livro)
        ON DELETE CASCADE,

    CONSTRAINT fk_autor
        FOREIGN KEY (id_autor)
        REFERENCES autor(id_autor)
        ON DELETE CASCADE
);

-- =========================
-- TABELA: EMPRESTIMOS
-- =========================
-- Controla empréstimos de livros

CREATE TABLE emprestimos (
    id_emprestimo SERIAL PRIMARY KEY,

    id_usuario INTEGER NOT NULL,
    id_livro INTEGER NOT NULL,

    data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_prazo TIMESTAMP,
    data_devolucao TIMESTAMP,

    status VARCHAR(20) NOT NULL,

    -- Validação de status (simula ENUM)
    CONSTRAINT chk_status
        CHECK (status IN ('emprestado', 'devolvido', 'atrasado')),

    -- Relacionamentos
    CONSTRAINT fk_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE,

    CONSTRAINT fk_livro_emprestimo
        FOREIGN KEY (id_livro)
        REFERENCES livros(id_livro)
        ON DELETE CASCADE
);

-- =========================
-- TABELA: ESTANTE
-- =========================
-- Controla a estante pessoal de livros dos usuários

CREATE TABLE estante (
    id_estante SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_livro INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Validação de status (simula ENUM)
    CONSTRAINT chk_status_estante
        CHECK (status IN ('lido', 'lendo', 'quero ler')),

    -- Relacionamentos
    CONSTRAINT fk_usuario_estante
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE,

    CONSTRAINT fk_livro_estante
        FOREIGN KEY (id_livro)
        REFERENCES livros(id_livro)
        ON DELETE CASCADE,

    -- Evita duplicidade do mesmo livro na estante do mesmo usuário
    CONSTRAINT uk_usuario_livro
        UNIQUE (id_usuario, id_livro)
);