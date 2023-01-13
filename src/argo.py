import base64
from pathlib import Path

from hera import Workflow, WorkflowService
from kubernetes import client, config

# set globals
HOST = "https://localhost:2746"
NAME = "argo-server"
NAMESPACE = "argo"


def generate_token(name: str = NAME, namespace: str = NAMESPACE) -> str:
    """Gets the token value from the specified service account name and namespace

    Args:
        name (str): Argo service account name
        namespace (str): Argo namespace

    Returns:
        str: Token value
    """
    argo_token = Path("argo_token").read_text()
    if argo_token:
        return argo_token
    else:
        v1 = client.CoreV1Api()
        sa_resource = v1.read_namespaced_service_account(name=name, namespace=namespace)
        token_resource_name = [s for s in sa_resource.secrets if "token" in s.name][
            0
        ].name
        secret = v1.read_namespaced_secret(
            name=token_resource_name, namespace=namespace
        )
        btoken = secret.data["token"]
        token = base64.b64decode(btoken).decode()

        return token


class MyWorkflowService(WorkflowService):
    """Internal service wrapper around Hera's WorkflowService to support consistency in auth token generation"""

    def __init__(self, host: str = HOST, token: str = generate_token()):
        super(MyWorkflowService, self).__init__(
            host=host, token=token, namespace=NAMESPACE, verify_ssl=False
        )


class MyWorkflow(Workflow):
    """Internal Workflow wrapper around Hera's Workflow to support consistent MyWorkflowService usage"""

    def __init__(
        self,
        name: str,
        service: WorkflowService = MyWorkflowService(),
        parallelism: int = 50,
        **kwargs
    ):
        super(MyWorkflow, self).__init__(
            name, service=service, parallelism=parallelism, **kwargs
        )
