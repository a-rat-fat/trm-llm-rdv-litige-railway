# Déploiement sur Railway — TRM LLM RDV/Litiges

## Prérequis
- Compte Railway (https://railway.app)
- Dépôt Git avec ce projet
- (Optionnel) Railway CLI : `npm i -g @railway/cli`

## Déploiement (interface web)
1. **New → Deploy from GitHub** et sélectionne ton repo.
2. Railway détecte le **Dockerfile** et build l'image.
3. Variables à vérifier : `PORT=8080`, `DATA_PATH=/app/data`.
4. Clique **Deploy**. Ouvre l'URL publique.

## Déploiement (CLI)
```bash
git clone <ton-repo.git>
cd trm-llm-rdv-litige
railway login
railway init
railway up
```

Endpoints :
- `GET /api/health`
- `POST /api/rdv/suggest_slots`
- `POST /api/litige/draft_email`