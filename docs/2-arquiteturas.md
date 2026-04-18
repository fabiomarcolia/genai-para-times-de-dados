# Arquiteturas recomendadas

## 1) RAG offline-first (ótimo para POCs)
- Retrieval com TF‑IDF / BM25
- Contexto pequeno + citações
- LLM opcional

Fluxo:
1- Ingestão e limpeza
2- Chunking
3- Indexação local
4- Recuperação top‑k
5- Prompt com contexto
6- Resposta com citações

## 2) RAG híbrido (produção)
- Keyword (BM25) + vetor (embeddings)
- Re-ranking
- Cache
- Observabilidade (latência/custo)
- Políticas de acesso (RBAC por fonte)

## 3) “Copilot” de SQL com validação
- Geração de SQL
- Explicação linha a linha
- Exec see-if-it-runs (sandbox)
- Testes (asserts sobre resultados)

## 4) Documentação automática
- Metadados (dbt, catálogo, Power BI)
- Templates de documentação
- Geração incremental por diffs
