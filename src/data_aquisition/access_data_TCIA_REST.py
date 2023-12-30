import requests
import os

from src.utils.path_utils import get_path_from_root


def download_images(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image saved: {save_path}")
    else:
        print(f"Error downloading image: {response.status_code}")


def get_images(collection_name, num_images):
    base_url = "https://services.cancerimagingarchive.net/services/v3/TCIA/query"
    query_url = f"{base_url}/getSeries?Collection={collection_name}"

    response = requests.get(query_url)
    if response.status_code != 200:
        print(f"Error fetching collection: {response.status_code}")
        return

    series = response.json()[:num_images]
    for s in series:
        image_url = f"{base_url}/getImage?SeriesInstanceUID={s['SeriesInstanceUID']}"
        save_path = os.path.join(get_path_from_root("data", "raw", "trial_set"),
                                 f"{s['SeriesInstanceUID']}.dcm")
        download_images(image_url, save_path)


if __name__ == "__main__":
    get_images('CPTAC-PDA', 5)