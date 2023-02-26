import shutil
import sys
import yaml
import re
import os

def main():
    if len(sys.argv) != 4:
        print(f"USAGE: {sys.argv[0]} COUNT EXPORT_DIR CARDSET_DIR")
        exit(1)

    with open(sys.argv[1], "r") as stream:
        try:
            counts = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    def lookup_count(file):
        base, _, ext = file.partition(".")
        if ext.upper() != 'PNG':
            print(f"Skipping {file}")
            return

        path = counts
        for component in base.split('_'):
            if type(path) is int:
                break
            if component not in path:
                print(f"Skipping {file}")
                return
            path = path[component]
        return (base, int(path))

    files = os.listdir(sys.argv[2])
    files.sort()
    img_cnt = 0
    for file in files:
        res = lookup_count(file)
        if not res: continue
        (base, count) = res
        for _ in range(count):
            shutil.copy(f'{sys.argv[2]}/{file}', f'{sys.argv[3]}/{img_cnt}.png')
            img_cnt += 1

if __name__ == "__main__":
    main()
