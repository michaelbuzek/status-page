from datetime import timedelta

TEST_TIMING = True

if TEST_TIMING:
    TIMINGS = {
        "setup-check": timedelta(minutes=-2),
        "fw-download": timedelta(minutes=-1),
        "run-test": timedelta(minutes=0),
    }
else:
    TIMINGS = {
        "setup-check": timedelta(days=-1, hours=16),
        "fw-download": timedelta(hours=-1),
        "run-test": timedelta(minutes=0),
    }
