# Practical Considerations for Phenomic and Genomic Analyses in the *All of Us* Research Program
This workspace accompanies the manuscript *"Practical Considerations for Phenomic and Genomic Analyses in the All of Us Research Program"* and contains code examples demonstrating analytical workflows in the *All of Us* Researcher Workbench.
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
| `height_prs.tsv` | `06.2_prs_height_plot_v9.ipynb` | Height PRS scores used for the PRS plotting script |
| `zip3_population_density_2014_2023.csv` | `02_geographic_distribution_and_wildfire_smoke_map_v9.ipynb` | Population density by 3-digit ZIP code |
| `zip3_year_light_med_heavy_2014_2025.csv` | `02_geographic_distribution_and_wildfire_smoke_map_v9.ipynb` | Wildfire smoke exposure data by 3-digit ZIP code and year |
### Notebooks
Notebooks are numbered in the order their outputs first appear in the manuscript.
| Notebook | Description |
|---|---|
| `01_data_availability_query_v9.ipynb` | Generates **Figure 2A** ("Data Availability and Geographic Distribution of *All of Us* Participants" — panel A: data availability in *All of Us* over time) and associated summary numbers used in the manuscript. Also demonstrates how to query the phenotypic data types described in **Supplementary Table 2** ("Available Phenotypic Data Types, Source Vocabulary, and OMOP Tables to Query"). |
| `02_geographic_distribution_and_wildfire_smoke_map_v9.ipynb` | Generates **Figure 2B** ("Data Availability and Geographic Distribution of *All of Us* Participants" — panel B: geographic distribution of participants and linking external wildfire smoke exposure data). |
| `03.1_cohort_builder_phenotyping_hypothyroidism_v7.ipynb` | Cohort-builder generated case-control cohort phenotyping algorithm implementation for primary autoimmune hypothyroidism. Contributes to **Figure 3** ("Comparison of Cohort Builder- and SQL-Based Phenotyping and GWAS Results for Primary Autoimmune Hypothyroidism"). |
| `03.2_sql_phenotyping_hypothyroidism_v7.ipynb` | User-written SQL case-control cohort phenotyping algorithm implementation for primary autoimmune hypothyroidism. Contributes to **Figure 3**. |
| `03.3_gwas_hypothyroidism_v7.ipynb` | Runs the GWAS for the hypothyroidism phenotype in both Cohort Builder and SQL cohorts. Contributes to **Figure 3**. |
| `03.4_plot_cohort_comparison_and_gwas_v7.ipynb` | Plots Cohort Builder and SQL cohort comparisons and GWAS results (i.e., beta comparison scatter plot, Manhattan plots, identifying top peaks). Generates the plots used in **Figure 3**. |
| `04_srWGS_callset_query_v9.ipynb` | Generates data used in **Table 2** ("*All of Us* Short-Read Whole Genome Sequencing (srWGS) Callset Comparison") and associated WGS data availability numbers. Also produces the genetic diversity comparison (global GWAS vs. *All of Us*) shown in **Figure 1** ("Overview of Phenomic and Genomic Analyses Workflow in the *All of Us* Research Program") and srWGS numbers referenced in the figure. |
| `05_pharmacogenomic_data_query_v9.ipynb` | Generates **Supplementary Table 5** ("Subset of Available *All of Us* Pharmacogenetic Data"). |
| `06.1_prs_height_calculation_v9.ipynb` | Computes the height polygenic risk score (PRS) used in **Figure 5** ("Typical Workflow for Height PRS Calculation and Validation using Measured Height in *All of Us* Participants"). |
| `06.2_prs_height_plot_v9.ipynb` | Generates the PRS plots for **Figure 5**, using output from `06.1_prs_height_calculation_v9.ipynb` and `External_files/height_prs.tsv`. |
> **Note:** Notebooks `03.1`–`03.4` together produce **Figure 3**, comparing Cohort Builder-based and user-written SQL-based approaches to phenotype hypothyroidism cases and controls and perform downstream GWAS for comparison between the two approaches.
>
## License
GPL-3.0
