from pathlib import Path

from jinja2 import Template
from prance import ResolvingParser

api_doc_file = Path("./templates/api_doc.j2").read_text()
api_doc_template = Template(api_doc_file)


def extract_api_docs(swagger_specs, uri_path, method):
    method_doc = swagger_specs.specification["paths"][uri_path.strip()][method.strip()]
    return api_doc_template.render(
        uri_path=uri_path, method=method, method_doc=method_doc
    )


def retrieve_swagger_doc(swagger_file):
    return ResolvingParser(url=swagger_file)
