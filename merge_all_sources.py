#!/usr/bin/env python3
"""OTA Data Merger v2"""
import os, re, json, requests
from datetime import datetime
from urllib.parse import quote

LOCAL_DATA_DIR = r"c:\Users\Dracula\WorkBuddy\20260425112947\oplus-ota-hunter\data\_repo_cache"
OUTPUT_FILE = "merged_data/ota_info.json"

DAXIAMU_MAP = {
    'LE2110':'一加9','LE2111':'一加9','LE2113':'一加9','LE2115':'一加9',
    'LE2117':'一加9R','MT2110':'一加9RT','IN2010':'一加8','IN2011':'一加8',
    'IN2013':'一加8','IN2015':'一加8','IN2017':'一加8','IN2020':'一加8 Pro',
    'IN2021':'一加8 Pro','IN2023':'一加8 Pro','IN2025':'一加8 Pro','IN2027':'一加8 Pro',
    'IN2019':'一加8T','KB2000':'一加8T','KB2001':'一加8T','KB2003':'一加8T',
    'KB2005':'一加8T','KB2007':'一加8T','GM1900':'一加7','GM1901':'一加7',
    'GM1903':'一加7','GM1905':'一加7','GM1907':'一加7','GM1910':'一加7 Pro',
    'GM1911':'一加7 Pro','GM1913':'一加7 Pro','GM1915':'一加7 Pro','GM1917':'一加7 Pro',
    'HD1900':'一加7T','HD1901':'一加7T','HD1903':'一加7T','HD1905':'一加7T',
    'HD1907':'一加7T','HD1910':'一加7T Pro','HD1911':'一加7T Pro','HD1913':'一加7T Pro',
    'HD1917':'一加7T Pro','HD1918':'一加7T Pro','HD1919':'一加7T Pro',
}
LOCAL_MAP = {
    "PJZ110":"一加13","PKX110":"一加13T","PJD110":"一加12","PHB110":"一加11",
    "PLK110":"一加15","PLZ110":"一加15T","PLQ110":"一加Ace6","PLR110":"一加Ace6T",
    "PKR110":"一加Ace5Pro","PKG110":"一加Ace5","PLC110":"一加Ace5至尊版","PLF110":"一加Ace5竞速版",
    "PJX110":"一加Ace3Pro","PJE110":"一加Ace3","PJF110":"一加Ace3V","PJA110":"一加Ace2Pro",
    "PHP110":"一加Ace2V","PHK110":"一加Ace2","OPD2401":"一加平板2Pro","OPD2301":"一加Pad2",
    "PHN110":"OPPOFindN3","PGEM10":"OPPOFindX6Pro","PHY110":"OPPOFINDX7Ultra",
}

def fetch_daxiaamu(code):
    versions = []
    name = DAXIAMU_MAP.get(code.upper())
    if not name: return versions
    try:
        url = f"https://yun.daxiaamu.com/{quote(name)}/"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            seen = set()
            for m in re.finditer(r'<a\s+href="([^"]+)"', resp.text):
                href = m.group(1)
                if href.startswith('http') or not href.endswith('/'): continue
                if any(k in href for k in ['ROOT','教程','百度网盘']): continue
                folder = href.rstrip('/')
                ota = re.search(r'([A-Z]{2,}_\d+\.\d+\.\d+\.\d+)', folder, re.I) or \
                      re.search(r'ColorOS\s*([\d.]+\s*[A-Z]\.\d+)', folder, re.I) or \
                      re.search(r'OxygenOS\s*([\d.]+)', folder, re.I)
                if not ota: continue
                ver = ota.group(1)
                if ver in seen: continue
                seen.add(ver)
                versions.append({"ota_version":ver,"version_name":folder,"coloros_version":re.search(r'ColorOS\s*([\d.]+)',folder,re.I).group(1) if re.search(r'ColorOS',folder) else "","download_url":url+href,"source":"daxiaamu"})
        print(f"  [daxiaamu] {code}: {len(versions)} versions")
    except Exception as e:
        print(f"  [daxiaamu] {code}: ERROR")
    return versions

def fetch_local(code, folder):
    versions = []
    txt = os.path.join(LOCAL_DATA_DIR,"models",folder,"ota-version.txt")
    if not os.path.exists(txt): return versions
    with open(txt,'r',encoding='utf-8') as f:
        for line in f:
            if '#' in line:
                ota,comment = line.split('#',1)
                cos = re.search(r'ColorOS[:\s]*([^\s#]+)',comment)
                versions.append({"ota_version":ota.strip(),"version_name":cos.group(1) if cos else "","coloros_version":cos.group(1) if cos else "","download_url":"","source":"local"})
            elif line.strip():
                versions.append({"ota_version":line.strip(),"version_name":"","coloros_version":"","download_url":"","source":"local"})
    return versions

def merge(d,v):
    m = {x["ota_version"]:x for x in v}
    for x in d:
        k = x["ota_version"]
        if k not in m: m[k]=x
        elif x["download_url"] and not m[k]["download_url"]: m[k]=x
    return list(m.values())

def sort_key(v):
    m = re.search(r'_(\d+)\.(\d+)\.(\d+)\.(\d+)_',v["ota_version"])
    return tuple(int(x) for x in m.groups()) if m else (0,0,0,0)

print("OTA Data Merger v2")
all_data = {"version":2,"updated_at":datetime.now().isoformat(),"sources":["daxiaamu","local"],"models":{}}
for code in sorted(set(LOCAL_MAP.keys())|set(DAXIAMU_MAP.keys())):
    print(f"Processing: {code}")
    d = fetch_daxiaamu(code)
    v = fetch_local(code, LOCAL_MAP.get(code.upper(),""))
    m = merge(d,v)
    m.sort(key=sort_key,reverse=True)
    if m:
        all_data["models"][code]={"code":code,"name":LOCAL_MAP.get(code.upper(),DAXIAMU_MAP.get(code.upper(),code)),"total_versions":len(m),"versions":m}
        print(f"  -> Total: {len(m)} versions")

os.makedirs("merged_data",exist_ok=True)
with open(OUTPUT_FILE,'w',encoding='utf-8') as f: json.dump(all_data,f,ensure_ascii=False,indent=2)
print(f"Done! {len(all_data['models'])} models -> {OUTPUT_FILE}")
