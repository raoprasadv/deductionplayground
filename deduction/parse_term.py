
class ParseError(Exception):
    def __init__(self, s, consumed, message):
        self.string = s
        self.consumed = consumed
        self.message = message

    def __repr__(self):
        return "ParseError(%s, %s, %s)" % (self. string, self.consumed, self.message)


def consume_term(s):
    ret_list = []
    pointers = [ret_list]
    consumed = ''
    current_token = None
    for idx, ch in enumerate(s):
        consumed += ch
        if ch == ' ' or ch == '\t':
            pass
        elif ch == '(':
            if current_token is not None:
                pointers[-1].append(current_token)
                current_token = None
            temp = list()
            pointers[-1].append(temp)
            pointers.append(temp)
        elif ch == ')':
            if current_token is not None:
                pointers[-1].append(current_token)
                current_token = None
            pointers.pop()
            if len(pointers) == 1:
                return ret_list, idx
        elif ch == ',':
            if current_token is not None:
                pointers[-1]. append(current_token)
                current_token = None
            else:
                raise ParseError(s, consume_term, "Comma follows non-atom")
        elif ch == '.':
            if current_token is not None:
                pointers[-1].append(current_token)
            return ret_list, idx
        elif current_token is not None:
            if s[idx -1] in [' ', '\t']:
                raise ParseError(s, consumed, 'space separated atoms')
            current_token += ch
        else:
            current_token = '' + ch
    if len(pointers) == 1 and len(pointers[0]) == 0:
        if current_token is not None:
            pointers[-1].append(current_token)
        return ret_list, len(s)
    else:
        raise ParseError(s, consumed, "Unflushed Stack %s" % (pointers, ))


    def parse_rule(s):
        splits = s.split(':-')
        if len(splits) == 1:
            return {
                'head': consume_term(splits[0]),
                'body': []
            }