from enum import Enum


class IssueStatus(Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    IN_PROGRESS = 'IN_PROGRESS'
    REOPENED = 'REOPENED'
    RESOLVED = 'RESOLVED'