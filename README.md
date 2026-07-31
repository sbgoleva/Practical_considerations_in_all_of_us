# Practical Considerations for Phenomic and Genomic Analyses in the *All of Us* Research Program
This workspace accompanies the manuscript *Practical Considerations in All of Us* and contains code examples demonstrating analytical workflows in the *All of Us* Researcher Workbench.
## Repository Structure
```
Practical_considerations_in_all_of_us/
├── External_files/
└── Notebooks/
```
### External_files
Contains supporting files required to run certain notebooks. Each file's generation is documented within the notebook that uses it.
| File | Used by | Description |
|---|---|---|
| `height_prs.tsv` | `05.2_v9_PYTHON_PRS_PLOT.ipynb` | Height PRS scores used for the PRS plotting script |
| `zip3_population_density_2014_2023.csv` | `03_query_chloropleth_map.ipynb` | Population density by 3-digit ZIP code |
| `zip3_year_light_med_heavy_2014_2025.csv` | `03_query_chloropleth_map.ipynb` | Wildfire smoke exposure data by 3-digit ZIP code and year |
### Notebooks
| Notebook | Description |
|---|---|
| `01_query_data.ipynb` | Generates **Figure 2A** (data availability in *All of Us* over time) and associated summary numbers. Also demonstrates how to query the phenotypic data types described in **Supplementary Table 2** (Available Phenotypic Data Types, Source Vocabulary, and OMOP Tables to Query). |
| `02_query_srWGS_data.ipynb` | Generates **Table 2** (*All of Us* Short-Read Whole Genome Sequencing Callset Comparison) and associated WGS data availability numbers. Also produces the genetic diversity comparison (global GWAS vs. *All of Us*) shown in **Figure 1** (Overview of Phenomic and Genomic Analyses Workflow in the *All of Us* Research Program). |
| `03_query_chloropleth_map.ipynb` | Generates **Figure 2B** — geographic distribution of *All of Us* participants, linked with external wildfire smoke exposure data. |
| `04_query_pharmacogenomic_tables.ipynb` | Generates **Supplementary Table 5** (Subset of Available *All of Us* Pharmacogenetic Data). |
| `05.1_v9_Height_PRS.ipynb` | Computes the height polygenic risk score (PRS) used in **Figure 5**. |
| `05.2_v9_PYTHON_PRS_PLOT.ipynb` | Generates the PRS plots for **Figure 5**, using output from `05.1_v9_Height_PRS.ipynb` and `External_files/height_prs.tsv`. |
| `06.1_HM_hypothyroidism_id_v1.ipynb` | User-written SQL case-control cohort phenotyping algorithm implementation for primary autoimmune hypothyroidism. Contributes to **Figure 3**. |
| `06.2_CB_case_phenotype_algorithm_V2_SQL_query.ipynb` | Cohort-builder generated case-control cohort phenotyping algorithm implementation for primary autoimmune hypothyroidism. Contributes to **Figure 3**. |
| `06.3_CB_GWAS_MF.ipynb` | Runs the GWAS for the hypothyroidism phenotype in both CB and SQL cohorts. Contributes to **Figure 3**. |
| `06.4_Plotting_cohorts_and_gwas.ipynb` | Plots CB and SQL cohort comparisons and GWAS results (i.e., beta comparison scatter plot, Manhattan plots, identifying top peaks). Contributes to **Figure 3**. |
> **Note:** Notebooks `06.1`–`06.4` together produce **Figure 3** (Comparison of Cohort Builder- and SQL-Based Phenotyping and GWAS Results for Primary Autoimmune Hypothyroidism), comparing Cohort Builder-based and user-written SQL-based approaches to phenotype hypothyroidism cases and controls and perform downstream GWAS for comparison between the two approaches.
## License
GPL-3.0
