import os
import sys
import shlex
import shutil
from subprocess import Popen, PIPE
from subprocess import STDOUT, check_output as qx
from subprocess import CalledProcessError
from subprocess import TimeoutExpired
def execute_cmd(cmd):
    process = Popen(shlex.split(cmd), stdout=PIPE, stderr = PIPE)
    output, err = process.communicate()
    process.wait()
    output = output.decode('utf-8')
    err = err.decode('utf-8')
    return [output, err]
    
#log = open('runlog.txt', 'w+')

#inputLocation = sys.argv[2]
#outputLocation = sys.argv[3]

def get_testcase_files(testcase_dir='testcases'):
    testcase_files = []
    testcase_output_files = []
    
    for testcase_file in os.listdir(testcase_dir):
        if not os.path.isfile(testcase_dir+os.path.sep+testcase_file):
            continue
        if testcase_file.find('.in') >= 0:
            testcase_files.append(testcase_dir+os.path.sep+testcase_file)
            output_file = testcase_file[:testcase_file.find('.in')]+'.out'
            testcase_output_files.append(testcase_dir+os.path.sep+output_file)
            
    return [testcase_files, testcase_output_files]

def get_student_projects(project_dir='projects'):
    student_project_dirs = []
    
    for student_dir in os.listdir(project_dir):
        if not os.path.isdir(project_dir+os.path.sep+student_dir) or student_dir.find('.') == 0:
            continue
        student_project_dirs.append(project_dir+os.path.sep+student_dir)
        print('student_dir:' + student_dir)
        
    return student_project_dirs

def get_error_line_number(error_text):
    text_parts = error_text.split(":")
    if len(text_parts) != 3:
        print('*****---+++ ERROR: split by : returns ' + str(len(text_parts)) + ' elements. Expected:3')
        return -1
    line_part = text_parts[1]
    line_part = line_part.strip(" ")
    number_parts = line_part.split(" ")
    if len(number_parts) != 2:
        print('*****---+++ ERROR: split of line_parts by " " returns ' + str(len(number_parts)) + ' elements. Expected:2')
        return -1
    error_line = int(number_parts[1])
    return error_line

def read_true_error_line(file_name):
    # we assume that true error output files has only a single line
    fp = open(file_name)
    for line in fp:
        line = line.strip("\n")
        if line != "":
            return get_error_line_number(line)
    
    print('*****---+++ ERROR ERROR with the erorcase file:' + file_name)
    return -1
            

def main():
    testcases = get_testcase_files()
    errorcases = get_testcase_files('errorcases')
    student_dirs = get_student_projects()
    
    for student_dir in student_dirs:
        print('*****Start processing for:' + student_dir)
        student_score = 0
        os.chdir(student_dir)
        if os.path.exists('testcases'):
            shutil.rmtree('testcases')
        if os.path.exists('errorcases'):
            shutil.rmtree('errorcases')
            
        shutil.copytree('..'+os.path.sep+'..'+os.path.sep+'testcases', 'testcases')
        shutil.copytree('..'+os.path.sep+'..'+os.path.sep+'errorcases', 'errorcases')
        testcase_files = testcases[0]
        testcase_output_files = testcases[1]
        for i in range(len(testcase_files)):
            print('*****---Testcase:' + testcase_files[i])
            cmd = 'make all'
            execute_cmd(cmd)
            cmd = 'make run ARGS="'+testcase_files[i]+'"'
            execute_cmd(cmd)
            ir_code_file = testcase_files[i][:testcase_files[i].find('.')]+'.ll'
            cmd = 'lli-3.5 ' + ir_code_file
            [output, err] = execute_cmd(cmd)
            if (len(err) > 0):
                print('*****---+++ERR:' + err)
            output_fp = open(testcase_output_files[i])
            true_outputs = []
            for line in output_fp:
                line = line.strip("\n")
                if line != "":
                    true_outputs.append(int(line))
            
            # create integers from users outputs
            student_output_splits = output.split("\n")
            student_outputs = []
            for output in student_output_splits:
                if output != "":
                    student_outputs.append(int(output))
            
            # compare outputs
            if len(true_outputs) != len(student_outputs):
                print('*****---+++ERROR: unequal output line numbers')
            else:
                correct_count = 0
                for i in range(len(true_outputs)):
                    if (true_outputs[i] != student_outputs[i]):
                        print('*****---+++ERROR: output missmatch ' + str(true_outputs[i]) + ' != ' + str(student_outputs[i]))
                    else:
                        correct_count += 1
                if correct_count == len(true_outputs):
                    print('*****---+++TRUE OUTPUT')
                    student_score += 1
        
        errorcase_files = errorcases[0]
        errorcase_output_files = errorcases[1]
        for i in range(len(errorcase_files)):
            print('*****---Errorcase:'+errorcase_files[i])
            cmd = 'make all'
            execute_cmd(cmd)
            cmd = 'make run ARGS="'+errorcase_files[i]+'"'
            [output, err] = execute_cmd(cmd)
            student_output_splits = output.split("\n")
            error_line_number = -1
            for line in student_output_splits:
                line = line.strip("\n")
                if output != "":
                    error_line_number = get_error_line_number(output)
                    break
            
            # get the true error line
            true_error_line_number = read_true_error_line(errorcase_output_files[i])
            
            if error_line_number != -1 and true_error_line_number != -1:
                if error_line_number == true_error_line_number:
                    print('*****---+++TRUE OUTPUT')
                    student_score += 1
                else:
                    print('*****---+++ERROR ' + str(error_line_number) + ' != ' + str(true_error_line_number))
            else:
                print('*****---+++ERROR error_line_number=' + str(error_line_number) + ' and true_error_line_number=' + str(true_error_line_number))
            
        
        print('*****'+student_dir+' SCORE:' + str(student_score) + ' out of ' + 
        str(len(testcase_files) + len(errorcase_files)))
        # go back to the base dir
        os.chdir('..'+os.path.sep+'..')

if __name__ == '__main__':
    main()
            
#        if '.py' in input:
#            for testcase in os.listdir('testcases'):
#                cmd = input + ' '
#                #if b cmd = cmd + '-b '
#                #if f cmd = cmd +'-f '
#                cmd = cmd + '-s ' + testcase.replace('\n','')
#                cmd = cmd + '-i '
#                cmd = cmd + 'testdir'
#                try:
#                    #print(all)
#                    output = qx(shlex.split(cmd), stderr = STDOUT, timeout = 10)
#                except CalledProcessError as e:
#                    log.write('Error on ' + input)
#                    log.write(':{0} {1}\n'.format(e.returncode, e.output))
#                except TimeoutExpired as e:
#                    log.write('Error on ' + input)
#                    log.write('Time out is expired\n' + str(e.timeout))
#                except:
#                    log.write('Error on ' + input)
#                    log.write('Unexpected error\n' + str(sys.exc_info()))
#

