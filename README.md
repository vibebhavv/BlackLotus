
# [⚠️Discontinued] BlackLotus

**BlackLotus** is an advanced live scraping tool designed specifically for the GitHub search engine. It automates the process of discovering and collecting sensitive information such as exposed API keys, access tokens, credentials, and secret keys. By leveraging custom-crafted dorks, BlackLotus continuously scans public repositories and commits in real-time, helping security researchers, bug bounty hunters, and developers identify accidental leaks of confidential data before they can be exploited.

## Features

- Uses github search engine
- Easily scrapes API/Token/creds/Key
- Supports Proxies
- Check Github dorking pattern for file-type search

## Installation

```bash
  git clone https://github.com/vibebhavv/BlackLotus
  cd BlackLotus
  pip3 install requests
  python3 main.py --help
```

### Use case

Github Auth token **REQUIRED**

```
python3 main.py -s {API/TOKEN/CRED/KEY} --limit 20 -ftype {env/txt/json/config/log} -o output.txt
```
## Other resources

This section includes links, documentation, and references to the sources and tools that inspired **BlackLotus**. Here you’ll find related open-source scrapers, GitHub dorking techniques, and guides explaining how crafted dorks work to pinpoint sensitive information like keys and tokens. These resources will help you understand the logic behind GitHub search operators, refine your own dorks, and explore similar tools for ethical reconnaissance and security research.

- [Github dorking pattern](https://gist.github.com/win3zz/0a1c70589fcbea64dba4588b93095855)
- [Trufflehog](https://github.com/trufflesecurity/trufflehog)
- [Lock-Picker](https://github.com/42zen/lock-picker)
- [KeyHack](https://github.com/streaak/keyhacks)
