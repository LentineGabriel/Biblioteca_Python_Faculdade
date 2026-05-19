# 🌟 Estante Inteligente - Biblioteca & Leitura Simplificada

> Um sistema de gestão de acervo e estante virtual pessoal projetado sob a ótica da **acessibilidade digital**, com interface clean e navegação direta, desenvolvido sob medida para pessoas que amam ler, mas possuem baixa afinidade com sistemas tecnológicos complexos.

Este projeto representa o trabalho acadêmico desenvolvido por alunos da **Universidade Nove de Julho (Uninove) — Campus Santo Amaro**.

---

## 👥 Integrantes e Desenvolvedores

| Nome Completo | Registro Acadêmico (RA) |
| :--- | :--- |
| **Gabriel Henrique Marinho Lentine** | `2225105706` |
| **Ana Clara Menezes Maciel** | `2225101484` |
| **Murillo do Nascimento Silva** | `2225102975` |
| **Bruno Pereira Silva** | `2225105721` |
| **Danyelle dos Santos Hengler** | `2325100583` |
| **Gustavo Oliveira Santos** | `2225105333` |
| **Rafael Azevedo Santos** | `2325103526` |

---

## 🎯 O Propósito Humano do Projeto

Muitos leitores ávidos — especialmente idosos ou pessoas que não cresceram imersas na era digital — sentem-se intimidados por sistemas de bibliotecas repletos de tabelas complexas, submenus confusos, campos de digitação minúsculos e jargões técnicos.

A **Estante Inteligente** resolve essa barreira com uma filosofia de design focada no acolhimento e no suporte ao usuário:
*   **Single Page Application (SPA)**: O usuário realiza todas as ações em uma única tela. Ele nunca se perde trocando de página ou carregando novos links no navegador.
*   **Design System Dark Mode Premium**: Cores escuras e relaxantes que eliminam a fadiga visual, acompanhadas da tipografia arredondada *Outfit* (Google Fonts), ideal para leitura em telas.
*   **Formulários "Sem Rodeios"**: Se o usuário estiver cadastrando um livro e perceber que o Autor ou Editora não existem na listagem, ele pode criá-los clicando em um pequeno botão `[ + ]` direto no formulário. O sistema cria o autor e o seleciona automaticamente, evitando fechamentos de janelas e perda de progresso.
*   **Tradutor de Erros para Linguagem Humana**: Em vez de códigos de erro misteriosos como `ValidationError: [422]`, o sistema traduz falhas de validação de e-mails ou telefones em alertas vermelhos didáticos e acolhedores (ex: *"O telefone precisa conter DDD e o número formatado como (DD) 9XXXX-XXXX"*).

---

## 🏗️ Arquitetura do Sistema

O projeto foi projetado utilizando boas práticas de desenvolvimento backend sênior em camadas e front-end com tecnologia Web pura, garantindo leveza absoluta e velocidade instantânea de carregamento:

```text
Python_Biblioteca_Faculdade/
├── back-end/                # Camada de Backend (FastAPI, Python e PostgreSQL)
│   ├── app/
│   │   ├── api/             # Isolamento das rotas HTTP (APIRouter)
│   │   ├── core/            # Configurações globais, conexões e validações de borda
│   │   ├── models/          # Entidades de negócio tipadas
│   │   ├── repositories/    # Persistência SQL bruta psycopg (sem ORMs pesados)
│   │   ├── schemas/         # Validação rígida de dados na borda com Pydantic V2
│   │   └── main.py          # Inicializador da API FastAPI e Middleware de CORS
│   ├── Dockerfile           # Imagem leve de containerização da API
│   ├── init.sql             # Script automático de criação física de tabelas no Postgres
│   └── requirements.txt     # Dependências de pacotes
├── front-end/               # Camada de Apresentação (Acessível, Clean e Premium)
│   ├── index.html           # Esqueleto HTML5 da SPA estruturado com Lucide Icons
│   ├── style.css            # Folha de estilos Dark Mode, Glassmorphism e Transições
│   └── app.js               # Lógica em JavaScript ES6 de consumo assíncrono à API (fetch)
└── docker-compose.yml       # Orquestrador de rede local do Banco + API
```

---

## 🚦 Como Executar a Aplicação

Para fins de praticidade acadêmica e de desenvolvimento, o ecossistema pode ser executado localmente em menos de 2 minutos.

### Passo 1: Subir o Backend (Docker)
Com o Docker instalado na máquina, abra o terminal na raiz do projeto e execute:
```bash
docker compose up --build
```
Isso inicializará de forma totalmente resiliente o banco de dados PostgreSQL e a API FastAPI. A API estará ativa na porta `http://localhost:8000/`. Você pode testar e interagir diretamente com os endpoints na documentação autogerada em **`http://localhost:8000/docs`**.

### Passo 2: Acessar a Interface do Usuário (Front-end)
Graças à escolha de tecnologias nativas (HTML, CSS e JavaScript puros), não há necessidade de empacotadores complicados ou comandos do Node.js para rodar a interface:
1.  Navegue até a pasta **`front-end/`**.
2.  **Dê dois cliques no arquivo `index.html`**!
3.  O painel visual e acessível se abrirá instantaneamente no seu navegador de internet padrão e se comunicará perfeitamente com a API local.

---

## 🎓 Instituição de Ensino
*   **Universidade Nove de Julho — UNINOVE**
*   **Campus**: Santo Amaro, São Paulo - SP.
*   **Projeto Acadêmico de Análise e Desenvolvimento de Sistemas**
