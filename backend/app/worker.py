import logging
import os
import pathlib
import signal
import time

from . import db

HEARTBEAT_FILE = pathlib.Path("/tmp/worker-heartbeat")
INTERVAL = int(os.environ.get("WORKER_INTERVAL_SECONDS", "30"))

running = True


def stop(signum, frame):
    """Коректне завершення при сигналі SIGTERM (фактор IX з 12-Factor App)."""
    global running
    logging.info("Отримано сигнал зупинки, завершую роботу")
    running = False


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    logging.info("Воркер запущено, інтервал %s с", INTERVAL)

    while running:
        try:
            db.ping()
            HEARTBEAT_FILE.touch()
            logging.info("Воркер працює, база доступна")
        except Exception:
            logging.exception("Не вдалося підключитися до бази")
        for _ in range(INTERVAL):
            if not running:
                break
            time.sleep(1)


if __name__ == "__main__":
    main()
