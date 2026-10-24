# Blog 6 — Linking Generations in PSID: A SQL Guide to Family Income Persistence

A reproducible Python and SQLite tutorial using **only the seven official PSID archives supplied for this project**. Part I constructs a parent–child family income table in SQL with actual query previews. Part II estimates intergenerational family-income elasticity (IGE) using **log–log OLS**, compares income measures and visualizes dispersion. This is not logistic regression.

## Preview and website installation

### Replacing an older post6 safely

Rename the existing `blog/posts/post6/` folder to `blog/posts/_post6_backup/`, then put the new ZIP's `post6/` folder in its place. Do not only overlay new files: an old `code/article_body.md` left behind can still be discovered by Quarto. The underscore backup preserves your old files while excluding them from normal render discovery.

The editable template is now `code/_article_body.md`, and the Chinese companion is `_Chinese_guide.md`. Quarto excludes underscore-prefixed inputs by default. There is no external `include-in-header: code/article_style.html` in the article YAML; the generated QMD already contains its CSS. Layout uses `body-classes: blog6-report`, scoped to `main.content`, instead of an outer fenced Div. This removes the fragile `:::` wrapper without changing the website's theme or navigation width.

From the **website root**, preview only the actual post:

```bash
quarto preview blog/posts/post6/index.qmd --to html --no-watch-inputs --no-browse
```

The log's separate warning about a `theme` in `post1/index.qmd` is not the post6 fatal error. To silence it while retaining your current site theme, remove the document-level `theme` entry from post1. If changing the entire website theme, configure it under the existing root `_quarto.yml` → `format` → `html` → `theme`. Do not replace your root configuration with the post folder's contents.

Open `index.html` first. All three 300-dpi figures are embedded in **both QMD and HTML**. The builder inserts PNG bytes as data URLs, so article images require no relative-path requests. Linked code, documentation and the listing thumbnail still require the project folder. Equations use MathML.

Part I keeps tutorial code visible. Part II puts its four Python blocks in native, keyboard-accessible **Show / hide Python code** panels, closed by default. Readers can inspect the code without hiding the results, tables or explanations. No JavaScript or notebook engine is required for the toggles.

The shorter edition trims repeated prose and the published file tree. Supporting Tables 3, 5 and 6 are now in closed, reader-expandable panels; their calculations, source links and numbered targets remain available. The four-model definitions, percentage interpretation, eight-specification table, all three figures, core SQL tutorial, Takeaway and source notes remain in the reading flow. This changes presentation only.

Figure 1 now labels models A–D, with exact father/child family income years in Table 1. Table 2 converts each unrounded coefficient using `100 * (1.10**beta - 1)`: 10% is an illustrative father-family-income comparison, not observed income growth. Tables 3–6 display age-window contrasts, the eight specifications, dispersion calculations and influence ranges. Each table and figure links its result CSV. Footnotes are short explanatory notes; technical specifications remain here.

The headline estimates and father/child decomposition now form one section, **Whose family income is averaged matters**. Table 4 adds an explicit child-averaging change column: −0.091 and −0.105 in early adulthood, versus +0.004 and −0.019 in midlife, with the father measure held fixed within each row. The single **Takeaway** summarizes SQL construction, the sample, main results, uncertainty and a short outlook. There is no separate Summary section. These are descriptive changes in estimated IGE, not established causal age effects.

Copy the **whole project folder** to `blog/posts/post6/` in your Quarto website. From the website root, run:

```bash
quarto render
```

The QMD declares its listing thumbnail with `image: result/figures/figure1_ige_windows.png` and includes figure resources. Responsive CSS sets content-width images and automatic height. Embedded HTML does not remove the website listing's need for its PNG thumbnail. There is no post-level `_quarto.yml` overriding the site configuration. Code examples are static and do not execute during rendering.

## Official sources and file relationships

