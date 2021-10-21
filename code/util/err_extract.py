'''
Description: Extract and process vulnerability reports
LastEditTime: 2021-10-21 16:46:35
'''
import json
import pandas as pd
from pandas import DataFrame
import re
import os

from util.frontend import print_to_log


def single_version_extract(jsonpath, txtpath, output_path, name):
    '''
    description: Handle vulnerability report and return dataframe
    param {
        jsonpath:      Path of report.json
        txtpath:       Path of report.txt
        output_path:    Path of processed analysis report
        name:           Name of project
    }
    return {
        df:  Processed analysis report
    }
    '''    

    if os.path.isdir(output_path):
        pass
    else:
        os.mkdir(output_path)


    jsonrecords = [json.loads(line) for line in open(jsonpath)]
    allbug = jsonrecords[0]#All scanned vulnerabilities

    with open(txtpath) as f:
        txt = f.readlines()
    
    f.close()

    # Exclude false positive
    index_to_del = []
    for i in range(len(allbug)):
        if (allbug[i]["bug_type"] == "NULL_DEREFERENCE" 
            and allbug[i]["qualifier"].find('`null`') != -1 
            ):
            index_to_del.append(i)
    index_to_del.sort()
    del_num = 0
    for i in range(len(index_to_del)):
        del allbug[index_to_del[i]-del_num]
        del_num += 1

    i = 0
    for no in range(0, len(allbug)*10, 10):
        # Create a new field to save the error code line
        allbug[i]["error_code_line"] = txt[no+5]
        i = i+1

    pattern = re.compile(r'[a-z_A-Z]+\((.*?)\)')
    count = 0
    other = 0

    for i in range(len(allbug)):
        # Number the detected bug
        allbug[i]["sequence"] = i+1  

        line = allbug[i]["error_code_line"]
        # Create a new field to save the name of the API involved in the vulnerability
        if pattern.search(line):
            APIname = pattern.search(line).group().split('(')[0]
            allbug[i]["API_name"] = APIname

            if(APIname[:3] == '_Py' or APIname[:2] == 'Py'):# Python/C API
                allbug[i]["is_pythonCAPI"] = 1
                count = count+1
            else:
                allbug[i]["is_pythonCAPI"] = 0
                other = other+1
                
        else:
            allbug[i]["API_name"] = ''
            allbug[i]["is_pythonCAPI"] = -1

    df = DataFrame(allbug)

    df.to_csv(output_path + '/' + name + '.csv', index = False)#csv

    df.to_excel(output_path + '/' + name + '.xlsx', index = False)#excel

    
    return df

def single_version_sum(df, log_path):
    '''
    description: Count the number of various types of vulnerabilities
    param {
        df:         Processed analysis report
        log_path:   Path of log file
    }
    return {
        sum: Statistical results
    }
    '''    
    dead_store = len(df.loc[(df.bug_type == 'DEAD_STORE')])
    py_dead_store = len(df.loc[(df.bug_type == 'DEAD_STORE') & (df.is_pythonCAPI == 1)])
    uninitialized_value = len(df.loc[(df.bug_type == 'UNINITIALIZED_VALUE')])
    py_uninitialized_value = len(df.loc[(df.bug_type == 'UNINITIALIZED_VALUE') & (df.is_pythonCAPI == 1)])
    null_dereference = len(df.loc[(df.bug_type =='NULL_DEREFERENCE')])
    py_null_dereference = len(df.loc[(df.bug_type =='NULL_DEREFERENCE') & (df.is_pythonCAPI == 1)])
    resource_leak = len(df.loc[(df.bug_type == 'RESOURCE_LEAK')])
    py_resource_leak = len(df.loc[(df.bug_type == 'RESOURCE_LEAK') & (df.is_pythonCAPI == 1)])
    bug_sum = len(df)
    py_bug_sum = len(df.loc[df.is_pythonCAPI == 1])
    
    sum = {'Dead_Store': dead_store, 
            'pyc_Dead_Store': py_dead_store,
            'Uninitialized_Value': uninitialized_value,
            'pyc_Uninitialized_Value': py_uninitialized_value,
            'Null_Dereference': null_dereference,
            'pyc_Null_Dereference': py_null_dereference,
            'Resource_Leak': resource_leak,
            'pyc_Resource_Leak': py_resource_leak,
            'BUG_SUM': bug_sum,
            'pyc_BUG_SUM': py_bug_sum
            }
    
    for key in sum:
        print_to_log('      ' + str(key) + ': ' + str(sum[key]), log_path)
    
    return sum




def all_version_data(data_path, output_path):
    '''
    description: Integrate analysis results of all projects
    param {
        data_path:      Path of result of each project
        output_path:    Path to save total result
    }
    '''    
    dirs = os.listdir(data_path)
    if os.path.isdir(output_path):
        pass
    else:
        os.mkdir(output_path)

    alldata = pd.ExcelWriter(os.path.join(output_path, 'alldata.xlsx'))

    version = []
    dead_store = []
    py_dead_store = []
    uninitialized_value = []
    py_uninitialized_value = []
    null_dereference = []
    py_null_dereference = []
    resource_leak = []
    py_resource_leak = []
    bug_sum = []
    py_bug_sum = []

    for folder in dirs:
        jsonpath = os.path.join(data_path, folder, 'infer-out/report.json')
        txtpath = os.path.join(data_path, folder, 'infer-out/report.txt')
        output = output_path + '/' +folder+'/'

        df= single_version_extract(jsonpath, txtpath, output, 'analysis')

        version.append(folder)
        dead_store.append(len(df.loc[(df.bug_type == 'DEAD_STORE')]))
        py_dead_store.append(len(df.loc[(df.bug_type == 'DEAD_STORE') & (df.is_pythonCAPI == 1)]))
        uninitialized_value.append(len(df.loc[(df.bug_type == 'UNINITIALIZED_VALUE')]))
        py_uninitialized_value.append(len(df.loc[(df.bug_type == 'UNINITIALIZED_VALUE') & (df.is_pythonCAPI == 1)]))
        null_dereference.append(len(df.loc[(df.bug_type =='NULL_DEREFERENCE')]))
        py_null_dereference.append(len(df.loc[(df.bug_type =='NULL_DEREFERENCE') & (df.is_pythonCAPI == 1)]))
        resource_leak.append(len(df.loc[(df.bug_type == 'RESOURCE_LEAK')]))
        py_resource_leak.append(len(df.loc[(df.bug_type == 'RESOURCE_LEAK') & (df.is_pythonCAPI == 1)]))
        bug_sum.append(len(df))
        py_bug_sum.append(len(df.loc[df.is_pythonCAPI == 1]))

        df.to_excel(alldata, sheet_name = folder)

    alldata.close()


    interest = {'version': version,
            'DEAD_STORE': dead_store,
            'PY_DEAD_STORE':py_dead_store,
            'UNINITIALIZED_VALUE':uninitialized_value,
            'PY_UNINITIALIZED_VALUE':py_uninitialized_value,
            'NULL_DEREFERENCE':null_dereference,
            'PY_NULL_DEREFERENCE':py_null_dereference,
            'RESOURCE_LEAK':resource_leak,
            'PY_RESOURCE_LEAK':py_resource_leak,
            'bug_sum':bug_sum,
            'py_bug_sum':py_bug_sum
            }
    dfout = pd.DataFrame(interest)

    dfout.to_excel(output_path + '/version_analyze.xlsx', index = False)#excel
    dfout.to_csv(output_path + '/version_analyze.csv', index = False)#csv
   

