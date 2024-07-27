from json import load
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

from core.dependencies import (
    get_db,
)

type Tables = list[list[str]]


class Command:
    file_path: Path = Path(__file__)
    directory: Path = file_path.parent
    trigger = directory / 'trigger.sql'
    models = directory / 'models.json'
    statement: str
    tables: Tables

    def obtain_statement(self) -> str:
        with self.trigger.open() as file:
            return file.read()

    def obtain_tables(self) -> Tables:
        with self.models.open() as file:
            data = load(fp=file)
        return data.get('models', [])

    def __init__(self) -> None:
        super().__init__()
        self.statement = self.obtain_statement()
        self.tables = self.obtain_tables()

    def set_trigger(
        self, source: str, target: str,
        session: Session,
    ) -> None:
        lower_source = source.replace(
            '.', '_',
        )
        lower_target = target.replace(
            '.', '_',
        )
        statement = self.statement.format(
            source=source, target=target,
            lower_source=lower_source,
            lower_target=lower_target,
        )
        session.execute(
            statement=text(
                text=statement,
            ),
        )

    def handle(
        self, db: type[Session] = get_db(),
    ) -> None:
        with db() as session, session.begin():
            for source, target in self.tables:
                self.set_trigger(
                    source=source,
                    target=target,
                    session=session,
                )


if __name__ == '__main__':
    Command().handle()
