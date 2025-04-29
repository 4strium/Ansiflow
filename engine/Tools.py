import sys
import select
import time

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def get_key():
    if isData() :
        return ord(sys.stdin.read(1))
