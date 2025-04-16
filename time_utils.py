from collections import defaultdict

def gruppiere_events_nach_auftrag(events):
    gruppiert = defaultdict(dict)
    for e in events:
        gruppiert[e.auftrag_id]["auftrag_id"] = e.auftrag_id
        gruppiert[e.auftrag_id][e.type] = e
    return dict(gruppiert)
