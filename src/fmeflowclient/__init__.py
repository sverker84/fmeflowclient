import requests
from typing import List, Dict, Any

class FMEFlowClient:
    def __init__(self, base_url, token):
        """
        Initialize the FME Flow client with base URL and token.
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'fmetoken token={token}',
            'Accept': 'application/json'
        }

    def list_repositories(self):
        """
        List all repositories in FME Flow.
        """
        url = f"{self.base_url}/fmerest/v3/repositories"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def list_all_workspaces(self) -> List[Dict[str, Any]]:
        """
        Retrieves all workspaces across all repositories.

        This method queries each repository and aggregates all workspace information into a single list.

        Returns:
            List[Dict[str, Any]]: 
                A list of dictionaries, each representing a workspace.

        Raises:
            requests.HTTPError: If an HTTP request to the FME Flow REST API fails.
        """
        repositories = self.list_repositories()
        all_workspaces: List[Dict[str, Any]] = []
        for repo in repositories.get('items', []):
            repo_name = repo.get('name')
            if repo_name:
                url = f"{self.base_url}/fmerest/v3/repositories/{repo_name}/workspaces"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                workspaces = response.json().get('items', [])
                for ws in workspaces:
                    all_workspaces.append(ws)
        return all_workspaces

    def run_workspace(self, repository, workspace, parameters=None):
        """
        Run a workspace with optional parameters.
        """
        url = f"{self.base_url}/fmerest/v3/transformations/submit/{repository}/{workspace}"
        payload = {
            "parameters": parameters or {}
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_job_status(self, job_id):
        """
        Get the status of a job by job ID.
        """
        url = f"{self.base_url}/fmerest/v3/transformations/jobs/{job_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
