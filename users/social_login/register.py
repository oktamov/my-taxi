from users.models import User


def register_social_user(email, first_name=None, last_name=None):
    filtered_user_by_email = User.objects.filter(email=email).first()

    if filtered_user_by_email:
        return {
            "email": filtered_user_by_email.email,
            "full_name": filtered_user_by_email.full_name,
            "tokens": filtered_user_by_email.tokens,
        }
    else:
        user_data = {"email": email}
        user = User.objects.create_user(**user_data)
        return {"email": user.email, "tokens": user.tokens}
