"""Run Athena-BH workflows using the WorkflowRunner.

This script loads a project configuration from the tests directory,
initializes all modules defined in athena.modules, and then executes
a named workflow using the WorkflowRunner. It serves as a simple
entry point for running predefined workflows such as 'discovery'.
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

# Import the workflow runner
from workflow_runner import WorkflowRunner


def load_project_config(path: Path) -> dict:
    """Load a YAML project configuration into a Python dictionary."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def initialize_modules() -> dict:
    """Instantiate each module defined in the athena.modules file.

    Returns a dictionary of module instances keyed by their class name.
    Optional modules are instantiated only if their 'enabled' attribute is True.
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
        "ar_scan_module": ARScanModule() if getattr(ARScanModule, "enabled", False) else None,
        "sustainability_scoring": SustainabilityScoring() if getattr(SustainabilityScoring, "enabled", False) else None,
    }


def main(workflow_name: str = "discovery") -> None:
    """Main function executed when running this script as a program.

    Args:
        workflow_name: Name of the workflow to execute, default is 'discovery'.
    """
    # Determine the path to the sample project configuration relative to this file
    config_path = Path(__file__).resolve().parents[1] / "tests" / "sample_project.yaml"
    project = load_project_config(config_path)

    # Initialize modules according to the definitions
    modules = initialize_modules()

    # Print a summary of the loaded project for the user
    print(f"Loaded project: {project.get('project_name')}")
    print(f"Jurisdiction: {project.get('jurisdiction')}")
    print(f"Scope: {project.get('scope')}")

    # Create a WorkflowRunner and execute the requested workflow
    runner = WorkflowRunner(modules=modules)
    print(f"\nRunning '{workflow_name}' workflow…")
    runner.run_workflow(workflow_name)


if __name__ == "__main__":
    main()
