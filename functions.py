from datetime import date


def date2gpstime(sp_date):
    """
    :param sp_date: yyyy, mm, dd, hh, mm, ss
    :return:
    """
    dd = date.toordinal(date(sp_date[0], sp_date[1], sp_date[2])) - date.toordinal(date(2019, 4, 7))
    week = dd // 7
    dow = dd % 7
    tow = dow * 86400 + sp_date[3] * 3600 + sp_date[4] * 60 + sp_date[5]
    return week, tow
