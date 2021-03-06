"""Context manager for database connection."""

import sqlite3
import logging

class DBCM():
    """Handles all connections to the database."""

    def __init__(self, db_name) -> None:
        try:
            self.db_name = db_name
            self.conn = None
            self.curs = None
        except Exception as error:
            logging.warning("Error: DBCM: Init: %s", error)
    def __enter__(self) -> 'curs':
        try:
            self.conn = sqlite3.connect(self.db_name)
        except Exception as error:
            logging.warning("Error: DBCM: Enter: Creating cursor: %s", error)
        try:
            self.curs = self.conn.cursor()
            return self.curs
        except Exception as error:
            logging.warning("Error: DBCM: Enter: Creating cursor: %s", error)
    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        try:
            self.conn.commit()
            self.curs.close()
            self.conn.close()
        except Exception as error:
            logging.warning("Error: DBCM: Exit: Committing or closing: %s", error)
