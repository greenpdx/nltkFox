#!/usr/bin/env python3

import requests
import urllib.parse as urlparse
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

url = 'https://foxnews.com'

# 3 content sections, ( pre-content, page-content, post-content)
# page-content)
#   <main class_=main-content>
#     <div class_=main main-primary
#       <article class_=article story-1
#           <a href
#               <div class_=kicker          # kicker
#               <header class_=info-header  # main-title
#                   <a href                 # main-article
#               <div class_=related
#                   <a href                 # top-articles
#        <div class_=main main-secondary
#           <article class_=article story-NN
#               <a href                     # articles
# post-content)
#  <section class_=collection
#    <header class=heading
#      <h3.a.string                         # section-name
#    <div class=content
#      
#      <article
#        <div class=m                       # image 
#        <div class=info
#          <header class=info-header
#            <div class=meta                # meta 



def rdpage(rslt, coll):
  
    rslt['ts'] = int(time.time())
    #print("\n\n",rslt)
    if coll.find_one_and_update({"href" : rslt['href'] }, { '$set': { 'last': rslt['ts']}}):
        #print("FOUND ", rslt['href'])
        return None
    print("INSERT ", rslt['href'])
    response = requests.get(rslt['href'])
    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.find("main")
    artcl = main.find("article")
    #print(len(artcl))
    rslt['h1'] = artcl.find("h1", class_="headline").string.strip()
    h2 = artcl.find("h2", class_="sub-headline")
    if h2:
        rslt['h2'] = h2.string.strip()
    #print(rslt)
    artcl = artcl.find("div", class_="article-body")
    if not artcl:
        return None
    ps = artcl.find_all("p")
    txt = ""
    for p in ps[1:]:
        if p.strong:
            continue
        for strs in p.strings:
            txt = txt + " " + strs.strip()

    #print(txt)
    rslt['txt'] = txt[1:]
    idx = coll.insert_one(rslt).inserted_id
    return idx

def parse_article(art):
    l = len(art.contents)
    jart = {}
    ##* jart['clss'] = art['class']
    m = art.find("div", class_="m")
    info = art.find("div", class_="info")
    #print(l, info, "\n", m, "###\n\n")

    kicker = art.find("div", class_="kicker")
    if kicker:
        jart['kicker'] = kicker.string

    if m:
        #print(m)
        jm = {}
        href = m.find("a")['href']
        url = urlparse.urlparse(href)
        if url.netloc[:5] == 'video':
            #print(url)
            jm['vid'] = True
        else:
            jm['vid'] = False
        #print(url)
        if url.scheme == '':
            href = 'https:' + href
            #print("MREF ", href)
        jm['href'] = href 
        alt = m.find("img")
        if alt:
            jm['alt'] = alt['alt']
        #jart['m'] = jm

    ahs = info.find_all("a")
    jart['lnks'] = []
    for a in ahs:
        jlnk = {}
        href = a['href']
        if a.string is None:
            print("NO TITLE", a)
            continue
        jlnk['title'] = a.string
        url = urlparse.urlparse(href)
        if url.scheme == '':
            href = 'https:' + href
            #print("HREF ", href)
            continue
        jlnk['href'] = href
        if url.netloc[:5] == 'video' or url.path[1:9] == 'category' or url.path[:6] == '/watch':
            #print(url)
            continue
        else:
            idx = url.path.rfind('/')
            if idx == 0:
                #print("NO",idx, url)
                continue

        jart['lnks'].append(jlnk)
    
        #cont = info.find("div", class_="content")
        #if cont:
        #    mlnks = cont.find_all('a')
        #    for ml in mlnks:
        #        lnk = {}
        #        lnk['href'] = ml['href']
        #        lnk['title'] = ml.string
        #        jart['lnks'].append(lnk)

    #print(len(jart['lnks']))
    #print(ahdr['href'])

    if len(jart['lnks']) == 0:
        return None
    else:
        jart['pri'] = len(jart['lnks'])
    return jart


def bs(url, db):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    dbcol = db['prelp']

    arts = soup.find_all("article", class_="article", limit=1000)
    print(len(arts))
    cnt = [0,0,0,0,0,0]
    for art in arts:
        rslt = parse_article(art)
        if rslt:
            print(rslt, '\n')
            for idx, lnk in enumerate(rslt['lnks']):
                pri = len(rslt['lnks']) if idx != 0 else len(rslt['lnks'])+1
                lnk['pri'] = pri
                if 'kicker' in rslt:
                    lnk['kr'] = rslt['kicker']

                url = urlparse.urlparse(lnk['href'])
                if url.netloc[-11:] != 'foxnews.com' and url.netloc[-15:] != 'foxbusiness.com':
                    cnt[0] =cnt[0] +1
                    dbcol.insert_one(lnk)
                    continue
                if lnk['title'] == None:
                    cnt[1] = cnt[1] +1
                    dbcol.insert_one(lnk)
                    continue

                jrtn = rdpage(lnk, dbcol)
                cnt[2] = cnt[2] +1
        else:
            cnt[3] =cnt[3] + 1
    print(cnt)
    return

    main = soup.find("main")


    stry1 = main.find_all("div", class_="main")
    print(len(stry1))
    n = 0
    f = 0
    for stry in stry1:
        colls = stry.find_all("div", class_="collection")
        #print("  ", len(colls) )

        for coll in colls:
            arts1 = coll.find_all("article")
            #print("    ", len(list(arts1)))

            for art in arts1:
                kikr = art.find(class_="kicker")
                if kikr:
                    print(kikr.string)
                lnks = art.find_all("a")
                #print("        ", len(lnks))
                for lnk in lnks:
                    #if len(list(lnk.children)) == 1:
                    if lnk.string:
                        if ' ' in lnk.string:
                            pagdata = rdpage(lnk, dbcol)
                            if pagdata:
                                print(pagdata)
                                idx = dbcol.insert_one(pagdata).inserted_id
                                n = n + 1
                            else:
                                f = f + 1
                            #return
            #break

    print(n, f) 



def main():
    client = MongoClient('mongodb://10.0.42.168:27017/')
    db = client['foxnews2']
    #coll = db['prelp']
    #idx = coll.insert_one({}).inserted_id
    #print(idx)
    bs(url, db)


if __name__ == "__main__":
    # execute only if run as a script
    main()



