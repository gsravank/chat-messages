def identify_special_texts(text):
    if text[:2] == '[[':
        return True
    else:
        return False


def identify_links(text):
    if text[:4] == 'http':
        return True
    else:
        return False


def identify_forwards(text):
    if text[:5] == '{{FWD':
        return True
    else:
        return False


def separate_emojis_at_the_end_of_tokens(text):
    return


def seperate_special_characters_at_the_end_of_tokens(text):
    return


def convert_smileys_to_emojis(text):
    return


def handle_special_characters_at_the_start_of_tokens(text):
    return


def separate_tokens_with_dots(text):
    return