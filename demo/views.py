import subprocess
import platform
import wmi
import psutil
import pythoncom
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # traverse the info
    Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
    Data = subprocess.check_output(['wmic', 'product', 'get', 'name'])
    new = []
    a = str(Data)
    # print("SYSTEM INFORMATION")

    system_info = []
    # arrange the string into clear info
    for item in Id:
        new.append(str(item.split("\r")[:-1]))
    for i in new:
        # print(i[2:-2])
        system_info.append(i[2:-2])

    list_of_softwares = []
    # print("LIST OF SOFTWARES INSTALLED")
    try:

        # arrange the string
        for i in range(len(a)):
            list_of_softwares.append(a.split("\\r\\r\\n")[6:][i])

    except IndexError as e:
        print("All Done")
    pythoncom.CoInitialize()
    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]

    # print(f"Manufacturer: {my_system.Manufacturer}")
    # print(f"Model: {my_system. Model}")
    # print(f"Name: {my_system.Name}")
    # print(f"NumberOfProcessors: {my_system.NumberOfProcessors}")
    # print(f"SystemType: {my_system.SystemType}")
    # print(f"SystemFamily: {my_system.SystemFamily}")

    # my_system = platform.uname()

    # print(f"System: {my_system.system}")
    # print(f"Node Name: {my_system.node}")
    # print(f"Release: {my_system.release}")
    # print(f"Version: {my_system.version}")
    # print(f"Machine: {my_system.machine}")
    # print(f"Processor: {my_system.processor}")

    # print(f"Memory :{psutil.virtual_memory()}")

    context = {
        'manufacturer': my_system.Manufacturer,
        'model': my_system. Model,
        'name': my_system.Name,
        'num_of_processes': my_system.NumberOfProcessors,
        'system_type': my_system.SystemType,
        'system_family': my_system.SystemFamily,
    }

    my_system = platform.uname()
    context.update({
        'system': my_system.system,
        'node_name': my_system.node,
        'release': my_system.release,
        'version': my_system.version,
        'machine': my_system.machine,
        'processor': my_system.machine,
        'memory': psutil.virtual_memory(),
        'system_info': system_info,
        'list_of_softwares': list_of_softwares
    })

    return render(request, 'demo/home.html', context)
