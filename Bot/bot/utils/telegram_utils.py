chars_to_escape = [
    '_',
    '[',
    ']',
    '(',
    ')',
    '~',
    '`',
    '>',
    '#',
    '+',
    '-',
    '=',
    '|',
    '{',
    '}',
    '.',
]

def escape_text(text: str) -> str:
    for c in chars_to_escape:
        text = text.replace(c, "\\" + c)
    return text