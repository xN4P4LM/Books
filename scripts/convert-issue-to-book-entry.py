#!/bin/python3

## this script does the following: 
    # 1. Read the relevant information from the environment variables
    # 2. Convert the issue text to a book entry in a markdown column format
    # 3. Append the book entry to either the readme.md or alt-lifestyle.md file
    # 4. Commit the changes to the repo
    # 5. Push the changes to the repo
    # 6. Create a pull request, referencing the issue, and assign it to the issue creator
    # 7. Add the issue to the project board


# import the necessary libraries to read the environment variables
from nis import cat
import os
from pickle import TRUE

LEADING_CHARACTERS_TO_STRIP = 2
DELIMITER = str("#")
LEADING_CHARACTER_CATEGORIES = str(DELIMITER + " ")
LEADING_CHARACTER_BOOK_ENTRY = str("|")
LEADING_CHARACTER_ISSUE_BODY = str("##")

# This checks if the script is running locally or in the github action
def CI():
    
    # check if the script is running locally or in the github action
    if os.getenv("CI") == "true":
        return True
    else:
        return False

# This function takes a provider color and converts it to the appropriate ANSI color code for the terminal
def Shell_color_formatting(color):

    # normalize the color
    color = color.lower()

    # create a dictionary of the color codes
    color_codes = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37"
    }

    if color not in color_codes:
        # if the color is not in the dictionary, return the default color code
        return color_codes["white"]

    # return the color code
    return color_codes[color]

def Print_Header(message, message_color, message_type, header_color = "white", header_message = "Message"):
    print("\033[%sm%s - %s:\033[0m" % (Shell_color_formatting(header_color), header_message, message_type))

def Print_message_to_terminal(message, message_color):
    print("\033[%sm%s\033[0m" % (Shell_color_formatting(message_color), message))

def Print_Separator():
    print("\033[0m\n----------------------------------------------------\n")

# Rudimentary logging function to the terminal
def Print_message(message = None, message_type = None, message_color = None, header = False, header_color = "white", header_message = "Info", only_message = False, print_separator = False):
    
    if print_separator:
        Print_Separator()

    elif header and only_message == False and print_separator == False:
        Print_Separator()
        Print_Header(message, message_color, message_type, header_color, header_message)
        Print_message_to_terminal(message, message_color)     
        
    elif only_message == False and print_separator == False:
        Print_Separator()
        Print_Header(message, message_color, message_type, header_color, header_message)
        Print_message_to_terminal(message, message_color)

    else:
        Print_message_to_terminal(message, message_color)
        
# This function determines the file to append the book entry to based on the primary category normalized in the primary category of the book
def File_to_edit(book_category):

    # create the book entry file variable
    book_entry_file = ""

    # create the alt-lifestyle array from the environment variable if in Github Actions
    if CI():
        alt_lifestyle = os.environ["ALT_LIFESTYLE"].split(",")
    else:
        alt_lifestyle = ["Polyamory and Ethical Non-monogamy"]

    # normalize the alt-lifestyle array
    alt_lifestyle = [category.lower() for category in alt_lifestyle]

    # normalize the categories
    normalized_book_category = book_category.lower()

    # determine the file to append the book entry to
    if normalized_book_category in alt_lifestyle:

        # set the book entry file to alt-lifestyle.md
        book_entry_file = "alt-lifestyle.md"

        # print a message to the terminal
        Print_message("The book entry will be appended to the alt-lifestyle.md file", "File to be written too", "white", False, "blue")

    else:

        # set the book entry file to README.md
        book_entry_file = "README.md"

        # print a message to the terminal
        Print_message("The book entry will be appended to the README.md file", "File to be written too", "white", False, "blue")

    return book_entry_file

def Create_book_entry(issue):
    # get the issue's title which is the book entry's title
    book_title = issue[1]

    # get the issue's body
    issue_body = issue[2]

    # parse the issue's body into an array of lines
    issue_body_lines = issue_body.strip("#").splitlines()

    # normalize the issue's body by removing the # from each line
    issue_body_lines = [line.lstrip(DELIMITER+DELIMITER+" ") for line in issue_body_lines]

    # get the line after Author(s) Name(s)
    book_author = issue_body_lines[issue_body_lines.index("Author(s) Name(s)") + 2]

    # get the line after ISBN-13 Number
    book_isbn = issue_body_lines[issue_body_lines.index("ISBN-13 Number") + 2]

    # get the line after Category
    book_category = issue_body_lines[issue_body_lines.index("Category") + 2]

    # get the line after Sub Category
    book_sub_category = issue_body_lines[issue_body_lines.index("Sub Category") + 2]

    # get the line after Amazon Link
    book_amazon_link = issue_body_lines[issue_body_lines.index("Amazon Link") + 2]

    # create the book entry using the markdown table format of 
    # | Book name | Author | SubCategory | ISBN-13 | Amazon Link | Have Read? |
    book_entry = "| %s | %s | %s | %s | [Amazon Link](%s) | Yes |" % (book_title, book_author, book_sub_category, book_isbn, book_amazon_link)

    # print that the book entry was created and return the book entry
    Print_message("The book entry was created", "Entry Created", "white", True, "blue")

    # print the book entry to the terminal
    Print_message(book_entry, "Entry", "white", True, "blue")
    

    return book_entry, book_category, book_title

