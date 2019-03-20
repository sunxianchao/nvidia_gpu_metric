#! /usr/bin/env python
# -*- coding:utf-8 -*-

import time
import os.path
import os
import traceback
import sys
from socket import gethostname
from xml.etree import ElementTree as et

class GpuMetric():
    def __init__(_self):
        ##metric name
        _self.GPU_UTIL_METRIC = 'gpu.util'
        _self.GPU_MEMORY_UTIL_METRIC = 'gpu.memory.util'

        ## xml element name
        _self.GPU_UTIL = 'gpu_util'
        _self.GPU_MEMORY_TOTAL = 'gpu_memory_total'
        _self.GPU_MEMORY_USED = 'gpu_memory_used'

        _self.eleToXPath = {_self.GPU_MEMORY_TOTAL: './gpu/fb_memory_usage/total',
                _self.GPU_MEMORY_USED: './gpu/fb_memory_usage/used',
                _self.GPU_UTIL: './gpu/utilization/gpu_util',
        }


    def getTag(_self):
        env_dist = os.environ
        hostname = gethostname()
        host_res = os.popen('armory --fields dns_ip,nodename,nodegroup  -1  -n'+gethostname())
        armory_info = host_res.read().split(',')
        tagkv = {
            "host_ip": armory_info[0],
            #"hostname": armory_info[1],
            #"appGroup": armory_info[2].replace("\n", ""),
            # "scene_id": env_dist[]
        }
        return tagkv

    def nvidiaSmi(_self):
        gpuInfoDict = {}
        gpuXml = os.popen('nvidia-smi -q -x')
        tree = et.parse(gpuXml)
        root = tree.getroot()
        for key, value in _self.eleToXPath.items():
            eleTxt = root.find(value).text
            gpuInfoDict[key] = eleTxt.replace(" MiB", "").replace(" %", "")
        return gpuInfoDict

    def printMetric(_self, metric, value, ts, tags):
        if tags:
            tags = " "+" ".join("%s=%s" %(name, value) for name, value in tags.iteritems())
        else:
            tags = ""
        print ("%s %s %s %s" %(metric, ts, value, tags))

    def handleValue(_self, gpuDict, tagDict):
        gpuUtil = gpuDict[_self.GPU_UTIL]
        gpuMemoryUsed = gpuDict[_self.GPU_MEMORY_USED]
        gpuMemoryTotal = gpuDict[_self.GPU_MEMORY_TOTAL]
        gpuMemoryUtil = '%.2f' % (float(gpuMemoryUsed) / float(gpuMemoryTotal) * 100)
        ts=int(time.time())
        _self.printMetric(_self.GPU_UTIL_METRIC, gpuUtil, ts, tagDict)
        _self.printMetric(_self.GPU_MEMORY_UTIL_METRIC, gpuMemoryUtil, ts, tagDict)

def main():
    try:
        gpuMetric = GpuMetric()
        tags = gpuMetric.getTag()
        while True:
            gpuInfoDict = gpuMetric.nvidiaSmi()
            gpuMetric.handleValue(gpuInfoDict, tags)
            time.sleep(10)
    except:
        pass
        #traceback.print_exc()

if __name__ == '__main__':
    main()
