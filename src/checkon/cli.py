import datetime
import json
import pathlib
import sys

import attr
import click
import hyperlink
import tabulate
import toml

import checkon.results

from . import app


def run_cli(dependents_lists, **kw):
    dependents = [d for ds in dependents_lists for d in ds]

    print(app.run_many(dependents=dependents, **kw))


def compare_cli(dependents_lists, output_format, log_file, **kw):

    dependents = [d for ds in dependents_lists for d in ds]
    if str(log_file) == "-":
        log_file = "/dev/stdout"
    pathlib.Path(log_file).parent.mkdir(exist_ok=True, parents=True)

    with open(log_file, "w") as log_file:
        records = checkon.app.test(dependents=dependents, log_file=log_file, **kw)

    if output_format == "json":
        print(json.dumps(records))
    elif output_format == "table":
        print(tabulate.tabulate(records, headers="keys"))

    else:
        raise ValueError(output_format)

    if records:
        sys.exit(1)


def read_from_file(file):
    dependents_ = toml.load(file)["dependents"]
    return [app.Dependent(d["repository"], d["toxenv_regex"]) for d in dependents_]


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
        callback=lambda dependents: [app.Dependent(repo, ".*") for repo in dependents],
        help="List dependent project urls on the command line.",
    ),
]


test = click.Group(
    "test",
    commands={c.name: c for c in dependents},
    params=[
        click.Option(["--upstream-new"], help="Depdendency version(s).", multiple=True),
        click.Option(
            ["--upstream-pull-requests"],
            type=hyperlink.URL.from_text,
            help="Inject each of the GitHub pull requests against the `upstream-base` version.",
        ),
        click.Option(["--upstream-base"], help="Baseline dependency version."),
        click.Option(
            ["--output-format"],
            type=click.Choice(["json", "table"]),
            default="table",
            help="Output format",
        ),
        click.Option(
            ["--log-file"],
            type=click.Path(allow_dash=True),
            default=".checkon/logs/" + datetime.datetime.utcnow().isoformat() + ".log",
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
