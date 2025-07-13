# 📄 get-papers-list-VigR

A Python CLI tool to fetch PubMed research papers and filter them to include only those with **at least one author affiliated with a biotech or pharmaceutical company**. Export the results to CSV for further analysis.

---

## 🚀 Features

- 🔍 Supports full [PubMed query syntax](https://pubmed.ncbi.nlm.nih.gov/advanced/)
- 🏢 Filters papers with **non-academic** authors based on affiliation
- 📧 Extracts corresponding author email (when available)
- 📄 Outputs structured results to CSV
- ⚙️ Installable CLI via Poetry or pip
- ✅ Unit tested and published on [TestPyPI](https://test.pypi.org/project/get-papers-list-Vignesh_R/)

---

## 📦 Installation (from TestPyPI)

```bash
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  get-papers-list-VigR
```

### Example Usage:
```bash
get-papers-list "CRISPR AND 2023[dp]" --file crispr.csv
```

## Development Setup
```bash
# Clone the repo and install dependencies with Poetry
git clone https://github.com/Vigneshviku09/get-papers-list.git
cd get-papers-list
poetry install
# Run the CLI locally
poetry run get-papers-list "cancer AND 2022[dp]" --file output.csv
```