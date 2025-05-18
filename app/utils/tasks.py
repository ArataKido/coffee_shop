import logging

from app.repositories.user_repository import UserRepository
from app.services.email_service import EmailService
from app.utils.celery import celery

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
def check_user_status_task(user_id: int):
    try:
        # Import UserService here to avoid circular imports
        from app.db import get_db_sync
        from app.services.user_service import UserService

        # Get a db session and create user_service directly using синхронный метод
        db = next(get_db_sync())
        user_repo = UserRepository(db)
        user_service = UserService(db, user_repo)

        if not user_service.is_user_active_sync(user_id):
            user_service.delete_user_sync(user_id)
            return "deleted"
        return "not deleted"
    except Exception as e:
        logger.exception(f"Error getting user by ID {user_id}: {e!s}")
        return None


@celery.task(name="send_admin_order_notification")
def send_admin_order_notification(user_id: int, order_id: int):
    try:
        # Import UserService here to avoid circular imports
        from app.db import get_db_sync
        from app.services.user_service import UserService

        # Get a db session and create user_service directly using синхронный метод
        db = next(get_db_sync())
        user_repo = UserRepository(db)
        user_service = UserService(db, user_repo)
        email_service = EmailService()

        admin_emails = user_service.get_admin_emails_sync()
        email_service.send_batch_order_notification_sync(admin_emails=admin_emails, user_id=user_id, order_id=order_id)
    except Exception as e:
        logger.exception(f"Error getting user by ID {user_id}: {e!s}")
        return
