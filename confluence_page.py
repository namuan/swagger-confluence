import collections

from bs4 import BeautifulSoup

ConfluencePage = collections.namedtuple(
    "ConfluencePage", "page_id title space version content"
)


def update_all_tokens(html_content, swagger_doc_extractor):
    soup = BeautifulSoup(html_content, features="html.parser")
    for tag in soup.findAll("ac:structured-macro"):
        if tag.attrs["ac:name"] == "expand":
            uri = tag.findChild("ac:parameter")
            path, method = uri.text.split(";")
            api_doc = swagger_doc_extractor(path, method)
            api_doc_bs = BeautifulSoup(api_doc, features="html.parser")
            doc_tag = tag.findChild("ac:rich-text-body")
            doc_tag.clear()
            doc_tag.append(api_doc_bs)

    return soup.prettify(formatter="none")
