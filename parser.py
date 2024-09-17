import re


# create temp file with the cirles moved to the beggining of the paragraph
with open('index.html') as file:
    temp_file = []
    last_text_index = 0
    first_match = True # indicates the first match on a chain of matches
    prev_attr_str = ""
    prev_y = 0
    for line in file:
        if re.match(r"^.*<text.*?</text>$", line):
            # get variables
            fill: str = re.findall(r" fill=\"(.+?)\"", line)[0]
            text: str = re.findall(r"^.*<text.*>(.+)</text>$", line)[0]
            y = re.findall(r" y=\"(.+?)\"", line)[0]

            # get attribute string
            attr_str: str = re.findall(r"^.*<text(.*)>.+</text>$", line)[0]
            attr_str_x: str = re.findall(r"^.*<text.*( x=\".*?\").*>.+</text>$", line)[0]
            attr_str_y: str = re.findall(r"^.*<text.*( y=\".*?\").*>.+</text>$", line)[0]
            attr_str_font_weight: str = re.findall(r"^.*<text.*( font-weight=\".*?\").*>.+</text>$", line)[0]

            if fill == "black":
                attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '').replace(attr_str_font_weight, '')

            else:
               attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '')

            if first_match or attr_str != prev_attr_str or y > prev_y:
                prev_y = y
                first_match = False
                last_text_index = len(temp_file)

            prev_attr_str = attr_str

        else:
            first_match = True

        if re.match(r"^.*<circle.*?</circle>$", line) and re.findall(r" fill=\"(.+?)\"", line)[0] == "black":
            temp_file.insert(last_text_index, line)
            continue

        temp_file.append(line)

with open('temp.html', 'w') as file:
    for line in temp_file:
        file.write(line)

with open('temp.html') as file:
    final_file = []
    first_match = True # indicates the first match on a chain of matches
    prev_attr_str = ""

    for line in file:
        line = line.rstrip('\n')
        # print(line)
        # input()

        # search for text elements
        if re.match(r"^.*<text.*?</text>$", line):
            # get relevant attributes
            fill = re.findall(r" fill=\"(.+?)\"", line)[0]
            font_wight = re.findall(r" font-weight=\"(.+?)\"", line)[0]
            x = float(re.findall(r" x=\"(.+?)\"", line)[0])

            # get attribute string
            attr_str: str = re.findall(r"^.*<text(.*)>.+</text>$", line)[0]
            attr_str_x: str = re.findall(r"^.*<text.*( x=\".*?\").*>.+</text>$", line)[0]
            attr_str_y: str = re.findall(r"^.*<text.*( y=\".*?\").*>.+</text>$", line)[0]
            attr_str_font_weight: str = re.findall(r"^.*<text.*( font-weight=\".*?\").*>.+</text>$", line)[0]

            if fill == "black":
                attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '').replace(attr_str_font_weight, '')

            else:
               attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '')

            # preserve the text element if it's first
            # remove the </text>
            if first_match or attr_str != prev_attr_str:
                if attr_str != prev_attr_str:
                    final_file[-1] += "</text>"

                prev_y = float(re.findall(r" y=\"(.+?)\"", line)[0])
                line = line.rstrip("</text>")
                final_file.append(line)
                first_match = False
            
            # remove the text elemnt and append to previous line
            else:
                y = float(re.findall(r" y=\"(.+?)\"", line)[0])

                line = re.findall(r"^.*<text.*>(.+)</text>$", line)[0]

                if font_wight == "bold":
                    line = f'<tspan font-weight="bold">{line}</tspan>'
                    if prev_y < y:
                        line = f'<tspan font-weight="bold" x={x} dy="1.2em">{line}</tspan>'

                else:
                    line = f'<tspan font-weight="normal">{line}</tspan>'
                    if prev_y < y:
                        line = f'<tspan font-weight="normal" x={x} dy="1.2em">{line}</tspan>'

                final_file[-1] += line
                prev_y = y
            
            prev_attr_str = attr_str
        
        else:
            if not first_match:
                final_file[-1] += "</text>"
                first_match = True

                # print(final_file[-1])
                # input()
        
            final_file.append(line)

with open('output.html', 'w') as file:
    for line in final_file:
        file.write(line + '\n')