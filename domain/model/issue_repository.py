import abc

from domain.model.issue_id import IssueId
from domain.model.issue import Issue


class IssueRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'save') and callable(subclass.save)
                and hasattr(subclass, 'find_by_id')
                and callable(subclass.find_by_id) or NotImplemented)

    def save(self, issue: Issue) -> bool:
        raise NotImplementedError

    def find_by_id(self, issue_id: IssueId) -> Issue:
        raise NotImplementedError