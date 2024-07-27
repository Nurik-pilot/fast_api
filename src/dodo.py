from pathlib import Path
from typing import (
    Callable, Generator,
)

from doit import task_params

default_c = 'term-missing'
default_n: int = 4
default_f: int = 1

ignored_warnings = (
    'DeprecationWarning', '.'.join(
        (
            'pydantic', 'json_schema',
            'PydanticJsonSchemaWarning',
        ),
    ),
)
template = '-W ignore::{warning}'
strings = (
    template.format(
        warning=warning,
    ) for warning
    in ignored_warnings
)

full_test: str = ' '.join(
    (
        'pytest', '-vv',
        '--cov', '.',
        '--cov-report',
        '{coverage_report_type}',
        '--cov-fail-under=100',
        '--numprocesses',
        '{number_of_processes}',
        '--exitfirst',
        '--randomly-seed=last',
        '--flake-finder',
        '--flake-runs',
        '{flake_runs}',
        '--durations=4',
        '-W error',
        *strings,
    ),
)

single_test: str = ' '.join(
    (
        'pytest', '--exitfirst',
        '-vvs', '{target}',
        '--disable-pytest-warnings',
    ),
)

flake8 = 'flake8 .'
mypy = 'mypy .'
bandit = 'bandit -r . --exclude tests'
blocklint = 'blocklint .'
ruff = 'ruff check .'

safety: str = ' -i '.join(
    (
        'safety check',
        '42194', '51457', '67599',
    ),
)

outdated = 'poetry show --outdated'

up: str = ' && '.join(
    (
        ' '.join(
            (
                'poetry self add',
                'poetry-plugin-up',
            ),
        ),
        'poetry update',
        'poetry up --latest',
    ),
)

migration: str = ' '.join(
    (
        'alembic --config',
        '/src/db/alembic.ini',
        'revision --autogenerate',
        '--message "{message}"',
    ),
)

migrate: str = ' '.join(
    (
        'alembic --config',
        '/src/db/alembic.ini',
        'upgrade head',
    ),
)

export: str = ' && '.join(
    (
        ' '.join(
            (
                'poetry self add',
                'poetry-plugin-export',
            ),
        ),
        ' '.join(
            (
                'poetry export',
                '--format requirements.txt',
                '--output requirements.txt',
                '--with dev',
                '--without-hashes',
                '--without-urls',
            ),
        ),
    ),
)

default_verbosity = 2

type Actions = tuple[
    str | Callable[[], None], ...,
]

type MetaData = dict[str, Actions | int]


def metadata_from(
    actions: Actions,
    verbosity: int = default_verbosity,
) -> MetaData:
    return {
        'actions': actions,
        'verbosity': verbosity,
    }


@task_params(
    param_def=[
        {
            'name': 'target',
            'long': 'target',
            'short': 't', 'type': str,
            'default': '',
        },
        {
            'name': 'number_of_processes',
            'long': 'number_of_processes',
            'short': 'n', 'type': int,
            'default': default_n,
        },
        {
            'name': 'coverage_report_path',
            'long': 'coverage_report_path',
            'short': 'c', 'type': str,
            'default': '',
        },
        {
            'name': 'flake_runs',
            'long': 'flake_runs',
            'short': 'f', 'type': int,
            'default': default_f,
        },
    ],
)
def task_test(
    target: str = '',
    flake_runs: int = default_f,
    coverage_report_path: str = '',
    number_of_processes: int = default_n,
) -> MetaData:
    report_types: dict[str, str] = {
        '': default_c,
    }
    report_type: str = report_types.get(
        coverage_report_path,
        f'xml:{coverage_report_path}',
    )
    first = 'coverage_report_type'
    second = 'number_of_processes'
    third = 'flake_runs'
    kwargs = {
        first: report_type,
        second: number_of_processes,
        third: flake_runs,
    }
    full_run = full_test.format(**kwargs)
    actions: dict[str, str] = {
        '': full_run,
    }
    single_run = single_test.format(
        target=target,
    )
    action: str = actions.get(
        target, single_run,
    )
    return metadata_from(actions=(action,))


def task_ruff() -> MetaData:
    return metadata_from(actions=(ruff,))


def task_flake8() -> MetaData:
    actions = (flake8,)
    return metadata_from(actions=actions)


def task_mypy() -> MetaData:
    return metadata_from(actions=(mypy,))


def task_bandit() -> MetaData:
    actions = (bandit,)
    return metadata_from(actions=actions)


def task_safety() -> MetaData:
    actions = (safety,)
    return metadata_from(actions=actions)


def task_blocklint() -> MetaData:
    actions = (blocklint,)
    return metadata_from(actions=actions)


def task_up() -> MetaData:
    return metadata_from(actions=(up,))


def task_lint() -> MetaData:
    return metadata_from(
        actions=(
            ruff, flake8, mypy,
            blocklint, bandit,
        ),
    )


@task_params(
    param_def=[
        {
            'name': 'message',
            'long': 'message',
            'short': 'm', 'type': str,
            'default': 'random message',
        },
    ],
)
def task_migration(
    message: str,
) -> MetaData:
    action = migration.format(
        message=message,
    )
    actions: tuple[str] = (action,)
    return metadata_from(actions=actions)


def task_migrate() -> MetaData:
    actions = (migrate,)
    return metadata_from(actions=actions)


def task_outdated() -> MetaData:
    actions = (outdated,)
    return metadata_from(actions=actions)


def fix_requirements() -> None:
    path = Path('requirements.txt')
    lines: list[str]
    truncated: Generator[
        str, None, None,
    ]
    divided: Generator[
        list[str], None, None,
    ]
    fixed: str
    with path.open(mode='r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        divided = (
            line.split(
                ' ', 1,
            ) for line in lines
        )
        truncated = (
            next(iter(line))
            for line in divided
        )
        fixed = '\n'.join(truncated)
        file.write(fixed + '\n')


def task_export() -> MetaData:
    actions = (export, fix_requirements,)
    return metadata_from(actions=actions)


def task_all() -> MetaData:
    first = 'coverage_report_type'
    second = 'number_of_processes'
    third = 'flake_runs'
    kwargs = {
        first: default_c,
        second: default_n,
        third: default_f,
    }
    full_run = full_test.format(
        **kwargs,
    )
    return metadata_from(
        actions=(
            full_run, ruff,
            flake8, mypy,
            bandit, blocklint,
            outdated,
        ),
    )
