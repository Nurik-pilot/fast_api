from common.models import Snapshot


class UserSnapshot(Snapshot):
    __tablename__ = 'faas_user_snapshots'