# This function handles the reading and writing of the book entry file
def Access_File(action, book_entry_file, book_entry_file_contents = ""):

    if action == "read":
        # open the book entry file
        with open(book_entry_file, "r") as file:
            book_entry_file_contents = file.readlines()
        return book_entry_file_contents
    
    if action == "write":
        # open the book entry file
        with open(book_entry_file, "w") as file:
            file.writelines(book_entry_file_contents)
        return book_entry_file_contents

# This function takes the book entry and the book entry file and appends the book entry to the file
def UpdateFile(book_entry_file_contents, book_entry, book_category, book_entry_file):

    # create the entry inserted flag
    entry_inserted = False

    # create the entry already in file flag
    entry_already_in_file = False

    # update the text in the file to include the book entry at the first blank line after the category and a blank line after the book entry using markdown table format
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
                        book_entry_file_contents[index + index2] = book_entry + "\n"

                        # set the entry inserted flag to true
                        entry_inserted = True

                        # set the entry already in file flag to true
                        entry_already_in_file = True
                    
                    # check if the line is blank
                    if line2.strip() == "":

                        # insert the book entry after the blank line
                        book_entry_file_contents.insert(index + index2, book_entry + "\n")

                        # set the entry inserted flag to true
                        entry_inserted = True

                    # check if the entry was inserted
                    if entry_inserted:              
                        # write the file locally
                        Access_File("write", book_entry_file, book_entry_file_contents)
                        break

    # check if the entry was inserted                    
    if(entry_inserted):
        # print a message that the entry was inserted
        Print_message("The book entry was inserted into the file %s." % (book_entry_file), "Entry Inserted", "white", TRUE, "green", "Success")

        # return the entry inserted flag
        return entry_inserted, entry_already_in_file
    else:
        # print a message that the entry was not inserted
        Print_message("The book entry was not inserted into the file %s. Please check the file and try again." % (book_entry_file), "Entry Not Inserted", "white", TRUE, "red", "ERROR")

        # exit the program
        exit(-1)

def Get_categories(book_entry_file_contents):

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

# This function creates the markdown table format after the last category but before the comments in the file
def Create_category(book_entry_file_contents, book_category, categories):
    
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
    book_entry_file_contents.insert(last_category_index + 1, "# %s\n" % book_category)
    book_entry_file_contents.insert(last_category_index + 2, "| Book name | Author | SubCategory | ISBN-13 | Amazon Link | Have Read? |\n")
    book_entry_file_contents.insert(last_category_index + 3, "| --------- | ------ | ----------- | ------- | ----------- | ---------- |\n")


# This function check if the category exists in the book_entry_file_contents, and if it doesn't exist.
# Create the markdown table format after the last category but before the comments in the file
# # Category
# | Book name | Author | SubCategory | ISBN-13 | Amazon Link | Have Read? |
# | --------- | ------ | ----------- | ------- | ----------- | ---------- |
def Check_category(book_entry_file,book_entry_file_contents, book_category, categories):
    if book_category not in categories:

        # set the category found flag to false
        category_found = False

        # print a message that the category was not found and that it will be created along with the new category name
        Print_message("The category %s was not found in the file %s. The category will be created." % (book_category, book_entry_file), "Category Not Found", "white", TRUE, "yellow", "Warning")
       
        # create the category
        Create_category(book_entry_file_contents, book_category, categories)

        # advise the user that the category was created
        Print_message("The category %s was created in the file %s." % (book_category, book_entry_file), "Category Created", "white", TRUE, "green", "Success")
    else:
        
        # set the category found flag to true
        category_found = True

        # print a message that the category was found
        Print_message("The category %s was found in the file %s." % (book_category, book_entry_file), "Category Found", "white", TRUE, "green", "Success")

    # return the category found flag
    return category_found

# This function gets the issue information from the GitHub Actions Environment Variables
def Get_Live_Data():
        
        # get the issue number from the environment variables
        issue_number = os.getenv("ISSUE_NUMBER")

        # get the issue title from the environment variables
        issue_title = os.getenv("ISSUE_NAME")

        # get the issue body from the environment variables
        issue_body = os.getenv("ISSUE_BODY")

        # create the issue as an array of strings
        issue = [issue_number, issue_title, issue_body]

        # return the issue
        return issue

