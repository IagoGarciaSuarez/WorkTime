import json
import os
from string import Template

HELP_INFO = '''
Available commands:
> create <project>  --> Creates a project registry.
> start <project>   --> Starts the timer for the current session in a given project.
> stop              --> Stops the timer for the current session and project.
> add [-minutes | -hours] <time> <project> --> Adds time in hours or minutes to a given project.
'''

WORK_TIME_BANNER = '''
 ____ ____ ____ ____ _________ ____ ____ ____ ____ 
||W |||o |||r |||k |||       |||T |||i |||m |||e ||
||__|||__|||__|||__|||_______|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|

'''

TIME_FORMAT = '%d-%m-%Y - %H:%M:%S'
WORKTIME_DIR = os.path.dirname(os.path.realpath(__file__))

STATS_TEMPLATE = '''
Total time in $projectname\t$total_time
'''
def readWtFile(file):
    worktimefile = os.path.join(WORKTIME_DIR, file)
    with open(worktimefile, 'r') as f:
        wtData = json.load(f)
        f.close()
    return wtData

def writeWtFile(wtData, file):
    worktimefile = os.path.join(WORKTIME_DIR, file)
    with open(worktimefile, 'w+') as f:
        json.dump(wtData, f) 
        f.close()   

def formatStats(projectname, total_time):
    return Template(STATS_TEMPLATE).substitute(projectname=projectname, total_time=total_time)

