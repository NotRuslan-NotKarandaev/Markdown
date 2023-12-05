"""https://en.wikipedia.org/wiki/Markdown"""
from modules import string,array


class Tag:
    """Opening and closing tag and codeword
    that corresponds them."""
    def __init__(self,start:str,end:str,
                 codeword:str):
        self.start = start
        self.end = end
        self.codeword = codeword


def bold(s:str)->str:
    """Returns string with tags <strong>, </strong>
    instead of string with ** and **."""
    s = replace_with_tags(s,[BOLD])
    return s


def itallic(s:str)->str:
    """Returns string with tags <em>, </em>
    instead of string with * and *."""
    s = replace_with_tags(s,[ITALLIC])
    return s


def replace_with_tags(s:str,tags:list[Tag]):
    """Replaces codewords from string with specified
    types of tags."""
    current_tags = []
    for tag in tags:
        overlapped_indexes = \
            [i for i, _ in enumerate(s) if s.startswith(tag.codeword, i)]

        indexes = []
        for index in overlapped_indexes:
            if len(current_tags) == 0:
                indexes.extend(overlapped_indexes)
                break
            failed = False
            for c_tag in current_tags:
                if (index + len(tag.codeword) \
                    <= c_tag[1]) or ((c_tag[1] + \
                    len(c_tag[0].codeword) <= index) \
                    and (index + len(tag.codeword) <= \
                    c_tag[2])) or (c_tag[2] + len(c_tag[0].codeword) \
                    <= index):
                    continue
                else:
                    failed = True
                    break
            if not failed:
                indexes.append(index)

        deltas = []
        for i in range(1,len(indexes)):
            delta = indexes[i] - indexes[i - 1] - \
                len(tag.codeword)
            if delta >= 0:
                deltas.append( \
                    [delta,indexes[i - 1], \
                    indexes[i]])
        deltas.sort(reverse=True,key=lambda x: x[1])
        deltas.sort(reverse=True)
        _i = len(deltas) - 1
        while _i > 0:

            if (deltas[_i][2] + len(tag.codeword)) > deltas[_i - 1][1]:
                del deltas[_i - 1]

            _i -= 1

        deltas = deltas[::-1]
        for delta in deltas:
            delta[0] = tag
            current_tags.append(delta)
        
    result = ""
    prev_start = 0
    tags = []
    for tag in current_tags:
        tags.append([tag[1],tag[0].start,tag[0].codeword])
        tags.append([tag[2],tag[0].end,tag[0].codeword])
    tags.sort()

    for tag in tags:
        result += s[prev_start:tag[0]] + tag[1]
        prev_start = tag[0] + len(tag[2])
    if len(tags) > 0:
        prev_start = tags[-1][0] + len(tags[-1][2])
    result += s[prev_start:]
    return result


BOLD = Tag("<strong>",'</strong>','**')
ITALLIC = Tag("<em>",'</em>','*')
