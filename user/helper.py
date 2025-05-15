from django.contrib.auth import get_user_model
from django.contrib import messages


User = get_user_model()


def validate_and_create_user(request, data):
    username = data.get("username", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    password1 = data.get("password1", "")
    password2 = data.get("password2", "")
    role = data.get("role", "")

    if not all([username, first_name, last_name, password1, password2]):
        return False, "All fields are required."

    if " " in username:
        return False, "Username cannot contain spaces."

    if len(password1) < 8:
        return False, "Password must be at least 8 characters long."

    if password1.strip() == "":
        return False, "Password cannot be all spaces."

    if password1 != password2:
        return False, "Passwords do not match."

    if User.objects.filter(username=username).exists():
        return False, "Username already taken."

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password1,
    )
    if role:
        user.role = role
        user.save()

    return True, user
