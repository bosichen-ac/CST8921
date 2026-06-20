import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, StaticWebsite

ACCOUNT = os.environ["STORAGE_ACCOUNT_NAME"]
account_url = f"https://{ACCOUNT}.blob.core.windows.net"

cred = DefaultAzureCredential()
service = BlobServiceClient(account_url, credential=cred)

service.set_service_properties(
    static_website=StaticWebsite(
        enabled=True,
        index_document="index.html",
        error_document404_path="404.html",   # <-- SEE WARNING BELOW
    )
)
print("Static website hosting enabled.")
