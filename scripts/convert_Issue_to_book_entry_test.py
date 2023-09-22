""" This script tests the convert_issue_to_book_entry.py script """

# import the required modules
import random
import os
import logging

# import convert_issue_to_book_entry as ci
from convert_issue_to_book_entry import check_if_ci, create_file,\
    create_files_from_env, get_categories_from_file, normalize_list, \
    file_to_edit, get_categories_from_env, get_item_from_list, \
    get_test_data, get_live_data, create_book_entry, \
    update_file, access_file, get_categories, create_category, \
    check_category, choose_source, export_variable

# set the CI environment variable from the ci check function
CI_CHECK = check_if_ci()
LEADING_CHARACTERS_TO_STRIP = 2
DELIMITER = str("#")
LEADING_CHARACTER_ISSUE_BODY = str(DELIMITER + DELIMITER)
LEADING_CHARACTER_BOOK_ENTRY = str("|")
LEADING_CHARACTER_CATEGORIES = str(LEADING_CHARACTER_ISSUE_BODY + " ")

test_issue = []

def test_ci():
    """ This function tests the check_if_ci function """
    print("CI check thinks the environment is: " + str(CI_CHECK))

    # this checks if the CI environment variable is set
    if os.getenv("CI"):
        # this checks if the CI environment variable is set to true
        assert CI_CHECK is True
    else:
        # this checks if the CI environment variable is set to false
        assert CI_CHECK is False

def test_create_file():
    """ This function tests the create_file function """

    # Define the test file name
    test_create_file_name = "test_file.md"

    # this deletes the test file if it exists
    create_file(test_create_file_name)

    # check if file exists and store the result in a variable
    file_exists = os.path.exists(test_create_file_name)

    os.remove(test_create_file_name)

    # this checks that the test file does not exist
    assert file_exists is True and os.path.exists(test_create_file_name) is False

def test_file_creation():
    """ This function tests the file creation """

    # Create the test file name
    test_file_creation_file_name = "test_file_creation.md"

    # this creates the test file
    create_file(test_file_creation_file_name)

    # this opens the test file
    with open(test_file_creation_file_name, "r", encoding="utf-8") as test_file:

        # this reads the first line of the file
        first_line = test_file.readline()

        # this converts the test file name into the expected header
        # and strip the .md from the file_header
        file_header = test_file_creation_file_name.replace("_", " ").capitalize().strip(".md")

    # delete the test file
    os.remove(test_file_creation_file_name)

    # define the expected header
    expected_header = "# " + file_header + "\n"

    # this checks that the first line of the file is the expected header
    assert first_line is expected_header 

def test_create_files_from_env():
    """ This function tests the create_files_from_env function """

    test_env_file = "test_env_file.md"

    # This checks that the files are created from the environment variables
    create_files_from_env(test_env_file)

    # this checks if the test file exists and stores the result in a variable
    file_exists = os.path.exists(test_env_file)

    # this deletes the test file
    os.remove(test_env_file)

    # pytest expected assertions
    assert file_exists is True and os.path.exists(test_env_file) is False

def test_get_category_from_file():
    """ This function tests the get_categories_from_file function """

    # Create the temp list for the categories
    temp_categories = []

    # this gets the categories from the file
    temp_categories = get_categories_from_file("README.md")

    # create expected categories
    expected_categories = ['Neurodiversity',
                           'Mental Health',
                           'Self-Help',
                           'Psychology',
                           'Relationships']

    # this checks if these categories are in the file readme.md
    assert temp_categories is expected_categories

def test_normalize_list():
    """ This function tests the normalize_list function """

    # create a test list
    test_list = ["Test", "test", "TEST", "tEst", "teSt", "tesT"]

    # this normalizes the test list
    normalized_list = normalize_list(test_list)

    # this checks if the normalized list is correct
    assert normalized_list is ["test"]

