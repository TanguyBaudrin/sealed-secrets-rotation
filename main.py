from kubernetes import config
import kubernetes.client
from pprint import pprint
from kubernetes.client.rest import ApiException


def main():
    
    print("I'm here")
    # Configs can be set in Configuration class directly or using helper utility
    configuration = config.load_kube_config()
    
    print("I'm here")

    with kubernetes.client.ApiClient(configuration) as api_client:
        custom_objects_api = kubernetes.client.CustomObjectsApi(api_client)
        core_api = kubernetes.client.CoreV1Api(api_client)

        namespaces = core_api.list_namespace()
        
        for namespace in namespaces.items:
            try:
                sealed_secrets=custom_objects_api.list_namespaced_custom_object(group="bitnami.com", version="v1alpha1", namespace=namespace.metadata.name, plural="sealedsecrets")
                for secret in sealed_secrets.get('items'):
                    pprint(secret)
            except ApiException as e:
                print("Exception when calling CustomObjectsApi->list_namespaced_custom_object: %s\n" % e)

main()