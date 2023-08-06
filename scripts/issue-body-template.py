# This command will create the body for a PR from a template environmental variable in GitHub Actions
# using jinja2 for the template engine

import os
from jinja2 import Template

# Get the template from the templates directory

# find the path in the dir structure to the template 'templates/pr-body-template.j2'
template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'pr-body-template.j2')

# Open the template file
with open(template_path) as f:
    # Read the template file
    template = f.read()

# Get the issue name from the environment
issue_name = os.environ.get('ISSUE_NAME', "Test Issue")

# Get the issue number from the environment
issue_number = os.environ.get('ISSUE_NUMBER', "100")

# Get the file name from the .files_changed file
with open('.files_changed') as f:
    file_name = f.read().strip()

# Create the body of the PR
body = Template(template)

# Render the body of the PR
body = body.render( issue_name=issue_name, file_name=file_name, issue_number=issue_number)

# Print the body of the PR in a way that can be used in a GitHub CLI
print(body)

exit(0)