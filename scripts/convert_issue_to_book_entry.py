""" This script converts a GitHub issue to a book entry
    in the corresponding markdown files in the repo """
#!/bin/python3

# This script converts an issue to a book entry in the corresponding .md files in the repo

# This script does the following:
# 1. Check if the script is running locally or in GitHub actions
# 2. Read the relevant information from either the environment variables or the test data
# 3. Convert the read text in to a book entry in a markdown column format
# 4. Append the book entry to either the corresponding .md files


# import the necessary libraries to read the environment variables
import os
import logging

LEADING_CHARACTERS_TO_STRIP = 2
DELIMITER = str("#")
LEADING_CHARACTER_ISSUE_BODY = str(DELIMITER + DELIMITER)
LEADING_CHARACTER_BOOK_ENTRY = str("|")
LEADING_CHARACTER_CATEGORIES = str(LEADING_CHARACTER_ISSUE_BODY + " ")

def check_if_ci():
    """ This checks if the script is running locally or in the GitHub action """

    # check if the script is running locally or in the GitHub action
    if os.getenv("CI") == "true":
        logging.debug("The script is running in the GitHub Action")
        return True

    logging.warning("The script is running locally")
    return False


def create_file(file_name):
    """ this function creates a file from the passed file name
        and then adds markdown to the file to initialize the file """

    # log we are creating the file

    logging.debug("Creating the file %s", file_name)

    # create the file
    with open(file_name, "w", encoding="utf-8") as created_file:

        # normalize the file name where the first letter is capitalized and
        # either the - or _ is replaced with a space and strip the .md extension from the header
        file_header = file_name.replace("_", " ").replace("-", " ").capitalize().strip(".md")

        # log what the file header will be
        logging.debug("The file header is %s", file_header)

        # add the markdown to the file
        created_file.write(f"{DELIMITER} {file_header}\n")

        # log the file was created
        logging.debug("The file %s was created", file_name)

        # close the file
        created_file.close()


def create_files_from_env(file):
    """ create files from environment variables """

    # advise the user that we are checking if the file exists
    logging.debug("Checking if the file %s exists", file)

    # check if the file exists
    if not os.path.isfile(file):

        # advise the user that the file does not exist and that we are creating the file
        logging.warning(
            "The file: %s does not exist, creating the file from the environment variables", file)

        # create the file
        create_file(file)


def get_categories_from_file(file):
    """ This function get the categories from the passed file
      and checks if they are already in the passed list """

    # create holding variable for categories
    categories = []

    # log the file
    logging.debug("The file is %s", file)

    # normalize and remove the filename extension from the file
    file_header = file.strip(".md").replace("_", " ").replace("-", " ").capitalize()

    # log the file header
    logging.debug("The file header is %s", file_header)

    # create a list of the file header and 'Categories' to check if
    # the line is either the file header or the categories
    categories_to_ignore = [file_header, "Category",'Books :books:']

    with open(file, "r",encoding="utf-8") as open_file:
        # read the file
        in_file = open_file.readlines()

    # close the file
    open_file.close()

    for line in in_file:
        # check if the line starts with the delimiter
        if line.startswith(DELIMITER):

            # check if the line does not either have the filename or just catagories
            if line.strip(DELIMITER).strip() not in categories_to_ignore:
                # remove the delimiter from the line and leading whitespace
                modified_line = line.strip(DELIMITER).strip()

                # create log message that the category was added from the file
                debug_log_msg = f"The category {modified_line} was added from the file {file}"

                # log the category added from the file
                logging.debug(debug_log_msg)

                # add the line to the categories variable
                categories.append(modified_line)

    return categories

