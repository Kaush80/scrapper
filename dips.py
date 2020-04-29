def get_page(url):
    try:
        import urllib.request
        return str(urllib.request.urlopen(url).read())
    except:
        return " "
        

def get_next_target(page):
    start_link=page.find('<a href=')
    if start_link==-1:
        return None, 0
    start_quote = page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links=[]
    while True:
        url, endpos=get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

""" Union of two Links"""
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
            
def crawl_web(seed, max_depth): 
    tocrawl=[seed]
    crawled=[]
    depth=0
    next_depth=[]
    index=[]
    while tocrawl and depth <= max_depth:
        page=tocrawl.pop()
        if page not in crawled:
            content=get_page(page)
            add_page_to_index(index, page, content)
            union(next_depth,get_all_links(content))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth+=1
    '''return crawled'''
    return index

def split_string(source,splitlist):
    output=[]
    atsplit=True #at a split point
    for char in source:#iterate through string
        if char in splitlist:
            atsplit=True
        else:
            if atsplit:
                output.append(char)
                atsplit=False
            else:
                #add character to last word of the outputlist
                output[-1]=output[-1]+char
    return output
            
            
def add_to_index(index,keyword,url):
    for entry in index:
        if entry[0]==keyword:
            if not url in entry[1]:
                entry[1].append(url)
        return
    index.append([keyword,[url]])

def add_page_to_index(index,url,content):
    words= content.split()
    for word in words:
        add_to_index(index,word,url)

def lookup(index,keyword):
    for entry in index:
        if entry[0]==keyword:
            return entry[1]
    return []
            
        
"""x=crawl_web(get_page("https://en.m.wikipedia.org/wiki/The_Magic_Words_are_Squeamish_Ossifrage"))
x=(crawl_web("http://xkcd.com/353",5))
print(x)"""
