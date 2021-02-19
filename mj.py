import time
import requests
import json
import datetime
from pandas import DataFrame


def get_config():
    c = open("config.json")
    return json.loads(c.read())


def a(end, s000, u, l, lfrom,since_id=""):
    n = since_id
    print("loading... from:" + lfrom + " since_id:" + since_id)
    j = json.loads(requests.get(u + since_id).text)
    v = j['data']['cards']
    since_id = str(j['data']['cardlistInfo']['since_id'])
    sv1, sv2, sv3, sv4, s = 0, 0, 0, 0, 0
    e = int(time.mktime(time.strptime(end, "%Y-%m-%d")))
    s001 = int(time.mktime(time.strptime(s000, "%Y-%m-%d")))
    for i in v:
        if i["card_type"] != 9:
            continue
        k = i['mblog']
        d465 = str(k['created_at'])
        s = int(time.mktime(time.strptime(d465, "%a %b %d %H:%M:%S %z %Y")))
        if n == '' and s < e:
            continue
        if s < e:
            break
        elif s > s001:
            continue
        v1, v2, v3, v4 = int(k['comments_count']), int(k['attitudes_count']), int(k['pending_approval_count']), int(
            k['reposts_count'])
        l.append((v1, v2, v3, v4, k['created_at'], k['text'][0:5]))
        sv1, sv2, sv3, sv4 = sv1 + v1, sv2 + v2, sv3 + v3, sv4 + v4
    if s >= e:
        rk, (_a, _b, _c, _d) = a(end, s000, u, l, lfrom,since_id)
        sv1, sv2, sv3, sv4 = sv1 + _a, sv2 + _b, sv3 + _c, sv4 + _d
    return l, (sv1, sv2, sv3, sv4)


def get_data_and_write(start, end, sour,url):
    rk, p = a(start, end, url, [], sour,'')

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
    c = get_config()
    start = c["time_start"]
    end = c["time_end"]
    for v in c["lists"]:
        if v['enable']:
            get_data_and_write(start,end,v["name"],v["url"])


