import pandas as pd
from git import Repo
import re, signal, sys, time, pwn, pdb, os
import json

def handler_signal(signal, frame):
    print('\n\n[!] Out ..........\n')
    sys.exit(1)

def extract(url):
    repo = Repo(url)
    commits = list(repo.iter_commits('develop'))
    return commits

def transform(commits, KEY_WORDS):
    coincidencias = {}
    for commit in commits:
        for word in KEY_WORDS:
            if re.search(word, commit.message, re.IGNORECASE):
                coincidencias[str(commit.hexsha)] = str(commit.message)
                #coincidencias.append(str(f'Commit: {commit.hexsha} -> {commit.message}'))
    return coincidencias

def load(coincidencias):
    with open("leaks.json",'w') as file:
        json.dump(coincidencias, file, indent=2)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler_signal)

    DIR_REPO = "./skale/skale-manager"
    KEY_WORDS = ['credentials','password','key'] #,'password','username','key'

    commits  = extract(DIR_REPO)

    coincidencias = transform(commits, KEY_WORDS)

    load(coincidencias)
