import subprocess
import os

def collectdata(query,num,startd,endd):
    collect = 'python Exporter.py --querysearch "'
    collect = collect + query
    collect = collect + '" --since '+startd+' --until '+endd+' --maxtweets '+num
    print(collect)
    subprocess.call(collect, shell=True)


