import json, sys, urllib.request
dois = """10.1016/j.applthermaleng.2023.120340
10.1109/TCAPT.2008.2001197
10.1109/EDL.1981.25367
10.1115/1.4007407
10.1016/B978-0-12-407819-2.00004-9
10.1080/01457632.2018.1480868
10.1016/j.ijheatmasstransfer.2023.124453
10.3390/ma15155459
10.1016/j.mne.2023.100235
10.1115/1.2822693
10.1016/j.applthermaleng.2006.02.023
10.1115/1.1560145
10.1016/j.ijheatmasstransfer.2010.05.043
10.1016/j.ijheatmasstransfer.2016.05.093""".split()
for d in dois:
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d, headers={"User-Agent":"refcheck (mailto:shubhraneelpal@gmail.com)"}), timeout=30)
        m = json.load(r)["message"]
        au = ", ".join(a.get("family","") for a in m.get("author",[])[:4])
        yr = (m.get("issued",{}).get("date-parts") or [[None]])[0][0]
        print("OK ", d, "|", m["title"][0][:90], "|", au, "|", yr, "|", (m.get("container-title") or [""])[0][:40], m.get("volume"), m.get("issue"), m.get("page") or m.get("article-number"))
    except Exception as e:
        print("ERR", d, e)
