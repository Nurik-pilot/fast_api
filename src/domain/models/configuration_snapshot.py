from common.models import Snapshot


class ConfigurationSnapshot(Snapshot):
    __plural = 'configuration_snapshots'
    """
    Service global configuration
    """
    __tablename__ = f'domain_{__plural}'
