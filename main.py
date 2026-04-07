
CODE = """
number = 100
"""

VALUE = {}




def strip(string_):
    start = -1
    s = ''
    for i in string_:
        if (i != None and start != -1):
            s += i
        else:
            if (start == -1):
                start = i
            else:
                break      

    if start == -1:
        return ''
    else:
        return s
    
print(strip(CODE))


# for c in CODE:
#     print(c)

