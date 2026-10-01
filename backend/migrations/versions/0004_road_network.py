"""Create persistent GIS-ready road network.

Revision ID: 0004_road_network
Revises: 0003_auth_two_role
Create Date: 2026-09-26
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_road_network"
down_revision: Union[str, Sequence[str], None] = "0003_auth_two_role"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "network_meta",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "road_nodes",
        sa.Column("node_id", sa.String(length=96), nullable=False),
        sa.Column("label", sa.String(length=160), nullable=False),
        sa.Column("node_type", sa.String(length=32), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("external_ref", sa.String(length=160), nullable=True),
        sa.Column("properties", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("node_id"),
    )
    op.create_index(op.f("ix_road_nodes_node_type"), "road_nodes", ["node_type"], unique=False)
    op.create_index(op.f("ix_road_nodes_external_ref"), "road_nodes", ["external_ref"], unique=False)

    op.create_table(
        "road_edges",
        sa.Column("edge_id", sa.String(length=96), nullable=False),
        sa.Column("source_node_id", sa.String(length=96), nullable=False),
        sa.Column("target_node_id", sa.String(length=96), nullable=False),
        sa.Column("bidirectional", sa.Boolean(), nullable=False),
        sa.Column("travel_minutes", sa.Float(), nullable=False),
        sa.Column("distance_meters", sa.Float(), nullable=True),
        sa.Column("base_risk", sa.Float(), nullable=False),
        sa.Column("current_risk", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("failure_horizon_minutes", sa.Float(), nullable=True),
        sa.Column("external_ref", sa.String(length=160), nullable=True),
        sa.Column("geometry_geojson", sa.JSON(), nullable=True),
        sa.Column("updated_by_user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_node_id"], ["road_nodes.node_id"]),
        sa.ForeignKeyConstraint(["target_node_id"], ["road_nodes.node_id"]),
        sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("edge_id"),
    )
    op.create_index(op.f("ix_road_edges_source_node_id"), "road_edges", ["source_node_id"], unique=False)
    op.create_index(op.f("ix_road_edges_target_node_id"), "road_edges", ["target_node_id"], unique=False)
    op.create_index(op.f("ix_road_edges_status"), "road_edges", ["status"], unique=False)
    op.create_index(op.f("ix_road_edges_external_ref"), "road_edges", ["external_ref"], unique=False)
    op.create_index(op.f("ix_road_edges_updated_by_user_id"), "road_edges", ["updated_by_user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_road_edges_updated_by_user_id"), table_name="road_edges")
    op.drop_index(op.f("ix_road_edges_external_ref"), table_name="road_edges")
    op.drop_index(op.f("ix_road_edges_status"), table_name="road_edges")
    op.drop_index(op.f("ix_road_edges_target_node_id"), table_name="road_edges")
    op.drop_index(op.f("ix_road_edges_source_node_id"), table_name="road_edges")
    op.drop_table("road_edges")

    op.drop_index(op.f("ix_road_nodes_external_ref"), table_name="road_nodes")
    op.drop_index(op.f("ix_road_nodes_node_type"), table_name="road_nodes")
    op.drop_table("road_nodes")
    op.drop_table("network_meta")
