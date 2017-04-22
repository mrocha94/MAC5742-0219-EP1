import numpy as np
import matplotlib.pyplot as plt

import re

# make({thread: 1, size: [10, 100], method: ["omp", "pth"], region: "full", x: "size", line: "method"})
def make_plot(arg):
  x_type = arg["x"]
  x_value = arg[x_type]
  line_type = arg["line"]
  line_value = arg[line_type]
  fixed_line_type = "region" if(line_type == "method") else "method"
  fixed_line_value = arg[fixed_line_type]
  fixed_x_type = "size" if(x_type == "thread") else "thread"
  fixed_x_value = arg[fixed_x_type]
  colors = ['g', 'b', 'r', 'm']

  lines = {}

  for line in line_value:
    lines[line] = []

  for item in data:
    if(item[fixed_x_type] == fixed_x_value and item[fixed_line_type] == fixed_line_value and item[line_type] in line_value and item[x_type] in x_value):
      lines[item[line_type]].append((item[x_type], item["time"], item["deviation"]))

  subtitle = []
  fig = plt.figure()
  ax = plt.subplot(111)
  for line in lines.items():
    if (line[1]):
      c = colors.pop()
      line[1].sort(key = lambda x: x[0])
      axis = map(list, zip(*line[1]))
      subtitle.append(line[0])
      plt.plot(axis[0], axis[1], color=c)
      errors = [a*b/100 for a,b in zip(axis[1],axis[2])]
      plt.errorbar(axis[0], axis[1], errors, linestyle='None', marker='.', color=c)

  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
  ax.legend(subtitle, loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=4)
  plt.ylabel("time (s)")
  plt.ylim(ymin=0)
  plt.xlabel(x_type)
  plt.xlim(xmin=0)

  plt.show()

methods = ["omp", "pth", "seq", "seq_io"]
regions = ["elephant", "full", "seahorse", "triple_spiral"]
sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
threads = [1, 2, 4, 8, 16, 32]

data = []
pattern = "Performance counter stats for '.* ([\d]+) ([\d]+)' \(10 runs\):\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\s+branch-misses\s+([\d\.]+) seconds time elapsed \s+\( \+\-\s+([\d\.]+)\% \)"
regex = re.compile(pattern)

for method in methods:
  for region in regions:
    filename = "results_final/mandelbrot_{0}/{1}.log".format(method, region)
    textfile = open(filename, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = regex.findall(filetext)
    for match in matches:
      item = {}
      item["method"] = method
      item["region"] = region
      item["size"] = int(match[0])
      item["thread"] = int(match[1])
      item["time"] = float(match[2].replace(',', '.'))
      item["deviation"] = float(match[3].replace(',', '.'))
      data.append(item)

# lines = make_plot({"thread": [1,2,4,8,16,32], "size": 8192, "method": ["pth", "omp"], "region": "full", "x": "thread", "line": "method"})
# lines = make_plot({"thread": 1, "size": sizes, "method": methods, "region": "full", "x": "size", "line": "method"})
#lines = make_plot({"thread": 1, "size": sizes, "method": "seq", "region": regions, "x": "size", "line": "region"})
# lines = make_plot({"thread": threads, "size": 8192, "method": "omp", "region": regions, "x": "thread", "line": "region"})
lines = make_plot({"thread": threads, "size": 32, "method": methods, "region": "full", "x": "thread", "line": "method"})

# for method in ["omp", "pth"]:
#   region = "full"
#   size = 32
#   # line = {th: a}
#   plt.plot(line.keys(), line.items())

# data
# cmd(metodo, regiao, size): {th: (a, b)}
# [th1, th2, th3], [a1, a2, a3, a4]

# plt.plot([1, 4, 3, 2], [1, 16, 9, 4])
# plt.plot([1, 2, 3, 4], [1, 8, 27, 64])
# plt.ylabel('some numbers')
