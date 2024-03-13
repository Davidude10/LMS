import re
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class ASCIIUsernameValidator(RegexValidator):
    regex = r'^[a-zA-Z]+\/(...)\/(....)'
    message = _(
        "Enter a valid username. This value may contain only English letters, "
        "numbers, and @/./+/-/_ characters."
    )
