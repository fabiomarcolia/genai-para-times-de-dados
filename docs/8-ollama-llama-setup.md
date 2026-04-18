# 06 — Setup de Llama local com Ollama (Windows / macOS / Linux)

Este guia mostra como **instalar o Ollama**, baixar um **modelo Llama** e configurar variáveis de ambiente para usar o **LLM local** nas demos do repositório.

---

## Pré-requisitos

- Acesso ao terminal (PowerShell no Windows, Terminal no macOS/Linux)
- Python instalado (para rodar as demos)
- Espaço em disco (modelos podem ter alguns GB)

---

## 1) Instalar o Ollama

### Windows
1- Baixe e instale o Ollama para Windows (instalador oficial).  
2- Abra o app do Ollama (ele mantém o serviço rodando).

### macOS
1- Instale o Ollama (app/DMG oficial).  
2- Abra o app do Ollama.

### Linux
Instalação típica via script oficial (o instalador configura o serviço).

> Após instalar, feche e abra o terminal novamente.

### Verificar instalação
```bash
ollama --version
```

---

## 2) Baixar e rodar um modelo Llama

### Modelos recomendados (comece por 1)
- `llama3.1:8b` — equilíbrio ótimo para uso geral
- `llama3:8b` — alternativa semelhante
- `qwen2.5:7b` — forte para tarefas de código (opcional)

Baixar o modelo:
```bash
ollama pull llama3.1:8b
```

Rodar no terminal:
```bash
ollama run llama3.1:8b
```

Teste rápido (dentro do prompt do Ollama):
> Responda em pt-br: o que é RAG em 2 linhas.

Para sair do modo interativo: `Ctrl+C`

---

## 3) Confirmar a API local do Ollama

Por padrão, o Ollama expõe uma API em:
- `http://localhost:11434`

Listar modelos disponíveis:
```bash
curl http://localhost:11434/api/tags
```

Se retornar um JSON com modelos, está OK.

---

## 4) Configurar o repositório para usar Ollama

A ideia é padronizar 3 variáveis:

- `LLM_PROVIDER=ollama`
- `OLLAMA_BASE_URL=http://localhost:11434`
- `OLLAMA_MODEL=llama3.1:8b`

### macOS / Linux
```bash
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.1:8b
```

### Windows (PowerShell)
Para a sessão atual:
```powershell
$env:LLM_PROVIDER="ollama"
$env:OLLAMA_BASE_URL="http://localhost:11434"
$env:OLLAMA_MODEL="llama3.1:8b"
```

Opcional: persistir no sistema (vale para novos terminais):
```powershell
setx LLM_PROVIDER "ollama"
setx OLLAMA_BASE_URL "http://localhost:11434"
setx OLLAMA_MODEL "llama3.1:8b"
```

> Se usar `setx`, feche e abra o terminal depois.

---

## 5) Rodar demos usando o Llama local

### Demo 05 — Agente de relatório → PDF → Slack/Email
Exemplo:
```bash
python demos/05-agent-relatorio/pipeline.py   --input demos/05-agent-relatorio/sample_data.csv   --out out
```

### Demo 06 — Linguagem natural → código Python
Exemplo:
```bash
python demos/06-nl-to-python/generate.py   --task demos/06-nl-to-python/examples/task.md   --data demos/06-nl-to-python/examples/input.csv   --out out
```

---

## 6) Troubleshooting (problemas comuns)

### 1) `ollama: command not found`
- Reinicie o terminal
- Reinstale o Ollama e confirme que ele está no PATH

### 2) `connection refused` em `localhost:11434`
- O serviço do Ollama não está rodando
- No Windows/macOS, abra o app do Ollama
- Verifique com:
```bash
curl http://localhost:11434/api/tags
```

### 3) Muito lento
- Use um modelo menor
- Evite rodar outras coisas pesadas
- Se tiver GPU compatível, a experiência melhora bastante

### 4) Falta de memória (RAM)
- Modelos 8B podem exigir bastante RAM
- Feche apps pesados e tente um modelo menor

### 5) Resposta “inventando” (alucinação)
- Isso pode acontecer em qualquer LLM
- Mitigue com:
  - RAG com citações
  - prompts restritivos (“use apenas contexto”)
  - validações (sanity checks/testes)

---

## 7) Boas práticas (produção)

- **Logs**: registre prompt (com redactions), latência, tokens e custo (quando aplicável)
- **Fallback**: tenha modo “offline” (templates/regras) se o LLM falhar
- **Evals**: mantenha um conjunto de casos de teste e rode regressão quando mudar modelo/prompt
- **Segurança**: nunca passe segredos no prompt (tokens, senhas, chaves)

---

## Referência rápida

- Modelo atual sugerido: `llama3.1:8b`
- Base URL padrão: `http://localhost:11434`
- Comando para ver modelos: `ollama list`
