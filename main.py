import time
import requests
import json
import datetime
from pandas import DataFrame


# 百度的


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


def baidu(start, end):
    u = "https://m.weibo.cn/api/container/getIndex?type=uid&value=1799201635&containerid=1076031799201635&since_id="

    rk, p = a(start, end, u, [], '')
    datas = []
    for i in range(len(rk)):
        (m, b, c, d, t, u) = rk[i]
        datas.append(
            {'title': u, 'comments_count': m, 'attitudes_count': b, 'pending_approval_count': c, 'reposts_count': d,
             'time': t, 'cal': m + b + c + d})

    file_path = './百度微博汇总数据.xlsx'
    DataFrame(datas).to_excel(file_path, sheet_name='Sheet1', index=False,
                              columns=['title', 'comments_count', 'attitudes_count', 'pending_approval_count',
                                       'reposts_count', 'time',
                                       'cal'])


def gaode(start, end):
    u = "https://m.weibo.cn/api/container/getIndex?type=uid&value=1661169385&containerid=1076031661169385&since_id="

    rk, p = a(start, end, u, [], '')

    datas = []
    for i in range(len(rk)):
        (m, b, c, d, t, u) = rk[i]
        datas.append(
            {'title': u, 'comments_count': m, 'attitudes_count': b, 'pending_approval_count': c, 'reposts_count': d,
             'time': t, 'cal': m + b + c + d})

    file_path = './高德微博汇总数据.xlsx'
    DataFrame(datas).to_excel(file_path, sheet_name='Sheet1', index=False,
                              columns=['title', 'comments_count', 'attitudes_count', 'pending_approval_count',
                                       'reposts_count', 'time',
                                       'cal'])


if __name__ == '__main__':
    start = "2020-12-10"
    end = "2020-12-16"
    baidu(start, end)
    gaode(start, end)