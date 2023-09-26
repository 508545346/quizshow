def check_email_url(email):
    postfix = email[-4:]
    if postfix != '.com':
        return True

    at_cont = 0
    for element in email:
        if element == '@':
            at_cont += 1
        elif element == ' ':
            return True

    if at_cont != 1:
        return True

    for element in email:
        if element.isalpha() is False and element.isdigit() is False:
            if element != '.' and element != '@' and element != '_':
                return True
    return False
