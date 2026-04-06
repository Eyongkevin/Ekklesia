from app.db.uow import UnitOfWork

def get_db():
    with UnitOfWork() as uow:
        yield uow
