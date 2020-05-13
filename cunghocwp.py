import requests
import base64
from bs4 import BeautifulSoup


def getpost(domain='cunghocwp.com'):
    result = []
    ep = f"https://{domain}/wp-json/wp/v2/posts?per_page=100&page="
    for i in range(1, 400):
        epurl = ep + str(i)
        r = requests.get(epurl)
        result.extend(r.json())
        print(f"Done i={i} ==> result {len(r.json())} from {domain}")
        if len(r.json()) < 100:
            break
    return result


def get_images(content):
    soup = BeautifulSoup(content, 'lxml')
    img = soup.find_all('img')
    imglinks = [x['src'] for x in img if x.get(
        'src') and 'cunghocwp.com' in x.get('src')]
    return imglinks


def replace_string(string, repl_list):
    for repl in repl_list:
        string = string.replace(repl[0], repl[1])
    return string


def process_post(posts):
    result = []
    for post in posts:
        title = post['title']['rendered']
        content = post['content']['rendered']
        imgs = get_images(content)
        repl_list = []
        for img in imgs:
            if "https://" in img:
                repl_list.append(
                    (img.replace("https://", "https://i3.wp.com/")))
            elif "http://" in img:
                repl_list.append(
                    (img.replace("http://", "https://i3.wp.com/")))
            elif "//" in img:
                repl_list.append((img.replace("//", "https://i3.wp.com/")))
        content = replace_string(content, repl_list)
        result.append((title, content))
    return result


def filter_dup(posts):
    posted = getpost(domain="wpjuicy.com")
    post_titles = [x['title']['rendered'] for x in posted]
    return [x for x in posts if x[0] not in post_titles]


def create_post(title, content):
    message = "wpbay:D48b bHGH WNMg HfeR mtiH mqDe"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    ep = "https://wpjuicy.com/wp-json/wp/v2/posts"
    headers = {'Authorization': 'Basic ' + base64_message}
    body = {
        'title': title,
        'status': 'publish',
        'content': content,
    }
    r = requests.post(ep, headers=headers, data=body)
    return r


def fetch():
    posts = getpost()
    processed = process_post(posts)
    filtered = filter_dup(processed)
    result = []
    for post in filtered:
        print(post[0])
        c = create_post(post[0], post[1])
        print(c)
        result.append(c)
    return result


if __name__ == "__main__":
    fetch()
