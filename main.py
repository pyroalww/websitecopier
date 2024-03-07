import requests
import os
import shutil
import logging
from urllib.parse import urlparse, urljoin, urlsplit
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def download_website(url, output_dir=None, user_agent=None, timeout=10, max_retries=3, retry_backoff_factor=1, verify_ssl=True, proxy=None, max_depth=3, allowed_content_types=None, cookies=None, custom_headers=None, max_concurrent_downloads=5):
    try:
        # Parse URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL. Please provide a valid URL including scheme and domain.")

        # Set output directory
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

        # Set user agent
        headers = {'User-Agent': user_agent} if user_agent else {}

        # Create a session with retry mechanism
        session = requests.Session()
        retries = Retry(total=max_retries, backoff_factor=retry_backoff_factor)
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # Set custom headers
        if custom_headers:
            headers.update(custom_headers)

        # Set cookies
        if cookies:
            session.cookies.update(cookies)

        # Download website
        visited_urls = set()
        with ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
            download_url(url, session, headers, output_dir, visited_urls, verify_ssl, proxy, max_depth, allowed_content_types, executor)
        logging.info("Website download completed successfully.")
        print("Website download completed successfully.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print("Error:", e)

def download_url(url, session, headers, output_dir, visited_urls, verify_ssl, proxy, max_depth, allowed_content_types, executor):
    if url in visited_urls:
        return

    visited_urls.add(url)

    # Parse URL
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path) or 'index.html'
    output_path = os.path.join(output_dir, filename)

    # Download website
    with session.get(url, headers=headers, stream=True, timeout=timeout, verify=verify_ssl, proxies=proxy, allow_redirects=False) as response:
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').split(';')[0]
            if not allowed_content_types or content_type in allowed_content_types:
                # Save HTML content
                with open(output_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)


                if content_type == 'text/html':
                    if max_depth > 0:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        for link in soup.find_all('a', href=True):
                            next_url = urljoin(url, link['href'])
                            executor.submit(download_url, next_url, session, headers, output_dir, visited_urls, verify_ssl, proxy, max_depth - 1, allowed_content_types, executor)

                # Download embedded resources
                executor.submit(download_embedded_resources, response.content, parsed_url, output_dir, session, headers, verify_ssl, proxy)

        elif response.status_code == 301 or response.status_code == 302:

            location = response.headers.get('location')
            if location:
                next_url = urljoin(url, location)
                executor.submit(download_url, next_url, session, headers, output_dir, visited_urls, verify_ssl, proxy, max_depth, allowed_content_types, executor)
        else:
            logging.error(f"Failed to download: {url}. Status code: {response.status_code}")
            print(f"Failed to download: {url}. Status code:", response.status_code)

def download_embedded_resources(html_content, base_url, output_dir, session, headers, verify_ssl, proxy):
    soup = BeautifulSoup(html_content, 'html.parser')
    resources = []
    for tag in soup.find_all(['img', 'link', 'script']):
        if tag.name == 'img' and tag.get('src'):
            url = urljoin(base_url.geturl(), tag['src'])
            filename = os.path.basename(urlsplit(url).path)
        elif tag.name == 'link' and tag.get('href'):
            url = urljoin(base_url.geturl(), tag['href'])
            filename = os.path.basename(urlsplit(url).path)
        elif tag.name == 'script' and tag.get('src'):
            url = urljoin(base_url.geturl(), tag['src'])
            filename = os.path.basename(urlsplit(url).path)
        else:
            continue
        output_path = os.path.join(output_dir, filename)
        resources.append((url, output_path))

    with ThreadPoolExecutor() as executor:
        futures = []
        for url, output_path in resources:
            futures.append(executor.submit(download_resource, url, output_path, session, headers, verify_ssl, proxy))
        
        for future in tqdm(futures, total=len(resources), desc="Downloading Resources", unit="resource"):
            future.result()

def download_resource(url, output_path, session, headers, verify_ssl, proxy):
    try:
        with session.get(url, headers=headers, stream=True, timeout=10, verify=verify_ssl, proxies=proxy) as response:
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
            else:
                logging.error(f"Failed to download resource: {url}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error occurred while downloading resource {url}: {e}")

# Config
url = "https://example.com"
output_dir = "downloaded_websites"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
timeout = 10 
max_retries = 3
retry_backoff_factor = 1
verify_ssl = True
proxy = {'http': 'http://user:password@proxy.example.com:8080', 'https': 'https://user:password@proxy.example.com:8080'}
max_depth = 3
allowed_content_types = {'text/html', 'text/css', 'image/jpeg', 'image/png', 'image/gif'}
cookies = {'session': 'abcdef123456'}
custom_headers = {'Accept-Language': 'en-US,en;q=0.5'}
max_concurrent_downloads = 5
download_website(url, output_dir, user_agent, timeout, max_retries, retry_backoff_factor, verify_ssl, proxy, max_depth, allowed_content_types, cookies, custom_headers, max_concurrent_downloads)
