from datetime import timedelta

import factory
from factory.django import DjangoModelFactory
from django.db.models import signals
from django.utils import timezone

from ..models import Event


class EventWithSignalsFactory(DjangoModelFactory):

    class Meta:
        model = Event

    title = "Test Event"
    start_date = timezone.now() + timedelta(days=10)
    end_date = timezone.now() + timedelta(days=11)
    sign_up = True

    start_registration_at = timezone.now() - timedelta(days=1)
    end_registration_at = timezone.now() + timedelta(days=9)
    sign_off_deadline = timezone.now() + timedelta(days=8)


@factory.django.mute_signals(signals.post_save)
class EventFactory(EventWithSignalsFactory):
    pass
