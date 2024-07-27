from common.models import Base
from domain.models import (
    Configuration,
    ConfigurationSnapshot,
)
from faas.models import (
    User, UserSnapshot,
    Email, EmailSnapshot,
    Phone, PhoneSnapshot,
)

mapper_classes: tuple[type[Base], ...]
mapper_classes = (
    User, UserSnapshot,
    Email, EmailSnapshot,
    Phone, PhoneSnapshot,
    Configuration,
    ConfigurationSnapshot,
)
