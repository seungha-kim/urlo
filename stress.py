from concurrent.futures import ThreadPoolExecutor

import requests

def post_url(url):
    res = requests.post('http://localhost:8000', data={'url': url, 'access_key': 'access_key'})
    print(f'url {url} submitted.')
    return res.json()['id']

def test():
    result = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(1, 500):
            url = 'url' + str(i)
            result.append((url, executor.submit(post_url, url)))
    result = list(map(lambda arg: (arg[0], arg[1].result()), result))
    return result

if __name__ == '__main__':
    print(test())
