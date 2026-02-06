input_file = "./url_constants.h"
output_file = "./url_constants_numbered.h"

TARGET = '"https://github.com/left-TTC/kilo-browser"'

counter = 0

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in fin:
        if TARGET in line:
            counter += 1
            line = line.replace(
                TARGET,
                f'"https://github.com/left-TTC/kilo-browser{counter}"',
                1
            )
        fout.write(line)
