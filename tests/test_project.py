"""Tests for the Athena-BH project configuration and module definitions."""

from pathlib import Path
import json
import yaml

# Import all modules to ensure they can be referenced
import athena.modules as amod


def test_load_sample_config() -> None:
    """Ensure the sample project YAML loads correctly."""
    config_path = Path(__file__).resolve().parent / "sample_project.yaml"
    data = yaml.safe_load(config_path.read_text())
    assert data["project_name"] == "Sample Renovation"
    assert "jurisdiction" in data
    assert "codes" in data


def test_modules_defined_in_meta_exist() -> None:
    """Ensure each module listed in the meta directive has a corresponding class in athena.modules."""
    meta_path = Path(__file__).resolve().parents[1] / "config" / "athena_meta.json"
    meta = json.loads(meta_path.read_text())
    module_names = meta["modules"].keys()

    missing = []
    for module_name in module_names:
        # Convert snake_case module name to PascalCase class name
        class_name = "".join(part.title() for part in module_name.split("_"))
        if not hasattr(amod, class_name):
            missing.append((module_name, class_name))

    assert not missing, f"Missing module classes: {missing}"
