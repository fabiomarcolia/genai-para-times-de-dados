# Top 50 Prompts — aprender, explicar e usar ferramentas (LLMs/GenAI)

> Copie e cole. Substitua os campos entre colchetes.  
> Dica: sempre inclua **contexto**, **objetivo**, **restrições** (formato de saída, limites, fontes permitidas) e **o que você já tentou**.

---

## A) Aprender LLMs e fundamentos (1–12)

1. **Explique como se eu fosse Staff**  
   Explique **[tópico]** para um time de dados nível senior. Traga: definição, onde falha, trade-offs, exemplos práticos, anti‑padrões e checklist de produção.

2. **Mapa mental + trilha**  
   Crie um mapa mental de **[tópico]** e uma trilha de estudo em 4 semanas com entregáveis semanais e critérios de “pronto”.

3. **Do zero ao “ship”**  
   Quero aplicar **[tópico]** em produção. Liste os passos do discovery ao deploy, com riscos e decisões arquiteturais.

4. **Pergunte antes**  
   Antes de responder, faça no máximo 7 perguntas para reduzir ambiguidades sobre **[tarefa]**. Depois, proponha a solução.

5. **Comparação com analogia**  
   Compare **[A] vs [B]** usando uma analogia simples + uma tabela de trade-offs + recomendação por cenário.

6. **Efeito dominó**  
   Se eu errar **[decisão]** em um sistema com LLM, quais são as consequências em qualidade, custo, segurança e operação?

7. **Glossário rápido**  
   Monte um glossário essencial de **[tópico]** com definições de 1 linha e exemplo real.

8. **O que eu devo evitar**  
   Liste os 10 erros mais comuns em **[tópico]** e como identificar cada um na prática.

9. **Plano de entrevista**  
   Me prepare para uma entrevista sobre **[tópico]**: 15 perguntas difíceis + respostas modelo + o que o entrevistador quer ouvir.

10. **Teste seu entendimento**  
   Faça um quiz com 12 questões (múltipla escolha + explicação) sobre **[tópico]**.

11. **Checklist de produção**  
   Crie um checklist de produção para **[app com LLM]** cobrindo: segurança, privacidade, custos, logs, fallback, observabilidade e testes.

12. **Arquitetura em texto**  
   Descreva uma arquitetura de referência para **[tópico]** (componentes + fluxos + armazenamento + monitoramento), e gere um diagrama Mermaid.

---

## B) RAG e busca com fontes (13–22)

13. **RAG blueprint**  
   Desenhe um blueprint RAG para **[tipo de conteúdo: PDFs/Notion/Confluence/SQL docs]**: ingestão, chunking, embeddings, retrieval, re-ranking, geração, citações e cache.

14. **Chunking strategy**  
   Dado este tipo de documento **[descreva]**, qual estratégia de chunking você recomenda? Dê parâmetros e motivos.

15. **Avaliação de RAG**  
   Crie um plano de avaliação para RAG com métricas: recall@k, faithfulness, citation accuracy, latency e custo. Sugira dataset de perguntas.

16. **Perguntas “bom retrieval”**  
   Gere 30 perguntas que validem se a base RAG está boa para **[domínio]** (perguntas fáceis, médias, difíceis).

17. **Prompt com citações**  
   Responda usando **apenas** o contexto abaixo. Inclua citações no formato `[fonte:trecho]` ou `[doc:linha]`. Se faltar info, diga “não encontrado no contexto”.

18. **RAG anti-alucinação**  
   Sugira guardrails para reduzir alucinação em RAG: políticas de resposta, thresholds, fallback e mensagens ao usuário.

19. **Reranker**  
   Quando usar reranker? Explique trade-offs e proponha uma configuração mínima com exemplos.

20. **Cache e custo**  
   Proponha um plano de cache (embeddings, retrieval, geração) para reduzir custo em **[app]**, com limites e invalidação.

21. **Multi-tenant RAG**  
   Como implementar RAG multi-tenant com isolamento de dados? Liste riscos e controles.

22. **RAG para SQL/BI**  
   Como adaptar RAG para responder perguntas sobre **tabelas, métricas e dashboards** sem inventar? Proponha o pipeline.

---

## C) Agentes e automação (23–32)

23. **Agente “planejar → executar → revisar”**  
   Crie um agente para **[tarefa]** com 3 etapas: planner, executor, reviewer. Defina entradas, saídas e critérios de aprovação.

24. **Ferramentas do agente**  
   Liste as ferramentas necessárias (SQL, API, arquivos, email, Slack). Para cada uma, defina: input schema, output schema, erros e retries.

25. **Playbook de incidentes**  
   Desenhe um agente que monitora **[KPI]** e gera um incident report com: impacto, hipótese, evidências e próximos passos.

