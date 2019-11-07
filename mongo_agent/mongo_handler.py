
def name():
    return "mongo_handler"

def on_start_session(session):
    pass

def on_close_session(session):
    pass

def handle(frame, session):
    tokens = token_parse(frame)
    if not tokens:
        return False

    for token in tokens:
        print("  ",token)
    session.send("very ok\n")
    return True

def token_parse(frame):
    if frame[0:6] != "BEGIN:" or frame[-4:] != ":END":
        return None

    tokens = []
    token = []
    in_brack = 0
    in_squota = False
    in_dquota = False
    for c in frame:
        if c == '\'':
            if not in_dquota:
                in_squota = not in_squota
        elif c == '\"':
            if not in_squota:
                in_dquota = not in_dquota
        elif not in_squota and not in_dquota:
            if c == '{':
                in_brack += 1
            elif c == '}' and in_brack > 0:
                in_brack -= 1
            elif c == ':' and in_brack == 0:
                token_str = "".join(token).strip()
                tokens.append(token_str)
                token = []
                continue
        token.append(c)
    #get the last token after :
    token_str = "".join(token).strip()
    tokens.append(token_str)
    return tokens