- [Official PSID Packaged Data](https://simba.isr.umich.edu/Zips/ZipMain.aspx): choose the 1968–2023 cross-year Individual File and the six ordinary Family Files below.
- [Official documentation catalogue](https://psidonline.isr.umich.edu/Guide/documents.aspx).
- [Individual-file codebook](https://psidonline.isr.umich.edu/documents/psid/codebook/IND2023ER_codebook.pdf).

| Archive | Rows | Use |
|---|---:|---|
| `ind2023er.zip` | 85,536 | Stable person IDs, father pointers, birth years, annual family membership |
| `fam1999er.zip` | 6,997 | 1998 family income |
| `fam2001er.zip` | 7,406 | 2000 family income |
| `fam2003er.zip` | 7,822 | 2002 family income |
| `fam2015er.zip` | 9,048 | 2014 family income |
| `fam2017er.zip` | 9,607 | 2016 family income |
| `fam2019er.zip` | 9,569 | 2018 family income |

The user downloaded these archives from PSID and supplied them. Python parses the local official files; it does not claim a new scripted authenticated download. No third-party archive, synthetic microdata, wealth supplement or external CPI is used. Supplied family releases are 9, 7, 9, 2, 3 and 1, in that order; the individual file is release 2.

The parser extracts 52 original individual columns and three columns from each Family File, preserving names and values in `data/selected/`. It checks ZIP CRCs, source row counts against SAS dictionary headers, labels and fixed-width positions. `data/source_manifest.json` records archive and selected-file SHA-256 hashes. Full original ZIPs are supplied separately and are not duplicated in this bundle.

## Rebuild

Use Python **3.11 or later**. NumPy, pandas and Matplotlib are dependencies; SQLite and ZIP parsing use the standard library. Pillow, installed with Matplotlib, inspects figures. No R, SQL server or network is needed to rebuild from included selected columns.

```bash
python -m pip install -r requirements.txt
python code/run_all.py
python code/render_preview.py
python code/check_html.py
```

`requirements-lock.txt` records the three analysis package versions used. `run_all.py` verifies selected-file hashes, then runs:

The optional `render_preview.py` requires the Pandoc executable on your PATH; Python package installation does not install it. Alternatively, render `index.qmd` with your installed Quarto. Analysis and figure generation do not depend on either renderer.

1. `02_sql_audit.py`: loads original columns into SQLite; generates and runs preparation SQL; executes `02_match.sql`; saves audits, tables and database.
2. `03_validate_estimate.py`: independently rebuilds eligibility and six log-income measures with pandas; estimates the four main IGEs and intervals.
3. `05_further_analysis.py`: estimates eight measure combinations, paired contrasts, leave-one-father influence ranges and within-person dispersion.
4. `06_make_figures.py`: produces three 300-dpi PNGs.
5. `build_article.py`: inserts actual SQL statements, computed previews and six numbered results tables into the editable `code/_article_body.md` template. It also saves `income_interpretation.csv` and `dispersion_summary.csv` from existing verified results; it does not change the sample or the estimates.
6. `check_article.py`: executes all displayed analysis blocks from source-column CSVs and compares the entire matched table and eight slopes to production.

To repeat extraction, place all seven original archives in `data/raw/`, then run:

```bash
python code/01_extract_official.py
python code/run_all.py
python code/check_article.py --archives-dir data/raw
```

Alternatively, supply `01_extract_official.py --archives-dir /your/archive/folder`. The optional archive argument to `check_article.py` executes the article's fixed-width parsing example against the original 2001 ZIP and compares all 7,406 rows. Without it, that source example is compiled; the remaining tutorial executes fully. The delivered validation was also run with the supplied original archive.

Paths derive from each script's project location. For permanent prose changes, edit `code/_article_body.md` and run `build_article.py`. A full rebuild overwrites generated QMD and outputs. `01_prepare.sql` is generated from the field map: change normalization in `02_sql_audit.py`, rather than editing generated SQL temporarily.

## Keys, dates and measurement

- Stable person key: `ER30001*1000 + ER30002`. Father pointer uses `ER32016/ER32017`, with valid person numbers 1–399. Parenthood is not inferred from co-residence.
- `persons`: unique person; `roster`: unique person/survey-year; `family_income`: unique survey-year/annual family ID. Annual income joins require both year and family number.
- Each survey file supplies preceding-calendar-year income. Children born 1972–1976; fathers 45–60 in income year 2000; birth-year gap 15–55. Birth year is the latest valid individual report, without imputation.
- Require responding sequence 1–20 and reference-person/spouse/partner relationship 10/20/22. Father and child must have different family economic units in every early wave. Different units do not establish different physical addresses.
- Require three valid positive incomes in each of three windows: father early, child early, child midlife. All regressions use the same 187 children and 163 fathers: 109 daughters and 78 sons. This is 3.8% of the starting 4,925-child cohort.
- Single-year measures: father 2000; child 2000 or 2016. Central child ages are 24–28 and 40–44; full windows span 22–30 and 38–46. Father's full window spans 43–62: age 45–60 is required at its center.
- Multi-year measure is **mean natural log income**, equal to log geometric-mean levels, not log arithmetic-mean income. Equal coverage at common dates means annual common deflation subtracts a window constant and leaves an OLS slope with intercept unchanged. Nominal dollar purchasing power across windows is not comparable on this basis.
- Retain valid positive $1 observations. Flag the early fields' $9,999,999 top code; later fields have documented positive upper bound $9,999,997. No top codes or unexpected upper codes occur in the supplied files. Keep nonpositive values in raw data; exclude them only from logs. Source imputation and component censoring remain.

## Results

| Child stage | Both single-year | Father’s family averaged only | Child’s family averaged only | Both averaged |
|---|---:|---:|---:|---:|
| Early career | 0.285 | 0.407 | 0.194 | 0.302 |
| Midlife | 0.311 | 0.508 | 0.315 | 0.489 |

Unweighted OLS has an intercept and no other controls. The bootstrap samples 163 fathers, retaining siblings: 1,000 draws, seed 20261023. All eight specifications and paired differences use identical resamples. Added contrasts are exploratory, without multiplicity adjustment.

The averaged midlife-minus-early difference is 0.187, with paired 95% interval **[−0.008, 0.383]**. Its direction fits lifecycle concerns, but the age-window difference is not significant at 5%. Period changes, family composition and selection also affect interpretation. Neither window observes lifetime income.

Averaging fathers' family income raises the slope; averaging child family income does not consistently do so. A separate, explicitly named check asks whether one year's income is a stable snapshot of family resources. For the same 187 children, subtract the sample mean log income in each year, then calculate each person's sample standard deviation across the three observations in each life stage. This measures fluctuations relative to the group's yearly average, not percentile ranks or stability for all middle-aged Americans. The median falls from 0.307 to 0.147 (52%); 129 children (69%) have smaller midlife fluctuations. Real family-resource changes remain in this measure, so it does not establish validity as a lifetime-income proxy. The heading, Figure 3, Table 5 and Takeaway use this interpretation without an ordinal reference. Leaving out each father cluster preserves the averaged IGE ordering, but is not a significance test.

## Validation and rendering status

- Seven ZIP CRCs and source row counts passed; source-column hashes are checked on rebuild.
- Annual responding-person/family joins have zero unmatched IDs in all six waves; unique keys and SQLite integrity passed.
- Independent pandas reconstruction matches the 187-child sample and all six log-income measures.
- Tutorial execution covers five Python analysis blocks and nine SQL blocks. The complete **187 × 21** table, eight slopes, main bootstrap intervals, percentage conversions and dispersion summaries match production. The original extraction example also matched all 7,406 original 2001 records.
- Three charts were visually inspected and saved at 300 dpi. Checks verify that all three QMD image data URLs exactly match the PNG bytes, the HTML embeds the images, and there is one Takeaway with no separate Summary. They also check nine footnotes, fragment targets, local links, equations and responsive CSS. They also verify that all four Part II Python blocks start collapsed, Part I code stays visible and six numbered results tables exist. The current preview has 16 tables in total, including tutorial previews.

**Renderer limitation:** native Quarto is unavailable in the current environment. `check_quarto_source.py` verifies that the default render-target rules select only `index.qmd`, there are no fenced Div markers or external header dependencies, and Pandoc parses the source with `--fail-if-warnings`. This does not execute Quarto’s Lua filters or reproduce your entire website. Delivered HTML is generated with system Pandoc, embedded figures and MathML. Native whole-site Quarto rendering and browser layout were not verified here. Check the website's theme and listing integration by running `quarto render` in your website.

## Structure

```text
index.qmd
index.html
README.md
_Chinese_guide.md
requirements.txt
requirements-lock.txt
code/
├── 01_extract_official.py
├── 02_sql_audit.py
├── 03_validate_estimate.py
├── 04_report.py
├── 05_further_analysis.py
├── 06_make_figures.py
├── article_body.md
├── article_style.html
├── preview_head.html
├── build_article.py
├── check_article.py
├── check_html.py
├── render_preview.py
└── run_all.py
sql/
├── 01_prepare.sql
└── 02_match.sql
data/
├── raw/                         # original ZIPs supplied separately
├── selected/                    # seven unchanged original-column CSVs
├── processed/                   # generated SQLite database and tables
├── source_manifest.json
├── wave_mapping.json
└── variable_dictionary.csv
result/
├── matched_income.csv
├── pilot_ige.csv
├── factorial_ige.csv
├── paired_contrasts.csv
├── income_interpretation.csv
├── dispersion_summary.csv
├── factorial_bootstrap.npz
├── person_volatility.csv
├── further_analysis.json
├── validation.json
├── tutorial_validation.json
├── html_validation.json
├── ...                          # source quality, link and coverage audits
└── figures/                     # three 300-dpi PNGs
```

`04_report.py` regenerates the earlier Chinese data-check report and is optional. Its pilot results remain valid; it is not the article builder.

## Research references

Wave-specific income definitions: official Family File codebooks for [1999](https://psidonline.isr.umich.edu/documents/psid/codebook/fam1999er_codebook.pdf), [2001](https://psidonline.isr.umich.edu/documents/psid/codebook/fam2001er_codebook.pdf), [2003](https://psidonline.isr.umich.edu/documents/psid/codebook/fam2003er_codebook.pdf), [2015](https://psidonline.isr.umich.edu/documents/psid/codebook/fam2015er_codebook.pdf), [2017](https://psidonline.isr.umich.edu/documents/psid/codebook/FAM2017ER_codebook.pdf) and [2019](https://psidonline.isr.umich.edu/documents/psid/codebook/FAM2019ER_codebook.pdf).

- Haider and Solon (2006), [Life-Cycle Variation in the Association between Current and Lifetime Earnings](https://www.aeaweb.org/articles?id=10.1257/aer.96.4.1308), *AER*, 96(4), 1308–1320.
- Mazumder (2001), [Earnings Mobility in the US: A New Look at Intergenerational Inequality](https://www.chicagofed.org/publications/working-papers/2001/2001-18).
- Mazumder (2015), [Estimating the Intergenerational Elasticity and Rank Association in the U.S.](https://www.chicagofed.org/publications/working-papers/2015/wp2015-04).

## Income labels

All income variables represent total money income of the linked person’s family unit. Father pointers identify a person; the annual family-ID join attaches that person’s family income, potentially including the mother or other members. Adult children’s measures likewise include their own family members. The article does not estimate father-specific earnings persistence or distinguish mothers’ and fathers’ contributions. Existing CSV columns and SQL interfaces such as `father_log_multi` retain their names for reproducibility; they refer to family income, not individual earnings.

Render-target rules: [official Quarto documentation](https://quarto.org/docs/projects/quarto-projects.html#render-targets). `body-classes`: [official HTML options](https://quarto.org/docs/reference/formats/html.html#format-options).