def get_categories_from_env(file):
    """ This function gets the categories from the 
    environment variables based on the UPPER CASE 
    name of the file as the key"""

    # create the categories variable
    categories = []

    # log the file
    logging.debug("The file is %s", file)

    # remove the .md extension from the file
    file = file.strip(".md").upper()

    # log the modified file
    logging.debug("The file is %s", file)

    # get the environment variable for the file
    env_var = os.getenv(file)

    # check if the environment
    if env_var is not None:
        # split the environment variable into a list
        env_var_list = env_var.split(",")

        # log the environment variable list
        logging.debug("The environment variable list is %s", env_var_list)
    else:
        # print a warning that there is no environment variable for that file
        logging.warning(
            "There is no environment variable for the file: %s", file)
        return categories

    # iterate through the env_var and add to the categories
    # variable if it is not already in the variable
    for category in env_var_list:
        # check if the category is not already in the categories variable
        if category not in categories:

            # create f string for the debug log message
            debug_log_msg = f"The category {category} was \
                added from the environmental variable for file {file}"

            # add the category to the categories variable
            categories.append(category)

            # log the category in for the file
            logging.debug(debug_log_msg)

    return categories


def normalize_list(passed_list):
    """ Normalize the passed list by removing leading and 
    trailing whitespace and making all characters lowercase"""
    # create the normalized list variable
    normalized_list = []

    # log the passed list
    logging.debug("The passed list is %s", passed_list)

    # iterate through the passed list and normalize the items
    for item in passed_list:
        # normalize the item
        normalized_item = item.lower().strip(DELIMITER).strip()

        # add the normalized item to the normalized list
        normalized_list.append(normalized_item)

    # create a set from the normalized list to remove duplicates
    normalized_set = set(normalized_list)

    # clear the normalized list
    normalized_list.clear()

    # iterate through the normalized set and add the items to the normalized list
    for item in normalized_set:
        # add the item to the normalized list
        normalized_list.append(item)

    # log the normalized list
    logging.debug("The normalized list is %s", normalized_list)

    return normalized_list

def file_to_edit(book_category):
    """ This function determines the file to append the book entry too
    based on the primary category normalized in the primary category of the book entry"""

    # log the book category
    logging.debug("The book category is %s", book_category)

    # normalize the book category
    book_category = book_category.lower()

    # create the dictionary of categories and their associated files
    #  directly from the environment variables
    categories_by_env_var = {}

    # create the dictionary of categories and their associated files
    #  directly from the files
    categories_by_file = {}

    # create the book entry file variable
    book_entry_file = ""

    # get a list of all files that end with .md in the repository root
    files_from_env = os.getenv("FILES")

    if files_from_env is not None:
        candidate_files = files_from_env.split(",")
    else:
        candidate_files = [f for f in os.listdir(".") if f.endswith(".md")]

    # iterate through the candidate_files and create the categories_by_file dictionary
    for file in candidate_files:
        categories_by_file[file] = normalize_list(
            get_categories_from_file(file))
        categories_by_env_var[file] = normalize_list(
            get_categories_from_env(file))

    # iterate through the categories_by_file dictionary
    # and check if the book_category is in the list
    for file in candidate_files:
        # check if the book_category is in the list
        if book_category in categories_by_file[file]:
            # set the book_entry_file to the file
            book_entry_file = file
        if book_category in categories_by_env_var[file]:
            # set the book_entry_file to the file
            book_entry_file = file
            # create the file if exists in the environment variable and not in the repository
            create_files_from_env(file)

    # check if the book_entry_file is empty
    if book_entry_file == "":
        # create the f string for the error message
        error_msg = f"The book category {book_category} was not in any of the files \
                or the associated environmental variables in the repository. \
                Please either add the file or environmental variables ."

        # print an error message with the book_category, issue number,
        # to the terminal and exit the program
        logging.error(error_msg)

        # exit the program
        os._exit(1)

    # create the f string for the debug log message
    debug_log_msg = f"The book entry file for the category\
          {book_category} is {book_entry_file}"

    # log the book entry file for category
    logging.debug(debug_log_msg)

    return book_entry_file

