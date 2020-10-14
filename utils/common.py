def show_top_6_news_style(index):
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    return ""


def show_news_status_name(index):
    if index == 0:
        return "已通过"
    elif index == 1:
        return "审核中"
    elif index == -1:
        return "未通过"
    return ""


def show_news_status_style_name(index):
    if index == 0:
        return "pass"
    elif index == 1:
        return "review"
    elif index == -1:
        return "nopass"
    return ""


def show_top_7_news_style(index):
    if index == 2:
        return "股市"
    elif index == 3:
        return "债市"
    elif index == 4:
        return "商品"
    elif index == 3:
        return "外汇"
    elif index == 4:
        return "公司"
    return ""
