from hera import Task, Workflow, WorkflowService, TemplateRef, Parameter

from config import NAMESPACE, TOKEN
from tasks import say

ws = WorkflowService(
    host="https://localhost:2746", verify_ssl=False, token=TOKEN, namespace=NAMESPACE
)


with Workflow("hera-demo-", service=ws, generate_name=True) as w:
    a = Task("a", say, ["This is task A!"])
    b = Task("b", say, ["This is task B!"])
    c = Task(
        "c",
        template_ref=TemplateRef(
            name="execute-script-template",
            template="process-git-artifacts",
        ),
        inputs=[Parameter(name="git-revision", value="main")],
    )
    d = Task("d", say, ["This is task D!"])

    a >> [b, c] >> d

w.create()
