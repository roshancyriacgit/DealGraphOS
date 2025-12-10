# DealGraphOS (Open Source Backend Preview)

DealGraphOS is a modular, rule-based backend for analysing corporate transactions.
It converts structured deal data into regulatory triggers, checklist items, and risk flags.

This repository contains an open-source **backend preview** of DealGraphOS focusing on:

- A FastAPI application layer
- SQLModel-based data structures for deals and related entities
- YAML-driven rulepacks for jurisdiction-specific logic (India included as an example)
- A rules engine that maps deal facts to obligations, checks, and risks

## Structure

```text
backend/
    app/
        main.py
        api/
        core/
        models/
        rules/
    requirements.txt
```

## Running the backend (development)

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` in a browser to explore the API.

## Rulepacks

Under `backend/app/rules/jurisdictions/india/` you will find example rulepacks
that encode select Indian regulatory checks (e.g. competition, FDI, listed-company rules)
in YAML format. These files are illustrative and can be extended, replaced, or adapted
for other jurisdictions.

## License

This backend preview is released under the AGPL-3.0 license. See `LICENSE` for details.
