import matplotlib.pyplot as plt
import io
import base64
from markupsafe import Markup

plt.switch_backend("Agg")


def plot_top_transactions(session):
    from app import (
        Transaction,
        User,
        db,
    )

    subquery = (
        session.query(
            Transaction.user_id, db.func.max(Transaction.amount).label("max_amount")
        )
        .group_by(Transaction.user_id)
        .subquery()
    )

    top_transactions = (
        session.query(Transaction)
        .join(
            subquery,
            (Transaction.user_id == subquery.c.user_id)
            & (Transaction.amount == subquery.c.max_amount),
        )
        .order_by(Transaction.amount.desc())
        .limit(5)
        .all()
    )

    amounts = [t.amount for t in top_transactions]
    usernames = [session.query(User).get(t.user_id).username for t in top_transactions]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(usernames, amounts)
    plt.xlabel("Username")
    plt.ylabel("Transaction Amount")
    plt.title("Top 5 Users by Largest Transaction")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()


def render_top_transactions(session):
    img_data = plot_top_transactions(session)
    return Markup(f'<img src="data:image/png;base64,{img_data}" style="width:100%;" />')
