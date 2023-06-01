import json
import jinja2
import sys,time,os,re
import numpy as np

log_lines = []

process_memory_samples = {}
process_cpu_samples = {}
memory_all_data={}
cpu_all_data={}

def sample_log_data(arr):
    result_arr = []
    index = 0
    skip = int(len(arr)/200)
    if skip < 1:
        skip = 1
    while index < len(arr):
        result_arr.append([index,arr[index]])
        index+=skip
    return result_arr

def process_log_data():
    global process_memory_samples
    global process_cpu_samples
    global memory_all_data
    global cpu_all_data

    isFirstHeader = True
    for line in log_lines:
        prefix_re=r'.*hogsParse.h\s[0-9]*\s[0-9]*'
        line = re.sub(prefix_re,'',line)
        reObj = re.match('\s*PID\s*NAME\s*MSEC\s*PIDS\s*SYS\s*MEMORY', line)
        if reObj:
            #print(line)
            if not isFirstHeader:
                memory_data_map=process_memory_data()
                for process_name in memory_data_map:
                    if process_name not in memory_all_data:
                        memory_all_data[process_name] = []
                    memory_all_data[process_name].append(memory_data_map[process_name])

                cpu_data_map=process_cpu_data()
                for process_name in cpu_data_map:
                    if process_name not in cpu_all_data:
                        cpu_all_data[process_name] = []
                    cpu_all_data[process_name].append(cpu_data_map[process_name])
            isFirstHeader = False

        reObj = re.match('\s+[0-9]+\s+.*%', line)
        if reObj:
            reg=re.compile(r'\s+')
            line=reg.sub('|', line)
            str_array=line.split('|')[1:]
            print(str_array)
            process_name=str_array[1].strip()
            process_name=process_name.split('/')[-1].strip()
            if 'idle' in process_name:
                continue
            if process_name.isdigit():
                continue
            try:
                pid_str=str_array[0].strip()
                process_id_str= process_name + '-' + pid_str
                try:
                    process_memory_str=str_array[5].strip().replace('k', '')
                    process_memory=round(int(process_memory_str)/1024, 3)
                    process_memory_samples[process_id_str]=process_memory
                except:
                    #print('warning: process_memory_str')
                    pass

                try:
                    process_cpu_str=str_array[4].strip().replace('%', '')
                    process_cpu=round(float(process_cpu_str), 3)
                    process_cpu_samples[process_id_str]=process_cpu
                except:
                    print('warning: process_cpu_str')
                    pass
            except:
                print('skip error line')
                pass

def process_memory_data():
    global process_memory_samples

    MAX_MEMORY_SIZE=30784
    process_memory_map = {}

    for ch_key in process_memory_samples:
        process_name = ch_key[0:ch_key.rfind('-')]
        process_memory_value = process_memory_samples[ch_key]

        if process_name not in process_memory_map:
            process_memory_map[process_name] = process_memory_value
        else:
            process_memory_map[process_name] = process_memory_map[process_name] + process_memory_value
    
    for process_name in process_memory_map:
        process_memory_value = process_memory_map[process_name]
        process_memory_map[process_name] = round(process_memory_value, 3)

    process_memory_samples={}
    return process_memory_map

def process_cpu_data():
    global process_cpu_samples
    MAX_CPU=100
    process_cpu_map = {}

    for ch_key in process_cpu_samples:
        process_name = ch_key[0:ch_key.rfind('-')]
        process_cpu_value = process_cpu_samples[ch_key]
        if process_name not in process_cpu_map:
            process_cpu_map[process_name] = process_cpu_value
        else:
            process_cpu_map[process_name] = process_cpu_map[process_name] + process_cpu_value
    
    for process_name in process_cpu_map:
        process_cpu_map[process_name] = round(process_cpu_map[process_name]/12,3)
    
    process_cpu_samples={}
    return process_cpu_map


