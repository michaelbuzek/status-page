import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Verbindung zur Render-Datenbank
DATABASE_URL = "postgresql://meineapiuser:gk2u1YcUpTDkqVlhZY0U0qAtGcBWxXcD@dpg-cvrvbcur433s73eaj0k0-a.oregon-postgres.render.com/meineapidb"
engine = create_engine(DATABASE_URL)

# Nur run-test Events laden (damit pro Auftrag nur 1 gezählt wird)
df = pd.read_sql("""
    SELECT auftrag_id, router, status
    FROM trigger_events
    WHERE type = 'run-test'
""", engine)

# Gesamtanzahl Aufträge
total_orders = df["auftrag_id"].nunique()

# Aufträge nach Status (open, triggered, done)
status_counts = df["status"].value_counts()

# Router-Auswertung (wie oft ein Router getestet wurde)
router_counts = df["router"].value_counts()

# Ausgabe der Statistiken
summary = {
    "total_orders": total_orders,
    "status_counts": status_counts.to_dict(),
    "router_counts": router_counts.to_dict()
}

# Balkendiagramm für Router-Verteilung
plt.figure(figsize=(10, 5))
plt.bar(router_counts.index, router_counts.values)
plt.title("Häufigkeit getesteter Router (nur run-test)")
plt.xlabel("Router")
plt.ylabel("Anzahl")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("router_verteilung.png")  # Wird im aktuellen Verzeichnis gespeichert

print(summary)
