"""
Workflow runner for Athena-BH.
This module reads the meta directive configuration and orchestrates workflows by
initializing modules and invoking methods in the order specified in the JSON.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

# Import module classes from athena.modules
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

class WorkflowRunner:
    def __init__(self, meta_path: str = "config/athena_meta.json") -> None:
        """Initialize the workflow runner by loading the meta directive and instantiating modules."""
        self.meta = self.load_meta(meta_path)
        self.modules = self.initialize_modules()

    def load_meta(self, path: str) -> Dict[str, Any]:
        """Load the meta directive JSON from the given path."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Meta directive file not found at {p}")
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)

    def initialize_modules(self) -> Dict[str, Any]:
        """Instantiate each module defined in the meta directive.

        Disabled optional modules are set to None.
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
            # Optional modules: check for enabled flag in the meta directive
            "ar_scan_module": ARScanModule() if self.meta.get("modules", {}).get("ar_scan_module", {}).get("enabled", False) else None,
            "sustainability_scoring": SustainabilityScoring() if self.meta.get("modules", {}).get("sustainability_scoring", {}).get("enabled", False) else None,
        }

    def run_workflow(self, workflow_name: str) -> None:
        """Run the specified workflow by iterating through its steps and invoking module methods."""
        workflows = self.meta.get("workflows", {})
        workflow_steps: List[Dict[str, Any]] = workflows.get(workflow_name)
        if not workflow_steps:
            print(f"Workflow '{workflow_name}' is not defined in the meta directive.")
            return

        for step in workflow_steps:
            module_name = step.get("module")
            method_name = step.get("method")
            params = step.get("params", {})

            module_instance = self.modules.get(module_name)
            if module_instance is None:
                print(f"[WARN] Module '{module_name}' is not available or disabled.")
                continue

            method = getattr(module_instance, method_name, None)
            if not callable(method):
                print(f"[WARN] Method '{method_name}' not found in module '{module_name}'.")
                continue

            try:
                result = method(**params)
                if result is not None:
                    print(f"[INFO] {module_name}.{method_name} returned: {result}")
            except Exception as exc:
                print(f"[ERROR] Error executing {module_name}.{method_name}: {exc}")

    def list_workflows(self) -> List[str]:
        """Return a list of available workflow names."""
        return list(self.meta.get("workflows", {}).keys())

# Allow running via CLI for quick testing
if __name__ == "__main__":
    runner = WorkflowRunner()
    import sys
    workflow = sys.argv[1] if len(sys.argv) > 1 else "discovery"
    runner.run_workflow(workflow)
