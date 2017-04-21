from re import sub


def clear_multiple_spaces(s):
    return sub("\s+",' ',s)

def delete_break_line_DB(s):
    return sub("\r", '', sub("\n", ' ', s))

def delete_break_line_soap(s):
    return sub("\r", '', sub("\n", ' ', s))