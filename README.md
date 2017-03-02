# CMPE 230 HW1 Test Script

## Dependencies

- The code is tested on Ubuntu 14.04 64 bit. If you are using Windows for the project, you may use cygwin, it would be better if you use a linux system on a virtual machine.
- If you try on Windows operating system, please write your setup and the problems you encounter on piazza.
- To be able to use this script, you should install llvm. To check whether you have a valid installation run the following command on the terminal: `lli --help`. We will use lli to test the generated code.

## Steps to test your project
1. Download as a zip of clone this project.
2. Copy the directory of your project including the Makefile under "projects" folder.
3. Make sure that your Makefile has **run** target (you can check out the given sample Makefiles). Do not forget to use ${ARGS} argument for run target.
4. To test run the script as `./run_testcases.py`. The script will copy testcases and errorcases to your project directory and will test one by one. If there is an error with your program, it will show the output of your program and the expected output.
5. Finally, you will see the number of testcases your program is able to pass. With the message saying `projects/2012800009 SCORE:1 out of 6`

**If you have any problem, please ask on piazza.**

