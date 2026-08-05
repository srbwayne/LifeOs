from pytest_archon import archrule

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
