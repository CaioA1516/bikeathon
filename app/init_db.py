from app_manager import db
from models import Stats
from venmo_pull import fetch_venmo_balance
import sys

def init_db():
    db.drop_all()
    db.create_all()

    bal = get_bal()
    db.session.add(Stats(distance=0,
                         distance1=0,
                         distance2=0,
                         cash=0,
                         venmo=0,
                         card=0,
                         misc=0,
                         start_venmo_bal=bal))
    db.session.commit()

def get_bal():
    bal = fetch_venmo_balance()
    if bal is None:
        print("fetch_venmo_balance returned None. Please reauthorize to fetch "
              "initial venmo balance.")
        sys.exit("Database manipulation failed.")
    return bal

def reset_venmo(bal=None):
    if bal is None:
        bal = get_bal()
    stats = Stats.query.first()
    stats.start_venmo_bal = bal
    db.session.add(stats)
    db.session.commit()
