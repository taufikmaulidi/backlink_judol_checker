import requests
from bs4 import BeautifulSoup
import re
import argparse
from rich.console import Console
from rich.table import Table

console = Console()

def get_backlinks(domain):
    url = f"https://www.google.com/search?q=site:{domain}&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "http" in href:
            links.append(href.split("&")[0].replace("/url?q=", ""))
    return links

def is_gambling_site(url):
    gambling_keywords = ["judi", "casino", "poker", "slot", "bet", "sportsbook", "togel", "sbobet", "agenjudi"]
    for keyword in gambling_keywords:
        if keyword in url.lower():
            return True
    return False

def check_gambling_backlinks(domain):
    backlinks = get_backlinks(domain)
    gambling_backlinks = [link for link in backlinks if is_gambling_site(link)]
    return gambling_backlinks

def main():
    parser = argparse.ArgumentParser(description="Scanner Backlink Judi Online")
    parser.add_argument("domain", help="Domain yang ingin diperiksa")
    args = parser.parse_args()

    domain = args.domain
    console.print(f"[bold blue]Memeriksa backlink untuk domain:[/bold blue] {domain}")

    gambling_backlinks = check_gambling_backlinks(domain)

    if gambling_backlinks:
        console.print("[bold red]Ditemukan backlink ke situs judi online:[/bold red]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("No", style="dim")
        table.add_column("URL Backlink", style="cyan")

        for idx, link in enumerate(gambling_backlinks, start=1):
            table.add_row(str(idx), link)
        
        console.print(table)
    else:
        console.print("[bold green]Tidak ditemukan backlink ke situs judi online.[/bold green]")

if __name__ == "__main__":
    main()
