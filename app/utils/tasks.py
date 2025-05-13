from app.repositories.user_repository import UserRepository
from app.utils.celery import celery
from app.services.email_service import EmailService


import logging

logger = logging.getLogger(__name__)

@celery.task
def send_verification_email_task(recipient_email: str, token: str):
    """
    Celery task to send verification email
    
    Args:
        recipient_email (str): User's email address to send verification to
        token (str): Verification token
        
    Returns:
        bool: Result of email sending operation
    """
    # Асинхронные задачи в Celery не поддерживаются напрямую,
    # поэтому используем синхронный код для Email Service
    email_service = EmailService()
    # Возвращаем результат без await
    return email_service.send_verification_email_sync(recipient_email, token)


@celery.task(name="check_user_status_task")
def check_user_status_task(user_id:int):
    try: 
        # Import UserService here to avoid circular imports
        from app.services.user_service import UserService
        from app.db import get_db_sync
        
        # Get a db session and create user_service directly using синхронный метод
        db = next(get_db_sync())
        user_repo = UserRepository(db)
        user_service = UserService(db, user_repo)
        
        if not user_service.is_user_active_sync(user_id):
            user_service.delete_user_sync(user_id)
            return "deleted"
        return "not deleted"
    except Exception as e:
        logger.error(f"Error getting user by ID {user_id}: {str(e)}")
        return None

@celery.task(name="notify_all_admins")
def notify_all_admins(user_id:int order_id:int):
    pass