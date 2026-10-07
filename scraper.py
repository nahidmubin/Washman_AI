import requests
from bs4 import BeautifulSoup

WEB_DATA_PATH = "./data/walton_website_data.txt"

def get_wm_data(url):

    response = requests.get(url)
    if response.status_code == 200:
        model_data = ""
        soup = BeautifulSoup(response.text, "html.parser")

        model_name = soup.title.string.strip()
        wm_type = soup.find_all("li", class_="breadcrumb-item")[2].get_text(strip=True)
        price = soup.find("span", class_="final_price").get_text(strip=True)

        model_data += f"\nWashing Machine Model: {model_name},\nType: {wm_type},\nPrice: {price} Taka\n"

        tabs = soup.find_all("div", class_="tab-pane dc-extra-product-tab")

        for tab in tabs:
            tab_data = tab.get_text(strip=True, separator=", ")
            if tab_data and not tab_data.startswith("Download"):
                model_data += f"{tab_data}\n"

        return model_data

    else:
        print("Failed to retrieve page. Status code:", response.status_code)


def get_single_type_wm_data(url):

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select("div.single-prodcut h6 a")
        category_data = []
        for a in links:
            data = get_wm_data(a.get("href"))
            category_data.append(data)

        return category_data
    
    else:
        print("Failed to retrieve page. Status code:", response.status_code)


def get_all_wm_data(path_to_save):
    urls = [
        "https://waltonbd.com/washing-machine/automatic-top-load?limit=100",
        "https://waltonbd.com/washing-machine/automatic-front-load?limit=100",
        "https://waltonbd.com/washing-machine/semi-automatic?limit=100"
    ]

    all_models_data = []
    for url in urls:
        data = get_single_type_wm_data(url)
        all_models_data.extend(data)

    with open(path_to_save, "w", encoding='utf-8') as f:
        f.write("\n".join(all_models_data))

if __name__ == '__main__':

   chunks = get_all_wm_data(WEB_DATA_PATH)
   print(chunks)