# Athena-BH

Athena‑BH is an AI-driven assistant for BuildHers interior-renovation projects. It unifies design visualization, project orchestration and jurisdiction-specific code-compliance management.

## Architecture Overview

The system is composed of modular services defined in `config/athena_meta.json`. Each module implements a particular capability, for example:
- **code_intel_engine** – fetches and caches up-to-date code sections via the ICC Code Connect API and exposes helper functions for validating code compliance.
- **compliance_query_layer** – provides natural-language queries to code sections with UpCodes Copilot fallback.
- **jurisdiction_resolver** – detects locality, adopted code editions and amendments.
- **design_guardrails** – performs real-time geometric & ADA clearance checks inside BIM/CAD.
- **permit_pack_generator** – builds code sheets, narratives and stamped PDFs.
- **living_checklists** – manages phase-gated QA/QC tasks with pass/fail toggles and JSON log output.

A full list of modules and workflows can be found in the JSON configuration.

## Getting Started

1. **Clone the repository** and set up a Python virtual environment.
2. Install dependencies (this project uses Python; requirements will be added once modules are implemented).
3. Create a `.env` file or configure a secrets manager with the values from `config/athena_meta.json` under `secrets_template` (e.g. `ICC_CODE_CONNECT_KEY`, `UPCODES_API_TOKEN`, `SPACELY_API_URL`).
4. Run unit tests with `pytest` to ensure everything is wired correctly.

```bash
git clone https://github.com/thebrierfox/athena-bh.git
cd athena-bh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Project Structure

```
config/
    athena_meta.json     # Master meta-directive (version 1.2.0)
src/athena/
    __init__.py          # Package initialization
    modules.py           # Stub classes for each module
tests/
    sample_project.yaml  # Sample data for nightly testing
```

## Contribution & Testing

- Contributions should follow the design principles listed in the meta directive (Client‑Centric Clarity, Compliance-by-Default, Open-Source First, Modularity & Scalability, Transparent Collaboration).
- Add unit tests for new functionality in `tests/`.
- Nightly test suites are defined in `tests/sample_project.yaml` and are executed via GitHub Actions (CI configuration to be added).

## License

To be determined.
