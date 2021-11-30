import re
import argparse


#  OOP in order to encapsulate differences between output formats

class colors:
        none = '\033[0m'
        red = '\033[31m'
        green = '\033[32m'
        blue = '\033[34m'
        cyan = '\033[36m'
        yellow = '\033[93m'

class parameters:
    '''
    Defines output based on parameters selected from the command line.

    Optional command line parameters:
    -c Highlights matching text
    -m Machine-readable output as 
        file_name:no_line:start_pos:matched_text
    '''

    def __init__(self, file, line, line_num, match_pos, match):
        self.file = file
        self.line = line
        self.line_num = line_num
        self.match_pos = match_pos
        self.match = match


    def display_line(self): 
        '''
        Prints highlighted matching text in color when -c option is specified.
        '''
        if color:
            highlight = colors.cyan
        else:
            highlight = colors.none
        
        formatted_line = self.line.replace(match.group(), highlight+match.group()+colors.none)
        print(f'| File name: {self.file} | Line number: {self.line_num} | Match starts at: {self.match_pos} \n| Match found: {formatted_line}')


    def machine_line(self):
        '''
        Output is generated in machine-readable format when -m option is specified.
        Format: file_name:no_line:start_pos:matched_text
        '''
        print(f'{self.file}:{self.line_num}:{self.match_pos}:{match.group()}')


#  Parse arguments from user input

parser = argparse.ArgumentParser(
                    description = 'Search one or more files for a regular expression.')
parser.add_argument('regex', 
                    help = 'regex pattern to find.  Expression must be surrounded in quotes, example: "\d{3}-\d{3}-\d{4}"'
                    )
parser.add_argument('filename', 
                    nargs = '+', 
                    help = 'file(s) to search'
                    )
group = parser.add_mutually_exclusive_group()
group.add_argument('-c',
                    action = 'store_true',
                    help = 'highlight matches in color'
                    )
group.add_argument('-m', 
                    action = 'store_true',
                    help = 'print in machine-readable format'
                    )

args = parser.parse_args()
pattern = args.regex
input_file_list = args.filename
if args.c: 
    color = True
    machine = False
elif args.m:
    color = False
    machine = True
else:
    color = False
    machine = False


#  Search for matches and print output based on parameters

for file_name in input_file_list:
    for i, line in enumerate(open(file_name)):
        for match in re.finditer(pattern, line):
            output = parameters(file_name, line, i+1, match.start(), match.group())
            if machine:
                output.machine_line()
            else:
                output.display_line()                

