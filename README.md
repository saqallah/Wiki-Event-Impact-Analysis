# Quantifying the Effects of Real-World Events on Wikipedia

This repository contains code and data related to the master thesis titled "Quantifying the Effects of Real-World Events on Wikipedia." The thesis explores how real-world events influence editing behavior on the English Wikipedia, with a focus on various event categories. Below, you'll find an overview of the thesis, instructions on how to acquire the necessary editing data, and guidance on extracting articles related to specific events.

## Thesis Overview

### Abstract

This thesis presents a quantitative analysis of how real-world events influence editing behavior on the English Wikipedia, with the objective of comprehending their impact on overall editing activity and patterns. The study explores variations in editing behavior across different event categories and investigates Wikipedia’s response to events through article protection. Our study reproduces previous work, establishes a novel analysis methodology, and quantifies the effects of 15 events across categories: Armed Conflicts and Wars, Elections, Natural Disasters, Sports and Entertainment Events, and Legal and Legislative Events.

Findings reveal a notable surge in editing activity following events, reflecting increased interest from editors. The Russian invasion of Ukraine event received the highest editing activity, while the Tigray War exhibited the highest effect size on total edits, despite less global attention. Reverted edits were most prevalent in articles related to the Tigray War, and vandalism-reverted edits were higher for controversial topics like same-sex marriage legislation in the United States. Editorial biases were evident, with events in the United States receiving more attention. Protective measures reduced vandalism during armed conflicts but had varied effectiveness in different categories. This research provides insights into the editing dynamics of Wikipedia during real-world events and highlights factors influencing editing behavior.

## Acquiring Editing Data

To perform the analysis described in the thesis, you will need to acquire the relevant editing data. We obtained this data by reproducing the methodology outlined in Kiesel et al.’s [2017] paper “Spatio-temporal Analysis of Reverted Wikipedia Edits.” You can access their paper at the following URL: [Kiesel et al., 2017 Paper](https://webis.de/publications.html#kiesel_2017c).

## Extracting Articles Related to Events

After obtaining the comprehensive editing data for all of the English Wikipedia until January 2023, you can extract articles related to specific events using the code provided in the `src` folder, specifically the `by_search_article_extraction.py` script. In this script, you should modify the code to include the event name as the search word and adjust the number of related articles. The process for choosing the number of related articles is explained in detail in the thesis.

To analyze the articles extracted from the English Wikipedia editing history, follow these steps:

**Before Running the Analysis Script, Modify the Configuration**:

Before executing the "run_all.py" script, you'll need to customize the configuration in the "config.json" file to specify the event you want to analyze. Here's what you should modify in the "config.json" file:

```json
{
    "given_date": "YYYY-MM-DD",  // Replace with the date of the event (e.g., "2023-01-15").
    "input_file": "Event_Data_File.xml.gz",  // Replace with the name of the extracted related articles file.
    "event_name_for_latex": "Event Name"  // Replace with the name of the event for LaTeX files.
}

Once you've customized the configuration, you can proceed to run the "run_all.py" script to perform the analysis.

## Performing Analysis on Extracted Articles

To analyze the articles extracted from the English Wikipedia editing history, follow these steps:

**Run the Main Script**: Execute the `run_all.py` script located in the `src` folder. This main script automates the analysis process by running the following five scripts:

1. `RevisionCounter.py`: This script counts the revisions that are part of our key metrics for the specified timeframe period, as outlined in the thesis.

2. `RevisionAnalysis.py`: After counting the revisions, use this script to perform an in-depth analysis. It provides essential statistical numbers to compare key metrics before and after the event. It also exports a text file with LaTeX code for creating tables containing these numbers.

3. `PageAnalysis.py`: This script analyzes the top articles and their contributions, helping to identify topics that attract the most attention. It also determines the number of protected articles, shedding light on Wikipedia editors' responses to events.

4. `RevisionPlotter.py`: Use this script to create graphical representations of the revisions. It covers two time frame periods:
   - 12th Month Period: Includes 6 months before and 6 months after events, assessing distinct patterns beyond immediate pre/post-event periods.
   - 8-Week Period: Analyzes 4 weeks before and 4 weeks after the event, quantifying editing behavior changes before and after the event and comparing to identify shifts and trends.

5. `pageAnalysisLatexv2.py`: This script is dedicated to generating a text file with LaTeX code for creating tables related to the top articles and their contributions and the number of protected articles, which were analyzed using script 3.

If you encounter any issues or have questions about the analysis process, feel free to reach out for assistance.

