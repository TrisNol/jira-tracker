from typing import List, Optional, Union

from atlassian import Jira


class JiraClient:
    """
    Internal wrapper around atlassian-python-api Jira.

    It preserves the SDK interface by delegating unknown attributes/methods,
    and overrides jql() for Jira Cloud to use the supported v3 search API.
    """

    def __init__(self, url: str, username: str, password: str):
        self._client = Jira(url=url, username=username, password=password)

    def __getattr__(self, name):
        return getattr(self._client, name)

    def jql(
        self,
        jql: str,
        fields: Union[str, List[str]] = "*all",
        start: int = 0,
        limit: Optional[int] = None,
        expand: Optional[str] = None,
        validate_query: Optional[str] = None,
    ):
        params = {
            "jql": jql,
            "startAt": int(start),
        }

        if limit is not None:
            params["maxResults"] = int(limit)
        if fields is not None:
            params["fields"] = (
                ",".join(fields) if isinstance(fields, (list, tuple, set)) else fields
            )
        if expand is not None:
            params["expand"] = expand
        if validate_query is not None:
            params["validateQuery"] = validate_query

        search_url = f"{self._client.url.rstrip('/')}/rest/api/3/search/jql"
        response = self._client._session.get(
            search_url,
            params=params,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()
