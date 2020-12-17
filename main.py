import time
import requests
import json
import datetime
from pandas import DataFrame


def get_config():
    config_file = open("source.cfg")
    dict_temp = {}
    try:
        for line in config_file:
            line = line.replace("\n", '')
            k = line.split("===")[0]
            v = line.split("===")[1]
            dict_temp[k] = v
    finally:
        config_file.close()
    return dict_temp


def a(end, s000, u, l, since_id=""):
    print("loading... please wait")
    j = json.loads(requests.get(u + since_id).text)
    v = j['data']['cards']
    since_id = str(j['data']['cardlistInfo']['since_id'])
    sv1, sv2, sv3, sv4, s = 0, 0, 0, 0, 0
    e = int(time.mktime(time.strptime(end, "%Y-%m-%d")))
    s001 = int(time.mktime(time.strptime(s000, "%Y-%m-%d")))
    for i in v:
        if not 'mblog' in i:
            continue
        k = i['mblog']
        d465 = str(tran(k['created_at']))
        s = int(time.mktime(time.strptime(d465, "%Y-%m-%d")))
        if s < e:
            break
        elif s > s001:
            continue
        v1, v2, v3, v4 = int(k['comments_count']), int(k['attitudes_count']), int(k['pending_approval_count']), int(
            k['reposts_count'])
        l.append((v1, v2, v3, v4, tran(k['created_at']), True))
        sv1, sv2, sv3, sv4 = sv1 + v1, sv2 + v2, sv3 + v3, sv4 + v4
    if s >= e:
        rk, (_a, _b, _c, _d) = a(end, s000, u, l, since_id)
        sv1, sv2, sv3, sv4 = sv1 + _a, sv2 + _b, sv3 + _c, sv4 + _d
    return l, (sv1, sv2, sv3, sv4)


def tran(t):
    if "小时前" in t:
        return datetime.date.today()
    elif "昨天" in t:
        return datetime.date.today() + datetime.timedelta(-1)
    elif "分钟前" in t:
        return datetime.date.today()
    elif "-" in t:
        return "2020-" + t
    else:
        return t


def get_data_and_write(start, end, sour):
    rk, p = a(start, end, get_config()[sour], [], '')

    datas = []
    for i in range(len(rk)):
        (m, b, c, d, t, u) = rk[i]
        datas.append(
            {'title': u, 'comments_count': m, 'attitudes_count': b, 'pending_approval_count': c, 'reposts_count': d,
             'time': t, 'cal': m + b + c + d})

    file_path = './' + sour + '.xlsx'
    DataFrame(datas).to_excel(file_path, sheet_name=sour, index=False,
                              columns=['title', 'comments_count', 'attitudes_count', 'pending_approval_count',
                                       'reposts_count', 'time',
                                       'cal'])


if __name__ == '__main__':
    start = "2020-12-10"
    end = "2020-12-16"
    get_data_and_write(start, end, "gaode")
    get_data_and_write(start, end, "baidu")
