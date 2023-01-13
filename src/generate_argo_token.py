import base64
from pathlib import Path

from kubernetes import client, config

from config import NAME, NAMESPACE

config.load_kube_config()


def get_token(name: str, namespace: str) -> str:
    """Gets the token value from the specified service account name and namespace

    Args:
        name (str): Argo service account name
        namespace (str): Argo namespace

    Returns:
        str: Token value
    """
    v1 = client.CoreV1Api()
    sa_resource = v1.read_namespaced_service_account(name=name, namespace=namespace)
    token_resource_name = [s for s in sa_resource.secrets if "token" in s.name][0].name
    secret = v1.read_namespaced_secret(name=token_resource_name, namespace=namespace)
    btoken = secret.data["token"]
    token = base64.b64decode(btoken).decode()

    return token


if __name__ == "__main__":
    token = get_token(NAME, NAMESPACE)

    filepath = Path("argo_token")
    with filepath.open("w") as f:
        f.write(token)
