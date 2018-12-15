import subprocess

def collectdata(query):
    collect = 'python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1'
    collect = 'python Exporter.py --querysearch "'
    collect = collect + query
    collect = collect + '" --since 2016-09-10 --until 2017-09-12 --maxtweets 1000'
    print(collect)
    subprocess.call(collect, shell=True)
