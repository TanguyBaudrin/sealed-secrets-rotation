from datetime import date, datetime
from kubernetes import config
import kubernetes.client
from pprint import pprint
from kubernetes.client.rest import ApiException
import os
import datetime

from rsa import PrivateKey

sealed_secrets_namespace=os.getenv("NAMESPACE", default="kube-system")

def main():
    
    # Configs can be set in Configuration class directly or using helper utility
    configuration = config.load_kube_config()

    with kubernetes.client.ApiClient(configuration) as api_client:
        custom_objects_api = kubernetes.client.CustomObjectsApi(api_client)
        core_api = kubernetes.client.CoreV1Api(api_client)

        namespaces = core_api.list_namespace()
        
        sealed_secrets_private_keys = core_api.list_namespaced_secret(namespace=sealed_secrets_namespace,label_selector="sealedsecrets.bitnami.com/sealed-secrets-key=active")

        last_private_key={}
        for private_key in sealed_secrets_private_keys.items:
            private_key_creation_date = private_key.metadata.creation_timestamp
            try:
                if last_private_key_creation_date <= private_key_creation_date:
                    last_private_key = private_key
            except NameError:     
                last_private_key = private_key

        pprint("Current active key: %s" % last_private_key)

        for namespace in namespaces.items:
            try:
                sealed_secrets=custom_objects_api.list_namespaced_custom_object(group="bitnami.com", version="v1alpha1", namespace=namespace.metadata.name, plural="sealedsecrets")
                for secret in sealed_secrets.get('items'):
                    pprint(secret)
            except ApiException as e:
                print("Exception when calling CustomObjectsApi->list_namespaced_custom_object: %s\n" % e)

main()