from pathlib import Path
import httpx



def load_urls(file_path: Path) -> list[str]:
    urls = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            url = line.strip()

            if url:
                urls.append(url)

    return urls


def inspect_url(url: str) -> bool:
    with httpx.Client(timeout=10.0, follow_redirects=True) as client:

        try:   

            response = client.get(url)

            

            print(f"Status: {response.status_code}")
            print(f"Successful: {response.is_success}")
            print(f"Body: {response.text[:400]}")

            return response.is_success
            
        except httpx.TimeoutException as error: 
            print(f"Timeout: {url} — {error}")
            return False

        except httpx.RequestError as error:
            print(f"Request failed: {url} — {error}")
            return False


def main() -> None:

    urls = load_urls(Path("urls.txt"))
    print(len(urls))

    print("First URL:", inspect_url(urls[0]))
    print("Last URL:", inspect_url(urls[-1]))
    print("Connection test:", inspect_url("http://127.0.0.1:1"))
    print("Program continued")

if __name__ == "__main__":
    main()