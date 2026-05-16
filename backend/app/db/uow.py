from app.db.session import SessionLocal

class UnitOfWork:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()

        self.db.close()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()