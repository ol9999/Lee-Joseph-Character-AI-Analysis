# Analysis

This directory contains the analysis notebooks for [_A Large-Scale Analysis of Public-Facing, Community-Built Chatbots on Character.AI_](https://arxiv.org/abs/2505.13354). The notebooks were run in order. Steps 1 and 2 depend on the scraped data described in the top-level README.

## Notebooks

### `01_data_processing.ipynb`
Converts the raw scraped data into analysis-ready formats.

- Parses `users.jsonl` into a flat CSV (`users_data.csv`) and a tab-separated following network (`net.csv`).
- Parses `characters_5per.jsonl` into a Parquet file with all character fields.
- Runs language detection on character greetings using the [`lingua`](https://github.com/pemistahl/lingua-py) library, filtering down to English-language greetings (`english_5per.parquet`).
- Post-processes named entity data produced by `02_code_run_on_ccr.ipynb`, cleaning and deduplicating entities and writing them to `ents.csv`.

**Key outputs:** `users_data.csv`, `net.csv`, `character_data_5per_all_col.parquet`, `english_5per.parquet`, `full_language_tagged_greetings.parquet`, `ents.csv`

---

### `02_code_run_on_ccr.ipynb`
GPU-accelerated preprocessing that was run on a high-performance computing cluster (CCR) using Apptainer/PyTorch containers.

- **NER masking:** Uses spaCy's `en_core_web_trf` transformer model to detect and replace PERSON entities in greetings with `[MASK]` tokens, and records the original entity strings. Output: `mask_result.parquet`.
- **Sentence embeddings:** Encodes the masked greetings using `sentence-transformers/all-mpnet-base-v2`. Output: `allmpv2_embeddings.npy`.
- **Power relationship extraction:** Uses spaCy dependency parsing to extract pronoun-based descriptions (e.g., "you are X", "he does Y") for pronouns `you`, `he`, `she`, `person`, `they`. Output: `power_result.parquet`.
- **Semantic similarity scoring:** Computes cosine similarities of extracted phrases against word lists for three semantic axes — power, evaluation, and gender — using the same sentence-transformer model.

**Requirements:** GPU, Apptainer with `nvcr.io/nvidia/pytorch:24.12-py3`, spaCy `en_core_web_trf`, `sentence-transformers`.

---

### `02_run_bertopic.ipynb`
Trains a [BERTopic](https://maartengptm.github.io/BERTopic/) topic model on the entity-masked character greetings.

- Loads `mask_result.parquet` and the pre-computed embeddings from `02_code_run_on_ccr.ipynb`.
- Filters greetings to those between 50–500 characters in length (~1.78M documents).
- Trains BERTopic with `all-mpnet-base-v2` embeddings, UMAP dimensionality reduction (8 components), and a minimum topic size of 250.
- Uses GPT-4o-mini via the OpenAI API to generate human-readable topic labels.
- Saves the fitted model, per-document topic assignments, and topic info.

**Key outputs:** `bert_allmpni_kj_5_8_25_diversity_250_min/` (saved model), `topic_labeled_char.parquet`, `topics_gen.csv`

---

### `03a_finalize_fandoms.ipynb`
Merges and finalizes fandom labels for character named entities.

- Combines fandom predictions from two LLMs (Claude and Gemini) that were run separately on extracted entity names.
- Maps entity names to their source fandom (e.g., a character name → the show/game/book it comes from).
- Merges with fandom type labels (e.g., Anime, Video Game, TV Show) and writes the final mapping.

**Key outputs:** `named_entities_to_fandom.csv`, `type_labeling2.csv`

---

### `03_final_analysis.ipynb`
R notebook that produces all tables and figures in the paper.

- Loads processed data from earlier steps (users, characters, language tags, topic assignments, fandom labels, power/gender similarity scores).
- Computes summary statistics on users and characters (follower/interaction distributions, concentration metrics).
- Analyzes language distribution across greetings by character count and total interactions.
- Generates all paper figures (saved to `img/`) and LaTeX tables.

**Requirements:** R with `data.table`, `arrow`, `ggplot2`, `ggrepel`, `scales`, `igraph`, `xtable`, `stringr`.

---

## Output File

### `final_topics.csv`
A CSV containing the finalized BERTopic topic labels used in the paper, produced from `02_run_bertopic.ipynb` after manual review.

---

## Pipeline Overview

```
users.jsonl / characters.jsonl
        │
        ▼
01_data_processing.ipynb
        │
        ├─► users_data.csv, net.csv
        ├─► character_data_5per_all_col.parquet
        └─► english_5per.parquet
                │
                ▼
        02_code_run_on_ccr.ipynb  (GPU server)
                │
                ├─► mask_result.parquet
                ├─► allmpv2_embeddings.npy
                └─► power_result.parquet
                        │
                        ├──────────────────────────────────────────┐
                        ▼                                          ▼
              02_run_bertopic.ipynb               01_data_processing.ipynb
                        │                         (post-NER step: ents.csv)
                        └─► topic_labeled_char.parquet             │
                                    │                              ▼
                                    │                  03a_finalize_fandoms.ipynb
                                    │                              │
                                    │                  named_entities_to_fandom.csv
                                    │                              │
                                    └──────────────────────────────┘
                                                    │
                                                    ▼
                                        03_final_analysis.ipynb  (R)
                                                    │
                                             paper figures/tables
```
