import jwt, hashlib, math, time, random, os, threading, tls_client, requests, os
from python_ghost_cursor import path
from datetime import datetime
from json import dumps

def scrape_proxies():
    os.system("cls")
    urls_to_scrape=[
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
    ]
    with open("proxies.txt","w") as f:
        f.write("")
        f.close()
    for i in urls_to_scrape:
        proxies = requests.get(url=i).text
        with open("proxies.txt","a+") as f:
            f.write(proxies)
            f.close()
        num = len(proxies.split('\n'))
        print(f"(+) Scraped: {i} | {num}")
    time.sleep(1)
    main()
def generate_hsl(req):
    x = "0123456789/:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    req = jwt.decode(req,options={"verify_signature":False})
    def a(r):
        for t in range(len(r) - 1, -1, -1):
            if r[t] < len(x) - 1:
                r[t] += 1
                return True
            r[t] = 0
        return False
    def i(r):
        t = ""
        for n in range(len(r)):
            t += x[r[n]]
        return t
    def o(r, e):
        n = e
        hashed = hashlib.sha1(e.encode())
        o = hashed.hexdigest()
        t = hashed.digest()
        e = None
        n = -1
        o = []
        for n in range(n + 1, 8 * len(t)):
            e = t[math.floor(n / 8)] >> n % 8 & 1
            o.append(e)
        a = o[:r]
        def index2(x,y):
            if y in x:
                return x.index(y)
            return -1
        return 0 == a[0] and index2(a, 1) >= r - 1 or -1 == index2(a, 1)
    def get():
        for e in range(25):
            n = [0 for i in range(e)]
            while a(n):
                u = req["d"] + "::" + i(n)
                if o(req["s"], u):
                    return i(n)
    result = get()
    hsl = ":".join([
        "1",
        str(req["s"]),
        datetime.now().isoformat()[:19] \
            .replace("T", "") \
            .replace("-", "") \
            .replace(":", ""),
        req["d"],
        "",
        result
    ])
    return hsl
def get_proxy():
    while True:
        with open("proxies.txt","r") as f:
            proxy = random.choice(f.read().splitlines())
            f.close()
            if not proxy == "" or proxy == "\n":
               break 
    return proxy
def scrape_images():
    os.system("cls")
    v = tls_client.Session(client_identifier="chrome_111").get("https://js.hcaptcha.com/1/api.js").text.split('nt="')[1].split('"')[0]
    class Scrapper():
        def __init__(self, site_key: str, host: str):
            self.sk = site_key
            self.host = host 
            self.session = tls_client.Session(client_identifier="chrome_111",random_tls_extension_order=True)
            self.session.headers={
                'authority': 'hcaptcha.com',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }
            self.proxy = get_proxy()
            self.session.proxies={
                "http": "http://"+self.proxy,
                "https": "http://"+self.proxy,
            }
        def get_c(self):
            headers = {
                'accept': 'application/json',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7',
                'cache-control': 'no-cache',
                'content-type': 'text/plain',
                'origin': 'https://newassets.hcaptcha.com',
                'pragma': 'no-cache',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
            }
            params = {'v':v,'host':self.host,'sitekey':self.sk,'sc':'1','swa':'1'}
            r = self.session.post('https://hcaptcha.com/checksiteconfig',params=params,headers=headers,timeout_seconds=10)
            c = r.json()["c"]
            c["type"] = "hsl"
            return c
        def get_captcha(self,c,hsl):
            headers = {
                'accept': 'application/json',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://newassets.hcaptcha.com',
                'pragma': 'no-cache',
                'referer': 'https://newassets.hcaptcha.com/',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
            }
            start = {'x': 100, 'y': 100}
            end = {'x': 600, 'y': 700}
            timestamp = int((time.time() * 1000) + round(random.random() * (120 - 30) + 30))
            mm = [[int(p['x']), int(p['y']), int(time.time() * 1000) + round(random.random() * (5000 - 2000) + 2000)] for p in path(start, end)]
            payload = {
                "v": v,
                "sitekey": self.sk,
                "host": self.host,
                "hl": "en",
                "motionData": dumps({"st":timestamp,"dct":timestamp,"mm":mm},separators=(",",":")),
                "n": hsl,
                "c": dumps(c,separators=(",",":"))
            }
            r = self.session.post(f'https://hcaptcha.com/getcaptcha/{self.sk}',headers=headers,data=payload,timeout_seconds=10)
            return r.json()
        def scrape_challenges(self):
            while True:
                try:
                    start = time.time()
                    c = self.get_c()
                    captcha_data = self.get_captcha(c,generate_hsl(c["req"]))
                    question = captcha_data["requester_question"]["en"]
                    folder_name = question.replace("Please click each image containing ","")
                    if not folder_name in os.listdir("images"):
                        os.mkdir(f"images/{folder_name}")

                    def download_n_save(image_name):
                        try:
                            sess = tls_client.Session(client_identifier="chrome_111")
                            sess.proxies={
                                "http": "http://"+self.proxy,
                                "https": "http://"+self.proxy,
                            }
                            image = sess.get(i["datapoint_uri"],timeout_seconds=10).content
                            image_name = hashlib.md5(image).hexdigest()
                            f = open(f"images/{folder_name}/{image_name}.jpg","wb")
                            f.write(image)
                            f.close()
                        except:
                            pass
                    threads = []
                    for i in captcha_data["tasklist"]:
                        thread = threading.Thread(target=download_n_save, args=(i["datapoint_uri"],))
                        threads.append(thread)
                        thread.start()
                    for t in threads:
                        t.join()

                    with open("questions.txt", "a+") as f:
                        f.seek(0)
                        if question not in f.read():
                            f.write(question + "\n")
                        f.close()
                    print(f"(+) Label: {folder_name} | Images: {len(captcha_data['tasklist'])} | Total: {len(os.listdir(f'images/{folder_name}'))} | {self.proxy} | {time.time()-start}s")
                except:
                    pass
    threads = range(int(input("(>) Threads >> ")))
    for _ in threads:
        threading.Thread(target=Scrapper("4c672d35-0701-42b2-88c3-78380b0db560","discord.com").scrape_challenges).start()

def main():
    os.system("cls")
    print("Super-Nova | Scraper".center(os.get_terminal_size().columns))
    print("1 - [ Image Scraper ]".center(os.get_terminal_size().columns))
    print("2 - [ Proxy Scraper ]".center(os.get_terminal_size().columns))
    inputed = int(input("(>) Input >> "))
    if inputed == 2:
        scrape_proxies()
    elif inputed == 1:
        scrape_images()
        if not "images" in os.listdir(os.curdir):
            os.mkdir("images")
        if open("proxies.txt").read() == "<# Free proxies work. #>":
            print("(-) No proxies detected in proxies.txt")
            input("(#) Press ENTER to continue.")
    else:
        print("(-) Invalid input.")
        input("(#) Press ENTER to return.")
        main()
main()
