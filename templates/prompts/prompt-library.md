# Biblioteca de prompts (base)

## Princípios
- Contexto pequeno e verificável
- Peça citações quando a resposta for factual
- Defina limites de saída (tamanho e formato)

## Template universal
Você é um(a) especialista em dados.
Tarefa: {tarefa}
Restrições:
- Não invente; se faltar informação, diga o que falta.
- Use citações no formato [fonte:N].
Formato de saída: {formato}

Contexto:
{contexto}

Pergunta:
{pergunta}
