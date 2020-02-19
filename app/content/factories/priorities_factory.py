import factory.django

from ..models import Priority
from ..enums import UserClass, UserStudy


class PrioritiesFactory(factory.DjangoModelFactory):

    class Meta:
        model = Priority

    user_class = UserClass.first
    user_study = UserStudy.dataIng


