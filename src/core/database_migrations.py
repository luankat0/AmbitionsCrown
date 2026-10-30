import sqlite3

from pathlib import Path
from collections.abc import Callable, Mapping

from src.core.database import Database
from src.core.database_audit import (
    validate_migration_integrity,
)


Migration = Callable[[sqlite3.Connection], None]


def apply_migrations(
    database: Database,
    migrations: Mapping[int, Migration],
    backup_path: str | Path | None = None
) -> int:
    """
    Executa migrations em ordem crescente.

    Exige auditoria e backup antes de modificar
    o esquema.

    Atualiza user_version na mesma transação
    das alterações estruturais.
    """

    current_version = database.get_schema_version()
    latest_version = max(migrations, default=0)

    if current_version > latest_version:
        raise ValueError(
            "O banco possui uma versão de esquema "
            "superior às migrations disponíveis."
        )

    pending = list(
        range(
            current_version + 1,
            latest_version + 1
        )
    )

    # Nenhuma migration pendente.
    if not pending:
        return current_version

    # Impede saltos entre versões.
    for version in pending:
        if version not in migrations:
            raise ValueError(
                f"Migration da versão {version} "
                "não encontrada."
            )

    if backup_path is None:
        raise ValueError(
            "É obrigatório informar o caminho "
            "do backup antes da migração."
        )

    connection = database.connection

    if connection.in_transaction:
        raise RuntimeError(
            "Finalize a transação atual antes "
            "de executar migrations."
        )

    # Primeira validação, antes do backup.
    validate_migration_integrity(connection)

    # O backup precisa estar concluído
    # antes de qualquer alteração estrutural.
    database.backup_to(backup_path)

    # Reserva a transação de escrita.
    connection.execute("BEGIN IMMEDIATE")

    try:
        # Confirma que a versão não mudou.
        if database.get_schema_version() != current_version:
            raise RuntimeError(
                "A versão do banco mudou durante "
                "a preparação da migração."
            )

        # Revalida a integridade com a
        # transação de escrita já iniciada.
        validate_migration_integrity(connection)

        for version in pending:
            migration = migrations[version]

            migration(connection)

            if not connection.in_transaction:
                raise RuntimeError(
                    "A migration encerrou a "
                    "transação inesperadamente."
                )

            connection.execute(
                f"PRAGMA user_version = {version}"
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    return database.get_schema_version()