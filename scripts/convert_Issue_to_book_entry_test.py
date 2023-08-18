import random

# import convert_issue_to_book_entry as ci
from convert_issue_to_book_entry import *

# set the CI environment variable from the ci check function
ci_check = check_if_CI()

test_issue = []

def test_ci():
    print("CI check: " + str(ci_check))

    # this checks if the CI environment variable is set
    if os.getenv("CI"):
        # this checks if the CI environment variable is set to true
        assert ci_check == True
    else:

        # this checks if the CI environment variable is set to false
        assert ci_check == False

def test_create_file():

    # Define the test file name
    test_create_file_name = "test_file.md"

    # this deletes the test file if it exists
    create_file(test_create_file_name)

    # check if file exists and store the result in a variable
    file_exists = os.path.exists(test_create_file_name)

    os.remove(test_create_file_name)

    # this checks that the test file does not exist
    assert file_exists == True and os.path.exists(test_create_file_name) == False

def test_file_creation():

    # Create the test file name
    test_file_creation_file_name = "test_file_creation.md"
    
    # this creates the test file
    create_file(test_file_creation_file_name)

    # this opens the test file
    with open(test_file_creation_file_name, "r") as f:

        # this reads the first line of the file
        first_line = f.readline()
        
        # this converts the test file name into the expected header and strip the .md from the file_header
        file_header = test_file_creation_file_name.replace("_", " ").capitalize().strip(".md")

    # delete the test file
    os.remove(test_file_creation_file_name)

    # this checks that the first line of the file is the expected header
    assert first_line == "# " + file_header + "\n"

def test_create_files_from_env():

    test_env_file = "test_env_file.md"
    
    # This checks that the files are created from the environment variables
    create_files_from_env(test_env_file)

    # this checks if the test file exists and stores the result in a variable
    file_exists = os.path.exists(test_env_file)

    # this deletes the test file
    os.remove(test_env_file)

    # pytest expected assertions
    assert file_exists == True and os.path.exists(test_env_file) == False

def test_get_Live_Data():

    # this gets the live data from the API
    live_data,lines_to_skip = get_live_data()

    issue_number = live_data[0]
    book_title = live_data[1]
    issue_body = live_data[2]
    
    if(ci_check):
        assert issue_number == "" and book_title == "" and issue_body == "" and lines_to_skip == 2
    else:
        assert True

def test_get_category_from_file():

    # Create the temp list for the categories
    temp_categories = []

    # this gets the categories from the file
    temp_categories = get_categories_from_file("README.md")
    
    # this checks if these categories are in the file readme.md
    assert temp_categories == ['Neurodiversity','Mental Health','Self-Help','Psychology','Relationships']
 
def test_normalize_list():

    # create a test list
    test_list = ["Test", "test", "TEST", "tEst", "teSt", "tesT"]

    # this normalizes the test list
    normalized_list = normalize_list(test_list)

    # this checks if the normalized list is correct
    assert normalized_list == ["test"]

def test_file_to_edit():

    returned_file = []
    test_category = []

    if check_if_CI():
        # get the files from the environment variable
        files_from_env = os.getenv("FILES")

        # log the files to debug
        logging.debug("Files from env: " + str(files_from_env))

        # this checks if the FILES environment variable is set
        if files_from_env is not None:
            # this splits the FILES environment variable into a list
            test_file_name = files_from_env.split(",")
        else:
            # fail the test if the FILES environment variable is not set
            assert False

        # log the test file names to debug
        logging.debug("Test file names: " + str(test_file_name))

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

    # log the test categories to debug
    logging.debug("Test categories: " + str(test_category))    
    
    # test all the files in the list and store the returned file in a variable
    for category in test_category:
        returned_file.append(file_to_edit(category))

    # log the returned files to debug
    logging.debug("Returned files: " + str(returned_file))

    # log the test file names to debug
    logging.debug("Test file names: " + str(test_file_name))

    # this checks if the returned lists are correct
    assert returned_file == test_file_name

def test_get_categories_from_env():

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
    assert returned_categories == test_categories

def test_get_item_from_list():

    lines_to_skip = 0

    if ci_check:
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
    assert returned_item == test_list[lines_to_skip]



def get_test_files():
    
    # create a list of all the files in the test_data directory
    source_data_files = os.listdir("test_data")

    # create a list of all the files in the test_data directory that end with .md
    source_data_files = [file for file in source_data_files if file.endswith(".md")]

    # append the path test_data to the file names
    source_data_files = ["test_data/" + file for file in source_data_files]

    # return the list of files
    return source_data_files



def test_create_test_data_valid_files():

    source_data_files = get_test_files()

    # list to store the issues from the source data
    source_data_issues = []

    # integer to count the number of files created
    file_count = 0

    # boolean to check if the test passed
    passed = False

    # log the name of the files to debug
    logging.debug(source_data_files)
    
    # loop through all the files in the source data directory
    for file in source_data_files:
         
        # this creates the test file from the source data
        issue,lines = create_test_data(file)

        # this appends the issue to the list
        source_data_issues.append(issue)

        # increment the file count
        file_count += 1

        # log the lines to debug
        logging.debug(lines)

        # log the issue to debug
        logging.debug(issue)

    # check if there are an equal number of files created as there are files in the source data directory
    if file_count == source_data_files.__len__():
        passed = True

    # this checks if the test passed
    assert passed == True


def test_get_live_data():

    # test if CI environment variable is set
    if check_if_CI():    
        # this gets the live data from the API
        live_data,lines_to_skip = get_live_data()

        # create an array of the expected live data
        expected_live_data = [os.getenv("ISSUE_NUMBER"),os.getenv("ISSUE_NAME"),os.getenv("ISSUE_BODY")]

        # this checks if the live data is correct
        assert live_data == expected_live_data and lines_to_skip == os.getenv("LINES_TO_SKIP")
    else:
        assert True