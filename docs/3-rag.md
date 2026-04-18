# RAG na prática (sem misticismo)

## O que é
RAG = Retrieval Augmented Generation  
Você **recupera** trechos relevantes e passa como **contexto** para o LLM responder melhor e alucinar menos.

## Quando usar
- Chat com dados/FAQs internos
- Assistente de analytics (“como está o mês?”)
- Geração de documentação (com base em fontes)

## Erros comuns
- Contexto gigante (custa caro e piora resposta)
- Chunking ruim (quebra significado)
- Não registrar fontes (sem rastreabilidade)

## Checklist
- Defina fontes e permissões
- Determine estratégia (keyword vs vetor)
- Faça avaliação com perguntas reais
- Monitore custo/latência/alucinação
