
from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "dealgraphos.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    from .deal import Deal
    from .party import Party
    from .instrument import Instrument
    from .action import Action
    from .checklist import ChecklistItem
    from .document import Document
    from .risk import RiskFlag
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
