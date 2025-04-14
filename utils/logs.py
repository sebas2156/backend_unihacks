from sqlalchemy.orm import Session
from models.logs import Logs  # Asegúrate de importar el modelo Log

def log_action(db: Session, action_type: str, endpoint: str, user_id: int, details: str = None):
    log = Logs(action_type=action_type, endpoint=endpoint, user_id=user_id, details=details)
    db.add(log)
    db.commit()
    db.refresh(log)