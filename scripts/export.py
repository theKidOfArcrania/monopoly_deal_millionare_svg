import sys
import yaml
import re
import os

templ = '''
\\documentclass[12pt]{scrartcl}
\\usepackage{graphicx}
\\usepackage[a4paper, margin=.3in]{geometry}

\\graphicspath{ {$EXPORT_PATH} }

\\setlength{\\parindent}{0pt}
\\setlength{\\parskip}{5pt}

\\begin{document}

\\centering

$BODY

\\end{document}
'''

class DocGen:
    def __init__(self):
        self.__lines = []
        self.__cnt = 0

    def add_img(self, base):
        self.__cnt += 1
        self.__lines.append(f'\\includegraphics{{{base}}} $\\:\\:$')
        if self.__cnt % 3 == 0:
            self.__lines.append('')

    def generate(self, export_path):
        return templ.replace('$EXPORT_PATH', export_path) \
            .replace('$BODY', '\n'.join(self.__lines))

def main():
    if len(sys.argv) != 4:
        print(f"USAGE: {sys.argv[0]} COUNT EXPORT_DIR OUT.tex")
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

    doc = DocGen()
    files = os.listdir(sys.argv[2])
    files.sort()
    for file in files:
        res = lookup_count(file)
        if not res: continue
        (base, count) = res
        for _ in range(count):
            doc.add_img(base)

    with open(sys.argv[3], 'w') as out:
        out.write(doc.generate(sys.argv[2]))

if __name__ == "__main__":
    main()