# This function creates the test data
def Create_Test_Data():

    # create the issue number
    issue_number = 1

    # create the issue title
    issue_title = "Test Book Entry"

    # create the issue body
    issue_body = """
    ## Book Name
    <!-- This should be the full Book Name, from the Issue Title -->
    Testing Book

    ## Author(s) Name(s)
    <!-- This should be the Author(s) Name(s) -->
    Testy

    ## ISBN-13 Number
    <!-- This should be the  ISBN-13 number -->
    928-515275241124

    ## Category
    <!-- This should be the books Primary category -->
    Neurodiversity

    ## Sub Category
    <!-- This should be the books Sub category -->
    testing

    ## Amazon Link
    <!-- This should be the raw Amazon link to purchase the book in the format of (https://www.amazon.com/dp/) -->
    https://www.amazon.com/dp/65874125
    """

    # create the issue as an array of strings

    issue = [issue_number, issue_title, issue_body]

    return issue
    
# This is the main helper function that determines if we use local test data or the GitHub API to get the issue information
def Choose_Source(ci):

    # create the issue variable
    issue = []

    # check if the script is 
    if ci == True:

        # get data from Action environment variables
        issue = Get_Live_Data()

    else:

        # create the test data
        issue = Create_Test_Data()    
    
    # return the issue
    return issue

# This function exports the file name as a file for GitHub Actions 
import os

def Export_variable(file_name, is_local):
    # export to a file named .files_changed for use in GitHub Actions
    if is_local:
        with open('.files_changed', 'a') as f:
            f.write(file_name)

        # read the file
        with open('.files_changed', 'r') as f:
            file_contents = f.read()

        # print the file contents
        print(file_contents)

        # print .files_changed full path
        print(os.path.abspath('.files_changed'))

        # print a message that the file name was exported
        Print_message("The file name %s was exported to .files_changed" % file_name, "File Name Exported", "white", True, "green", "Success")
    else:
        Print_message("The file name %s was not exported a file because the script is not running in CI." % file_name, "File Name Not Exported", "white", True, "yellow", "Warning")

        
# This function handles the main logic of the script
def Main():

    # Print the welcome message
    Print_message("Welcome to the convert-issue-to-book-entry python script", "Welcome", "white", TRUE, "blue", "Script Start")
    # Advise the user that the script will convert an issue to a book in markdown format
    Print_message("This script will convert a GitHub issue into to a markdown table containing the issues text and write it to the file", "Purpose", "white", TRUE, "blue","Script Start")

    # Checks if the script is running locally or in the github action
    is_local = CI()

    # if the script is running in GitHub Actions, print a message that the script is running there. 
    # Else print a message that the script is running locally
    if is_local:
        Print_message("The script is running in the GitHub Action", "Running in GitHub Actions", "white", TRUE, "green", "Success")
    else:
        Print_message("The script is running locally", "Running Locally", "white", TRUE, "yellow", "Warning")
 
    # If the script is running locally, it will use the test data
    # If the script is running in the github action, it will use the GitHub API to get the issue information
    issue = Choose_Source(is_local)

    # Create the book entry
    book_entry, book_category, book_title = Create_book_entry(issue) 
    
    # get the file to append the book entry to
    book_entry_file = File_to_edit(book_category)

    # export the file to a local variable using a terminal command
    Export_variable(book_entry_file, is_local)

    # get the file locally
    book_entry_file_contents = Access_File("read", book_entry_file)

    # get the categories in the file
    categories = Get_categories(book_entry_file_contents)

    # check if the category exists in the file
    category_found = Check_category(book_entry_file, book_entry_file_contents, book_category, categories)

    # update the file
    entry_inserted, entry_already_in_file = UpdateFile(book_entry_file_contents, book_entry, book_category, book_entry_file)

    if (entry_inserted == True and entry_already_in_file == True):

        # Print that book was added successfully to the category along with the book, category, and file name
        Print_message("Book: %s was updated successfully in the %s category in the file %s" % (book_title, book_category, book_entry_file), "Book Updated", "white", TRUE, "green", "Success")

    elif (entry_inserted == True and category_found == True):

        # Print that book was added successfully to the category along with the book, category, and file name
        Print_message("Book: %s was added successfully to the %s category in the file %s" % (book_title, book_category, book_entry_file), "Book added", "white", TRUE, "green", "Success")
    
    elif (entry_inserted == True and category_found == False):

        # Print that the book entry was added successfully, and a new category was created
        Print_message("Book: %s was added successfully to the new category: %s  in the file %s." % (book_title, book_category, book_entry_file), "Book and Category added", "white", TRUE, "green", "Success")

    elif (entry_inserted == False and category_found == True):

        # print that the book entry was not added successfully but the category was found
        Print_message("Book: %s was not added successfully to the %s category in the file %s." % (book_title, book_category, book_entry_file), "Category Found but book not inserted", "red", TRUE, "red", "Failure")
        exit(-1)
    
    elif (entry_inserted == False and category_found == False):
        
        # print that the book entry was not added successfully and the category was not found
        Print_message("Book: %s was not added, and category: %s was not found in file %s." % (book_title, book_category, book_entry_file), "Book not inserted", "red", TRUE, "red", "Failure")
        exit(-1)
    
    Print_message(print_separator=TRUE)

# call the main function
Main()