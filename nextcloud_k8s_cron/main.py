from loguru import logger
from kubernetes import client
from kubernetes import config as kube_config
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

from nextcloud_k8s_cron.config import Config

config = Config()


def get_nextcloud_pod() -> str:
    with client.ApiClient() as api_client:
        api_instance = client.CoreV1Api(api_client)
        try:
            pod_list = api_instance.list_namespaced_pod(namespace=config.namespace)
        except ApiException as e:
            logger.error(
                "Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e
            )

        for pod in pod_list.items:
            if pod.metadata.labels.get("app") == config.pod_label:
                return pod.metadata.name


def run_cron_jon(nextcloud_pod: str) -> str:
    with client.ApiClient() as api_client:
        api_instance = client.CoreV1Api(api_client)
        try:
            response = stream(
                api_instance.connect_get_namespaced_pod_exec,
                name=nextcloud_pod,
                namespace=config.namespace,
                command=config.command,
                stdout=True,
            )
            return response
        except ApiException as e:
            logger.error(
                "Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: %s\n"
                % e
            )


def main():
    logger.info("Starting cron job.")
    logger.info(f"Namespace: {config.namespace}; label: {config.pod_label}")

    kube_config.load_kube_config()

    nextcloud_pod = get_nextcloud_pod()
    logger.info(f"Found nextcloud pod: {nextcloud_pod}")

    logger.info(f"Output: {run_cron_jon(nextcloud_pod)}")
