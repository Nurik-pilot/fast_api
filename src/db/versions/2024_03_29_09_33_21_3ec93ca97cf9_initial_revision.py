"""
Initial revision
ID: 3ec93ca97cf9
Revises:
Create Date:
2024-03-29
09:33:21.670545+00:00
"""
from alembic import op
from sqlalchemy import (
    String, Column, UUID,
    DateTime, text, Text,
    PrimaryKeyConstraint,
    Boolean, UniqueConstraint,
    CheckConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy.dialects.postgresql import (
    JSONB,
)

from faas.models.email import email_regex

revision = '3ec93ca97cf9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'domain_configuration_snapshots',
        Column('id', UUID(), nullable=False),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'snapshot_type',
            String(length=128),
            nullable=False,
        ),
        Column(
            'data',
            JSONB(astext_type=Text()),
            nullable=False,
        ),
        PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'domain_configurations',
        Column('id', UUID(), nullable=False),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'updated_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'is_active', Boolean(),
            server_default=text('true'),
            nullable=False,
        ),
        PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'faas_email_snapshots',
        Column('id', UUID(), nullable=False),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'snapshot_type',
            String(length=128),
            nullable=False,
        ),
        Column(
            'data', JSONB(
                astext_type=Text(),
            ), nullable=False,
        ),
        PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'faas_phone_snapshots',
        Column('id', UUID(), nullable=False),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'snapshot_type',
            String(length=128),
            nullable=False,
        ),
        Column(
            'data',
            JSONB(astext_type=Text()),
            nullable=False,
        ),
        PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'faas_user_snapshots',
        Column('id', UUID(), nullable=False),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'snapshot_type',
            String(length=128),
            nullable=False,
        ),
        Column(
            'data',
            JSONB(astext_type=Text()),
            nullable=False,
        ),
        PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'faas_users',
        Column(
            'username',
            String(length=128),
            nullable=False,
        ),
        Column(
            'password',
            String(length=128),
            nullable=False,
        ),
        Column(
            'id', UUID(),
            nullable=False,
        ),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'updated_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'is_active', Boolean(),
            server_default=text('true'),
            nullable=False,
        ),
        PrimaryKeyConstraint('id'),
        UniqueConstraint('username'),
    )
    op.create_table(
        'faas_emails',
        Column(
            'address',
            String(length=64),
            nullable=False,
        ),
        Column(
            'user_id', UUID(),
            nullable=True,
        ),
        Column(
            'id', UUID(),
            nullable=False),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'updated_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'is_active', Boolean(),
            server_default=text('true'),
            nullable=False,
        ),
        CheckConstraint(
            sqltext=f'address ~* {email_regex}',
        ),
        ForeignKeyConstraint(
            ['user_id'],
            ['faas_users.id'],
            ondelete='CASCADE',
        ),
        PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'faas_phones',
        Column(
            'number',
            String(length=16),
            nullable=False,
        ),
        Column(
            'user_id', UUID(),
            nullable=True,
        ),
        Column(
            'id', UUID(),
            nullable=False,
        ),
        Column(
            'created_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'updated_at',
            DateTime(timezone=True),
            server_default=text('now()'),
            nullable=False,
        ),
        Column(
            'is_active', Boolean(),
            server_default=text('true'),
            nullable=False,
        ),
        CheckConstraint(
            sqltext='char_length(number) >= 1',
        ),
        ForeignKeyConstraint(
            ['user_id'],
            ['faas_users.id'],
            ondelete='CASCADE',
        ),
        PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table(
        table_name='faas_phones',
    )
    op.drop_table(
        table_name='faas_emails',
    )
    op.drop_table(
        table_name='faas_users',
    )
    op.drop_table(
        table_name='faas_user_snapshots',
    )
    op.drop_table(
        table_name='faas_phone_snapshots',
    )
    op.drop_table(
        table_name='faas_email_snapshots',
    )
    op.drop_table(
        table_name='domain_configurations',
    )
    op.drop_table(
        table_name='domain_configuration_snapshots',
    )
