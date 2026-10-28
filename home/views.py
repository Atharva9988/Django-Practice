import logging

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, send_mail
from django.core.validators import validate_email
from django.shortcuts import render

logger = logging.getLogger(__name__)

MAX_EMAILS_PER_HOUR = 10


def _over_limit(user_id):
    key = f"send_email:{user_id}"
    cache.add(key, 0, timeout=3600)
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=3600)
        count = 1
    return count > MAX_EMAILS_PER_HOUR


@login_required
def send_email_view(request):
    context = {'page': 'Send Email'}
    if request.method == "POST":
        data = {k: request.POST.get(k, "").strip() for k in ("to_email", "subject", "message")}
        context["form_data"] = data
        try:
            validate_email(data["to_email"])
            if not data["subject"] or not data["message"]:
                raise ValidationError("Subject and message are required.")
            if len(data["subject"]) > 150 or len(data["message"]) > 5000:
                raise ValidationError("Subject or message is too long.")
            if _over_limit(request.user.pk):
                raise ValidationError("Too many emails sent. Try again later.")

            send_mail(data["subject"], data["message"], None, [data["to_email"]])
            context["success"] = f"Email sent to {data['to_email']}."
            context["form_data"] = {}
        except ValidationError as e:
            context["error"] = " ".join(e.messages)
        except (BadHeaderError, OSError):
            logger.exception("Email send failed for user %s", request.user.pk)
            context["error"] = "Could not send the email. Try again."
    return render(request, "home/send_email.html", context)