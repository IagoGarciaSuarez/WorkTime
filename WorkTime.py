#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import cmd
import os
from os.path import isfile, splitext
from utils import TIME_FORMAT, WORK_TIME_BANNER
from datetime import datetime
import json

class WorkTime(cmd.Cmd):
    prompt = '>'
    intro = WORK_TIME_BANNER + '\nType help or ? to show available commands.\n'
    start_time = None
    file = None
    recording = False
    total_time = None
    wtData = None
    
    def do_start(self, argv, initial=None):
        'start <project> - Starts timing work on a given project.\n'
        if not argv:
            print('[ERROR] No project given. Check \'help start\' for more info.\n')
        else:
            self.file = argv + '.wt'
            if not self.recording:
                self.file = argv + '.wt'
                if isfile(self.file):
                    self.start_time=datetime.today().strftime(TIME_FORMAT)
                    self.recording = True
                    with open(self.file, 'r') as f:
                        self.wtData = json.load(f)
                        f.close()

                    print(f'[INFO] Now counting work time in {argv}: {self.start_time}')
                    print('[INFO] To stop and save work time type \'stop\'.\n')
                else:
                    if input(f'[CONFIRMATION] No project found with name \'{self.file}\'. Do you wish to create a new one? (y/n)\n>') == 'y':
                        self.do_newproject(argv)
                    else:
                        print('[INFO] Project creation cancelled.\n')
            else:
                print(f'[REMINDER] Currently counting worktime in {splitext(self.file)[0]}. Type \'stop\' to stop the count.\n')


    def do_newproject(self, argv, initial=None):
        'newproject <project> - Creates a new project given a name. To start counting work time type \'start <project>\'.\n'
        if not argv:
            print('[ERROR] No project given. Check \'help newproject\' for more info.\n')
        else:
            self.file = argv + '.wt'
            with open(self.file, 'w+') as f:
                self.wtData = {'star_time': 'total_time'}
                json.dump(self.wtData, f) 
                f.close()   
            print(f'[INFO] New project created. To start counting work time type \'start {argv}\'.\n')
        if self.recording:
            print(f'[REMINDER] Currently counting worktime in {splitext(self.file)[0]}. Type \'stop\' to stop the count.\n')


    def do_removeproject(self, argv, initial=None):
        'removeproject <project> - Removes a project by name. Needs confirmation.\n'
        if not argv:
            print('[ERROR] No project given. Check \'help removeproject\' for more info.\n')
        else:
            self.file = argv + '.wt'
            if not self.recording:
                if isfile(self.file):
                    if input(f'[CONFIRMATION] Are you sure you want to delete worktime data form project named \'{self.file}\'? (y/n)\n>') == 'y':
                        os.remove(self.file)
                        print(f'[INFO] Worktime data from {argv} removed successfully.\n')
                    else:
                        print('[INFO] Project deletion cancelled.\n')
                else:
                    print(f'[ERROR] No worktime file found with name {self.file}\n')
            else:
                print(f'[REMINDER] Currently counting worktime in {splitext(self.file)[0]}. Type \'stop\' to stop the count.\n')


    def do_listprojects(self, initial=None):
        'listprojects - Lists all projects in the current directory.\n'
        for self.file in os.listdir("."):
            if self.file.endswith(".wt"):
                print(splitext(self.file)[0])

    def do_stop(self, initial=None):
        'stop - Stops current worktime count and saves it to the project worktime data.\n'
        if not self.recording:
            print('[ERROR] No project worktime is active. Type \'help stop\' for more info.\n')
        else:
            total_time = datetime.strptime(datetime.today().strftime(TIME_FORMAT), TIME_FORMAT) - datetime.strptime(self.start_time, TIME_FORMAT)
            print(f'[INFO] Worktime counted for this last session in {splitext(self.file)[0]}: {total_time}\n')
            with open(self.file, 'w') as f:
                self.wtData[self.start_time] = str(total_time)
                json.dump(self.wtData, f)
                f.close()

            self.recording = False

    def do_exit(self, initial=None):
        'exit - Stop and exit WorkTime'
        return self.close()

    def close(self):
        self.do_stop()
        return True


if __name__ == "__main__":
    wt = WorkTime()
    try:
        wt.cmdloop()
    except KeyboardInterrupt:
        wt.close()
