'''
Description: Scan the project and output detailed vulnerability report
LastEditTime: 2021-10-21 12:55:26
'''

import os
from util.frontend import *
from time import time

def analysis(file_path):
    '''
    description: Scan the project and output detailed vulnerability report
    param {
        file_path: Path of the project to be scanned
    }
    return {
        analysis_time:  Time of analysis
        json_path:      Path of report.json
        txt_path:       Path of report.txt
    }
    '''    

    start = time()
    cur_path = os.path.abspath(os.getcwd())
    os.chdir(file_path)#Enter the unzipped folder

    os.system('./configure')
    os.system('make clean')
    os.system('infer run -- make --keep-going')

    end = time()
    analysis_time = (end - start)*1000

    json_path = os.path.join(os.getcwd(), 'infer-out', 'report.json')
    txt_path = os.path.join(os.getcwd(), 'infer-out', 'report.txt')  
    
      

    os.chdir(cur_path)

    return analysis_time, json_path, txt_path