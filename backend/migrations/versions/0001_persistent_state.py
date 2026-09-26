"""Create persistent scenario state tables.

Revision ID: 0001_persistent_state
Revises:
Create Date: 2026-09-26
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_persistent_state"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scenario_meta",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "road_status",
        sa.Column("road_id", sa.String(length=64), nullable=False),
        sa.Column("blocked", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("road_id"),
    )
    op.create_table(
        "shelter_status",
        sa.Column("shelter_id", sa.String(length=64), nullable=False),
        sa.Column("capacity_remaining", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("shelter_id"),
    )
    op.create_table(
        "ground_reports",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("road_id", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("accepted", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("reviewed_by", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["road_id"], ["road_status.road_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ground_reports_road_id"), "ground_reports", ["road_id"], unique=False)
    op.create_index(op.f("ix_ground_reports_status"), "ground_reports", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_ground_reports_status"), table_name="ground_reports")
    op.drop_index(op.f("ix_ground_reports_road_id"), table_name="ground_reports")
    op.drop_table("ground_reports")
    op.drop_table("shelter_status")
    op.drop_table("road_status")
    op.drop_table("scenario_meta")
