#!/usr/bin/env python3
"""Update data.json com metricas da Clint API.

Roda dentro do GitHub Action a cada 30 min.
Token vem da variavel CLINT_TOKEN (secret do repo).
"""
import os
import sys
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

CLINT_BASE = "https://api.clint.digital/v1"
TAG_QW = "afac6c75-4afe-48d5-a04e-4010ce63a388"
ORIGIN_WORKSHOP = "e33ad58f-ec59-43cb-895c-c39a1a149041"
STAGES = {
    1: "658e2b10-50cc-4ef0-8be6-5d2433e6a6d8",  # Lista Bruta
    2: "0419b875-c1cf-40cb-b803-4cebc54989f8",  # Em Abordagem
    3: "e74ff4d0-5ab5-4b58-8a16-39677a6ea534",  # Interessado
    4: "2b3cbbce-a70f-4e0e-a993-fec8c22fc0aa",  # Inscrito
    5: "0882e4b4-ad7f-4512-9633-0ece07c38a3f",  # Confirmando
    6: "fbdffc7f-4f90-40b5-ad9e-e4c6d6c5bc82",  # Compareceu
    7: "c181cd7c-973e-49d9-9a4d-45267f281a24",  # Em Venda Pos
    8: "cc7441f2-3aa3-44ed-8b6e-165b2e044296",  # Encerrado
}


def clint_count(path, token):
    url = f"{CLINT_BASE}{path}"
    req = Request(url, headers={"api-token": token, "Accept": "application/json"})
    try:
        with urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
            return int(data.get("totalCount", 0))
    except HTTPError as e:
        print(f"[clint] {path} -> {e.code}: {e.read()[:200].decode(errors='ignore')}",
              file=sys.stderr)
        return 0
    except Exception as e:
        print(f"[clint] {path} -> ERR: {e}", file=sys.stderr)
        return 0


def main():
    token = os.environ.get("CLINT_TOKEN", "").strip()
    if not token:
        print("ERRO: CLINT_TOKEN nao definido", file=sys.stderr)
        sys.exit(1)

    stages = {}
    for i, sid in STAGES.items():
        stages[i] = clint_count(f"/deals?stage_id={sid}&limit=1", token)
        print(f"  stage {i}: {stages[i]}")

    total_qualif = clint_count(f"/contacts?tag_ids={TAG_QW}&limit=1", token)
    print(f"  qualificados: {total_qualif}")

    out = {
        "stages": stages,
        "total_qualificados": total_qualif,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
        "source": "github-action",
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nOK -> data.json atualizado ({sum(stages.values())} deals total)")


if __name__ == "__main__":
    main()
