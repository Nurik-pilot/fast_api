from common.models import Snapshot


class EmailSnapshot(Snapshot):
    __tablename__ = 'faas_email_snapshots'
