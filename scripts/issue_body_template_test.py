
import logging

# import convert_issue_to_book_entry as ci
from issue_body_template import *


# define the expected output
expected_output = """## This pull request was created automatically by the .github/workflows/issue-automation.yaml workflow. ( DO NOT EDIT )

It adds the book Test Issue to test_file.md as part of #42

This PR will close issue: #42 through the following branch issue-42

**NOTE: This template is managed by templates/pr-body-template.j2**"""

# define the test function
def test_create_pr_body():

    # call the function
    body = create_pr_body(True)

    # debug and print the Expected Body
    logging.debug("Expected Body: " + expected_output)

    # debug and print the Actual Body
    logging.debug("Actual Body: " + body)

    # assert that the body is the expected output
    assert body == expected_output
    