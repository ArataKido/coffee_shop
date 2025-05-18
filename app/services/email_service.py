import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

    def get_smtp(self):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            return server
        except Exception as e:
            print(f"Error while creating server: {e}")
            return None

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
            server = self.get_smtp()
            # Send email
            server.send_message(message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e!s}")
            return False
        finally:
            server.quit()

    def send_batch_order_notification_sync(self, admin_emails: list[str], order_id: int, user_id: int):
        """
        Send batch notification emails to admins about a new order.

        Args:
            admin_emails (list): List of admin email addresses
            order_id (int): ID of the new order
            user_id (int): ID of the user who created the order

        Returns:
            int: Number of emails sent successfully

        """
        subject = "New Order Notification"
        sent_count = 0  # Counter for successfully sent emails
        admin_emails = ["user12@coffee.com", "user2@coffee.com"]
        for recipient_email in admin_emails:
            if not recipient_email:  # Check for empty email
                print("Skipping empty email address.")
                continue

            # Create a new message for each recipient
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject

            # Create email body
            body = f"""
            <html>
                <body>
                    <h2>New Order Notification</h2>
                    <p>Details of the new order:</p>
                    <p>User with id {user_id} created order: {order_id}</p>
                </body>
            </html>
            """

            message.attach(MIMEText(body, "html"))

            try:
                server = self.get_smtp()  # Create SMTP connection
                print(f"Sending email to: {recipient_email}")  # Log the recipient
                server.send_message(message)  # Send the email
                sent_count += 1  # Increment the counter for successfully sent emails
            except Exception as e:
                print(f"Failed to send email to {recipient_email}: {e!s}")
            finally:
                server.quit()  # Close the connection after each send

        return sent_count  # Return the number of successfully sent emails
