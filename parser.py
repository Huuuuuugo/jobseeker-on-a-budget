import os
import re


# create temp file with the cirles moved to the beggining of the paragraph
with open('index.html') as file:
    temp_file = []
    last_text_index = 0
    first_match = True # indicates the first match on a chain of matches
    prev_attr_str = ""
    prev_y = 0
    for line in file:
        # search for text elements
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
            
            # filter out the attributes that must be ignored
            if fill == "black":
                attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '').replace(attr_str_font_weight, '')

            else:
               attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '')

            # if this is the first on a sequence of text elements 
            # or the attribute string changed significantly
            # or the line being written changed
            if first_match or attr_str != prev_attr_str or y > prev_y:
                # update the index of the last text line
                prev_y = y
                first_match = False
                last_text_index = len(temp_file)

            prev_attr_str = attr_str

        else:
            first_match = True

        # search for circle elements with black color
        if re.match(r"^.*<circle.*?</circle>$", line) and re.findall(r" fill=\"(.+?)\"", line)[0] == "black":
            # move the element to right above the last text line
            temp_file.insert(last_text_index, line)
            continue

        temp_file.append(line)

with open('.temp.html', 'w') as file:
    for line in temp_file:
        file.write(line)

with open('.temp.html') as file:
    final_file = []
    first_match = True # indicates the first match on a chain of matches
    prev_attr_str = ""

    for line in file:
        line = line.rstrip('\n')

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

            # filter out the attributes that must be ignored
            # filtering font-weight out only when the text color is black will prevent some unintended things from being applied on topic sections
            if fill == "black":
                attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '').replace(attr_str_font_weight, '')

            else:
               attr_str = attr_str.replace(attr_str_x, '').replace(attr_str_y, '')

            # if this is the first on a sequence of text elements or the attribute string changed significantly
            if first_match or attr_str != prev_attr_str:
                # close the last text element
                if attr_str != prev_attr_str:
                    final_file[-1] += "</text>"

                # append a new text element preserving it's attributes
                prev_y = float(re.findall(r" y=\"(.+?)\"", line)[0])
                line = line.replace("</text>", '')
                final_file.append(line)
                first_match = False
            
            # if it's the second or later text element on a sequence of text elements
            else:
                # get the y cordinate of the element and its text
                y = float(re.findall(r" y=\"(.+?)\"", line)[0])
                text = re.findall(r"^.*<text.*>(.+)</text>$", line)[0]

                # apply bold font as tspan if the original text element had it
                if font_wight == "bold":
                    line = f'<tspan font-weight="bold">{text}</tspan>'

                    # increment the y distance if the original text element is on a diferrent line from the previous
                    if prev_y < y:
                        line = f'<tspan font-weight="bold" x={x} dy="1.2em">{text}</tspan>'

                # apply normal font if the original text element didn't specify it to be bold
                else:
                    line = f'<tspan font-weight="normal">{text}</tspan>'

                    # increment the y distance if the original text element is on a diferrent line from the previous
                    if prev_y < y:
                        line = f'<tspan font-weight="normal" x={x} dy="1.2em">{text}</tspan>'

                # add the new line to the current text element and update the previous y value
                final_file[-1] += line
                prev_y = y
            
            # update previous attribute string value
            prev_attr_str = attr_str
        
        # if the element is not a text element
        else:
            # close the last text element if the chain of text elements has just ended
            if not first_match:
                final_file[-1] += "</text>"
                first_match = True

            # simply append the element without modifications
            final_file.append(line)

# save output
with open('output.html', 'w') as file:
    for line in final_file:
        file.write(line + '\n')

os.remove(".temp.html")