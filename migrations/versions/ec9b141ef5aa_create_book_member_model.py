"""create book member model

Revision ID: ec9b141ef5aa
Revises:
Create Date: 2024-10-18 19:28:43.772598

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "ec9b141ef5aa"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "book",
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("authors", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("average_rating", sa.Float(), nullable=False),
        sa.Column("isbn", sa.Integer(), nullable=False),
        sa.Column("isbn13", sa.Integer(), nullable=False),
        sa.Column("language_code", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("num_pages", sa.Integer(), nullable=False),
        sa.Column("ratings_count", sa.Integer(), nullable=False),
        sa.Column("text_reviews_count", sa.Integer(), nullable=False),
        sa.Column("publication_date", sa.Date(), nullable=False),
        sa.Column("publisher", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_book_authors"), "book", ["authors"], unique=False)
    op.create_index(op.f("ix_book_id"), "book", ["id"], unique=False)
    op.create_index(op.f("ix_book_isbn"), "book", ["isbn"], unique=True)
    op.create_index(op.f("ix_book_isbn13"), "book", ["isbn13"], unique=True)
    op.create_index(op.f("ix_book_title"), "book", ["title"], unique=False)
    op.create_table(
        "member",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("outstanding_payment", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_member_email"), "member", ["email"], unique=False)
    op.create_index(op.f("ix_member_id"), "member", ["id"], unique=False)
    op.create_index(op.f("ix_member_name"), "member", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_member_name"), table_name="member")
    op.drop_index(op.f("ix_member_id"), table_name="member")
    op.drop_index(op.f("ix_member_email"), table_name="member")
    op.drop_table("member")
    op.drop_index(op.f("ix_book_title"), table_name="book")
    op.drop_index(op.f("ix_book_isbn13"), table_name="book")
    op.drop_index(op.f("ix_book_isbn"), table_name="book")
    op.drop_index(op.f("ix_book_id"), table_name="book")
    op.drop_index(op.f("ix_book_authors"), table_name="book")
    op.drop_table("book")
    # ### end Alembic commands ###
