import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class EmailService:
    def __init__(self):
        """Initialize EmailService with configuration from settings"""
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.sender_email = settings.sender_email
        self.verification_url = settings.verification_base_url

    async def send_verification_email(self, recipient_email, token):
        """
        Send verification email with a token link to the user (async version)
        
        Args:
            recipient_email (str): User's email address
            token (str): Verification token
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # Для совместимости с существующим кодом оставляем асинхронный метод,
        # но внутри него вызываем синхронную реализацию
        return self.send_verification_email_sync(recipient_email, token)
        
    def send_verification_email_sync(self, recipient_email, token):
        """
        Send verification email with a token link to the user (sync version for Celery)
        
        Args:
            recipient_email (str): User's email address
            token (str): Verification token
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        verification_link = f"{self.verification_url}?token={token}"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = "Verify Your Email Address"
        
        # Create HTML content with verification link
        html = f"""
        <html>
            <body>
                <h2>Email Verification</h2>
                <p>Thank you for registering. Please click the link below to verify your email address:</p>
                <p><a href="{verification_link}">Verify Email</a></p>
                <p>Or copy and paste this URL into your browser:</p>
                <p>{verification_link}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't request this verification, please ignore this email.</p>
            </body>
        </html>
        """
        
        message.attach(MIMEText(html, "html"))
        
        try:
            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            
            # Send email
            server.send_message(message)
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
