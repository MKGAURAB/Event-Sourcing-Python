import photonpump

from domain.model.event import Event
from domain.model.issue_closed import IssueClosed
from domain.model.issue_created import IssueCreated
from domain.model.issue_id import IssueId
from domain.model.issue_in_progress import IssueInProgress
from domain.model.issue_reopened import IssueReopened

from domain.model.issue_repository import IssueRepository
from domain.model.issue import Issue
from domain.model.issue_resolved import IssueResolved


class EventStoreIssueRepository(IssueRepository):
    def __init__(self, username: str, password: str):
        self._client = photonpump.connect(username=username, password=password)
        self._connected = False

    async def save(self, issue: Issue) -> bool:
        await self._check_connection()
        stream_name = self._create_stream_name(issue.issue_id)

        for event in issue.events:
            await self._client.publish_event(stream_name, event.type,
                                             event.encode())

        return True

    async def _check_connection(self):
        if not self._connected:
            await self._client.connect()
            self._connected = True

    def _create_stream_name(self, issue_id: IssueId) -> str:
        return f'issues-{issue_id.value}'

    async def find_by_id(self, issue_id: IssueId) -> Issue:
        await self._check_connection()

        stream_name = self._create_stream_name(issue_id)
        issue = Issue(issue_id)
        async for event in self._client.iter(stream=stream_name, from_event=0):
            await self._reconstruct_from_event(event, issue)

        issue.clear_events()

        return issue

    async def _reconstruct_from_event(self, event, issue):
        domain_event = await self.convert_to_domain_event(event)
        issue.reconstruct_from_event(domain_event)

    @staticmethod
    async def convert_to_domain_event(event) -> Event:
        event_types = {
            'IssueCreated': IssueCreated,
            'IssueClosed': IssueClosed,
            'IssueInProgress': IssueInProgress,
            'IssueReopened': IssueReopened,
            'IssueResolved': IssueResolved
        }
        converted = event.json()
        print(converted, event.type)
        return event_types[event.type](**converted)