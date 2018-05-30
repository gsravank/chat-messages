import emoji


def identify_special_texts(text):
    if text[:2] == '[[':
        type_of_text = text[2:]
        type_of_text = type_of_text.split(']]')[0]
        type_of_text = type_of_text.split(' ')[0]
        type_of_text = type_of_text.strip(',')

        return '[[' + type_of_text + ']]'
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


def char_is_emoji(char):
    return char in emoji.UNICODE_EMOJI


def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False


def separate_emojis_at_the_end_of_tokens(text):
    final_text = ''

    if text_has_emoji(text):
        for char in text:
            if char_is_emoji(char):
                if len(final_text):
                    if final_text[-1] != ' ':
                        final_text += ' '
                final_text += char
                final_text += ' '
            else:
                final_text += char
    else:
        final_text = text

    return final_text


def separate_special_characters_at_the_end_of_tokens(text):
    special_characters = [',', '.']

    for special_character in special_characters:
        text = text.replace(special_character, '')

    text = ' '.join(text.split())

    return text


def convert_smileys_to_emojis(text):
    smileys = [':)', ':p', ':(']
    emojis = ['😀', '😟','😋']

    for smiley, emoji in zip(smileys, emojis):
        text = text.replace(smiley, emoji)

    return text
