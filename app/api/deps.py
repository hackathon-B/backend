def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
