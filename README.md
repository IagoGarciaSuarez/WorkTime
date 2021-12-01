# WorkTime
Simple app to control worktime in each project.

## Commands
HELP
- help -> Shows every command.
- help <command> -> Show detailed information for a given command

START PROJECT
- newproject <project> -> creates a project with the given name.
- start <project> -> starts to count in a given project. If no worktime file is found for the project, it will ask to create a new one, but it will need to be    started afterwards.

END PROJECT
- removeproject <project> -> removes a given project. Needs confirmation.
- stop -> stops the current count and saves the worktime data.
- exit -> calls stop command to save the current worktime count and ends the program.

DISPLAY PROJECT
- listprojects -> lists all available projects in the worktime program directory.
- worktime <project> -> displays worktime stats for a given project
  
