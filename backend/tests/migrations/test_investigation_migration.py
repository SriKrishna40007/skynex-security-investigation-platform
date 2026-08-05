from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


MIGRATION_REVISION = "4d9f21c8a7e3"
MIGRATION_PARENT = "7b4f2c9e1a10"
MIGRATION_PATH = Path("alembic/versions/4d9f21c8a7e3_add_investigations_table.py")


def _migration_source() -> str:
    return MIGRATION_PATH.read_text(encoding="utf-8")


def test_investigation_migration_exists() -> None:
    assert MIGRATION_PATH.is_file()


def test_investigation_migration_extends_current_head() -> None:
    config = Config("alembic.ini")
    scripts = ScriptDirectory.from_config(config)

    revision = scripts.get_revision(MIGRATION_REVISION)

    assert revision is not None
    assert revision.down_revision == MIGRATION_PARENT


def test_investigation_migration_creates_expected_table() -> None:
    source = _migration_source()

    assert "op.create_table(" in source
    assert '"investigations"' in source


def test_investigation_migration_contains_owner_foreign_key() -> None:
    source = _migration_source()

    assert '"owner_id"' in source
    assert '"users.id"' in source
    assert '"fk_investigations_owner_id_users"' in source
    assert 'ondelete="CASCADE"' in source


def test_investigation_migration_indexes_owner() -> None:
    source = _migration_source()

    assert '"ix_investigations_owner_id"' in source


def test_investigation_migration_contains_snapshot_columns() -> None:
    source = _migration_source()

    for column in (
        "investigation_type",
        "status",
        "risk_score",
        "severity",
        "summary",
        "result",
        "created_at",
        "updated_at",
    ):
        assert f'"{column}"' in source


def test_investigation_migration_has_downgrade() -> None:
    source = _migration_source()

    assert "def downgrade()" in source
    assert 'op.drop_table("investigations")' in source
