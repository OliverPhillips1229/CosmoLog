import requests

NASA_IMAGES_API = "https://images-api.nasa.gov/search"

def get_mars_images(count=4):
    params = {"q": "mars", "media_type": "image"}
    r = requests.get(NASA_IMAGES_API, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    items = data.get("collection", {}).get("items", [])
    images = []
    for item in items:
        links = item.get("links", [])
        if links:
            img_url = links[0].get("href")
            title = item.get("data", [{}])[0].get("title", "Mars Image")
            description = item.get("data", [{}])[0].get("description", "")
            images.append({
                "img_src": img_url,
                "title": title,
                "description": description
            })
        if len(images) >= count:
            break
    return images
