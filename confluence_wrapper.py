import json
import os

import requests
from requests.auth import HTTPBasicAuth

from confluence_page import ConfluencePage

CONFLUENCE_BASE = os.getenv("CONFLUENCE_BASE")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
CONFLUENCE_PASS = os.getenv("CONFLUENCE_PASS")


def find_page_id(page_title):
    response = requests.get(
        url=CONFLUENCE_BASE + "/content",
        params={"title": page_title, "spaceKey": "AD", "expand": "history"},
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_PASS),
    )
    json_response = response.json()
    return json_response["results"][0]["id"]


def retrieve_page_contents(confluence_page_id):
    response = requests.get(
        url=CONFLUENCE_BASE + f"/content/{confluence_page_id}",
        params={"expand": "body.storage,version,space"},
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_PASS),
    )
    json_response = response.json()
    title = json_response["title"]
    space = json_response["space"]["key"]
    content = json_response["body"]["storage"]["value"]
    version = json_response["version"]["number"]
    return title, space, content, version


def find_confluence_page(confluence_page_title):
    page_id = find_page_id(confluence_page_title)
    title, space, content, version = retrieve_page_contents(page_id)
    return ConfluencePage(
        page_id=page_id, title=title, space=space, version=version, content=content
    )


def update_content_in_confluence(confluence_page, new_content):
    return requests.put(
        url=CONFLUENCE_BASE + f"/content/{confluence_page.page_id}",
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_PASS),
        data=json.dumps(
            {
                "body": {
                    "storage": {"value": new_content, "representation": "storage"}
                },
                "id": confluence_page.page_id,
                "title": confluence_page.title,
                "space": {"key": confluence_page.space},
                "type": "page",
                "version": {"number": confluence_page.version + 1},
            }
        ),
    )
