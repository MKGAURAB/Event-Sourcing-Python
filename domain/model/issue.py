from .aggregate import Aggregate, method_dispatch
from domain.model.event import Event
from domain.model.issue_closed import IssueClosed
from domain.model.issue_created import IssueCreated
from domain.model.issue_id import IssueId
from domain.model.issue_in_progress import IssueInProgress
from domain.model.issue_reopened import IssueReopened
from domain.model.issue_resolved import IssueResolved
from domain.model.issue_status import IssueStatus


class Issue(Aggregate):
    def __init__(self, issue_id: IssueId):
        super().__init__()
        self._issue_id = issue_id

    @property
    def status(self) -> IssueStatus:
        return self._status

    @property
    def issue_id(self) -> IssueId:
        return self._issue_id

    @method_dispatch
    def apply(self, event: Event):
        raise ValueError('Unknown event!')

    @classmethod
    def create(cls, issue_id: IssueId):
        issue = cls(issue_id)
        issue.record_event(IssueCreated(issue_id.value))
        return issue

    @apply.register(IssueCreated)
    def _(self, event: IssueCreated):
        self._status = IssueStatus.OPEN

    def issue_in_progress(self) -> None:
        if self.status == IssueStatus.OPEN or self.status == IssueStatus.REOPENED:
            self.record_event(IssueInProgress(self.issue_id.value))
        else:
            raise Exception(
                'Only Open and Reopend issues can be put in-progress')

    @apply.register(IssueInProgress)
    def _(self, event: IssueInProgress):
        self._status = IssueStatus.IN_PROGRESS

    def resolve(self) -> None:
        if self.status == IssueStatus.OPEN or self.status == IssueStatus.REOPENED or self.status == IssueStatus.IN_PROGRESS:
            self.record_event(IssueResolved(self.issue_id.value))
        else:
            raise Exception(
                'Only Open/Reopend/In-Progress issues can be resolved')

    @apply.register(IssueResolved)
    def _(self, event: IssueResolved):
        self._status = IssueStatus.RESOLVED

    def close(self) -> None:
        if self.status == IssueStatus.OPEN or self.status == IssueStatus.REOPENED or self.status == IssueStatus.IN_PROGRESS or self.status==IssueStatus.RESOLVED:
            self.record_event(IssueClosed(self.issue_id.value))
        else:
            raise Exception(
                'Only Open/Reopend/In-Progress issues can be closed')

    @apply.register(IssueClosed)
    def _(self, event: IssueClosed):
        self._status = IssueStatus.CLOSED

    def reopen(self) -> None:
        if self.status == IssueStatus.CLOSED or self.status==IssueStatus.RESOLVED:
            self.record_event(IssueReopened(self.issue_id.value))
        else:
            raise Exception('Only Closed issues can be re-opened')

    @apply.register(IssueReopened)
    def _(self, event: IssueReopened):
        self._status = IssueStatus.REOPENED