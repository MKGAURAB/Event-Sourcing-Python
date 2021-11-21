from datetime import datetime

from domain.model.event import Event


class IssueCreated(Event):
    def __init__(self,
                 aggregate_id: str,
                 occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(aggregate_id, occurred_at)