# TM-INTELLIGENCE / `.github`

Fichiers d’organisation GitHub :

- **`profile/README.md`** — page de présentation de l’org ([docs](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile))
- **`catalog/repos.yml`** — source de vérité des projets Oktoneo
- **`assets/`** — logo Oktoneo (SVG)
- **`scripts/`** — génération README + sync descriptions/topics

## Mettre à jour le catalogue

1. Éditer [`catalog/repos.yml`](catalog/repos.yml) (nouveau repo, blurb, homepage, topics).
2. En local : `python3 scripts/generate_profile_readme.py`
3. Commit / push — ou laisser l’Action `sync-profile` régénérer.

Ne pas éditer à la main la section projets de `profile/README.md` (écrasée à chaque génération).

## CI

Workflow [`.github/workflows/sync-profile.yml`](.github/workflows/sync-profile.yml) :

- push sur le catalogue / template
- cron lundi 07:15 UTC
- `workflow_dispatch`

Il régénère le README et tente de synchroniser descriptions + topics GitHub.

## Check local

```bash
pip install pyyaml
python3 scripts/generate_profile_readme.py --check
```

Plane : **OPS-112**
