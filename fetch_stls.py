from onshape_client.client import Client
from onshape_client.onshape_url import OnshapeElement
import json
import warnings

### Authentication
# API keys
access = "ACCESS"
secret = "SECRET"

base = "https://cad.onshape.com"

client = Client(configuration={"access_key": access, "secret_key": secret})

### Select CAD model
# Onshape URL
url = "URL"

element = OnshapeElement(url)

### Extract model parts
# List-of-parts endpoint
endpoint = "/api/parts/d/did/w/wid/e/eid/"

endpoint = endpoint.replace("did", element.did)
endpoint = endpoint.replace("wid", element.wvmid)
endpoint = endpoint.replace("eid", element.eid)

method = "GET"

params = {}
payload = {}
headers = {
    "Accept": "application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1",
    "Content-Type": "application/json",
}

response = client.api_client.request(
    method, url=base + endpoint, query_params=params, headers=headers, body=payload
)

# Parse JSON response
response_json = json.loads(response.data)

# Extract parts and store them in list
parts = []
for dictionary in response_json:
    if "partId" in dictionary:
        parts.append(str(dictionary["partId"]))

# Extract material names
materials = []
for i in range(len(parts)):
    materials.append(str((response_json[i]["material"]["id"])))

# Merge lists into part:material dictionary
components = dict(zip(parts, materials))

### GET MATERIALS?

### Download STL file for each part
def exportPartSTL(url, partId, filename):
    endpoint = "/api/parts/d/did/w/wid/e/eid/partid/" + partId + "/stl"

    element = OnshapeElement(url)

    method = "GET"

    params = {"units": "millimeter"}
    payload = {}
    headers = {
        "Accept": "application/vnd.onshape.v1+octet-stream",
        "Content-Type": "application/json",
    }

    endpoint = endpoint.replace("did", element.did)
    endpoint = endpoint.replace("wid", element.wvmid)
    endpoint = endpoint.replace("eid", element.eid)

    response = client.api_client.request(
        method, url=base + endpoint, query_params=params, headers=headers, body=payload
    )

    with open(filename, "wb") as f:
        f.write(response.data.encode())


# Catch and ignore UserWarning
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)

    for partId, material in components.items():
        # print(partId, material)
        exportPartSTL(url, partId, partId + ".stl")
