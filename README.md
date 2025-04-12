# 🔎 GitMiner – GitHub Profile Repository Scraper

**GitMiner** is a modern Python-based web scraper that extracts comprehensive public repository data from any GitHub user or organization. It’s a practical tool designed for developers, recruiters, analysts, and data scientists to analyze GitHub profiles with ease and speed.

---

## 📌 Features

- ✅ Command-line input for GitHub username or organization  
- ✅ Pagination handling for unlimited repositories  
- ✅ Fork detection and source attribution  
- ✅ Extracts:
  - Repository name  
  - Description  
  - Programming language  
  - Star count  
  - License  
  - Forked status and source (if applicable)  
  - Repository URL  
- ✅ Output in well-formatted CSV (centralized, with bold headers)  
- ✅ Respectful scraping (auto delay to avoid rate limits)

---

## 📂 Example Output

The generated CSV file includes:

| Repository | Description | Language | Stars | License | Forked | URL |
|------------|-------------|----------|--------|---------|--------|-----|
| `hydra-themes` | Custom Hydra Launcher Themes | CSS | 1 | MIT | Yes (from `hydralauncher/hydra-themes`) | [Link](https://github.com/AlmightyMatheus/hydra-themes) |

---

## ⚙️ Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

### `requirements.txt` content:

```
beautifulsoup4==4.13.3  
certifi==2025.1.31  
charset-normalizer==3.4.1  
idna==3.10  
lxml==5.3.1  
requests==2.32.3  
soupsieve==2.6  
typing_extensions==4.13.1  
urllib3==2.3.0
```

---

## 🚀 How to Use

```bash
python github_scraper.py
```

The script will ask you to enter the GitHub username or organization handle. It then generates a CSV file with all repository data.

---

## 📌 License

MIT License

---

## 🙋 About the Developer

Built by [AlmightyMatheus](https://github.com/AlmightyMatheus) – Python developer focused on automation, data scraping, and real-world utility tools.
