from fastapi_mail import FastMail, MessageSchema
from config import mail_config
from jinja2 import Environment, FileSystemLoader

async def send_verification_email(email: str, token: str, name: str = "User"):
    verification_link = f"http://127.0.0.1:8000/api/email/verify?token={token}"

    env = Environment(loader=FileSystemLoader("backend/templates"))
    template = env.get_template("onboarding_email.html")
    body = template.render(email=email, verification_link=verification_link, name=name)

    message = MessageSchema(
        subject="Verification",
        recipients=[email],
        cc=["support@example.com"],
        bcc=["audit@example.com"],
        reply_to=["noreply@example.com"],
        body=body,
        subtype="html"
)

    ##Send the email
    print(f"Verification email queued for {email} with token {token}")
    try:
        fm = FastMail(mail_config)
        await fm.send_message(message)
        print(f"Verification email sent to {email} in mailHog")
    except Exception as e:
        print(f"Failed to send email: {e}")


    

    fm = FastMail(mail_config)
    await fm.send_message(message)