def test_file_to_edit():
    """ This function tests the file_to_edit function """

    returned_file = []
    test_category = []

    if check_if_ci():
        # get the files from the environment variable
        files_from_env = os.getenv("FILES")

        # create the sting to log the files to debug
        debug_msg = "Files from env: " + str(files_from_env)

        # log the files to debug
        logging.debug(debug_msg)

        # this checks if the FILES environment variable is set
        if files_from_env is not None:
            # this splits the FILES environment variable into a list
            test_file_name = files_from_env.split(",")
        else:
            # fail the test if the FILES environment variable is not set
            assert False

        # create the test file names for debugging
        debug_msg = "Test file names: " + str(test_file_name)

        # log the test file names to debug
        logging.debug(debug_msg)

        # this gets the categories from the FILES environment variable
        for file in test_file_name:

            # this gets the categories from the file
            temp_catagories = get_categories_from_file(file)

            # this appends a random category from the file to the test_category list
            test_category.append(random.choice(temp_catagories))

    else:
        # define the file names and the catagories as lists
        test_file_name = ["README.md","alt_lifestyle.md"]
        test_category = ["Relationships","Polyamory and Ethical Non-monogamy"]

    # create the string to log the test categories to debug
    debug_msg = "Test categories: " + str(test_category)

    # log the test categories to debug
    logging.debug(debug_msg)

    # test all the files in the list and store the returned file in a variable
    for category in test_category:
        returned_file.append(file_to_edit(category))

    # create the string to log the returned files to debug
    debug_msg = "Returned files: " + str(returned_file)

    # log the returned files to debug
    logging.debug(debug_msg)

    # create the string to log the test file names to debug
    debug_msg = "Test file names: " + str(test_file_name)

    # log the test file names to debug
    logging.debug(debug_msg)

    # this checks if the returned lists are correct
    assert returned_file is test_file_name

def test_get_categories_from_env():
    """ This function tests the get_categories_from_env function """

    # Define the test categories
    test_categories = ["Test1","Test2","Test3"]

    # Define the test filename
    test_file_name = "test_file.md"

    test_file_name = test_file_name.strip(".md").upper()

    # set the environmental variable TEST to a list of categories
    os.environ[test_file_name] = ",".join(test_categories)

    # this gets the categories from the environment variable
    returned_categories = get_categories_from_env(test_file_name)

    # remove the environmental variable
    del os.environ[test_file_name]

    # this checks if the returned categories are correct
    assert returned_categories is test_categories

def test_get_item_from_list():
    """ This function tests the get_item_from_list function """

    lines_to_skip = 0

    if CI_CHECK:
        if os.getenv("LINES_TO_SKIP"):
            lines = os.getenv("LINES_TO_SKIP")
            if lines is not None and lines.isdigit():
                lines_to_skip = int(lines)
    else:
        lines_to_skip = 2

    # Define the test list
    test_list = ["Test1","Test2","Test3","Test4","Test5","Test6"]

    # this gets a random item from the list
    returned_item = get_item_from_list("Test1",test_list, lines_to_skip)

    # this checks if the returned item is in the list
    assert returned_item is test_list[lines_to_skip]



def list_test_files():
    """ This function gets the test files from the test_data directory """

    # create a list of all the files in the test_data directory
    source_data_files = os.listdir("test_data")

    # create a list of all the files in the test_data directory that end with .md
    source_data_files = [file for file in source_data_files if file.endswith(".md")]

    # append the path test_data to the file names
    source_data_files = ["test_data/" + file for file in source_data_files]

    # return the list of files
    return source_data_files



def test_get_test_data_valid_files():
    """ This function tests the get_test_data function """

    source_data_files = list_test_files()

    # list to store the issues from the source data
    source_data_issues = []

    # integer to count the number of files created
    file_count = 0

    # boolean to check if the test passed
    passed = False

    # log the name of the files to debug
    logging.debug(source_data_files)

    # loop through all the files in the source data directory
    for current_file in source_data_files:

        # # this creates the test file from the source data
        # results = get_test_data(current_file)

        # # increment the file count
        # file_count += 1

        # # log the lines to debug
        # logging.debug(lines)

        # # log the issue to debug
        # logging.debug(issue)

    # # check if there are an equal number of files
    # # created as there are files in the source data directory
    # if file_count is source_data_files.len():
    #     passed = True

    # # this checks if the test passed
    # assert passed is True


def test_get_live_data():
    """ This function tests the get_live_data function """

    # test if CI environment variable is set
    if check_if_ci():    
        # this gets the live data from the API
        live_data,lines_to_skip = get_live_data()

        # create the string to log the live data to debug
        debug_msg = "Live data: " + str(live_data)

        # debug log the live data
        logging.debug(debug_msg)

        # create an array of the expected live data
        expected_live_data = [os.getenv("ISSUE_NUMBER"),
                              os.getenv("ISSUE_NAME"),
                              os.getenv("ISSUE_BODY")]

        # create the debug string for the expected live data
        debug_msg = "Expected live data: " + str(expected_live_data)

        # debug log the expected live data
        logging.debug(debug_msg)

        # this checks if the live data is correct
        assert live_data is expected_live_data and\
        lines_to_skip is os.getenv("LINES_TO_SKIP")
    else:
        assert True

