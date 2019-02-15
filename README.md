# python1
The program ensure that the data in a column does not exceed the maximum specified number of characters. 
For the event name, and athlete’s first name and surname, if they exceed the maximum specified number of characters the name is to be truncated to the maximum allowed number of characters. 
For all other columns, if the data exceeds the maximum specified number of characters then the data in the row is considered to be corrupt.
The program also ensure that the data in a column is correct according to the specified format rules. 
If the country code is three letters but they are not all in uppercase then your program should convert them to uppercase. 
If the medal column contains the strings Gold, Silver or Bronze, but with different letter case, 
then the program should convert the strings to be exactly Gold, Silver or Bronze (i.e. first letter is uppercase and all others are lowercase). Any other illegal values, according to a column’s format rules, mean that the row is considered to be corrupt.
The program should also ensure that the rules regarding data being in a particular column are also correctly implemented. 
If these rules are broken the row is considered to be corrupt.
Every row that is identified as being corrupt is to be output to the result file, as it was read in from the raw data file (minus the athlete id column), and with an extra column added to that row containing the text CORRUPT.
