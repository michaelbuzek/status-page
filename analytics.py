from flask import Blueprint, render_template
from models import db, TriggerEvent
from collections import Counter

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics")
def analytics():
    events = TriggerEvent.query.all()

    # Router-Nutzung zählen
    router_counter = Counter([e.router for e in events if e.router])

    router_labels = list(router_counter.keys())
    router_values = list(router_counter.values())

    return render_template("analytics.html", router_labels=router_labels, router_values=router_values)
