# `arxivscraper` *(Coursework)*

Repository created as part of the "How can we capture data from the web?" assignment for the course *M2.851 - Typology and Data Life Cycle* in the Master's Degree in Data Science (UOC) program. In it, we where asked to identify and extract relevant data for an analytical project using web scraping techniques and tools. As a use case, we selected the preprint plataform **arXiv** to implement a web scraper aimed at extracting metadata and relevant information from selected scientific articles.

In this repository we present the source-code we developed for this endevour, collected into the [`arxivscraper`](https://github.com/clopezvice/PRACT_1.-Web-Scraping/tree/main/arxivscraper) library; alongside an example database (publised on [Zenodo](https://zenodo.org/)), a [project report]() and a [project video]().

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

#### CLI example use
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
---
### Output example
After running `arxivscraper`, the output is saved as a `.csv` file containing metadata for the collected preprints, here we pressent a snippet of said data
```csv
index,title,tags,authors,abstract
2505.24868,Consistent line clustering using geometric hypergraphs,"['math.ST', 'stat.ML']","['Kalle Alaluusua', 'Konstantin Avrachenkov', 'B. R. Vinay Kumar', 'Lasse Leskelä']","Traditional data analysis often represents data as a weighted graph with pairwise similarities, but many problems do not naturally fit this framework. In line clustering, points in a Euclidean space must be grouped so that each cluster is well approximated by a line segment. Since any two points define a line, pairwise similarities fail to capture the structure of the problem, necessitating the use of higher-order interactions modeled by geometric hypergraphs. We encode geometry into a 3-uniform hypergraph by treating sets of three points as hyperedges whenever they are approximately collinear. The resulting hypergraph contains information about the underlying line segments, which can then be extracted using community recovery algorithms. In contrast to classical hypergraph block models, latent geometric constraints in this construction introduce significant dependencies between hyperedges, which restricts the applicability of many standard theoretical tools. We aim to determine the fundamental limits of line clustering and evaluate hypergraph-based line clustering methods. To this end, we derive information-theoretic thresholds for exact and almost exact recovery for data generated from intersecting lines on a plane with additive Gaussian noise. We develop a polynomial-time spectral algorithm and show that it succeeds under noise conditions that match the information-theoretic bounds up to a polylogarithmic factor."
2505.24861,A localized consensus-based sampling algorithm,"['math.NA', 'math.OC']","['Arne Bouillon', 'Alexander Bodard', 'Panagiotis Patrinos', 'Dirk Nuyens', 'Giovanni Samaey']","We develop a novel interacting-particle method for sampling from non-Gaussian distributions. As a first step, we propose a new way to derive the consensus-based sampling (CBS) algorithm, starting from ensemble-preconditioned Langevin diffusions. We approximate the target potential by its Moreau envelope, such that the gradient in the Langevin equation can be replaced by a proximal operator. We then approximate the proximal operator by a weighted mean, and finally assume that the initial and target distributions are Gaussian, resulting in the CBS dynamics. If we keep only those approximations that can be justified in the non-Gaussian setting, the result is a new interacting-particle method for sampling, which we call localized consensus-based sampling. We prove that our algorithm is affine-invariant and exact for Gaussian distributions in the mean-field setting. Numerical tests illustrate that localized CBS compares favorably to alternative methods in terms of affine-invariance and performance on non-Gaussian distributions."
2505.24828,"Coherent structures in long range FPUT lattices, Part I: Solitary Waves","['math.AP', 'math.DS']","['J. Douglas Wright', 'Udoh Akpan']",We consider long range variants of Fermi-Pasta-Ulam-Tsingou lattice and in particular allow for particles to interact over arbitrarily long distances. We develop sufficient conditions which allow for the construction of solitary wave solutions.
2505.24821,Asymptotics for the harmonic descent chain and applications to critical beta-splitting trees,"['math.PR', 'math.CO']","['Anna Brandenberger', 'Byron Chin', 'Elchanan Mossel']","Motivated by the connection to a probabilistic model of phylogenetic trees introduced by Aldous, we study the recursive sequence governed by the rule $x_n = \sum_{i=1}^{n-1} \frac{1}{h_{n-1}(n-i)} x_i$ where $h_{n-1} = \sum_{j=1}^{n-1} 1/j$, known as the harmonic descent chain. While it is known that this sequence converges to an explicit limit $x$, not much is known about the rate of convergence. We first show that a class of recursive sequences including the above are decreasing and use this to bound the rate of convergence. Moreover, for the harmonic descent chain we prove the asymptotic $x_n - x = n^{-γ_* + o(1)}$ for an implicit exponent $γ_*$. As a consequence, we deduce central limit theorems for various statistics of the critical beta-splitting random tree. This answers a number of questions of Aldous, Janson, and Pittel."
2505.24815,Convex Approximations of Random Constrained Markov Decision Processes,"['math.OC', 'eess.SY']","['V Varagapriya', 'Vikas Vikram Singh', 'Abdel Lisser']","Constrained Markov decision processes (CMDPs) are used as a decision-making framework to study the long-run performance of a stochastic system. It is well-known that a stationary optimal policy of a CMDP problem under discounted cost criterion can be obtained by solving a linear programming problem when running costs and transition probabilities are exactly known. In this paper, we consider a discounted cost CMDP problem where the running costs and transition probabilities are defined using random variables. Consequently, both the objective function and constraints become random. We use chance constraints to model these uncertainties and formulate the uncertain CMDP problem as a joint chance-constrained Markov decision process (JCCMDP). Under random running costs, we assume that the dependency among random constraint vectors is driven by a Gumbel-Hougaard copula. Using standard probability inequalities, we construct convex upper bound approximations of the JCCMDP problem under certain conditions on random running costs. In addition, we propose a linear programming problem whose optimal value gives a lower bound to the optimal value of the JCCMDP problem. When both running costs and transition probabilities are random, we define the latter variables as a sum of their means and random perturbations. Under mild conditions on the random perturbations and random running costs, we construct convex upper and lower bound approximations of the JCCMDP problem. We analyse the quality of the derived bounds through numerical experiments on a queueing control problem for random running costs. For the case when both running costs and transition probabilities are random, we choose randomly generated Markov decision problems called Garnets for numerical experiments."
```
> ℹ️ **Note:** Only the first 5 entries are shown here for brevity. The full dataset is available on [Zenodo](https://zenodo.org/).

---
### ⚠️ Usage Notes

Some **arXiv** categories are exceptionally prolific. To avoid overwhelming the server and to ensure smooth operation, the script introduces a polite 15-second delay for every 200 results retrieved.  

We recommend:
- Focusing the search on short time periods (even a single day).
- Performing a preliminary search on the **arXiv** website to estimate the number of results your query might return.



[![CanoJones](https://img.shields.io/badge/author-CanoJones-blue?logo=github&logoColor=white)](https://github.com/Cano-Jones)
[![clopezvice](https://img.shields.io/badge/author-clopezvice-orange?logo=github&logoColor=white)](https://github.com/clopezvice)



[![CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by-nc-nd/4.0/)


