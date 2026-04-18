# 🤖 GenAI para Times de Dados

Aplicações práticas de IA Generativa (LLMs) para **Analytics** e **Engenharia de Dados**: RAG, agentes, avaliação, guardrails, observabilidade e custo.

<!-- Tech Stack / Tooling Badges -->
[![Python](https://img.shields.io/badge/Python-3.10%2B-0b1f36)](#)
[![SQL](https://img.shields.io/badge/SQL-ANSI%20%7C%20Postgres%20%7C%20BigQuery-0b1f36)](#)
[![Docker](https://img.shields.io/badge/Docker-Ready-0b1f36)](#)
[![VS%20Code](https://img.shields.io/badge/VS%20Code-Dev%20Setup-0b1f36)](#)

<!-- GenAI / LLM -->
[![LLM](https://img.shields.io/badge/LLM-OpenAI%20%7C%20Ollama%20%7C%20Claude-0b1f36)](#)
[![RAG](https://img.shields.io/badge/RAG-Embeddings%20%2B%20Citations-0b1f36)](#)
[![Agents](https://img.shields.io/badge/Agents-Tool%20Calling%20%2B%20Workflows-0b1f36)](#)
[![Evaluation](https://img.shields.io/badge/Evaluation-Quality%20%2F%20Cost%20%2F%20Regression-0b1f36)](#)

---

A Inteligência Artificial Generativa (GenAI) está transformando a área de dados ao automatizar tarefas complexas que antes exigiam esforço manual exaustivo. Segundo especialistas do Databricks, essa tecnologia não apenas interpreta informações, mas cria novos conteúdos e contextos a partir de grandes conjuntos de dados. 

As principais aplicações da GenAI no ciclo de vida dos dados incluem:

- **Análise de Dados Interativa**: Permite que usuários façam perguntas em linguagem natural para gerar consultas SQL ou relatórios complexos automaticamente.
- **Geração de Dados Sintéticos**: Cria datasets artificiais que mantêm as propriedades estatísticas dos dados reais, essencial para proteger a privacidade e treinar modelos onde há escassez de informação.
- **Engenharia e Limpeza de Dados**: Facilita a criação de pipelines de dados e a identificação de padrões para limpeza e normalização de registros.
- **Insights Preditivos**: Aumenta a capacidade de prever tendências futuras ao analisar volumes massivos de dados históricos de forma rápida. 

No entanto, a implementação bem-sucedida depende de uma base de dados sólida. Conforme destacado pela Bain & Company, a arquitetura e a governança de dados são os maiores desafios e, ao mesmo tempo, os pilares fundamentais para que a GenAI entregue valor real.

---

Playbook + templates + demos para aplicar LLMs/GenAI em times de Dados (Analytics, Engenharia de Dados, BI e Produto) com foco em **valor**, **segurança** e **custo controlado**.

## 🔎 O que você encontra aqui
- **Playbook**: padrões, arquitetura e boas práticas (RAG, avaliação, guardrails, observabilidade).
- **Templates**: prompts, datasets de avaliação, esqueleto de agentes e checklists.
- **Demos executáveis**: mini-projetos prontos (offline-first; LLM opcional).
- **Prompts super valiosos**: Os melhores prompts para aprender, construir e resolver problemas com dados.


## ⏳Quickstart (5 minutos) - Vamos praticar!

  
Pré-requisitos:
- Python 3.11+ (recomendado)
- Git
- (Opcional) Docker

    - Se quiser aprender Python para Dados, veja [aqui](https://github.com/fabiomarcolia/python-para-dados])

---

1- Crie o ambiente
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

2- Rode a demo de RAG (offline-first)
```bash
python demos/01-rag-csv/app.py --question "Qual foi o faturamento total por mês?"
```

3- (Opcional) Use um LLM local via Ollama
```bash
# em outro terminal:
ollama pull llama3.1

# depois:
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.1
python demos/01-rag-csv/app.py --question "Resuma os 3 principais insights do dataset."
```

> Dica de custo: por padrão, as demos usam **busca TF-IDF local**, sem embeddings pagas e sem chamadas externas.

---

⚠️ Veja a documentação: [Documentação importante](docs)

## Demos para praticar
- [RAG:](demos/1-rag-csv)
  RAG simples em cima de CSV (chunking + retrieval + resposta com citações). Offline-first.

- [SQL Copilot:](demos/2-sql-copilot):
  “Copilot” de SQL: pergunta → SQL + explicação + validação em SQLite (dataset sintético).

- [Dashboard Docs:](demos/3-dashboard-docs):
  Gerador de documentação a partir de metadados de dashboard (modelo simples e extensível).

- [Data Quality:](demos/4-data-quality):
  Data quality + narrativa: profiling → regras sugeridas → relatório em Markdown (LLM opcional).

- [Agente de Relaório:](demos/5-agent-relatorio): 
  Lê um dataset > Faz uma análise > Gera Relatório > Envia por email.

- [Linguagem Natural para Python:](demos/6-nl-to-python): 
  Recebe uma instrução em PT-BR (ex.: “limpe nulos, crie faixas, faça agregação e gere gráfico”) > Gera um script Python padronizado (pandas + matplotlib)


## 📂 Estrutura do repositório
```text
docs/                 guias e playbook
templates/            prompts, checklists, datasets e esqueletos
demos/                mini-projetos executáveis
datasets/             dados sintéticos (seguros para repo público)
src/                  utilitários compartilhados
tests/                testes unitários
.github/workflows/     CI (lint + tests)
```

## 💸 Como evitar custo e surpresas
- Use **LLM local** (Ollama) para estudo e protótipos.
- Evite embeddings pagas no início: comece com **TF‑IDF** e migre quando fizer sentido.
- Coloque limites: `MAX_TOKENS`, `TOP_K`, `MAX_CONTEXT_CHARS`.
- Logue custo e latência (mesmo local): isso vira disciplina do time.

Veja: `docs/05-seguranca-custos.md`

## 🎁 Recursos
 - [Dashboard Docs](templates/prompts/dashboard-docs.md)
 - [Prompt Library](templates/prompts/prompt-library.md)
 - [SQL Copilot](templates/prompts/sql-copilot.md)
 - [Top 50 prompts super úteis](templates/prompts/top-50.md)


---
## Autor - Fabio Marçolia | Carreira em Dados & IA

Para mais conteúdo Carreira em Dados e IA, ou se quiser falar comigo sobre dúvidas, sugestões ou feedback:

- Linkedin: [Vamos nos conectar e me envie uma mensagem🤝](http://linkedin.com/in/fabiomarcolia)
- Mais Recursos de Carreira: [Veja aqui](https://topmate.io/fabiomarcolia)

Agradeço seu apoio e fique a vontade de entrar em contato comigo!