def process_all_charts_data():
    global memory_all_data
    global cpu_all_data

    process_memory_pie_data_array = []
    MAX_MEMORY_SIZE=30784
    system_memory_sum = 0
    for process_name in memory_all_data:
        process_memory_sum = 0
        for sample_data in memory_all_data[process_name]:
            process_memory_sum = process_memory_sum + sample_data
        process_memory_value = process_memory_sum / len(memory_all_data[process_name])
        process_memory_pie_data = {'name': process_name,'value': round(process_memory_value, 3)}
        process_memory_pie_data_array.append(process_memory_pie_data)
        system_memory_sum = system_memory_sum + process_memory_value
    process_memory_pie_data = {'name': 'Others', 'value':  round(MAX_MEMORY_SIZE - system_memory_sum, 3)}
    process_memory_pie_data_array.append(process_memory_pie_data)
    process_memory_pie_series = {'name': 'Process Memory (MB)', 'type':'pie', 'radius': '50%', 'data': sorted(process_memory_pie_data_array, key=lambda k:(k['value']), reverse=True)}
    process_memory_pie_charts_data = {'title': 'Memory Pies','series':process_memory_pie_series}


    process_cpu_pie_data_array = []
    MAX_CPU=100
    system_cpu_sum = 0
    for process_name in cpu_all_data:
        process_cpu_sum = 0
        for sample_data in cpu_all_data[process_name]:
            process_cpu_sum = process_cpu_sum + sample_data
        process_cpu_value = process_cpu_sum / len(cpu_all_data[process_name])
        process_cpu_pie_data = {'name': process_name,'value': round(process_cpu_value, 3)}
        process_cpu_pie_data_array.append(process_cpu_pie_data)
        system_cpu_sum = system_cpu_sum + process_cpu_value
    process_cpu_pie_data = {'name': 'Idle', 'value':  round(MAX_CPU - system_cpu_sum,3)}
    process_cpu_pie_data_array.append(process_cpu_pie_data)
    process_cpu_pie_series = {'name': 'Process CPU (%)', 'type':'pie', 'radius': '50%', 'data': sorted(process_cpu_pie_data_array, key=lambda k:(k['value']), reverse=True)}
    process_cpu_pie_charts_data = {'title': 'CPU Pies','series':process_cpu_pie_series}

    process_memory_series_array = []
    process_memory_legend_array = []
    for process_name in memory_all_data:
        process_memory_series = {'symbolSize': 5, 'type':'line', 'name': process_name, 'data': sample_log_data(memory_all_data[process_name])}
        process_memory_series_array.append(process_memory_series)
        process_memory_legend_array.append(process_name)
    process_memory_charts_data = {'title': 'Memory Lines','series':process_memory_series_array, 'legend': process_memory_legend_array}

    process_cpu_series_array = []
    process_cpu_legend_array = []
    for process_name in cpu_all_data:
        process_cpu_series = {'symbolSize': 5, 'type':'line', 'name': process_name, 'data': sample_log_data(cpu_all_data[process_name])}
        process_cpu_series_array.append(process_cpu_series)
        process_cpu_legend_array.append(process_name)
    process_cpu_charts_data = {'title': '%','series':process_cpu_series_array, 'legend': process_cpu_legend_array}

    charts_data_map = {
        'process_memory_pie_charts_data': process_memory_pie_charts_data,
        'process_cpu_pie_charts_data': process_cpu_pie_charts_data,
        'process_memory_charts_data': process_memory_charts_data,
        'process_cpu_charts_data': process_cpu_charts_data
    }
    return charts_data_map


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: input log file(*.log) not specified')
        sys.exit()
    

    path = os.getcwd().replace("\\", "/")
    temp_path = '/templates/template.html'
    full_path = path+temp_path

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
    temp = env.get_template(temp_path)

    log_lines = []
    with open(sys.argv[1], 'r', encoding='utf8',errors='ignore') as log_file:
        log_content = log_file.read()
        log_lines = log_content.split('\n')
        
    print("lines: ", len(log_lines))
    process_log_data()

    charts_data = process_all_charts_data()

    temp_out = temp.render(charts_data_map=charts_data)
    full_path2 = path+'/reports'
    if not os.path.exists(full_path2):
        os.mkdir(full_path2)
    full_path2=full_path2+'/hogs_report.html'
    with open(full_path2, 'w', encoding='utf-8') as f:
        f.writelines(temp_out)
        f.close()