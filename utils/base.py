INVALID_NAMES = [
    'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password',
    'phone_number', 'field', 'section', 'setting', 'update', 'upgrade',
    'register', 'login', 'logout', 'signup', 'signin', 'signout', 'auth', 'users',
    'delete', 'edit', 'change', 'remove', 'posts', 'explore', 'detail', 'verify',
]


def send_sms(phone_number, message):
    "Send a sms to a phone number"
    print(f"\n{phone_number} - {message}\n")
