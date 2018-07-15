import os

def push_redis():
    cmd = 'type redis_crawl.txt | redis-cli -p 6381'
    os.system(cmd)

if __name__ == '__main__':
    push_redis()