#------------------------------------------#
# Title: Assignment06
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# JRoe, 2020-Aug-18, Created File
# JRoe, 2020-Aug-18, Edited File
# DKlos, 2020-Aug-23, Pass in local variables to class methods.
# DKlos, 2020-Aug-23, Correct function calls for revised functions.
# Add structured error handling around the areas where there is user interaction, type casting (string to
#int) or file access operations. You do NOT need to create custom error classes; the python build in ones
#are plenty capable for this!
#Modify the permanent data store to use binary data
#------------------------------------------#

import pickle
import sys

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
open(strFileName, 'wb').close() #Creates blank file

# -- PROCESSING -- #

class DataProcessor:
    """Processing the data within code"""
    @staticmethod
    # Pass lstTbl in to the function
    def add_todict(cd_id, cd_title, cd_artist, table):
        """Function to add entered data to dictionary list in local memory
        Args:
            3 positional arguements, in this case coorelating to user inputs
        Returns:
            None.
        """
        dicRow = {'ID': cd_id, 'Title': cd_title, 'Artist': cd_artist}
        table.append(dicRow)

    @staticmethod
    # TODO add error message for non-integer ALL ERRORS IN FXNS
    def delete_fxn(id_to_remove, table):
        """Function to add delete entries based on ID
        Args:
            None.
        Returns:
            None.
        """        
        intRowNr = -1
        blnCDRemoved = False
        # Use a local copy of lstTbl (table)
        # for row in lstTbl:
        for row in table:
            intRowNr += 1
            # Use the local variable id_to_remove
            # if row['ID'] == intIDDel:
            if row['ID'] == id_to_remove:
                # Again use a local copy of this
                # del lstTbl[intRowNr]
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
    
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries
        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        Returns:
            None.
        """
        # TODO maybe add a "filenotfound?"
        # TODO Pickle
        
        table.clear()  # this clears existing data and allows to load data from file
        with open(file_name, 'rb') as item:
            list1 = pickle.load(item)

        
    @staticmethod
    def save_fxn(file_name, table):
        """Function to save entered data to designated file
        Args:
            None.
        Returns:
            None.
        """      
        with open(file_name, 'wb') as item:
            pickle.dump(table, item)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user
        Args:
            None.
        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection
        Args:
            None.
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice
    
    @staticmethod
    def user_entry(table): 
        """Gets user input for "enter data" section 
        Args:
            None.
        Returns:
            ID, song, and title
        """
        while True:
            strID = input('Enter ID: ').strip()
            # Ensure only integer inputs
            try:
                intID = int(strID)
                break
            except ValueError:
                print('\nIntegers Only!\n')
                continue
            except:
               for row in table:
                   if row['ID'] == intID:
                       print('This ID has been used!')
                
               

        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()     
        return intID, strTitle, stArtist      
    
    @staticmethod
    def show_inventory(table):
        """Displays current inventory table
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

# 1. When program starts, read in the currently saved Inventory
#FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    # need to create a blank file
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODO prevent user from entering same CD
        ID, Title, Artist = IO.user_entry(lstTbl)
        # 3.3.2 Add item to the table
        DataProcessor.add_todict(ID, Title, Artist, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_fxn(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.save_fxn(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')



