<div align="center">

<img src="https://raw.githubusercontent.com/TM-INTELLIGENCE/.github/main/assets/oktoneo.svg" alt="Oktoneo" width="320" />

# TM INTELLIGENCE · Oktoneo

**Logiciel de prise de commande terrain, logistique et intelligence commerciale pour la distribution B2B.**

[Site](https://oktoneo.fr) · [Organisation GitHub](https://github.com/TM-INTELLIGENCE)

</div>

---

## À propos

**Oktoneo** est la suite logicielle de **TM INTELLIGENCE** pour la distribution B2B :
prise de commande terrain (SFA), préparation entrepôt, fret, expédition e-commerce et station chargeur.

Les dépôts listés ci-dessous sont le catalogue produit. La plupart sont privés — les membres de l’org y ont accès directement.

## Projets

<!-- BEGIN:PROJECTS -->
| Projet | Dépôt | Description |
|--------|-------|-------------|
| **[Oktoneo SFA](https://github.com/TM-INTELLIGENCE/TMINTELLIGENCE-OKTONEO)**<br/><sub>[site](https://oktoneo.fr)</sub> | [`TMINTELLIGENCE-OKTONEO`](https://github.com/TM-INTELLIGENCE/TMINTELLIGENCE-OKTONEO) | Prise de commande terrain, simulation tarifaire, catalogue, ML rupture/churn — monorepo produit (BlitzPAL). |
| **[Oktoneo Pick](https://github.com/TM-INTELLIGENCE/oktoneo-pick)** | [`oktoneo-pick`](https://github.com/TM-INTELLIGENCE/oktoneo-pick) | Préparation entrepôt / BL / Teliae — PWA + API FastAPI. |
| **[Oktoneo Fret](https://github.com/TM-INTELLIGENCE/oktoneo-fret)**<br/><sub>[site](https://fret.tmintelligence.fr)</sub> | [`oktoneo-fret`](https://github.com/TM-INTELLIGENCE/oktoneo-fret) | TMS fret (cotation LTL/FTL) — UI + API autonomes. |
| **[Oktoneo Ship](https://github.com/TM-INTELLIGENCE/oktoneo-ship)** | [`oktoneo-ship`](https://github.com/TM-INTELLIGENCE/oktoneo-ship) | Génération d’étiquettes e-commerce (rempl. ShippyPro) + pipeline facture_ecommerce Softwell. |
| **[Oktoneo Station](https://github.com/TM-INTELLIGENCE/oktoneo-station)**<br/><sub>[site](https://station.tmintelligence.fr)</sub> | [`oktoneo-station`](https://github.com/TM-INTELLIGENCE/oktoneo-station) | Station chargeur (réplicat TELIAE) — runtime lab. |
| **[Oktoneo Karrio](https://github.com/TM-INTELLIGENCE/oktoneo-karrio)** | [`oktoneo-karrio`](https://github.com/TM-INTELLIGENCE/oktoneo-karrio) | Stack Karrio (plugins transporteurs + compose lab). |
<!-- END:PROJECTS -->

## Comment rester à jour

Le fichier `profile/README.md` est **généré**. Source de vérité : [`catalog/repos.yml`](../catalog/repos.yml).

| Quand | Quoi |
|-------|------|
| Nouveau dépôt / rename / blurb | Éditer `catalog/repos.yml`, pousser — l’Action régénère le README |
| Chaque lundi | Action `sync-profile` (cron) + sync des descriptions GitHub |
| Manuel | `python3 scripts/generate_profile_readme.py` puis commit |

Voir le [README du dépôt](../README.md) pour le détail.

## Contact

→ [oktoneo.fr](https://oktoneo.fr)
