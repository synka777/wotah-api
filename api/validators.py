from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if user:
            user_attributes = [user.username, user.email]
            for attr in user_attributes:
                if attr and attr.lower() in password.lower():
                    raise ValidationError("Password cannot contain parts of your username or email.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

    def get_help_text(self):
        return "Your password must be at least 8 characters long, contain one uppercase letter, one number, and one special character."
