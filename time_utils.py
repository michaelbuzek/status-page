from datetime import datetime
from timing_config import TIMINGS

def calculate_event_times(base_time: datetime):
    """
    Berechnet die drei geplanten Zeitpunkte für setup-check, fw-download und run-test
    basierend auf dem übergebenen Zeitpunkt (meist execute_at für den run-test).
    """

    return {
        "setup_check_time": base_time + TIMINGS["setup-check"],
        "fw_download_time": base_time + TIMINGS["fw-download"],
        "run_test_time": base_time + TIMINGS["run-test"]
    }
