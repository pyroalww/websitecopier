
# Website Downloader

This Python script allows you to download a website and its embedded resources.

## Usage

### Installation

Clone the repository or download the `website_downloader.py` file.

### Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Dependencies

- `requests`
- `bs4` (Beautiful Soup)
- `tqdm`

Install dependencies using pip:

```bash
pip install requests beautifulsoup4 tqdm
```

### Running the Script

```python
python website_downloader.py
```

### Parameters

- `url`: The URL of the website to download.
- `output_dir`: The directory where the downloaded website will be saved.
- `user_agent`: User agent string to be used in the HTTP requests.
- `timeout`: Timeout for the HTTP requests in seconds.
- `max_retries`: Maximum number of retries for failed requests.
- `retry_backoff_factor`: Backoff factor for retrying failed requests.
- `verify_ssl`: Whether to verify SSL certificates.
- `proxy`: Proxy server settings (optional).
- `max_depth`: Maximum depth for recursive downloading of linked pages.
- `allowed_content_types`: Set of allowed content types to download.
- `cookies`: Dictionary of cookies to be sent with the requests.
- `custom_headers`: Custom headers to be sent with the requests.
- `max_concurrent_downloads`: Maximum number of concurrent downloads.

## Example

```python
url = "https://example.com"
output_dir = "downloaded_website"
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
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
