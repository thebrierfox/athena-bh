"""Main entry point for the Athena-BH assistant.

This script demonstrates how to load a sample project configuration and
initialize the various modules defined in the athena.modules package. It
is intended as a placeholder orchestrator until full workflow logic is
implemented.
"""

from pathlib import Path
import yaml

# Import module classes from the athena package
from athena.modules import (
    CodeIntelEngine,
    ComplianceQueryLayer,
    JurisdictionResolver,
    DesignGuardrails,
    PermitPackGenerator,
    LivingChecklists,
    ResourceSourcing,
    ProjectManagement,
    VirtualDesign,
    ResilienceLayer,
    SecretsManager,
    LoggingLayer,
    HistoricRegistryCheck,
    LocalAmendmentsOverrides,
    ARScanModule,
    SustainabilityScoring,
)


def load_project_config(path: Path) -> dict:
    """Load a YAML project configuration into a Python dictionary."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def initialize_modules() -> dict:
    """Instantiate each module defined in the athena.modules file.

    Returns a dictionary of module instances keyed by their class name.
    """
    return {
        "code_intel_engine": CodeIntelEngine(),
        "compliance_query_layer": ComplianceQueryLayer(),
        "jurisdiction_resolver": JurisdictionResolver(),
        "design_guardrails": DesignGuardrails(),
        "permit_pack_generator": PermitPackGenerator(),
        "living_checklists": LivingChecklists(),
        "resource_sourcing": ResourceSourcing(),
        "project_management": ProjectManagement(),
        "virtual_design": VirtualDesign(),
        "resilience_layer": ResilienceLayer(),
        "secrets_manager": SecretsManager(),
        "logging_layer": LoggingLayer(),
        "historic_registry_check": HistoricRegistryCheck(),
        "local_amendments_overrides": LocalAmendmentsOverrides(),
        # Optional modules: leave disabled by default
        "ar_scan_module": ARScanModule() if ARScanModule.enabled else None,
        "sustainability_scoring": SustainabilityScoring() if SustainabilityScoring.enabled else None,
    }


def main() -> None:
    """Main function executed when running this script as a program."""
    # Load the sample project configuration (relative to project root)
    config_path = Path(__file__).resolve().parents[1] / "tests" / "sample_project.yaml"
    project = load_project_config(config_path)

    # Initialize modules (placeholder implementations)
    modules = initialize_modules()

    # Output summary to console for demonstration
    print(f"Loaded project: {project.get('project_name')}")
    print(f"Jurisdiction: {project.get('jurisdiction')}")
    print(f"Scope: {project.get('scope')}")
    print("\nInitialized modules:")
    for name, instance in modules.items():
        status = "enabled" if instance is not None else "disabled"
        print(f"- {name}: {status}")

    print("\nTODO: Implement workflow orchestration per athena_meta.json")


if __name__ == "__main__":
    main()