def get_item_from_list(searched_item, passed_list, lines_to_skip):
    """ This function will try and pull the passed item from the passed list and return them,
      it will also catch any errors or empty values and exit the program if they are found """

    # create a blank variable to hold the item
    item = ""

    # try to get the item from the list
    try:

        # get the item at index + lines_to_skip
        item = passed_list[passed_list.index(searched_item) + lines_to_skip]

        # check if the item is empty
        if item == "":

            # create warning message using f string
            warning_msg = f"The {searched_item} was blank.\
                 Please update the issue with the {searched_item}."

            # print a warning that the item was empty and to update the issue
            logging.warning(warning_msg)
            # exit the program
            os._exit(1)

    # catch the error if the item is not in the list or out of range with the error message
    except (ValueError, IndexError) as exception_msg:

        # create f string for the error message
        error_msg = f"The {searched_item} was not in the list.\
                Please update the issue with the {searched_item}."

        # print an error message that the item was not in the list and exit the program
        logging.error(error_msg, exception_msg)

        # exit the program
        os._exit(1)

    # return the item
    return item


def create_book_entry(issue,lines_to_skip):
    """ This function creates the book entry from the passed issue """

    # get the issue's title which is the book entry's title
    book_title = issue[1]

    # get the issue's body
    issue_body = issue[2]

    # parse the issue's body into an array of lines
    issue_body_lines = issue_body.strip("#").splitlines()

    # normalize the issue's body by removing the # from each line
    issue_body_lines = [line.lstrip(DELIMITER+DELIMITER+" ")
                        for line in issue_body_lines]

    # get the line after Author(s) Name(s)
    book_author = get_item_from_list(
        "Author(s) Name(s)", issue_body_lines, lines_to_skip)

    # get the line after ISBN-13 Number
    book_isbn = get_item_from_list(
        "ISBN-13 Number", issue_body_lines, lines_to_skip)

    # get the line after Category
    book_category = get_item_from_list(
        "Category", issue_body_lines, lines_to_skip)

    # get the line after Sub-Category
    book_sub_category = get_item_from_list(
        "Sub-Category", issue_body_lines, lines_to_skip)

    # get the line after Amazon Link
    book_amazon_link = get_item_from_list(
        "Amazon Link", issue_body_lines, lines_to_skip)

    # create the book entry using the markdown table format of
    # | Book name | Author | SubCategory | ISBN-13 | Amazon Link | Have Read? |
    book_entry = "| %s | %s | %s | %s | [Amazon Link](%s) | Yes |", (
        book_title, book_author, book_sub_category, book_isbn, book_amazon_link)

    # print that the book entry was created and return the book entry
    logging.debug("The book entry was created")

    # print the book entry to the terminal
    logging.debug(book_entry)

    return book_entry, book_category

def access_file(action, book_entry_file, book_entry_file_contents=""):
    """ This function handles the reading and writing of the book entry file """

    if action == "read":
        # open the book entry file
        with open(book_entry_file, "r", encoding="utf-8") as file:
            book_entry_file_contents = file.readlines()

    if action == "write":
        # open the book entry file
        with open(book_entry_file, "w", encoding="utf-8") as file:
            file.writelines(book_entry_file_contents)

    return book_entry_file_contents

def update_file(
        book_entry_file_contents,
        book_entry,
        book_category,
        book_entry_file):
    """ This function takes the book entry and the book entry file
         and appends the book entry to the file """

    inserted = False

    # update the text in the file to include the book entry at the
    # first blank line after the category and a blank line after
    # the book entry using markdown table format
    for index, line in enumerate(book_entry_file_contents):

        # check if the line begins with the markdown header delimiter
        if line.startswith(DELIMITER):

            # strip the leading characters and check if the category was found
            if line.strip(DELIMITER).strip() == book_category:

                # loop through the lines after the category
                for index2, line2 in enumerate(book_entry_file_contents[index:]):

                    # check if entry is already in the file
                    if book_entry in line2:

                        # if the entry is already in the file, replace the entry with the new entry
                        book_entry_file_contents[index +
                                                 index2] = book_entry + "\n"

                        # print that the book entry was replaced in the file
                        logging.debug(
                            "The book entry was replaced in the file %s.", (book_entry_file))

                        # set inserted to true
                        inserted = True

                        # break out of the loop
                        break

                    # check if the line is blank
                    if line2.strip() == "":

                        # insert the book entry after the blank line
                        book_entry_file_contents.insert(
                            index + index2, book_entry + "\n")

                        # print that the book entry was inserted into the file
                        logging.debug(
                            "The book entry was inserted into the file %s.", (book_entry_file))

                        # set inserted to true
                        inserted = True

                        # break out of the loop
                        break

   # if the entry was not inserted, print an error message to the terminal
    if not inserted:
        logging.warning(
            "The book entry was not inserted into the file %s.", (book_entry_file))
    else:
        # write the updated file contents to the file
        access_file("write", book_entry_file, book_entry_file_contents)


