import json
import os
import hashlib

def salvar_sistema(sistema, ARQUIVO_JSON):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(sistema, f, ensure_ascii=False, indent=2)

def carregar_sistema(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"torneio": {}, "torneio_ativo": None, "confronto_ativo": None}

def salvar_todos(sistema, arquivo_staff):
    salvar_sistema(sistema, arquivo_staff)
    salvar_sistema(sistema, "sistema_salvo.json")