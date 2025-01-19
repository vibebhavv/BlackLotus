import time
import json
import urllib.request
import requests
import argparse
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime

class Scraper:
    def __init__(self, dork_wordlist=r'search-dork.txt'):
        self.result = {}
        self.dork_wordlist = dork_wordlist
        self.parser = argparse.ArgumentParser(description='Available Commands for [ BlackLotus ]')

    def banner(self):
        print("")      
        print("\t\t"r"___  _    ____ ____ _  _  _    ____ ___ _  _ ____    v1.0") 
        print("\t\t"r"|__] |    |__| |    |_/   |    |  |  |  |  | [__  ")
        print("\t\t"r"|__] |___ |  | |___ | \_  |___ |__|  |  |__| ___] ")
        print("")
        
    def user_auth(self):
        """Asks for github access token from user to access github search engine feature"""
        auth_token = input("Enter Github auth token: ").strip()
        auth_struct = {
            "auth_token": f"{auth_token}"
        }
        try:
            # Fixed: Changed json.load to json.dump for writing
            with open(r'db\AUTH_KEY.json', 'w+') as f:
                json.dump(auth_struct, f, indent=4)
                print(f"Auth token saved to AUTH_KEY.json")
        except Exception as e:
            print(f"[ERR] Failed to save auth token: {str(e)}")
    
    def arg_commands(self):
        """Available command line arguments"""
        self.parser.add_argument('--token', help='Fetch exposed tokens, including jwt tokens')
        self.parser.add_argument('--api', help='Fetch exposed api')
        self.parser.add_argument('-e', help='Fetch .env,config.json,etc files')
        self.parser.add_argument('--cred', help='Fetch DB credentials')
        self.parser.add_argument('--key', help='Fetch Private keys like ssh,rsa,tls/ssl')
        self.parser.add_argument('--proxy', help='Use proxy from a given file')
        self.parser.add_argument('-w', '--wordlist', help='Use custom dork list from a given file')
        self.parser.add_argument('-o', '--output', help='Save to output file')

        return self.parser.parse_args()

    def proxies(self, proxy_file):
        # Fixed: Changed self.proxies to proxy_file parameter
        try:
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            return proxies
        except Exception as e:
            print(f"[ERR] Failed to load proxies: {str(e)}")
            return []

    def scrape_with_proxies(self, url, proxy):
        # Fixed: Added self parameter
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            return response.status_code, response.text[:100]
        except Exception as e:
            return None, str(e)

    def search_tokens(self, query):
        """Search for exposed tokens"""
        token_dorks = [
            'filename:.env "JWT_SECRET"',
            'filename:.env "API_TOKEN"',
            'filename:.env "AUTH_TOKEN"',
            'filename:config.json "token"'
        ]
        for dork in token_dorks:
            # Fixed: Added proper query formatting
            search_query = f"{dork} {query}".strip()
            self.search_engine(search_query)
            time.sleep(2)  # Avoid rate limiting

    def search_api(self, query):
        """Search for exposed APIs"""
        api_dorks = [
            'filename:swagger.json',
            'filename:api.yaml',
            'filename:openapi.json',
            'filename:.env "API_URL"'
        ]
        for dork in api_dorks:
            search_query = f"{dork} {query}".strip()
            self.search_engine(search_query)
            time.sleep(2)

    def search_env_files(self, query):
        """Search for environment and config files"""
        env_dorks = [
            'filename:.env',
            'filename:config.json',
            'filename:settings.json',
            'filename:.env.local'
        ]
        for dork in env_dorks:
            search_query = f"{dork} {query}".strip()
            self.search_engine(search_query)
            time.sleep(2)

    def search_credentials(self, query):
        """Search for database credentials"""
        cred_dorks = [
            'filename:.env "DB_PASSWORD"',
            'filename:.env "DATABASE_URL"',
            'filename:config.json "password"',
            'filename:.env "MYSQL"'
        ]
        for dork in cred_dorks:
            search_query = f"{dork} {query}".strip()
            self.search_engine(search_query)
            time.sleep(2)

    def search_keys(self, query):
        """Search for private keys"""
        key_dorks = [
            'filename:.pem private',
            'filename:.key private',
            'filename:id_rsa',
            'filename:.ssh/config'
        ]
        for dork in key_dorks:
            search_query = f"{dork} {query}".strip()
            self.search_engine(search_query)
            time.sleep(2)

    def run(self):
        args = self.arg_commands()
        
        if args.token:
            print(f"[INFO] Trying to fetch {args.token} token")
            self.search_tokens(args.token)

        if args.api:
            print(f"[INFO] Trying to fetch {args.api} api")
            self.search_api(args.api)
            
        if args.e:
            print(f"[INFO] Trying to fetch .env,config.json,etc files")
            self.search_env_files(args.e)
            
        if args.key:
            print(f"[INFO] Trying to fetch {args.key} keys")
            self.search_keys(args.key)
        
        if args.cred:
            print(f"[INFO] Trying to fetch {args.cred} credentials")
            self.search_credentials(args.cred)

        if args.wordlist:
            try:
                with open(args.wordlist, 'r') as f:
                    custom_dorks = [line.strip() for line in f if line.strip()]
                    for dork in custom_dorks:
                        self.search_engine(dork)
                        time.sleep(2)
            except FileNotFoundError:
                print(f"[ERR] Error file {args.wordlist} not found!")

        if args.proxy:
            print(f"[INFO] Using proxies from {args.proxy}")
            proxies = self.proxies(args.proxy)
            if proxies:
                print(f"[INFO] Loaded {len(proxies)} proxies")
                # Fixed: Added proxy usage implementation
                for proxy in proxies:
                    print(f"[INFO] Testing proxy: {proxy}")
                    status, _ = self.scrape_with_proxies("https://api.github.com", proxy)
                    if status == 200:
                        print(f"[INFO] Proxy {proxy} is working")
                    else:
                        print(f"[WARN] Proxy {proxy} failed")

        if args.output:
            try:
                with open(args.output, 'w') as f:
                    json.dump(self.result, f, indent=4)
                print(f"[INFO] Output saved to {args.output}")
            except Exception as err:
                print(f"[ERR] Failed to save result: {str(err)}")

    def search_engine(self, query):
        """Function for accessing github search engine feature"""
        encoded_query = urllib.parse.quote(query)
        # Fixed: Changed to code search endpoint
        url = f"https://api.github.com/search/code?q={encoded_query}"

        try:
            with open(r'db\AUTH_KEY.json', 'r') as f:
                auth_data = json.load(f)
                headers = {
                    "Authorization": f"token {auth_data['auth_token']}",
                    "Accept": "application/vnd.github.v3+json",  # Fixed: Added Accept header
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.38 Safari/537.36 Brave/75"
                }
        except Exception as e:
            print(f"[WARN] Failed to load auth token: {str(e)}")
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.38 Safari/537.36 Brave/75"
            }

        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

                print(f"\nFound {data['total_count']} results for query: {query}\n")

                for item in data['items'][:10]:
                    print(f"\nFile: {item['path']}")
                    print(f"Repository: {item['repository']['full_name']}")
                    print(f"URL: {item['html_url']}")
                    
                    # Store results
                    if query not in self.result:
                        self.result[query] = []
                    self.result[query].append({
                        'path': item['path'],
                        'repo': item['repository']['full_name'],
                        'url': item['html_url'],
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    print("-" * 100)
                    
        except urllib.error.HTTPError as e:
            print(f"[ERR] Error: {e.code} - {e.reason}")
            if e.code == 403:
                print("[INFO] Rate limit exceeded. Please wait before trying again")
            elif e.code == 401:
                print("[INFO] Authentication failed. Please check your GitHub token")
        except Exception as e:
            print(f"[ERR] An error occurred: {e}")

if __name__ == '__main__':
    # Fixed: Changed variable name to lowercase
    scraper = Scraper()
    scraper.banner()
    #scraper.user_auth()
    scraper.run()