# This command will create the body for a PR from a template environmental variable in GitHub Actions
# using jinja2 for the template engine

import os
from jinja2 import Template

# Get the template from the templates directory

def create_pr_body(test=False):
    # find the path in the dir structure to the template 'templates/pr-body-template.j2'
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'pr-body-template.j2')

    # Open the template file
    with open(template_path) as f:
        # Read the template file
        template = f.read()

    # Get the issue name from the environment
    issue_name = os.environ.get('ISSUE_NAME')

    # Get the issue number from the environment
    issue_number = os.environ.get('ISSUE_NUMBER')

    file_name = None

    # if test is true then set file_name to test_file.md
    if test:
        file_name = "test_file.md"
        issue_name = "Test Issue"
        issue_number = "42"
    else:
        # Get the file name from the .files_changed file
        with open('.files_changed') as f:
            file_name = f.read().strip()

    if (issue_name == None or issue_number == None or file_name == None):
        raise ValueError("ISSUE_NAME or ISSUE_NUMBER is not set of no file has been changed")
    
    # Create the body of the PR
    body = Template(template)

    # Render the body of the PR
    body = body.render( issue_name=issue_name, file_name=file_name, issue_number=issue_number)

    # return the body of the PR
    return body

def Main():
    
    # Create the body of the PR
    body = create_pr_body()

    # Print the body of the PR
    print(body)

# initialize the script using init
if __name__ == "__main__":
    Main()