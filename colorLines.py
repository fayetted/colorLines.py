#!/usr/bin/env python
"""
colorLine.py is a small application that will take in STDIN and read each line.
It has 4 color modes based on lines and regex paterns.
    Mode 1: Do nothing (-l and -w ommited)
    Mode 2: Change entire line color (-l flag used)
    Mode 3: Change regex color (-w flag used)
    Mode 4: Change line and regex color (-l and -w flag used)
If -l and -w are given the colors will contrast each other.

Caveate: First REGEX match wins. (If your regular expression search finds 2 matches the first one wins.)
"""

import sys
import re
import argparse


class termColor():
    RED     = '\033[0m\033[91m'
    GREEN   = '\033[0m\033[92m'
    YELLOW  = '\033[0m\033[93m'
    BLUE    = '\033[0m\033[94m'
    PURPLE  = '\033[0m\033[95m'
    CYAN    = '\033[0m\033[96m'
    WHITE   = '\033[0m\033[97m'
    BLACK   = '\033[0m\033[98m'

    NONE = '\033[0m'

    BG_RED      = '\033[41m\033[97m'
    BG_GREEN    = '\033[42m\033[97m'
    BG_YELLOW   = '\033[43m\033[97m'
    BG_BLUE     = '\033[44m\033[97m'
    BG_PURPLE   = '\033[45m\033[97m'
    BG_CYAN     = '\033[46m\033[97m'
    BG_WHITE    = '\033[47m\033[30m'
    BG_BLACK    = '\033[48m\033[97m'


parser = argparse.ArgumentParser(description='Change colors of input lines and Regular Expresion matches.')
parser.add_argument("-l", "--line", action="store_true", dest="colorLine", default=False, help="Change line color based on regex")
parser.add_argument("-w", "--word", action="store_true", dest="colorWord", default=False, help="Change regex color in each line")
options = parser.parse_args()


#
## Make sure that the length of the regexList is not longer than the length of the color list.
#

#
## IPTables
#
regexList   = ['Dropped', 'SRC=\w+.\w+.\w+.\w+', 'DPT=\d+']
# regexList   = ['Dropped', 'Passed']
# regexList   = ['Dropped', 'Passed', '\wPT=\d+']
# regexList   = ['Passed', '\wPT=\d+']
# regexList   = ['PROTO=TCP', 'PROTO=ICMP', 'PROTO=UDP']
# regexList   = ['PROTO=ICMP', 'PROTO=UDP']
# regexList   = ['PROTO=\w+']     # This will color each line that contains PROTO and and highlight each instance of PROTO with the same color.
# regexList   = ['SPT=\d+', 'DPT=\d+']
# regexList   = ['[SD]PT=\d+']
# regexList   = ['\wPT=\d+']

#
## IPF
#
# regexList   = [' b ', ' p ']

#
## Squid
#
# regexList   = [ 'TCP_DENIED:\w+', 'TCP_HIT:\w+', 'TCP_CLIENT_REFRESH_MISS:DIRECT', 'TCP_REFRESH_\w+', 'TCP_MISS:\w+']

#
## AuthLog
#
# regexList   = [ '[iI]nvalid user \w+', 'User (\w+ from \S+) not allowed because not listed in AllowUsers', 'Received disconnect from \S+', 'Accepted publickey for \w+ from \S+', 'Did not receive identification string from']

#
## Generic
#
# regexList   = ['[tT][cC][pP]', '[iI][cC][mM][pP]', '[uU][dD][pP]']
# regexList   = ['[iI][gG][mM][pP]', '[iI][cC][mM][pP]', '[tT][cC][pP]', '[uU][dD][pP]']


fg_color       = ["NONE", "RED", "YELLOW", "BLUE", "PURPLE", "CYAN", "GREEN"]
bg_color    = ["NONE", "BG_RED", "BG_YELLOW", "BG_BLUE", "BG_PURPLE", "BG_CYAN", "BG_GREEN"]

termFuncFGColor = {'NONE':termColor.NONE, 'RED':termColor.RED, 'YELLOW':termColor.YELLOW, 'BLUE':termColor.BLUE, 'PURPLE':termColor.PURPLE, 'CYAN':termColor.CYAN, 'GREEN':termColor.GREEN}
termFuncBGColor = {'NONE':termColor.NONE, 'BG_RED':termColor.BG_RED, 'BG_YELLOW':termColor.BG_YELLOW, 'BG_BLUE':termColor.BG_BLUE, 'BG_PURPLE':termColor.BG_PURPLE, 'BG_CYAN':termColor.BG_CYAN, 'BG_GREEN':termColor.BG_GREEN}

if len(regexList) > len(fg_color):
    print "You don't have enough colors to match all your regular expressions."
    sys.exit()


# Start with your terminal's default color Scheme.
print termColor.NONE

while 1:
    # Read in STDIN, asign it to 'line' and strip off any [NEW LINE FEEDS].
    try:
        line = sys.stdin.readline()
        line = line.rstrip('\n')
    # Accept and break on [CTRL-C]
    except KeyboardInterrupt:
        break

    if not line:
        break

    # Reset the found Regex tracker.
    found = 0


    # Loop through each regular expresion you submitted and keep a count (c1).
    for c1, regex in enumerate(regexList):
        if re.search(regex, line):
            # If the regex was found in the line we set the Regex tracker
            found = 1

            # If you requested entire lines to change color, set the color based on c1 and change the line to that color.
            if options.colorLine:
                try:
                    line = lineColor + line
                except:
                    lineColor = termFuncFGColor[fg_color[c1+1]]
                    line = lineColor + line
            # IF you did not want the lines to be colored set the lineColor variable to the default color scheme.
            else:
                lineColor = termColor.NONE

            # If you requested each REGEX to change color.
            if options.colorWord: 
                # Find each regex in the line and store it as list (x)
                x=re.findall(regex, line)
                # Loop over each found regex and change the color
                for c2, match in enumerate(x):
                    line = re.sub(match, termFuncBGColor[bg_color[c1+1+c2]] + match + lineColor, line)

    print line + termColor.NONE
    lineColor = None
