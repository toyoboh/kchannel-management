def patterns_replace(text, pattern_list, after):
    for pattern in pattern_list:
        text = text.replace(pattern, after)
    return text
