from argparse import ArgumentParser

from confluence_page import update_all_tokens
from confluence_wrapper import find_confluence_page, update_content_in_confluence
from swagger_reader import retrieve_swagger_doc, extract_api_docs


def parse_args():
    parser = ArgumentParser(description="Uploads Swagger API Snippets to Confluence.")
    parser.add_argument(
        "-s",
        type=str,
        required=True,
        dest="swagger",
        help="http link to swagger document",
    )
    parser.add_argument(
        "-p",
        type=str,
        required=True,
        dest="confluence",
        help="name of the confluence page to update",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    confluence_page = find_confluence_page(args.confluence)
    swagger_doc = retrieve_swagger_doc(args.swagger)
    updated_content = update_all_tokens(
        confluence_page.content,
        lambda path, method: extract_api_docs(swagger_doc, path, method),
    )
    response = update_content_in_confluence(confluence_page, updated_content)
    print('Response after updating content: {status_code}'.format(status_code=response.status_code))
    if response.status_code >= 300:
        print('Error: Response after updating content: {content}'.format(content=response.content))


if __name__ == "__main__":
    main()
