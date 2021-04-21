def convert_price(price_str: str, website) -> float:
    """
    Converts price string from website string to float
    :param website:
    :param price_str:
    :return:
    """
    price_str = price_str.strip()

    if website == "olx":
        if price_str == "Za darmo":
            return 0
        elif price_str == "Zamienię":
            return -1

    elif website == "witrigs":
        return float(price_str[3:])

    # remove " zł" suffix and do the rest
    return float(price_str[:-3].replace(",", ".").replace(" ", ""))
