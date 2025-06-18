def split_text(data, delimiter="---"):
    """Splits the text from the data dictionary using the specified delimiter."""

    textList = data['texts'].split(delimiter)
    try:
        return {
            'title': data['title'],
            'khmer': textList[0].strip(),
            'english': textList[1].strip(),
        }
    except IndexError:
        return {
            'title': data['title'],
            'khmer': textList[0].strip(),
            'english': None,
        }