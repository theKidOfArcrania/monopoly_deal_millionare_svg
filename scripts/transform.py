import sys
import yaml
import re

def main():
    if len(sys.argv) != 5:
        print(f"USAGE: {sys.argv[0]} NAMES TEMP.svg FMT OUT.svg")
        exit(1)

    with open(sys.argv[1], "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    fmt, _, num = sys.argv[3].partition('_')
    num = int(num) - 1
    data = data[fmt]
    repls = dict(data.get('replace', {}))
    vars = dict(data.get('vars', {}))
    n1, n2 = data['names'][num].split(' ')
    vars['NAME'] = n1
    vars['NAME2'] = n2

    with open(sys.argv[2], 'r') as templ:
        with open(sys.argv[4], 'w') as out:
            for line in templ:
                line_new = ''
                i = 0
                while i < len(line) - 1:
                    if line[i:i+2] == '${':
                        end = line.index('}', i)
                        line_new += str(vars[line[i + 2:end]])
                        i = end
                    else:
                        line_new += line[i]
                    i += 1
                line_new += line[i]
                for (old, new) in repls.items():
                    line_new = line_new.replace(str(old), new)
                out.write(line_new)

if __name__ == "__main__":
    main()
