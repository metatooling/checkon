import pathlib

import attr
import click
import tabulate
import toml

import checkon.results

from . import app


def run_cli(dependents_lists, hide_passed, **kw):
    dependents = [d for ds in dependents_lists for d in ds]

    print(app.run_many(dependents=dependents, **kw))


def compare_cli(dependents_lists, hide_passed, output_format, **kw):
    dependents = [d for ds in dependents_lists for d in ds]
    records = checkon.app.compare(dependents=dependents, **kw)
    if hide_passed:
        records = [r for r in records if r["text"] is not None]

    import json

    if output_format == "json":
        print(json.dumps(records))
    elif output_format == "table":
        print(tabulate.tabulate(records, headers="keys"))

    else:
        raise ValueError(output_format)


def read_from_file(file):
    dependents_ = toml.load(file)["dependents"]
    return [app.Dependent(d["repository"], d["toxenv_glob"]) for d in dependents_]


dependents = [
    click.Command(
        "dependents-from-librariesio",
        params=[
            click.Argument(["pypi-name"]),
            click.Option(
                ["--api-key"],
                required=True,
                envvar="CHECKON_LIBRARIESIO_API_KEY",
                help="libraries.io API key",
            ),
            click.Option(
                ["--limit"],
                type=int,
                help="Maximum number of dependents to find.",
                default=5,
                show_default=True,
            ),
        ],
        callback=app.get_dependents,
        help="Get dependent projects on PyPI, via https://libraries.io API",
    ),
    click.Command(
        "dependents-from-file",
        params=[click.Argument(["file"], type=click.File())],
        help="List dependent project urls in a toml file.",
        callback=read_from_file,
    ),
    click.Command(
        "dependents",
        params=[click.Argument(["dependents"], nargs=-1, required=True)],
        callback=lambda dependents: [app.Dependent(repo, "*") for repo in dependents],
        help="List dependent project urls on the command line.",
    ),
]


hide_passed = click.Option(
    ["--hide-passed"], is_flag=True, help="Whether to hide tests that passed."
)


test = click.Group(
    "test",
    commands={c.name: c for c in dependents},
    params=[
        click.Option(["--inject"], help="Depdendency version(s).", multiple=True),
        hide_passed,
        click.Option(
            ["--output-format"],
            type=click.Choice(["json", "table"]),
            default="table",
            help="Output format",
        ),
    ],
    result_callback=compare_cli,
    chain=True,
    help="Compare multiple versions of a depdendency on their depdendents tests.",
)


def make_config(dependents):

    return toml.dumps({"dependents": [attr.asdict(d) for d in dependents]})


make_config_cli = click.Group(
    "make-config",
    commands={c.name: c for c in dependents},
    result_callback=lambda ds: print(
        make_config(ds)
    ),  # lambda **kw: print(make_config(**kw)),
    help="Make toml configuration of dependent libraries.",
)
cli = click.Group(
    "run",
    commands={"make-config": make_config_cli, "test": test},
    help="Run tests of dependent packages using different versions of a depdendency library.",
)
