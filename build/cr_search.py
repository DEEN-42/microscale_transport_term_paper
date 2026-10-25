import json, sys, urllib.request, urllib.parse
qs = sys.argv[1:]
for q in qs:
    u = "https://api.crossref.org/works?rows=4&select=DOI,title,author,issued,container-title,volume,issue,page,article-number,is-referenced-by-count&query.bibliographic="+urllib.parse.quote(q)
    m = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"refcheck (mailto:shubhraneelpal@gmail.com)"}), timeout=30))["message"]["items"]
    print("##", q)
    for i in m:
        au = ", ".join(a.get("family","") for a in i.get("author",[])[:3])
        print("  ", i["DOI"], "|", i["title"][0][:85], "|", au, "|", (i.get("issued",{}).get("date-parts") or [[None]])[0][0], "|", (i.get("container-title") or [""])[0][:35], i.get("volume"), i.get("page") or i.get("article-number"), "| cites", i.get("is-referenced-by-count"))
