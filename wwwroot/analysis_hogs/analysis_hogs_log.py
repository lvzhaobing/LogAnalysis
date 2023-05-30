import json
import jinja2
import sys,time,os,re
import numpy as np

log_lines = []

process_memory_samples = {}
process_cpu_samples = {}

def sample_log_data(arr):
    result_arr = []
    index = 0
    skip = int(len(arr)/200)
    if skip < 1:
        skip = 1
    while index < len(arr):
        result_arr.append(arr[index])
        index+=skip
    return result_arr


def process_log_data():
    global process_memory_samples
    global process_cpu_samples

    for line in log_lines:
        reObj = re.match('\s+[0-9]+\s+.*%', line)
        if reObj:
            print(line)
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
                    if process_id_str not in process_memory_samples:
                        process_memory_samples[process_id_str] = []
                    process_memory_samples[process_id_str].append([len(process_memory_samples[process_id_str]), process_memory])
                except:
                    print('process_memory_str error')
                    pass

                try:
                    process_cpu_str=str_array[4].strip().replace('%', '')
                    process_cpu=round(float(process_cpu_str), 3)
                    if process_id_str not in process_cpu_samples:
                        process_cpu_samples[process_id_str] = []
                    process_cpu_samples[process_id_str].append([len(process_cpu_samples[process_id_str]), process_cpu])
                except:
                    print('process_cpu_str error')
                    pass

                
            except:
                print('skip error line')
                pass

def process_charts_data():
    global process_memory_samples
    global process_cpu_samples

    process_memory_pie_data_array = []
    MAX_MEMORY_SIZE=30784
    system_memory_sum = 0
    process_memory_map = {}

    for ch_key in process_memory_samples:
        process_name = ch_key[0:ch_key.rfind('-')]
        process_memory_sum = 0
        for sample_data in process_memory_samples[ch_key]:
            process_memory_sum = process_memory_sum + sample_data[1]
        process_memory_value = process_memory_sum / len(process_memory_samples[ch_key])

        if process_name not in process_memory_map:
            process_memory_map[process_name] = process_memory_value
        else:
            process_memory_map[process_name] = process_memory_map[process_name] + process_memory_value
    
    for process_name in process_memory_map:
        process_memory_value = process_memory_map[process_name]
        system_memory_sum = system_memory_sum + process_memory_value
        process_memory_pie_data = {'name': process_name,'value': round(process_memory_value, 3)}
        process_memory_pie_data_array.append(process_memory_pie_data)

    process_memory_pie_data = {'name': 'Others', 'value':  round(MAX_MEMORY_SIZE - system_memory_sum, 3)}
    process_memory_pie_data_array.append(process_memory_pie_data)
    process_memory_pie_series = {'name': 'Process Memory (MB)', 'type':'pie', 'radius': '50%', 'data': sorted(process_memory_pie_data_array, key=lambda k:(k['value']), reverse=True)}
    process_memory_pie_charts_data = {'title': 'Memory Pies','series':process_memory_pie_series}


    process_cpu_pie_data_array = []
    MAX_CPU=100
    system_cpu_sum = 0
    process_cpu_map = {}

    for ch_key in process_cpu_samples:
        process_name = ch_key[0:ch_key.rfind('-')]
        process_cpu_sum = 0
        for sample_data in process_cpu_samples[ch_key]:
            process_cpu_sum = process_cpu_sum + sample_data[1]
        process_cpu_value = process_cpu_sum / len(process_cpu_samples[ch_key])
        if process_name not in process_cpu_map:
            process_cpu_map[process_name] = process_cpu_value
        else:
            process_cpu_map[process_name] = process_cpu_map[process_name] + process_cpu_value
    
    for process_name in process_cpu_map:
        process_cpu_value = round(process_cpu_map[process_name]/12,3)
        system_cpu_sum = system_cpu_sum + process_cpu_value
        process_cpu_pie_data = {'name': process_name,'value': process_cpu_value}
        process_cpu_pie_data_array.append(process_cpu_pie_data)

    process_cpu_pie_data = {'name': 'Idle', 'value':  round(MAX_CPU - system_cpu_sum,3)}
    print(process_cpu_pie_data)
    process_cpu_pie_data_array.append(process_cpu_pie_data)
    process_cpu_pie_series = {'name': 'Process CPU (%)', 'type':'pie', 'radius': '50%', 'data': sorted(process_cpu_pie_data_array, key=lambda k:(k['value']), reverse=True)}
    process_cpu_pie_charts_data = {'title': 'CPU Pies','series':process_cpu_pie_series}
    
    process_memory_series_array = []
    process_memory_legend_array = []
    for ch_key in process_memory_samples:
        process_memory_series = {'symbolSize': 5, 'type':'line', 'name': ch_key, 'data': sample_log_data(process_memory_samples[ch_key])}
        process_memory_series_array.append(process_memory_series)
        process_memory_legend_array.append(ch_key)
    process_memory_charts_data = {'title': 'Memory Lines','series':process_memory_series_array, 'legend': process_memory_legend_array}

    process_cpu_series_array = []
    process_cpu_legend_array = []
    for ch_key in process_cpu_samples:
        process_cpu_series = {'symbolSize': 5, 'type':'line', 'name': ch_key, 'data': sample_log_data(process_cpu_samples[ch_key])}
        process_cpu_series_array.append(process_cpu_series)
        process_cpu_legend_array.append(ch_key)
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

    charts_data = process_charts_data()
    temp_out = temp.render(charts_data_map=charts_data)

    

    full_path2 = path+'/reports'
    if not os.path.exists(full_path2):
        os.mkdir(full_path2)
    full_path2=full_path2+'/hogs_report.html'
    with open(full_path2, 'w', encoding='utf-8') as f:
        f.writelines(temp_out)
        f.close()