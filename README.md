# Workshop UpSummit Goiânia 06/05/2026 — Playbook + Dashboard

Site interno para o time comercial (Barbara) e CS (Antonio) acompanharem o playbook e métricas do funil em tempo (semi)real.

## Estrutura

- **`index.html`** — Playbook completo (recados, cadência, templates Meta, objeções, dashboard)
- **`data.json`** — Métricas atuais da Clint (atualizado a cada 30min via GitHub Action)
- **`update_dashboard.py`** — Script Python que consulta Clint e regenera `data.json`
- **`.github/workflows/update_dashboard.yml`** — Cron 30min que roda o script
- **`.github/workflows/pages.yml`** — Deploy do site no GitHub Pages

## Acesso

Site protegido por gate de senha JS. Senha deve ser combinada com Rafael.

## Secrets necessárias

- `CLINT_TOKEN` — token da Clint API (mesmo do Mac no Keychain). Cadastrar em **Settings → Secrets and variables → Actions → New repository secret**.

## Atualização manual

Action também aceita `workflow_dispatch` — pode ser disparada manualmente em **Actions → Update Dashboard → Run workflow**.