def get_categories(book_entry_file_contents):
    """ This function gets the categories from the file """

    # create an array of categories
    categories = []

    # loop through the lines in the file
    for line in book_entry_file_contents:

        # check if the line begins with the markdown header delimiter
        if line.startswith("# "):

            # Skip the first line which is the title
            if book_entry_file_contents.index(line) == 0:
                continue

            # append the category to the categories array
            categories.append(line.strip(DELIMITER).strip())

        # check if the line begins with the markdown table delimiter
        if line.startswith("<!--"):
            break

    # return the categories array
    return categories


def create_category(
        book_entry_file_contents,
        book_category,
        categories,
        book_entry_file):
    """ this function creates the category in the file if it does not exist """

    # create a variable to hold the index of the last category
    last_category_index = 0

    # find the index of the last category in the file
    for index, line in enumerate(book_entry_file_contents):

        # check if this line matches the last category from the categories array
        if line.strip(DELIMITER).strip() == categories[-1]:

            # next get the last line of the category
            for index2, line2 in enumerate(book_entry_file_contents[index:]):

                # check if the line is blank
                if line2.strip() == "":
                    last_category_index = index + index2
                    break

    # insert the category and the markdown table format after the last category
    book_entry_file_contents.insert(last_category_index + 1, "\n")

    # create the category header using f stings
    category_header = f"{DELIMITER} {book_category}\n"

    # create the table header using f strings
    table_header = "| Book name | Author | SubCategory | ISBN-13 | Amazon Link | Have Read? |\n"

    # create the table spacer using f strings
    table_spacer = "| --------- | ------ | ----------- | ------- | ----------- | ---------- |\n"

    book_entry_file_contents.insert(
        last_category_index + 1, category_header)
    book_entry_file_contents.insert(
        last_category_index + 2, table_header)
    book_entry_file_contents.insert(
        last_category_index + 3, table_spacer)

    # create the f string for the debug log message
    debug_log_msg = f"The category {book_category} was created in the file {book_entry_file}"

    # log that the category was created
    logging.debug(debug_log_msg)


def check_category(book_entry_file, book_entry_file_contents, book_category, categories):
    """ This function checks if the category exists in the file and creates it if it does not"""

    # create a variable to hold the category found flag
    category_found = False

    # check if the category is empty
    if book_category == "":
        # log a message that the category was blank and that you need to add a category
        logging.warning("The category was blank. Please add a category.")

        # exit the program
        os._exit(1)

    # check if the category is in the categories array
    if book_category not in categories:

        # set the category found flag to false
        category_found = False

        # create the f string for the warning log message
        warning_log_msg = f"The category {book_category} \
            was not found in the file {book_entry_file}."

        # log a message that the category was not found and that
        # it will be created along with the new category name
        logging.warning(warning_log_msg)

        # create the category
        create_category(book_entry_file_contents, book_category,
                        categories, book_entry_file)
    else:

        # set the category found flag to true
        category_found = True

        # create the f string for the debug log message
        debug_log_msg = f"The category {book_category} was \
            found in the file {book_entry_file}"

        # log a message that the category was found
        logging.debug(debug_log_msg)

    # return the category found flag
    return category_found

