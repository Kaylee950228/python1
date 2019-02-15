
__author__ = ""



from assign1_utilities import get_column, replace_column, truncate_string

def remove_athlete_id(row) :
    """Remove the first column of every row seperated by comma and return
       everything after the first comma.

    Parameters:
       row (str): String of data with comma separators (CSV format).
       
    Return:
       Everything after the first comma.
       
    Precondition:
       row != None
"""
    i = 0
    while row[i] != ',' :     #Find the first comma
        i += 1 
    return row[i+1:]

def isfloat(value):
    """ Function to check if a string can be converted to a float.

    Parameter:
        value(str): The string for checking.
        
    Return:
        If value can be transformed to a float, return True;
        otherwise, return false.

    Precondition:
        value != None
    """
    result = True
    try:
        float(value)
    except ValueError:    # Unable to convert value to a float
        result = False
    except TypeError:     
        result = False    # Not a valid type
    return result

def main() :
    """Main functionality of program."""
    with open("athlete_data.csv", "r") as raw_data_file, \
         open("athlete_data_clean.csv", "w") as clean_data_file :
        for row in raw_data_file :
            corrupt = False
            completed_game = False
            row = remove_athlete_id(row)
            row_to_process = row    # Saves row in original state, minus athlete id.

            #Check and fix the length of eventname, athlete’s Firstname and Surname
            for i in range(0,3) :
                name = get_column(row_to_process,i)
                if len(name) == 0 :
                    corrupt = True
                elif len(name) <= 30 :
                    for n in name :
                        if not (n.isalpha() or n.isdigit() or n.isspace() or n =="-" or n =="'") :
                            corrupt = True
                elif len(name) > 30 :
                    row_to_process = replace_column(row_to_process, truncate_string(name, 30), i)
            
            # Check the length of countrycode and test if it is uppercase alpha 
            country = get_column(row_to_process,3)
            if len(country) != 3 or country.isalpha() == 0 :
                corrupt = True
            else :
                country = country.upper()
                row_to_process = replace_column(row_to_process, country, 3) 

            # Check Score format
            score = get_column(row_to_process,5)
            if len(score) != 0 and (len(score) > 6 or isfloat(score) == 0) :
                corrupt = True
                
            # Check Time format
            time = get_column(row_to_process,6)
            if len(time) != 0 and (len(time) > 8 or isfloat(time) == 0) :
                corrupt = True

            # Check Place format
            place = get_column(row_to_process,4)
            if not ((len(place) <= 3
                     and (place. isdigit() and not (score == "" and time == "" ) and not (score.isdigit() and time.isdigit())
                     or place == ''
                     or place == 'DNS' or place == 'DNF' or place == 'PEN'))) :
                   corrupt = True
            
            # Check and fix the format of medal
            medal = str(get_column(row_to_process,7))
            if medal.upper() == "GOLD" :
                medal = "Gold"
            elif medal.upper() == "SILVER" :
                medal = "Silver"
            elif medal.upper() == "BRONZE" :
                medal = "Bronze"
            elif medal != "" :
                corrupt = True

            # Check the format of olympic record
            olympic_record = get_column(row_to_process,8)
            if not (len(olympic_record) <= 8
                    and isfloat(olympic_record)
                    and olympic_record == "") :
                   corrrupt = True

            # Check world record format
            world_record = get_column(row_to_process,9)
            if not (len(world_record) <= 8
                    and isfloat(world_record)
                    and world_record == olympic_record
                    or world_record == "") :
                   corrupt = True

            # Check track record format
            raw_track_record = get_column(row_to_process,10)
            track_record = raw_track_record[:-1]
                                                 # Delete a new line
                                                 # character at the end of row.
                                                 
            if len(track_record) != 0 \
               and (len(track_record) > 8
                    or isfloat(track_record) == 0) :
                corrupt = True             

            # Check correspondence between medal and place
            if medal == "Gold" and place != "1" :
                corrupt = True
            elif medal == "Silver" and place != "2" :
                corrupt = True
            elif medal == "Bronze" and place != "3" :
                corrupt = True
            elif place == "1" and medal != "Gold" :
                corrupt = True
            elif place == "2" and medal != "Silver" :
                corrupt = True
            elif place == "3" and medal != "Bronze" :
                corrupt = True
            
            # Save the row data to the cleaned data file.
            if not corrupt :
                clean_data_file.write(row_to_process)
            else :
                row = row[:-1]      # Remove new line character at end of row.
                clean_data_file.write(row + ",CORRUPT\n")
            
# Call the main() function if this module is executed
if __name__ == "__main__" :
    main()



