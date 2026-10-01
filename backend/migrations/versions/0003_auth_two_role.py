"""Add two-role authentication and actor linkage.

Revision ID: 0003_auth_two_role
Revises: 0002_incident_lifecycle
Create Date: 2026-09-26
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_auth_two_role"
down_revision: Union[str, Sequence[str], None] = "0002_incident_lifecycle"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_refresh_tokens_user_id"),
        "refresh_tokens",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_refresh_tokens_token_hash"),
        "refresh_tokens",
        ["token_hash"],
        unique=True,
    )

    with op.batch_alter_table("incident_reports") as batch_op:
        batch_op.add_column(sa.Column("reporter_user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_incident_reports_reporter_user_id_users",
            "users",
            ["reporter_user_id"],
            ["id"],
        )
    op.create_index(
        op.f("ix_incident_reports_reporter_user_id"),
        "incident_reports",
        ["reporter_user_id"],
        unique=False,
    )

    with op.batch_alter_table("audit_events") as batch_op:
        batch_op.add_column(sa.Column("actor_user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_audit_events_actor_user_id_users",
            "users",
            ["actor_user_id"],
            ["id"],
        )
    op.create_index(
        op.f("ix_audit_events_actor_user_id"),
        "audit_events",
        ["actor_user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_events_actor_user_id"), table_name="audit_events")
    with op.batch_alter_table("audit_events") as batch_op:
        batch_op.drop_constraint(
            "fk_audit_events_actor_user_id_users",
            type_="foreignkey",
        )
        batch_op.drop_column("actor_user_id")

    op.drop_index(
        op.f("ix_incident_reports_reporter_user_id"),
        table_name="incident_reports",
    )
    with op.batch_alter_table("incident_reports") as batch_op:
        batch_op.drop_constraint(
            "fk_incident_reports_reporter_user_id_users",
            type_="foreignkey",
        )
        batch_op.drop_column("reporter_user_id")

    op.drop_index(op.f("ix_refresh_tokens_token_hash"), table_name="refresh_tokens")
    op.drop_index(op.f("ix_refresh_tokens_user_id"), table_name="refresh_tokens")
    op.drop_table("refresh_tokens")

    op.drop_index(op.f("ix_users_role"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