def get_live_data():
    """ This function gets the issue information from 
    the GitHub Actions Environment Variables """

    # get the issue number from the environment variables
    issue_number = os.getenv("ISSUE_NUMBER")

    # get the issue title from the environment variables
    issue_title = os.getenv("ISSUE_NAME")

    # get the issue body from the environment variables
    issue_body = os.getenv("ISSUE_BODY")

    # get the number of lines to skip from the environment variables
    lines_to_skip = os.getenv("LINES_TO_SKIP")

    # create the issue as an array of strings
    issue = [issue_number, issue_title, issue_body]

    # return the issue
    return issue, lines_to_skip

def get_test_data(file):
    """ This function creates the test data """

    # create an array to hold the issue information

    # generate a random issue number
    issue_number = 1

    # create a variable to hold the issue title
    issue_title = ""

    # read the test body from the file as a solid block of text
    issue_body = ""

    # open the file
    with open(file, "r", encoding="utf-8") as opened_file:
        # read the file
        lines = opened_file.readlines()
        for line in lines:
            # add the line to the issue body
            issue_body += line

    # for each line in the test data
    for index, line in enumerate(issue_body):
        # for the first line, set the issue title
        if index == 3:
            issue_title = line.strip()

    # set the lines to skip to 2
    lines_to_skip = 2

    # log the issue information
    logging.debug("The test data was created.")

    # log the issue information
    logging.debug("The issue number is %s.", issue_number)
    logging.debug("The issue title is %s.", issue_title)
    logging.debug("The issue body is \n%s.", issue_body)

    # create the issue as an array of strings
    issue = [issue_number, issue_title, issue_body]

    # log the inserted issue information
    logging.debug("The issue information was inserted into the issue array.")

    return (issue, lines_to_skip)

def choose_source(is_ci):
    """ This is the main helper function that determines 
    if we use local test data or the GitHub API 
    to get the issue information """

    # create the issue variable
    issue = []

    # check if the script is
    if is_ci is True:

        # get data from Action environment variables
        issue = get_live_data()

    else:

        # create the test data
        issue = get_test_data()

    # return the issue
    return issue


def export_variable(file_name, environment):
    """ This function exports the file name as a file for GitHub Actions"""

    # export to a file named .files_changed for use in GitHub Actions
    if environment:
        # write the file name to a file
        with open('.files_changed', 'a', encoding="utf-8") as write_files_changed:
            write_files_changed.write(file_name)

        # read the file
        with open('.files_changed', 'r', encoding="utf-8") as read_files_changed:
            file_contents = read_files_changed.read()

        # print the file contents
        print(file_contents)

        # print .files_changed full path
        print(os.path.abspath('.files_changed'))

        # print a message that the file name was exported
        logging.debug(
            "The file name %s was exported to .files_changed", file_name)
    else:
        logging.warning(
            "The file name %s was not exported a file because \
                the script is not running in check_if_CI.", file_name)

def main():
    """ This function handles the main logic of the script """
    logging.basicConfig(level=logging.INFO)

    # Print the welcome message
    logging.debug("Welcome to the convert-issue-to-book-entry python script")
    # Advise the user that the script will convert an issue to a book in markdown format
    logging.debug(
        "This script will convert a GitHub issue into to a \
            markdown table containing the issues text and write it to the file")

    # Checks if the script is running locally or in the GitHub action
    environment = check_if_ci()

    # If the script is running locally, it will use the test data
    # If the script is running in the GitHub action,
    # it will use the GitHub API to get the issue information
    issue, lines_to_skip = choose_source(environment)

    # Create the book entry
    book_entry, book_category = create_book_entry(issue,lines_to_skip)

    # get the file to append the book entry to
    book_entry_file = file_to_edit(book_category)

    # export the file to a local variable using a terminal command
    export_variable(book_entry_file, environment)

    # get the file locally
    book_entry_file_contents = access_file("read", book_entry_file)

    # get the categories in the file
    categories = get_categories(book_entry_file_contents)

    # check if the category exists in the file
    check_category(book_entry_file, book_entry_file_contents,
                   book_category, categories)

    # update the file
    update_file(book_entry_file_contents, book_entry,
               book_category, book_entry_file)


# initialize the script using init
if __name__ == "__main__":
    main()
