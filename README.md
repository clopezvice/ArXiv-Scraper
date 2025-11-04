# `arxivscraper` *(Coursework)*

Repository created as part of the "How can we capture data from the web?" assignment for the course *M2.851 - Typology and Data Life Cycle* in the Master's Degree in Data Science (UOC) program. In it, we where asked to identify and extract relevant data for an analytical project using web scraping techniques and tools. As a use case, we selected the preprint plataform **arXiv** to implement a web scraper aimed at extracting metadata and relevant information from selected scientific articles.

In this repository we present the source-code we developed for this endevour, collected into the [`arxivscraper`]() library; alongside an example database (publised on [Zenodo](https://zenodo.org/)), a [project report]() and a [project video]().

## `arxivscraper` library
The centerpiece of this repo, the `arxivscraper` python module allows the user to gather the principal data of all preprints of a given topic published between two given dates. This data, published as a `.csv`, includes:
```
//data-point extract
{
  'index': '2510.23607',
  'title': 'Concerto: Joint 2D-3D Self-Supervised Learning Emerges Spatial Representations',
  'tags': ['cs.CV'],
  'authors: ['Yujia Zhang', 'Xiaoyang Wu', 'Yixing Lao', 'Chengyao Wang', 'Zhuotao Tian', 'Naiyan Wang', 'Hengshuang Zhao'],
  'abstract': 'Humans learn abstract concepts through multisensory synergy, and once formed, such representations can often be recalled from a single modality. Inspired by this principle, we introduce Concerto, a minimalist simulation of human concept learning for spatial cognition, combining 3D intra-modal self-distillation with 2D-3D cross-modal joint embedding. Despite its simplicity, Concerto learns more coherent and informative spatial features, as demonstrated by zero-shot visualizations. It outperforms both standalone SOTA 2D and 3D self-supervised models by 14.2% and 4.8%, respectively, as well as their feature concatenation, in linear probing for 3D scene perception. With full fine-tuning, Concerto sets new SOTA results across multiple scene understanding benchmarks (e.g., 80.7% mIoU on ScanNet). We further present a variant of Concerto tailored for video-lifted point cloud spatial understanding, and a translator that linearly projects Concerto representations into CLIP's language space, enabling open-world perception. These results highlight that Concerto emerges spatial representations with superior fine-grained geometric and semantic consistency.'
}
```
The collected articles are gathered from the advance search provided by the **arXiv** platform itself. The dates employed are taken to be the "Announcement date" for consistency and by default cross-listed papers are excluded (meaning that only the primary tag is consulted) unless the `--cross_list` flag is added to the incantation (see example use below). Only primary classifications are accepted for the search as this is what the advance search option allows (one can search for "astro-ph" but not "astro-ph.GA" for example). Three parameters are needed to be input by the user using the following flags: `--start_date` (`YYYY-mm-dd` format), `--end_date` (`YYYY-mm-dd` format) and `--category` (**arXiv**-compatible classification acronym). Two optional flags can be added: `--output` (file path for the resulting `.csv`) and `--cross_list`.

- CLI example use
```bash
$ python3 arxivscraper/arxivscraper.py \
  --start_date "2025-02-01" \
  --end_date "2025-05-01" \
  --category "nlin" \
  --output "Data/arxiv_data.csv" \
  --cross_list

```

Import use is also allowed, using the `arxivscraper` as a module, with `from arxivscraper.arxivscraper import main` which accepts dict-type object or args.parse as arguments with the same formats as the flags previously presented.

#### Installation instructions
```bash
git clone https://github.com/<user>/arxivscraper.git
cd arxivscraper
pip install -r requirements.txt

```




[![CanoJones](https://img.shields.io/badge/author-CanoJones-blue?logo=github&logoColor=white)](https://github.com/Cano-Jones)
[![clopezvice](https://img.shields.io/badge/author-clopezvice-orange?logo=github&logoColor=white)](https://github.com/clopezvice)



[![CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by-nc-nd/4.0/)


