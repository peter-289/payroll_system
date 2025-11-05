from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Boolean
from backend.database_setups.database_setup import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    token_type = Column(String(20), nullable=False, default='email_verification')  # 'email_verification' or 'password_reset'
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False, index=True)  # indexed for efficient cleanup
    is_used = Column(Boolean, default=False, nullable=False)

    # Relationship with user - tokens are deleted when user is deleted
    user = relationship("User", back_populates="tokens")