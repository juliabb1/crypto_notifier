import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Account, PlatformType
from app.services.base_service import BaseService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


class AccountService(BaseService):
    
    def get_or_create_account(self, platform: PlatformType, platform_id: str) -> Account:
        with self.get_session() as db:
            # Check if account already exists
            existing_account = db.query(Account).filter(
                Account.platform == platform,
                Account.platformId == str(platform_id)
            ).first()
            
            if existing_account:
                logging.info(f"Found existing {platform.value} account for {platform_id}")
                return existing_account
            
            # Create new account if it doesn't exist
            new_account = Account(
                platform=platform,
                platformId=str(platform_id),
                created_at=datetime.now()
            )
            db.add(new_account)
            db.flush()  # Get the ID before committing
            logging.info(f"Created new {platform.value} account for {platform_id}")
            return new_account
    
    def get_account(self, platform: PlatformType, platform_id: str) -> Account | None:
        with self.get_session() as db:
            return db.query(Account).filter(
                Account.platform == platform,
                Account.platformId == str(platform_id)
            ).first()