26. **Agente para relatório**  
   Gere um fluxo de agente que transforma dataset em relatório executivo: KPIs, gráficos, insights, riscos e recomendações.

27. **Agente “BI copilot”**  
   Projete um copilot para Power BI: explicar medidas DAX, sugerir visuais, documentar páginas e checar consistência de métricas.

28. **Agente para backlog**  
   Pegue esta lista de tarefas **[colar]** e transforme em backlog priorizado (RICE/ICE) com épicos, histórias e critérios de aceite.

29. **Agente para documentação**  
   Transforme este repositório **[descrição/arquivos]** em documentação: “como rodar”, “como contribuir”, FAQ e troubleshooting.

30. **Autonomia controlada**  
   Quais guardrails usar para permitir autonomia do agente sem risco? (limites de ferramentas, scopes, confirmação, dry‑run)

31. **Workflow de automação**  
   Modele um workflow em n8n/Make para **[processo]** e descreva módulos, variáveis e payloads JSON.

32. **SOP (procedimento padrão)**  
   Crie um SOP para **[tarefa repetitiva]** com passos, validações, tempo esperado, e “se der errado faça X”.

---

## D) NL → Python / SQL / Código (33–40)

33. **NL → Python com padrão de qualidade**  
   Gere um script Python para **[tarefa]** usando pandas + matplotlib. Regras: funções pequenas, docstrings, logs, e salvar outputs em `out/`.

34. **Explique o código**  
   Explique este código como se eu fosse analista iniciante. Depois explique como se eu fosse engenheiro senior. (cole o código)

35. **Refatoração segura**  
   Refatore este código para ficar mais legível e testável. Não mude a lógica. Gere também testes com pytest.

36. **SQL otimizado**  
   Escreva uma query SQL para **[objetivo]** e depois proponha otimizações (índices, particionamento, filtros, custo).

37. **Validação contra alucinação**  
   Dado esse schema **[tabelas/colunas]**, gere SQL **apenas com colunas existentes**. Se faltar coluna, peça ajuste.

38. **DAX assistant**  
   Crie a medida DAX para **[métrica]** e explique cada parte. Dê também alternativa em Power Query/M se fizer sentido.

39. **Notebook “didático”**  
   Monte um notebook passo a passo para **[tarefa]** com seções: objetivo, dados, limpeza, análise, conclusão.

40. **Code review**  
   Faça code review deste PR (cole o diff) focando: legibilidade, performance, edge cases, segurança e padrões.

---

## E) Evals, qualidade e confiabilidade (41–46)

41. **Crie um dataset de avaliação**  
   Gere um dataset de avaliação para **[app]** com 50 perguntas e respostas esperadas, incluindo casos ambíguos e adversariais.

42. **Rubrica de avaliação**  
   Defina uma rubrica (0–5) para avaliar: corretude, completude, citações, segurança e utilidade. Dê exemplos por nota.

43. **Teste de regressão**  
   Proponha testes de regressão para prompts/modelos: o que comparar, thresholds e como versionar resultados.

44. **A/B de prompts**  
   Crie 3 variações de prompt para **[tarefa]** e um plano de experimento para escolher o melhor.

45. **Observabilidade**  
   Quais logs e métricas registrar em uma app com LLM? Inclua: custo por request, tokens, latência, taxa de fallback e erro.

46. **Red team**  
   Faça um red teaming da minha aplicação: sugira 20 ataques/prompt injections e como mitigar.

---

## F) Ferramentas e produtividade (47–50)

47. **Escolha a ferramenta certa**  
   Para este cenário **[descreva]**, recomende a melhor ferramenta (ChatGPT/Claude/Gemini/NotebookLM/Ollama/etc.) e diga por quê, com alternativa.

48. **Setup VS Code + LLM**  
   Me dê um setup completo no VS Code para **[Python/SQL]** com extensões, atalhos, snippets e rotina diária.

49. **Prompt library pessoal**  
   Crie uma biblioteca de prompts para meu dia a dia como **[função]**, organizada por: análise, documentação, automação, revisão e comunicação.

50. **Transformar conhecimento em conteúdo**  
   Pegue este tema **[tópico]** e gere: 1 post LinkedIn, 1 roteiro curto YouTube e 1 checklist salvável, sem soar artificial.

---

## Prompt “base” para colar antes de qualquer um (recomendado)

Use este cabeçalho sempre que quiser respostas mais consistentes:

- Contexto: **[onde isso será usado]**
- Objetivo: **[resultado esperado]**
- Restrições: **[tempo, custo, segurança, formato]**
- Formato de saída: **[markdown/tabela/json]**
- Critérios de qualidade: **[como validar]**
- Se faltar info: **pergunte antes de inferir**
