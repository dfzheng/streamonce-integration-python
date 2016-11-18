import quopri

def decodeQP(originHTML):
    return str(quopri.decodestring(originHTML), 'utf-8')