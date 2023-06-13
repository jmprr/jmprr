import os
import requests
from bs4 import BeautifulSoup

google_image = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"

user_agent = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


saved_folder = '/Code/Test/Auto-download/images'


def main(result):
    if not os.path.exists(saved_folder):
        os.mkdir(saved_folder)
    download_images(result)
    
def download_images(result):
    data = result
    n_images = int(input('How many images do you want? '))

    print('searching...')

    search_url = os.path.join(google_image + 'q=' + data)

    response = requests.get(search_url, headers=user_agent)

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    count = 1
    links = []
    for result in results:
        try:
            link = result['data-src']
            links.append(link)
            count += 1
            if(count > n_images):
                break

        except KeyError:
            continue

    print(f"Downloading {len(links)} images...")
    print(html)

    for i, link in enumerate(links):
        response = requests.get(link)

        image_name = saved_folder + '/' + data + str(i+1) + '.jpg'

        with open(image_name, 'wb') as fh:
            fh.write(response.content)
            
if __name__ == "__main__":
    main()
    