"""
----------------------------------------------
MARKING:   ##### CSSE7030 #####

Total: 8

Meeting comments:
   Talked about function splitting

General comments:
   Programming Constructs
       Program is Well Structured & Readable
           Code structure highlights logical blocks and is easy to understand. Code does not employ global variables. Constants clarify code meaning.
       Variable and function names are meaningful
           All variable and function names are clear and informative, increasing readability of the code.
       Algorithmic logic is appropriate
           Algorithm design is simple, appropriate, and has no logical errors. Control structures are well used to implement expected logic.
       Functions used appropriately
           Functions represent useful logical functionality and parameters and return values are appropriate.
       Well-Designed Functions
           Program may use functions correctly, but some functions are large blocks of logic that implement multiple tasks.
   Functionality
       Column size limits
           All size limit rules are implemented correctly.
       Column format rules
           At least three of the five different format rules are implemented correctly
       Conditional constraints between columns
           At least two of the four different constraints between columns are implemented correctly.
       Extension
           Less than two of the rules listed under the heading “Extension” are implemented correctly.
   Documentation
       Clear & Concise Comments
           Comments provide useful information that elaborates on the code. These are useful in understanding the logic and are not too wordy.
       All functions having informative docstring comments
           All docstrings provide a complete, unambiguous, description of how to use the function.
       Appropriate use of inline comments
           Inline comments are used to explain logical blocks of code (e.g. significant loops or conditionals).
   General

----------------------------------------------
TEST RUN:
Tests version: 1.1.0
Version: 2018s1
/------------------------------------------------------------------------------\
|                              Summary of Results                              |
\------------------------------------------------------------------------------/
BasicTests
    +  1. Tests a file with no corruptions
ColumnSizeTests
    +  1. Tests that overlong event and athlete names are appropriately truncated
    +  2. Tests that corrupt size limit violations are correctly marked
ColumnFormatTests
    +  1. Tests the format of event and athlete names
    +  2. Tests the format of the country code column
    +  3. Tests the format of the place column
    -  4. Tests the format of the medal column
    -  5. Tests the format of the score, time, and record columns
ConditionalConstraintTests
    +  1. Tests conditional constraints between place, score and time
    +  2. Tests conditional constraints between place and medal
    +  3. Tests conditional constraints between record columns
MedalTieTests
    +  1. Tests that valid medal ties are not marked as corrupt
    -  2. Tests that invalid medal ties are correctly marked as corrupt
ThreeMedalRuleTests
    +  1. Tests valid violations of the three-medal-rule
    +  2. Tests corrupt violations of the three-medal rule
MasterFileTests
    +  1. Tests valid names and country codes
    -  2. Tests names and country codes that do not exist
    -  3. Tests that masterfile values have not been hardcoded
MegaDiff
    -  1. Mega diff test!
--------------------------------------------------------------------------------
/------------------------------------------------------------------------------\
|                                 Failed Tests                                 |
\------------------------------------------------------------------------------/
================================================================================
FAIL: ColumnFormatTests 4. Tests the format of the medal column
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Men's Luge,Chris,Mazdzer,USA,2,,190.728,silver,,,\n" != "Men's Luge,Chris,Mazdzer,USA,2,,190.728,Silver,,,\n"
    - Men's Luge,Chris,Mazdzer,USA,2,,190.728,silver,,,
    ?                                         ^
    + Men's Luge,Chris,Mazdzer,USA,2,,190.728,Silver,,,
    ?                                         ^
    
     : Test failed on line 18 of athlete_data_clean.csv
     This line tests: Capitalization of medal

================================================================================
FAIL: ColumnFormatTests 5. Tests the format of the score, time, and record columns
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Men's Luge,Johannes,Ludwig,GER,3,,190.932,bronzE,,,\n" != "Men's Luge,Johannes,Ludwig,GER,3,,190.932,Bronze,,,\n"
    - Men's Luge,Johannes,Ludwig,GER,3,,190.932,bronzE,,,
    ?                                           ^    ^
    + Men's Luge,Johannes,Ludwig,GER,3,,190.932,Bronze,,,
    ?                                           ^    ^
    
     : Test failed on line 21 of athlete_data_clean.csv
     This line tests: Invalid characters in score

================================================================================
FAIL: MedalTieTests 2. Tests that invalid medal ties are correctly marked as corrupt
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Wome[54 chars]ld,,,\n\nWomen's Speedskating 500m,Yara,van Ke[89 chars],,\n" != "Wome[54 chars]ld,,,,CORRUPT\n\nWomen's Speedskating 500m,Yar[113 chars]PT\n"
    Diff is 636 characters long. Set --diff to see it.
    
     : At least one of rows 15-17 should have been marked as corrupt
     These lines test: Invalid tie

================================================================================
FAIL: MasterFileTests 2. Tests names and country codes that do not exist
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Men's Mooguls,Rohan,Chapman-Davies,AUS,,,,,,,\n" != "Men's Mooguls,Rohan,Chapman-Davies,AUS,,,,,,,,CORRUPT\n"
    - Men's Mooguls,Rohan,Chapman-Davies,AUS,,,,,,,
    + Men's Mooguls,Rohan,Chapman-Davies,AUS,,,,,,,,CORRUPT
    ?                                              ++++++++
    
     : Test failed on line 8 of athlete_data_clean.csv
     This line tests: Mispelled event name
     This line should have been marked as corrupt

================================================================================
FAIL: MasterFileTests 3. Tests that masterfile values have not been hardcoded
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: 'Womens Half-Pipe,Elizabeth,Hocking,CAN,,,,,,,\n' != 'Womens Half-Pipe,Elizabeth,Hocking,CAN,,,,,,,,CORRUPT\n'
    - Womens Half-Pipe,Elizabeth,Hocking,CAN,,,,,,,
    + Womens Half-Pipe,Elizabeth,Hocking,CAN,,,,,,,,CORRUPT
    ?                                              ++++++++
    
     : Test failed on line 16 of athlete_data_clean.csv
     This line tests: NEW is valid in the replacement country file - this test ensures the masterfiles haven't been hardcoded into the code
     This line should have been marked as corrupt

================================================================================
FAIL: MegaDiff 1. Mega diff test!
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Men'[5297 chars].728,silver,,,\nMen's Luge,Johannes,Ludwig,GER[3962 chars],,\n" != "Men'[5297 chars].728,Silver,,,\nMen's Luge,Johannes,Ludwig,GER[4114 chars],,\n"
    Diff is 12119 characters long. Set --diff to see it.

--------------------------------------------------------------------------------
Ran 19 tests in 0.034 seconds with 13 passed/0 skipped/6 failed.


END TESTS
"""

