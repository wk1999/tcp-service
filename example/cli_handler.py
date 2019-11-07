
import redirector

keywords = [
        'show',
        'exit',
        'monitor',
        ]
__redi = None
__redi_owner = None

prompt="CLI#"

def name():
    return "cli_handler"

def on_start_session(session):
    session.send(prompt)

def on_close_session(session):
    global __redi
    global __redi_owner
    if __redi and __redi_owner == session:
        __redi.restore()
        __redi = None

def handle(frame, session):
    tokens = token_parse(frame)

    if not tokens:
        session.send(prompt)
        return True

    for token in tokens:
        print("  ",token)

    if tokens[0] == 'monitor':
        def monitor_help():
            session.send("% usage: monitor [on|off]\n")
        global __redi
        global __redi_owner
        if len(tokens) != 2:
            monitor_help()
        elif tokens[1] == 'on':
            if __redi:
                session.send("% already monitored by someone else\n")
            else:
                __redi = redirector.redirector(session.send)
                __redi.redirect()
                __redi_owner = session
        elif tokens[1] == 'off':
            if __redi:
                __redi.restore()
                __redi = None
                __redi_owner = None
        else:
            monitor_help()
    elif tokens[0] == 'show':
        def show_help():
            session.send("% usage: show [user]...to be done\n")
        if len(tokens) < 2:
            show_help()
        elif tokens[1] == 'user':
            session.send('user is %s\r\n' % session.get_user())
        else:
            show_help()
    elif tokens[0] == 'exit':
        def exit_help():
            session.send('% usage: exit\n')
        if len(tokens) != 1:
            exit_help()
        else:
            session.exit()
    else:
        session.send(prompt)
        return False

    session.send(prompt)
    return True

def token_parse(frame):
    kw_found = False
    frame_len = len(frame)
    for kw in keywords:
        s = len(kw)
        if 0 == cmp(kw, frame[0:s]) and (s == frame_len or ' ' == frame[s]):
            kw_found = True
            break

    if not kw_found:
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
            elif c == ' ' and in_brack == 0:
                token_str = "".join(token).strip()
                token = []
                if token_str:
                    tokens.append(token_str)
                continue
        token.append(c)
    #get the last token after :
    token_str = "".join(token).strip()
    tokens.append(token_str)
    return tokens
