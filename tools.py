import re
import logging

def debug(msg, exit_flag = 0) :
    print msg
    if exit_flag :
        exit(0)

def decode_html(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def create_logger(module):
    from settings import settings as gconfig
    if not (module in gconfig) :
        print 'wrong configuration.'
        exit(-1)

    config = gconfig[module]

    logger = logging.getLogger(module)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(config['log'])
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(fh)

    logger.info('Init logger for %s' % module)

    return logger

#---function---
def str_replace(html):
#{
    special_str = {
        '&#45;': '-',
        '&#32;': ' ',
    }

    for sp_str in special_str :
        html = html.replace(sp_str, special_str[sp_str])

    return html
#}

