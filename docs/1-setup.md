# Setup (local)
## Opção A: Python + venv (recomendado)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Opção B: Ollama (LLM local, sem custo por token)
1- Instale o Ollama
2- Baixe um modelo
```bash
ollama pull llama3.1
```

3- Configure
```bash
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.1
```

## Boas práticas
- Nunca commite `.env`
- Prefira datasets sintéticos em `datasets/`
- Mantenha limites (`MAX_TOKENS`, `TOP_K`) mesmo local
