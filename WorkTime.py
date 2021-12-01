#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import cmd
import os
from os.path import isfile, splitext
from utils import TIME_FORMAT, WORK_TIME_BANNER, formatStats, readWtFile, writeWtFile
from datetime import datetime

class WorkTime(cmd.Cmd):
    prompt = '>'
    intro = WORK_TIME_BANNER + '\nType help or ? to show available commands.\n'
    start_time = None
    file = None
    fileRecording = None
    recording = False
    total_time = None
    
    def do_start(self, arg, initial=None):
        'start <project> - Starts timing work on a given project.\n'
        if not arg:
            print('[ERROR] No project given. Check \'help start\' for more info.\n')
        else:
            self.file = arg + '.wt'
            if not self.recording:
                self.file = arg + '.wt'
                if isfile(self.file):
                    self.start_time=datetime.today().strftime(TIME_FORMAT)
                    self.recording = True
                    self.fileRecording = self.file

                    print(f'[INFO] Now counting work time in {arg}: {self.start_time}')
                    print('[INFO] To stop and save work time type \'stop\'.\n')
                else:
                    if input(f'[CONFIRMATION] No project found with name \'{self.file}\'. Do you wish to create a new one? (y/n)\n>') == 'y':
                        self.do_newproject(arg)
                    else:
                        print('[INFO] Project creation cancelled.\n')
            else:
                print(f'[ERROR] Currently counting worktime in {splitext(self.file)[0]}. Type \'stop\' to stop the count.\n')


    def do_newproject(self, arg, initial=None):
        'newproject <project> - Creates a new project given a name. To start counting work time type \'start <project>\'.\n'
        if not arg:
            print('[ERROR] No project given. Check \'help newproject\' for more info.\n')
        else:
            self.file = arg + '.wt'
            
            wtData = {'star_time': '0:00:00'}
            writeWtFile(wtData, self.file)

            print(f'[INFO] New project created. To start counting work time type \'start {arg}\'.\n')
        if self.recording:
            print(f'[REMINDER] Currently counting worktime in {splitext(self.file)[0]}. Type \'stop\' to stop the count.\n')


    def do_removeproject(self, arg, initial=None):
        'removeproject <project> - Removes a project by name. Needs confirmation.\n'
        if not arg:
            print('[ERROR] No project given. Check \'help removeproject\' for more info.\n')
        else:
            self.file = arg + '.wt'
            if not self.recording:
                if isfile(self.file):
                    if input(f'[CONFIRMATION] Are you sure you want to delete worktime data form project named \'{self.file}\'? (y/n)\n>') == 'y':
                        os.remove(self.file)
                        print(f'[INFO] Worktime data from {arg} removed successfully.\n')
                    else:
                        print('[INFO] Project deletion cancelled.\n')
                else:
                    print(f'[ERROR] No worktime file found with name {self.file}\n')
            else:
                print(f'[ERROR] Currently counting worktime in {splitext(self.file)[0]}. Type \'stop\' to stop the count.\n')


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
            print(f'[INFO] Worktime counted for this last session in {splitext(self.fileRecording)[0]}: {total_time}\n')

            wtData = readWtFile(self.fileRecording)
            wtData[self.start_time] = str(total_time)
            writeWtFile(wtData, self.fileRecording)

            self.recording = False

    def do_worktime(self, arg, initial=None):
        'worktime <project> - Shows the statistics recorded for a given project.\n'
        self.file = arg + '.wt'
        time_zero = datetime. strptime('00:00:00', '%H:%M:%S')
        result = datetime. strptime('00:00:00', '%H:%M:%S')

        if isfile(self.file):
            wtData = readWtFile(self.file)
            for entry in wtData:
                result = (result -time_zero + datetime.strptime(wtData[entry], '%H:%M:%S'))
                
            print(formatStats(arg, result.time()))
                
        else:
            print(f'[ERROR] No worktime file found with name {self.file}\n')

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
