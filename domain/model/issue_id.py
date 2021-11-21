from __future__ import annotations
import uuid


class IssueId:
    def __init__(self, code=''):
        if code == '':
            self._value = uuid.uuid4()
        else:
            self._value = uuid.UUID(f'{code}')

    @property
    def value(self) -> str:
        return str(self._value)

    def equals(self, issue_id: IssueId) -> bool:
        return issue_id.value == self.value

    def __str__(self):
        return self.value