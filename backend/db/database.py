import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

logger = logging.getLogger(__name__)

connect_args = {}
engine_kwargs = {"echo": False}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from .models import Base, Vehicle, VehicleImage, CreativeBrief, CustomerLead, TestDrive
    try:
        Base.metadata.create_all(bind=engine)
        # Ensure new columns exist on customer_leads table
        with engine.begin() as conn:
            from sqlalchemy import text
            cols_to_add = [
                ("phone_declined", "BOOLEAN DEFAULT FALSE"),
                ("honorific_preference", "VARCHAR(20)"),
                ("budget_min", "DOUBLE PRECISION"),
                ("budget_max", "DOUBLE PRECISION"),
                ("active_filters", "JSON DEFAULT '{}'::json"),
                ("conversation_state_json", "JSON DEFAULT '{}'::json"),
            ]
            for col_name, col_type in cols_to_add:
                try:
                    conn.execute(text(f"ALTER TABLE customer_leads ADD COLUMN IF NOT EXISTS {col_name} {col_type};"))
                except Exception as ex:
                    logger.debug(f"Column {col_name} check/migration note: {ex}")
        logger.info(f"Connected to database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise
