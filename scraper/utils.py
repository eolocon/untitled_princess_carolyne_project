import re

""" Module containing general utility functions """

def parse_list(l):
    """ Parse a comma separated list (a string) into a list of string
        
        Args:
            l (str): comma separated list

        Returns:
            l (list[str]): list of string, as parsed from input

    """

    pattern = '[\W]+'
    l = re.split(pattern, l)
    for index in [0,-1]:
        if '' == l[index]:
            l.pop(index)
    
    return l
