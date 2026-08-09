import ast
from pathlib import Path

from pytest_archon import archrule

CAPABILITIES = {"auth", "character", "read"}


def _imported_modules(file_path: Path) -> set[str]:
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
    return modules


def _cross_capability_imports(layer: str | None = None) -> list[str]:
    violations: list[str] = []
    for source_capability in sorted(CAPABILITIES):
        source_root = Path("app") / source_capability
        if layer is not None:
            source_root /= layer
        for file_path in source_root.rglob("*.py"):
            for module in _imported_modules(file_path):
                parts = module.split(".")
                if len(parts) < 3 or parts[0] != "app":
                    continue
                target_capability = parts[1]
                if target_capability in CAPABILITIES and target_capability != source_capability:
                    violations.append(f"{file_path}: {module}")
    return violations


def test_domain_should_not_depend_on_other_layers():
    (
        archrule("Check Domain Dependencies")
        .match("app.auth.domain*")
        .should_not_import(
            "app.auth.application*",
            "app.auth.infrastructure*",
            "app.auth.presentation*",
        )
        .check("app")
    )


def test_application_should_not_depend_on_infra_or_presentation():
    (
        archrule("Check Application Dependencies")
        .match("app.auth.application*")
        .should_not_import(
            "app.auth.infrastructure*",
            "app.auth.presentation*",
        )
        .check("app")
    )


def test_character_domain_should_not_depend_on_outer_layers():
    (
        archrule("Check Character Domain Dependencies")
        .match("app.character.domain*")
        .should_not_import(
            "app.character.application*",
            "app.character.infrastructure*",
            "app.character.presentation*",
        )
        .check("app")
    )


def test_character_application_should_not_depend_on_infrastructure_or_presentation():
    (
        archrule("Check Character Application Dependencies")
        .match("app.character.application*")
        .should_not_import(
            "app.character.infrastructure*",
            "app.character.presentation*",
        )
        .check("app")
    )


def test_read_domain_should_not_depend_on_outer_layers():
    (
        archrule("Check READ Domain Dependencies")
        .match("app.read.domain*")
        .should_not_import(
            "app.read.application*",
            "app.read.infrastructure*",
            "app.read.presentation*",
        )
        .check("app")
    )


def test_read_application_should_not_depend_on_infrastructure_or_presentation():
    (
        archrule("Check READ Application Dependencies")
        .match("app.read.application*")
        .should_not_import(
            "app.read.infrastructure*",
            "app.read.presentation*",
        )
        .check("app")
    )


def test_read_infrastructure_should_not_depend_on_presentation():
    (
        archrule("Check READ Infrastructure Dependencies")
        .match("app.read.infrastructure*")
        .should_not_import("app.read.presentation*")
        .check("app")
    )


def test_capability_domains_do_not_import_other_capabilities() -> None:
    assert _cross_capability_imports("domain") == []


def test_capability_applications_do_not_import_other_capability_internals() -> None:
    assert _cross_capability_imports("application") == []


def test_capability_infrastructure_does_not_import_other_capability_internals() -> None:
    assert _cross_capability_imports("infrastructure") == []


def test_character_does_not_import_auth_internals() -> None:
    violations = [
        violation
        for violation in _cross_capability_imports()
        if violation.startswith("app\\character") or violation.startswith("app/character")
    ]
    assert violations == []


def test_auth_does_not_import_character_internals() -> None:
    violations = [
        violation
        for violation in _cross_capability_imports()
        if violation.startswith("app\\auth") or violation.startswith("app/auth")
    ]
    assert violations == []
