import requests
from bs4 import BeautifulSoup
import csv
import time

def get_repositories(username):
    repos = []
    page = 1
    headers = {'User-Agent': 'Mozilla/5.0'}

    while True:
        url = f"https://github.com/{username}?page={page}&tab=repositories"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        repo_list = soup.find_all('li', class_='public')
        if not repo_list:
            break

        for repo in repo_list:
            name_tag = repo.find('a', itemprop='name codeRepository')
            if not name_tag:
                continue
            repo_name = name_tag.text.strip()
            repo_url = "https://github.com" + name_tag['href']
            language_tag = repo.find('span', itemprop='programmingLanguage')
            language = language_tag.text.strip() if language_tag else "N/A"
            description_tag = repo.find('p', itemprop='description')
            description = description_tag.text.strip() if description_tag else "N/A"
            star_tag = repo.find('span', class_='Counter js-social-count')
            stars = star_tag.text.strip() if star_tag else "0"

            # Verifica se é um fork
            repo_response = requests.get(repo_url, headers=headers)
            repo_soup = BeautifulSoup(repo_response.text, 'html.parser')
            forked_from = "No"
            fork_span = repo_soup.select_one('span.text-small.lh-condensed-ultra.no-wrap.mt-1')
            if fork_span and "forked from" in fork_span.text:
                fork_link = fork_span.find('a')
                if fork_link:
                    forked_from = fork_link.get_text(strip=True)

            repos.append({
                'Repository Name': repo_name,
                'Description': description,
                'Language': language,
                'Stars': stars,
                'URL': repo_url,
                'Forked From': forked_from
            })
            time.sleep(2)

        page += 1
    return repos

def save_to_csv(repos, username):
    filename = f"{username}_repos.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=repos[0].keys())
        writer.writeheader()
        writer.writerows(repos)
    return filename

# Interface
print("Welcome to the GitHub Repository Scraper!")
github_username = input("Enter a GitHub username or organization: ").strip()
data = get_repositories(github_username)

if data:
    file_created = save_to_csv(data, github_username)
    print(f"✅ Data successfully saved to {file_created}")
else:
    print("⚠️ No repositories found or failed to retrieve data.")
