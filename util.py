import json
import os
import hashlib

def salvar_sistema(sistema, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(sistema, f, ensure_ascii=False, indent=4)

def carregar_sistema(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"torneio": {}, "torneio_ativo": None, "confronto_ativo": None}