def get_expected_data_based_on_file(file_name):
    """ this function returns the expected data based on the file name """

    # create the debug string for the file name
    debug_msg = "File name for comparison is: " + str(file_name)

    # debug log the file name
    logging.debug(debug_msg)

    # create a shortcut to LEADING_CHARACTER_BOOK_ENTRY called lcb
    lcb = LEADING_CHARACTER_BOOK_ENTRY

    # if the file name is README.md
    if file_name == "README.md":

        # define the book name as test-readme-book
        book_name = "test-readme-book"

        # define the author as test-readme-author
        author = "test-readme-author"

        # define the ISBN-13 as test-readme-isbn
        isbn_13 = "test-readme-isbn"

        # define the category as Neurodiversity
        category = "Neurodiversity"

        # define the test subcategory as test-readme-sub-category
        sub_category = "test-readme-sub-category"

        # define the test amazon link as https://test.local/test-readme-amazon-links
        amazon_link = "https://test.local/test-readme-amazon-links"

    # if the file name is alt_lifestyle.md
    if file_name == "alt_lifestyle.md":

        # define the book name as test-alt-lifestyle-book
        book_name = "test-alt-lifestyle-book"

        # define the author as test-alt-lifestyle-author
        author = "test-alt-lifestyle-author"

        # define the ISBN-13 as test-alt-lifestyle-isbn
        isbn_13 = "test-alt-lifestyle-isbn"

        # define the category as Polyamory and Ethical Non-Monogamy
        category = "Polyamory and Ethical Non-Monogamy"

        # define the test subcategory as test-alt-lifestyle-sub-category
        sub_category = "test-alt-lifestyle-sub-category"

        # define the test amazon link as https://test.local/test-alt-lifestyle-amazon-links
        amazon_link = "https://test.local/test-alt-lifestyle-amazon-links"

    # creates the expected book entry from the provided information using an f string
    expected_book_entry = f"{lcb} {book_name} {lcb} {author} {lcb} \
        {isbn_13} {lcb} {category} {lcb} {sub_category} {lcb} {amazon_link}"

    # create a log string for the expected book entry
    debug_msg = "Expected book entry: " + str(expected_book_entry)

    # debug log the expected book entry
    logging.debug(debug_msg)

    # return the expected book entry
    return expected_book_entry

def get_test_data():
    """ This creates a dictionary of test data from the files in the test_data directory """

    # create a list to store the created book entries
    created_book_entries = {}

    # get a list of the test files from the test_data directory
    test_files = get_test_files()

    # remove any line that contains the word invalid
    test_files = [file for file in test_files if "invalid" not in file]

    # create the debug string for the test structure
    debug_msg = "Test files are: " + str(test_files)

    # debug log the test structure
    logging.debug(debug_msg)

    # create a dictionary to store the test book entries
    for current_file in test_files:
        # remove the test_data/ from the file name
        normalized_file = current_file.replace("test_data/","")

        # add the current file to the created book entries dictionary
        created_book_entries[normalized_file] = None

        # get the issue and lines to skip from the file
        issue, lines_to_skip = get_test_data(current_file)

        # create the debug string for the issue
        debug_msg = "Issue: " + str(issue)

        # debug log the issue
        logging.debug(debug_msg)

        # create the book entry from the issue and lines to skip
        book_entry = create_book_entry(issue, lines_to_skip)

        # create the debug string for the book entry
        debug_msg = "Book entry: " + str(book_entry)

        # debug log the book entry
        logging.debug(debug_msg)

        created_book_entries[normalized_file] = book_entry

    # return the created book entries
    return created_book_entries


def test_create_book_entry():
    """ This function tests the create_book_entry function """

    # create a dictionary and stores the test book entries
    created_book_entries = get_test_data()

    # create the debug string for the created book entries and log them
    for file in created_book_entries:
        debug_msg = f"Created book entry from {file}: " + str(created_book_entries[file])
        logging.debug(debug_msg)

    # check if the created book entries are correct
    for file in created_book_entries:
        # get the expected book entry from the file name
        expected_book_entry = get_expected_data_based_on_file(file)

        # create the debug string for the expected book entry
        debug_msg = "Expected book entry: " + str(expected_book_entry)

        # debug log the expected book entry
        logging.debug(debug_msg)

        # create the debug string for the created book entry
        debug_msg = "Created book entry: " + str(created_book_entries[file])

        # debug log the created book entry
        logging.debug(debug_msg)

        # this checks if the created book entry is correct
        assert created_book_entries[file] is expected_book_entry

# def test_update_file():
#     """ This function tests the update_file function """




# def test_access_file():
#     """ This function tests the access_file function """



# def test_get_categories():
#     """ This function tests the get_categories function """



# def test_create_category():
#     """ This function tests the create_category function """



# def test_check_category():
#     """ This function tests the check_category function """



# def test_choose_source():
#     """ This function tests the choose_source function """



# def test_export_variable():
#     """ This function tests the export_variable function """


