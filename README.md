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

For more details and guidance on using the code and data in this repository, please refer to the thesis document itself.

If you have any questions or need further assistance, feel free to reach out.

