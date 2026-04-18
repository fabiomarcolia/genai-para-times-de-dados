# Segurança e custo (prático)

## Regras simples que evitam desastre
1- Nunca envie PII para um provedor externo sem política e base legal
2- Separe dados públicos, internos e sensíveis
3- Crie “limites por padrão”:
- TOP_K baixo
- Contexto com tamanho máximo
- MAX_TOKENS controlado
4- Logue:
- prompt/response (com mascaramento)
- custo estimado
- latência
- fontes usadas (citações)

## Como evitar gasto
- Comece com offline-first (TF‑IDF) e LLM local (Ollama)
- Use cache de respostas
- Reduza tokens com prompts objetivos
- Limite o contexto por ranking e por tamanho
- Evite embeddings pagas até validar valor

## Guardrails (básico)
- Bloqueie pedido por credenciais/chaves
- Remova dados sensíveis do contexto
- Exija citações quando a resposta for factual
