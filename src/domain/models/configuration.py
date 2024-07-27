from common.models import Entity


class Configuration(Entity):
    __plural = 'configurations'
    """
    Service global configuration
    """
    __tablename__ = f'domain_{__plural}'
