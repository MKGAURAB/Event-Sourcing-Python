from uuid import UUID
from fastapi import FastAPI
from domain.model.issue import Issue
from domain.model.issue_id import IssueId
from infrastructure.model.event_store_issue_repository import EventStoreIssueRepository

from settings import EVENT_STORE_PASSWORD, EVENT_STORE_USERNAME

app = FastAPI()
evetn_store = EventStoreIssueRepository(username=EVENT_STORE_USERNAME,
                                        password=EVENT_STORE_PASSWORD)


async def save(issue: Issue):
    await evetn_store.save(issue)


async def find(issue_id: str):
    return await evetn_store.find_by_id(IssueId(issue_id))


@app.get("/issue/create")
async def create_issue() -> str:
    try:
        issue = Issue.create(IssueId())
        await evetn_store.save(issue)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return f'An issue was successfully created with id: {issue.issue_id.value}'


@app.post("/issue/close/{issue_id}")
async def close_issue(issue_id: UUID) -> str:
    try:
        issue = await find(str(issue_id))
        issue.close()
        await evetn_store.save(issue)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return f'Successfully closed issue: {issue_id}'


@app.post("/issue/reopen/{issue_id}")
async def reopen_issue(issue_id: UUID) -> str:
    try:
        issue = await find(str(issue_id))
        issue.reopen()
        await evetn_store.save(issue)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return f'Successfully reopened issue: {issue_id}'


@app.post("/issue/resolve/{issue_id}")
async def resolve_issue(issue_id: UUID) -> str:
    try:
        issue = await find(str(issue_id))
        print(issue.status)
        issue.resolve()
        await evetn_store.save(issue)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return f'Successfully resolved issue: {issue_id}'


@app.post("/issue/inprogress/{issue_id}")
async def progress_issue(issue_id: UUID) -> str:
    try:
        issue = await find(str(issue_id))
        issue.issue_in_progress()
        await evetn_store.save(issue)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return f'Successfully started issue: {issue_id}'


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=5000,
                log_level="debug",
                reload=True)
