"""Adiciona check constraints manualmente

Revision ID: 92f528bb3e90
Revises: f825fafcaa0c
Create Date: 2025-05-30 17:14:04.393233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92f528bb3e90'
down_revision = 'f825fafcaa0c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        constraint_name="ck_user_gender",
        table_name="users",
        condition="gender IN ('Masculino', 'Feminino', 'Outro')"
    )
    # repita para outras tabelas conforme necessário
    op.create_check_constraint(
        constraint_name="ck_elderly_gender",
        table_name="elderly",
        condition="gender IN ('Masculino', 'Feminino', 'Outro')"
    )
    op.create_check_constraint(
        constraint_name="ck_responsible_contact_method",
        table_name="responsible",
        condition="preferred_contact_method IN ('E-mail', 'Telefone', 'WhatsApp', 'Sem preferência')"
    )
    op.create_check_constraint(
        constraint_name="ck_contract_status_valid",
        table_name="contract",
        condition="status IN ('active', 'completed', 'cancelled')"
    )
    op.create_check_constraint(
        constraint_name="ck_caregiver_salary_non_negative",
        table_name="caregiver",
        condition="pretensao_salarial IS NULL OR pretensao_salarial >= 0"
    )


def downgrade():
    op.drop_constraint("ck_user_gender", "users", type_="check")
    op.drop_constraint("ck_elderly_gender", "elderly", type_="check")
    op.drop_constraint("ck_responsible_contact_method", "responsible", type_="check")
    op.drop_constraint("ck_contract_status_valid", "contract", type_="check")
    op.drop_constraint("ck_caregiver_salary_non_negative", "caregiver", type_="check")
