# Avaliação (Evals) para apps com LLM

## Por que importa
Sem avaliação você não sabe se:
- Melhorou ou piorou
- Está alucinando mais
- Está custando mais caro

## O mínimo viável
- Um dataset JSONL de perguntas (10–50 itens)
- Uma função de execução
- Métricas simples:
  - acerto (heurística)
  - citações presentes
  - tamanho do contexto
  - latência e custo estimado

Veja `templates/eval/`.
