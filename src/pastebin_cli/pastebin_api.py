import xml.etree.ElementTree as ET

import requests


def parse_paste(node: ET.Element):
    """
    Parses a single paste given an XML node
    """
    record = {attr.tag: attr.text for attr in node}
    return record


def parse_paste_list(xml_text: str):
    """
    Parses a list of pastes in XML format

    Sample:
        <paste>
            <paste_key>k0u6MEE2</paste_key>
            <paste_date>1366760895</paste_date>
            <paste_title>How to cache a function</paste_title>
            <paste_size>436</paste_size>
            <paste_expire_date>0</paste_expire_date>
            <paste_private>0</paste_private>
            <paste_format_long>Python</paste_format_long>
            <paste_format_short>python</paste_format_short>
            <paste_url>https://pastebin.com/k0u6MEE2</paste_url>
            <paste_hits>237</paste_hits>
        </paste>
        <paste>
        ...

    :param xml_text: The XML text containing the pastes information
    """
    xml_text = f"<pastes>{xml_text}</pastes>"
    root = ET.fromstring(xml_text)
    pastes = [parse_paste(paste) for paste in root.findall("paste")]
    return pastes


class PastebinAPI:
    def __init__(self, api_dev_key: str, api_user_key: str):
        self.api_dev_key = api_dev_key
        self.api_user_key = api_user_key
        self.url = "https://pastebin.com/api/api_post.php"
        self.session = requests.Session()

    def ls(self, api_results_limit: int = None) -> requests.Response:
        payload = {
            "api_dev_key": self.api_dev_key,
            "api_user_key": self.api_user_key,
            "api_option": "list",
        }
        if api_results_limit is not None:
            payload["api_results_limit"] = api_results_limit

        resp = self.session.post(self.url, data=payload)
        return resp

    def get(self, api_paste_key: str) -> requests.Response:
        payload = {
            "api_dev_key": self.api_dev_key,
            "api_user_key": self.api_user_key,
            "api_option": "show_paste",
            "api_paste_key": api_paste_key,
        }
        resp = self.session.post(self.url, data=payload)
        return resp

    def put(
        self,
        content: str,
        name: str = None,
        syntax: str = None,
        privacy: int = 2,
        expiry: str = None,
        folder: str = None,
    ):
        """Create a new paste"""
        payload = {
            "api_dev_key": self.api_dev_key,
            "api_user_key": self.api_user_key,
            "api_option": "paste",
            "api_paste_code": content,
            "api_paste_name": name,
            "api_paste_format": syntax,
            "api_paste_private": privacy,
            "api_paste_expire_date": expiry,
            "api_folder_key": folder,
        }
        resp = self.session.post(self.url, data=payload)
        return resp
