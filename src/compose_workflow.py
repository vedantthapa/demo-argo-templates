from hera import Task, Workflow, WorkflowService

from config import NAMESPACE, TOKEN
from tasks import fail_random, say

ws = WorkflowService(
    host="https://localhost:2746", verify_ssl=False, token=TOKEN, namespace=NAMESPACE
)


with Workflow("diamond-workflow-", service=ws, generate_name=True) as w:
    a = Task("a", say, ["This is task A!"])
    b = Task("b", say, ["This is task B!"])
    c = Task("c", fail_random)
    d = Task("d", say, ["This is task D!"])

    a >> [b, c] >> d

w.create()
