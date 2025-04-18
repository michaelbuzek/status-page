import time
import requests
from datetime import datetime
from sqlalchemy import create_engine, text

# Datenbank-URL (deine Render PostgreSQL)
DATABASE_URL = "postgresql://meineapiuser:gk2u1YcUpTDkqVlhZY0U0qAtGcBWxXcD@dpg-cvrvbcur433s73eaj0k0-a.oregon-postgres.render.com/meineapidb"

# Dein n8n Webhook
N8N_WEBHOOK_URL = "https://buzek.app.n8n.cloud/webhook/webhook"

def check_due_triggers():
    now = datetime.now()
    print(f"\n[INFO] Checker gestartet – Jetzt: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        query = text("""
            SELECT * FROM trigger_events
            WHERE status = 'open' AND execute_at <= :now
            ORDER BY execute_at ASC
        """)
        result = conn.execute(query, {"now": now}).fetchall()

        if not result:
            print("[INFO] Keine fälligen Events.")
            return

        for row in result:
            print(f"[TRIGGER] #{row.id} ({row.type}) wird jetzt ausgeführt")

            try:
                response = requests.get(N8N_WEBHOOK_URL)
                print(f"[n8n] Status {response.status_code}")
            except Exception as e:
                print(f"[FEHLER] Webhook fehlgeschlagen: {e}")
                continue

            # Status auf 'triggered' setzen
            update = text("""
                UPDATE trigger_events
                SET status = 'triggered'
                WHERE id = :id
            """)
            conn.execute(update, {"id": row.id})
            conn.commit()
            print(f"[DB] Status aktualisiert für ID {row.id}")

if __name__ == "__main__":
    while True:
        try:
            check_due_triggers()
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n[STOP] Manuell gestoppt.")
            break
        except Exception as e:
            print(f"[ERROR] Unerwarteter Fehler: {e}")
            time.sleep(10)
