import os
import pravega_client
import uuid

pravega_controller_uri = os.environ["PRAVEGA_CONTROLLER_URI"][6:]
pravega_scope = os.environ["PRAVEGA_SCOPE"]
pravega_stream = "litmus"
os.environ["pravega_client_auth_keycloak"] = os.environ["KEYCLOAK_SERVICE_ACCOUNT_FILE"]
os.environ["pravega_client_tls_cert_path"] = "/etc/ssl/certs/ca-certificates.crt"
manager = pravega_client.StreamManager(pravega_controller_uri, True, True)
reader_group_name = str(uuid.uuid4())
reader_group = manager.create_reader_group(reader_group_name, pravega_scope, pravega_stream)
reader = reader_group.create_reader("0")

while True:
    slice = await reader.get_segment_slice_async()
    for event in slice:
        try:
            str = event.data().decode("utf-8")
            print("Event data: %s" % str)
        except Exception as e:
            print("event data decode error: ", e)
    reader.release_segment(slice)
