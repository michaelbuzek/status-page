from datetime import timedelta

# Umschalten zwischen Testbetrieb und Produktion
TEST_TIMING = True  # True = Simulationsmodus (Minuten), False = Echtbetrieb (Tage/Stunden)

if TEST_TIMING:
    TIMINGS = {
        "setup-check": timedelta(minutes=-2),    # 2 Minuten vor run-test
        "fw-download": timedelta(minutes=-1),    # 1 Minute vor run-test
        "run-test": timedelta(minutes=0)         # Zeitpunkt wie übergeben
    }
else:
    TIMINGS = {
        "setup-check": timedelta(days=-1, hours=16),   # 1 Tag vorher um 16:00
        "fw-download": timedelta(hours=-1),            # 1 Stunde vorher
        "run-test": timedelta(minutes=0)
    }
