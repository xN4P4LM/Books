#!/bin/python3

## this script does the following: 
    # 1. Read the relevant information from the environment variables
    # 2. Convert the issue text to a book entry in a markdown column format
    # 3. Append the book entry to either the readme.md or alt-lifestyle.md file
    # 4. Commit the changes to the repo
    # 5. Push the changes to the repo
    # 6. Create a pull request, referencing the issue, and assign it to the issue creator
    # 7. Add the issue to the project board


# import the libraries for pyGithub
from math import e
from github import Github
from github import Auth

# import the libraries for gql
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

# import the necessary libraries to read the environment variables
import os

## reads the following environment variables into variables: 
    # EMAIL_DOMAIN
    # ISSUE_NAME
    # ISSUE_NUMBER
    # ISSUE_BODY
    # ISSUE_CREATOR
    # REPO_NAME
    # GITHUB_TOKEN

EMAIL_DOMAIN = os.getenv("EMAIL_DOMAIN")
ISSUE_NAME = os.getenv("ISSUE_NAME")
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")
ISSUE_BODY = os.getenv("ISSUE_BODY")
ISSUE_CREATOR = os.getenv("ISSUE_CREATOR")
REPO_NAME = os.getenv("REPO_NAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

## initialize the PyGithub client

# create an auth using the GITHUB_TOKEN
github_api_auth = Auth.Token(GITHUB_TOKEN)

# create a github instance
github_api = Github(auth=github_api_auth)

## initialize the gql client

# create a gql transport with authentication using the GITHUB_TOKEN
github_graphql_transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers={"Authorization": f"Bearer {GITHUB_TOKEN}"})

# create a gql client
github_graphql = Client(transport=github_graphql_transport, fetch_schema_from_transport=True)

## get the issue information

# get the repo
repo = github_api.get_repo(REPO_NAME)

# get the issue
issue = repo.get_issue(ISSUE_NUMBER)

## get the project board information

# get the project board using gql
query_project_id = gql(
    """
    query user {
        user(login: "xn4p4lm") {
            projectV2(number: 5) {
                id
            }
        }
    }
    """)
project_id = client.execute(query_project_id)

# get the issue's node_id
issue_node_id = issue.node_id


def add_issue_to_project_board():
    # add the issue to the project board using gql
    query_add_issue_to_project_board = gql(
        """
        mutation addIssueToProjectBoard {
            addProjectCard(input: {contentId: "%s", projectColumnId: "%s"}) {
                cardEdge {
                    node {
                        id
                    }
                }
            }
        }
        """ % (issue_node_id, project_id["user"]["projectV2"]["id"]))
    github_graphql.execute(query_add_issue_to_project_board)

## convert the issue to a book entry

# get the issue's title which is the book entry's title
book_title = issue.title

# get the issue's body
issue_body = issue.body

# parse the issue's body into an array of lines
issue_body_lines = issue_body.splitlines()

# get the line after ## Author(s) Name(s)
book_author = issue_body_lines[issue_body_lines.index("## Author(s) Name(s)") + 1]

# get the line after ## ISBN-13 Number
book_isbn = issue_body_lines[issue_body_lines.index("## ISBN-13 Number") + 1]

# get the line after ## Category
book_category = issue_body_lines[issue_body_lines.index("## Category") + 1]

# get the line after ## Sub Category
book_sub_category = issue_body_lines[issue_body_lines.index("## Sub Category") + 1]

# get the line after ## Amazon Link
book_amazon_link = issue_body_lines[issue_body_lines.index("## Amazon Link") + 1]

# Determine the file to append the book entry to based on the primary category normalized, alt-lifestyle categories include:
    # kink
    # BDSM
    # Polyamory
    # Ethical Non-Monogamy

# normalize the categories
normalized_book_category = book_category.lower()

# determine the file to append the book entry to
if normalized_book_category == "kink":
    book_entry_file = "alt-lifestyle.md"
elif normalized_book_category == "bdsm":
    book_entry_file = "alt-lifestyle.md"
elif normalized_book_category == "polyamory":
    book_entry_file = "alt-lifestyle.md"
elif normalized_book_category == "ethical non-monogamy":
    book_entry_file = "alt-lifestyle.md"
else:
    book_entry_file = "readme.md"

# create the book entry using the markdown table format of 
# | Book name | Author | SubCategory | ISBN-13 | Amazon Link | Have Read? |
book_entry = "| %s | %s | %s | %s | %s | [ ] |" % (book_title, book_author, book_sub_category, book_isbn, book_amazon_link)

## append the book entry to the file

# get the file locally
with open(book_entry_file, "r") as file:
    book_entry_file_contents = file.readlines()

# check if the book entry already exists in the file
if book_entry in book_entry_file_contents:
    print("Book entry already exists in the file")
    exit(-1)

# get all the categories in the file
categories = []
for line in book_entry_file_contents:
    if line.startswith("## "):
        categories.append(line[3:].strip())

# check if the category exists in the file
if book_category not in categories:
    print("Category does not exist in the file")
    exit(-1)

# update the text in the file to include the book entry at the first blank line after the category and a blank line after the book entry using markdown table format
for index, line in enumerate(book_entry_file_contents):
    if line.startswith("## "):
        if line[3:].strip() == book_category:
            for index2, line2 in enumerate(book_entry_file_contents[index:]):
                if line2.strip() == "":
                    book_entry_file_contents.insert(index + index2 + 1, book_entry + "\n")
                    break

# create a commit message for the book entry
commit_message = "Add book entry for %s" % (book_title)