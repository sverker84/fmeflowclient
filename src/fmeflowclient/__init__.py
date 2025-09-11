import requests
from typing import List, Dict, Any
from typing import Optional

class FMEFlowClient:
    '''
    FMEFlowClient provides a Python interface for interacting with the FME Flow REST API.
    This client allows you to authenticate with an FME Flow server, list repositories, retrieve all workspaces,
    run workspaces with parameters, and check the status of submitted jobs.
    '''
    def __init__(self, base_url: str, token: str, verify_ssl: bool = True) -> None:
        """
        Initializes the FME Flow client.

        Args:
            base_url (str): The base URL of the FME Flow server.
            token (str): The authentication token for FME Flow.
            verify_ssl (bool, optional): Whether to verify SSL certificates. Defaults to True.
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'fmetoken token={token}',
            'Accept': 'application/json'
        }
        self.verify_ssl = verify_ssl

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Sends an HTTP request to the FME Flow REST API.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint.
            **kwargs: Additional arguments to pass to the requests.request method.

        Returns:
            Any: The JSON-decoded response from the API.

        Raises:
            requests.HTTPError: If the HTTP request fails.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method,
            url,
            headers=self.headers,
            verify=self.verify_ssl,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    def list_repositories(self) -> Dict[str, Any]:
        """
        Lists all repositories in FME Flow.

        Returns:
            Dict[str, Any]: The response containing repository information.

        Raises:
            requests.HTTPError: If the HTTP request fails.
        """
        return self._request("GET", "/fmerest/v3/repositories")
    
    def list_all_workspaces(self) -> List[Dict[str, Any]]:
        """
        Retrieves all workspaces across all repositories.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a workspace.

        Raises:
            requests.HTTPError: If an HTTP request to the FME Flow REST API fails.
        """
        repositories: Dict[str, Any] = self.list_repositories()
        all_workspaces: List[Dict[str, Any]] = []
        for repo in repositories.get('items', []):
            repo_name: Optional[str] = repo.get('name')
            if repo_name:
                workspaces: List[Dict[str, Any]] = self._request(
                    "GET",
                    f"/fmerest/v3/repositories/{repo_name}/workspaces"
                ).get('items', [])
                all_workspaces.extend(workspaces)
        return all_workspaces

    def run_workspace(
        self,
        repository: str,
        workspace: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Runs a workspace with optional parameters.

        Args:
            repository (str): The name of the repository.
            workspace (str): The name of the workspace.
            parameters (Optional[Dict[str, Any]], optional): Parameters to pass to the workspace. Defaults to None.

        Returns:
            Any: The response from the API after submitting the workspace.

        Raises:
            requests.HTTPError: If the HTTP request fails.
        """
        payload = {
            "parameters": parameters or {}
        }
        return self._request(
            "POST",
            f"/fmerest/v3/transformations/submit/{repository}/{workspace}",
            json=payload
        )

    def get_job_status(self, job_id: str) -> Any:
        """
        Gets the status of a job by job ID.

        Args:
            job_id (str): The ID of the job.

        Returns:
            Any: The response containing the job status.

        Raises:
            requests.HTTPError: If the HTTP request fails.
        """
        return self._request(
            "GET",
            f"/fmerest/v3/transformations/jobs/{job_id}"
        )
