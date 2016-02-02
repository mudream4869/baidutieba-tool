import BeautifulSoup as bs
import requests
import sys

def printu(input_str):
    print(input_str.encode('utf-8'))

def ch2num(ch):
    arr = "0123456789"
    for x in range(10):
        if ch == arr[x]:
            return x
    return 0

def getLastNum(input_str):
    ret, a10 = 0, 1
    for ch in input_str[::-1]:
        if ch != '=':
            ret = ret + ch2num(ch)*a10
            a10 *= 10
        else:
            break
    return ret

def removetag(input_str, tagname):
    input_str = input_str.replace("</" + tagname + ">", "")
    
    while True:
        get_str = "<" + tagname
        l = len(get_str)
        s_ind = -1
        for i in range(len(input_str)):
            if i >= l and input_str[i-l:i] == "<" + tagname :
                s_ind = i
                break
        if s_ind == -1 : break

        for i in range(len(input_str)):
            if i < s_ind : continue
            get_str = get_str + input_str[i]
            if input_str[i] == ">" : break

        input_str = input_str.replace(get_str, "")

    return input_str

story_url = sys.argv[1]

printu("<head>")
printu("<title>Test</title>")
printu('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
printu("</head>")
printu("<body>")

printu("Story url = " + story_url + "</ br>")

res = requests.get(story_url)

if res.status_code != 200 :
    print("Error occur : when try to get request by url.")
    exit()

soup = bs.BeautifulSoup(res.text)
posts_div = soup.findAll("div", {"id": "j_p_postlist"})

if not len(posts_div):
    print("Error occur : no post exists.")
    exit()

## First : Get author

author_name = posts_div[0].findAll("a", {"class" : lambda x : x and "p_author_name" in x.split()})[0].text

printu("Author = " + author_name + "</ br>")

## Second : Get Last page number

pages_a = soup.findAll("li", 
    {"class" : "l_pager pager_theme_4 pb_list_pager"}
)[0].findAll("a")

last_page_num = getLastNum(pages_a[len(pages_a)-1].get("href"))

## Third : Seive post

for i in range(last_page_num):
    page = i + 1
    curent_url = story_url + "?pn=" + str(page)

    res = requests.get(curent_url)

    if res.status_code != 200 :
        print("Error occur : when try to get request by url at page %d."%(page,))
        continue

    soup = bs.BeautifulSoup(res.text)

    posts_div_list = soup.findAll("div", 
        {"class" : lambda x : x and "l_post" in x.split()}
    )

    for post in posts_div_list:
        post_author_name = post.findAll("a", 
            {"class" : lambda x : x and "p_author_name" in x.split()}
        )[0].text

        if post_author_name != author_name : continue

        id_name = "post_content"

        content = post.findAll("div", 
            {"id" : lambda x : x and len(x) > len(id_name) and x[0:len(id_name)] == id_name }
        )[0]

        print(str(content))

printu("</body>")
