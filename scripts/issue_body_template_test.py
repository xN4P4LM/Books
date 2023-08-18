
import logging

# import convert_issue_to_book_entry as ci
from issue_body_template import *

def get_expected_output():

    if os.getenv("CI"):
        # define the expected output
        expected_output = (        
"""## This pull request was created automatically by the [.github/workflows/issue-automation.yaml workflow.](https://github.com/xn4p4lm/Books/blob/main/.github/workflows/issue-automation.yaml) ( DO NOT EDIT )

It adds the book Test Issue to test_file.md as part of #42

This PR will close issue: #42 through the following branch issue-42

**NOTE: This template is managed by [templates/pr-body-template.j2](https://github.com/xn4p4lm/Books/blob/main/templates/pr-body-template.j2)**""")

    else:
        # define the expected output
        expected_output = (
"""## This pull request was created automatically by the .github/workflows/issue-automation.yaml workflow. ( DO NOT EDIT )

It adds the book Test Issue to test_file.md as part of #42

This PR will close issue: #42 through the following branch issue-42

**NOTE: This template is managed by templates/pr-body-template.j2**"""
        )

    # return the expected output
    return expected_output


# define the test function
def test_create_pr_body():

    # get the expected output
    expected_output = get_expected_output()

    # call the function
    body = create_pr_body(True)

    # debug and print the Expected Body
    logging.debug("Expected Body: " + expected_output)

    # debug and print the Actual Body
    logging.debug("Actual Body: " + body)

    # assert that the body is the expected output
    assert body == expected_output
    