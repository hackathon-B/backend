"""seed initial ai models

Revision ID: 8f9d49259084
Revises: 73c6db1e2ae3
Create Date: 2024-12-02 05:21:09.721243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f9d49259084'
down_revision: Union[str, None] = '73c6db1e2ae3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        # 初期データの投入を追加（最後に追加）
    op.execute("""
        INSERT INTO ai_models (ai_model_id, ai_model_name, description) 
        VALUES 
            (1, 'GPT-3.5-turbo', 'OpenAI GPT-3.5モデル'),
            (2, 'GPT-4o', 'OpenAI GPT-4モデル'),
            (3, 'Claude-3-5-sonnet', 'Anthropic Claudeモデル')
        ON DUPLICATE KEY UPDATE
            ai_model_name = VALUES(ai_model_name),
            description = VALUES(description)
    """)



def downgrade() -> None:
        op.execute("""
        DELETE FROM ai_models 
        WHERE ai_model_name IN (
            'GPT-3.5-turbo',
            'GPT-4o',
            'Claude-3-5-sonnet'
        )
    """)
