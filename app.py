import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

st.set_page_config(page_title="GitMiner", layout="centered")
st.markdown("<h1 style='text-align: center;'>🔎 GitMiner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Scrape GitHub profiles and export beautiful CSV/Excel files</p>", unsafe_allow_html=True)

username = st.text_input("🧑‍💻 Enter GitHub username or organization name", placeholder="e.g., torvalds")


@st.cache_data
def scrape_github_repos(user):
    base_url = f"https://github.com/{user}?tab=repositories"
    repos_data = []
    page = 1

    while True:
        url = f"{base_url}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        repo_list = soup.find_all('li', {'itemprop': 'owns'})

        if not repo_list:
            break

        for repo in repo_list:
            name_tag = repo.find('a', itemprop="name codeRepository")
            repo_name = name_tag.text.strip() if name_tag else "N/A"
            repo_url = f"https://github.com{name_tag['href']}" if name_tag else "N/A"
            description = repo.find('p', itemprop='description')
            description = description.text.strip() if description else "N/A"
            language = repo.find('span', itemprop='programmingLanguage')
            language = language.text.strip() if language else "N/A"
            stars_tag = repo.find('a', class_='Link--muted')
            stars = stars_tag.text.strip().replace(',', '') if stars_tag else "0"
            stars = int(stars) if stars.isdigit() else 0
            license_tag = repo.find('span', class_='mr-3')
            license_text = license_tag.text.strip() if license_tag else "N/A"

            # CORREÇÃO DO FORKED
            fork_span = repo.find('span', class_='text-small lh-condensed-ultra no-wrap mt-1')
            if fork_span and 'forked from' in fork_span.text.lower():
                fork_link = fork_span.find('a')
                forked = f"Yes (from {fork_link.text.strip()})" if fork_link else "Yes"
            else:
                forked = "No"

            repos_data.append({
                "Repository": repo_name,
                "Description": description,
                "Language": language,
                "Stars": stars,
                "License": license_text,
                "Forked": forked,
                "URL": repo_url
            })

        page += 1
        time.sleep(1.5)  # Delay para evitar bloqueios

    return pd.DataFrame(repos_data)


if username:
    with st.spinner("🔄 Scraping data from GitHub..."):
        df = scrape_github_repos(username)

    if not df.empty:
        st.success(f"✅ {len(df)} repositories found for '{username}'!")
        st.dataframe(df.style.set_properties(**{
            'text-align': 'left',
            'white-space': 'pre-wrap'
        }), use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, f"{username}_repos.csv", "text/csv")

        xlsx_file = f"{username}_repos.xlsx"
        df.to_excel(xlsx_file, index=False)
        with open(xlsx_file, "rb") as f:
            st.download_button("📗 Download XLSX", f, file_name=xlsx_file, mime="application/vnd.ms-excel")
    else:
        st.warning("⚠️ No repositories found. Please check the username.")
else:
    st.info("👈 Enter a GitHub username to begin.")
