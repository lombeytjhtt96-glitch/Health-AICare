"""add chain_id to badge tables for multi-chain support

Adds chain_id column to badge_templates, badge_issuances, and user_badges
to support deploying and minting NFT badges on multiple EVM chains
(EDU Chain, BNB Smart Chain, etc.).

All existing rows default to chain_id=656476 (EDU Chain Testnet) for
backward compatibility.

Revision ID: d4e2f7a8b1c3
Revises: c2a1f8e1d1a0
Create Date: 2026-02-09
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "d4e2f7a8b1c3"
down_revision = "c2a1f8e1d1a0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == 'sqlite'
    # --- badge_templates ---
    op.add_column(
        "badge_templates",
        sa.Column("chain_id", sa.Integer(), nullable=False, server_default="656476"),
    )
    op.create_index("ix_badge_templates_chain_id", "badge_templates", ["chain_id"])

    if not is_sqlite:
        try:
            op.drop_constraint("uq_badge_templates_contract_token", "badge_templates", type_="unique")
        except Exception:
            pass  # Constraint may not exist in all environments

        op.create_unique_constraint(
            "uq_badge_templates_chain_contract_token",
            "badge_templates",
            ["chain_id", "contract_address", "token_id"],
        )

    # --- badge_issuances ---
    op.add_column(
        "badge_issuances",
        sa.Column("chain_id", sa.Integer(), nullable=False, server_default="656476"),
    )
    op.create_index("ix_badge_issuances_chain_id", "badge_issuances", ["chain_id"])

    # --- user_badges ---
    op.add_column(
        "user_badges",
        sa.Column("chain_id", sa.Integer(), nullable=False, server_default="656476"),
    )
    op.create_index("ix_user_badges_chain_id", "user_badges", ["chain_id"])

    if not is_sqlite:
        try:
            op.drop_constraint("_user_badge_uc", "user_badges", type_="unique")
        except Exception:
            pass

        op.create_unique_constraint(
            "_user_badge_chain_uc",
            "user_badges",
            ["user_id", "badge_id", "chain_id"],
        )


def downgrade() -> None:
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == 'sqlite'
    # --- user_badges ---
    if not is_sqlite:
        try:
            op.drop_constraint("_user_badge_chain_uc", "user_badges", type_="unique")
        except Exception:
            pass
        op.create_unique_constraint("_user_badge_uc", "user_badges", ["user_id", "badge_id"])
    op.drop_index("ix_user_badges_chain_id", table_name="user_badges")
    op.drop_column("user_badges", "chain_id")

    # --- badge_issuances ---
    op.drop_index("ix_badge_issuances_chain_id", table_name="badge_issuances")
    op.drop_column("badge_issuances", "chain_id")

    # --- badge_templates ---
    if not is_sqlite:
        try:
            op.drop_constraint("uq_badge_templates_chain_contract_token", "badge_templates", type_="unique")
        except Exception:
            pass
        op.create_unique_constraint(
            "uq_badge_templates_contract_token",
            "badge_templates",
            ["contract_address", "token_id"],
        )
    op.drop_index("ix_badge_templates_chain_id", table_name="badge_templates")
    op.drop_column("badge_templates", "chain_id")
