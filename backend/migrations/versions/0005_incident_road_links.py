"""Link verified incidents to road-closure actions.

Revision ID: 0005_incident_road_links
Revises: 0004_road_network
Create Date: 2026-09-26
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0005_incident_road_links"
down_revision: Union[str, Sequence[str], None] = "0004_road_network"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "incident_road_links",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("incident_id", sa.Integer(), nullable=False),
        sa.Column("edge_id", sa.String(length=96), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["incident_id"], ["incidents.id"]),
        sa.ForeignKeyConstraint(["edge_id"], ["road_edges.edge_id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_incident_road_links_incident_id", "incident_road_links", ["incident_id"])
    op.create_index("ix_incident_road_links_edge_id", "incident_road_links", ["edge_id"])
    op.create_index("ix_incident_road_links_status", "incident_road_links", ["status"])


def downgrade() -> None:
    op.drop_index("ix_incident_road_links_status", table_name="incident_road_links")
    op.drop_index("ix_incident_road_links_edge_id", table_name="incident_road_links")
    op.drop_index("ix_incident_road_links_incident_id", table_name="incident_road_links")
    op.drop_table("incident_road_links")
