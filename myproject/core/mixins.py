from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.core.mail import send_mail, get_connection
from anymail.signals import tracking
from django.dispatch import receiver


class EmailMixin:
    email_to = None
    email_context_name = None
    email_template_name = None
    email_from = settings.DEFAULT_FROM_EMAIL
    email_subject = ''

    def send_mail(self):
        """
        Método para envio de email seguindo padrão send_mail do Django.
        """
        subject = self.email_subject
        from_ = self.email_from
        to = self.get_email_to()
        template_name = self.get_email_template_name()
        context = self.get_email_context_data()
        body = render_to_string(template_name, context)
        if (mailgunBackend(subject, body, from_, to)):
            return True
        elif (sendGridBackend(subject, body, from_, to)):
            return True
        elif (amazon_ses(subject, body, from_, to)):
            return True

    def get_email_template_name(self):
        if self.email_template_name:
            return self.email_template_name
        return None

    def get_email_context_data(self):
        context = self.get_context_data()
        return context

    def get_email_to(self):
        email_to = self.request.POST.get('email_to')
        if email_to:
            return email_to
        return ''


class MissingConnectionException(Exception):
    pass


def get_connection(label=None, **kwargs):
    if label is None:
        label = getattr(settings, 'EMAIL_CONNECTION_DEFAULT', None)

    try:
        connections = getattr(settings, 'EMAIL_CONNECTIONS')
        options = connections[label]
    except KeyError as AttributeError:
        raise MissingConnectionException(
            'Settings for connection "%s" were not found' % label)

    options.update(kwargs)
    return django.core.mail.get_connection(**options)


def smtpBackend(subject, body, from_, to):
    # SMTP backend
    smtp_backend = get_connection('django.core.mail.backends.smtp.EmailBackend')
    return send_mail(subject, body, from_, [to],
                     connection=smtp_backend)


def sendGridBackend(subject, body, from_, to):
    # Send grid
    sendgrid_backend = get_connection('anymail.backends.sendgrid.EmailBackend', api_key="asdfsadfl")
    return send_mail(subject, body, from_, [to],
                     connection=sendgrid_backend)


# mailgun
def mailgunBackend(subject, body, from_, to):
    mailgun_backend = get_connection('anymail.backends.mailgun.EmailBackend',
                                     api_key='asdfasdf54325rdflkdjlasdkf')
    return send_mail(subject, body, from_, [to],
                     connection=mailgun_backend)


# amazon ses
def amazon_ses(subject, body, from_, to):
    amazon_ses = get_connection("anymail.backends.amazon_ses.EmailBackend", api_key="asdflkj245troifljlkfjd")
    return send_mail(subject, body, from_, [to],
                     connection=amazon_ses)
