from django.core.mail import send_mail


def send_confirmation_code(user):
    subject = 'Код подтверждения'
    message = f'{user.confirmation_code} - ваш код для авторизации на YaMDb'
    admin_email = 'Admin@YaMDb.ru',
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)
