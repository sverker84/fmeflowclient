# fmeflowclient
fmeflowclient is a simple Python 3.x library for communicating with an FME Flow server using its rest API.

## Install fmeflowclient
fmeflowclient is available on PyPI:

```bash
$ python -m pip install fmeflowclient
```

fmeflowclient is currently develop on Python 3.11.

**This is not an offical client**

## Read The Docs
https://fmeflowclient.readthedocs.io

## Implemented API calls
### Automations
* list all workflows (fmecli.automations.all())
* list all tags (fmecli.automations.tags)

... and more not yet covered in the readme

## Sample usage
### Initialize the FME Flow API Client
```python
from fmeflowclient import FMEFlowClient
fmecli = FMEFlowClient("https://fmeflow-fqdn/", token="FMETOKENHERE")
```
### Get all workspace owners
```python

# Get a list of dictionaries of all workspaces
workspaces = fmecli.workspaces.all()

# Create a set of workspace owners
workspace_owners = {ws["userName"] for ws in workspaces}

print(workspace_owners)
```
### Healthcheck
```python
print(fmecli.healthcheck["status"])
```
