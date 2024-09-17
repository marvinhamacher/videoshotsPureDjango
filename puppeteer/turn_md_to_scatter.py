import markdown
import matplotlib.pyplot as plt
import numpy as np


def cleanString(string):
    string = string.replace("|", ";")
    string = string.replace("<p>", ";")
    string = string.replace("</p>", ";")
    string = "\n".join(string.splitlines()[3:])
    string = "\n".join(string.splitlines()[:75])
    return string

def createDiagramm(results):
    for  row in results.splitlines():
        slices = row.split(';')
        if len(slices) < 4:
            continue  # Skip if the row is malformed
        x = int(slices[1])
        y = int(slices[2])
        print(slices[3])
        if slices[3] == "Users: 5":
            color = 'red'
        elif slices[3] == "Users: 10":
            color = 'green'
        elif slices[3] == "Users: 20":
            color = 'purple'
        else:
            color = 'blue'

        plt.scatter(x, y, s=15, c=color, alpha=0.5)
    plt.show()

f = open('testergebnis.md', 'r')
htmlmarkdown=markdown.markdown( f.read() )
htmlmarkdown=cleanString(htmlmarkdown)
print(htmlmarkdown)
createDiagramm(htmlmarkdown)