import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class EmailSender:
    """
    A class to handle sending emails via SMTP.
    """

    def __init__(
            self,
            sender_email: str,
            sender_password: str,
            smtp_server: Optional[str] = "smtp.gmail.com",
            smtp_port: Optional[int] = 587,
            sender_alias: Optional[str] = None
    ):
        """
        Initialize the EmailSender with SMTP configuration.

        Args:
            smtp_server (str): SMTP server address.
            smtp_port (int): SMTP server port.
            sender_email (str): The sender's email address.
            sender_password (str): The sender's email password.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_alias = sender_alias
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email: str, subject: str, body: str):
        """
        Send an email using the configured SMTP server.

        Args:
            recipient_email (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The body of the email.
        """
        # Create the email message
        message = MIMEMultipart()
        message["From"] = self.sender_email if not self.sender_alias else f"{self.sender_alias} <{self.sender_email}>"
        message["To"] = recipient_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "HTML"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient_email,  message.as_string())
            logging.info("Email sent successfully!")
        except Exception as e:
            logging.error(f"Error sending email: {e}")
        finally:
            server.quit()
