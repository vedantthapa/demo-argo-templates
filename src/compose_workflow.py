from hera import Parameter, Task, TemplateRef, Workflow

from argo import MyWorkflow
from tasks import say

with MyWorkflow("hera-demo-", generate_name=True) as w:
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
