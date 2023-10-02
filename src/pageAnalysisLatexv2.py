import gzip
import xml.etree.ElementTree as ET
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import requests
import json
from datetime import datetime


## this function checkes for both move and edit protection
# def get_protection_status(page_id):
#     base_url = 'https://en.wikipedia.org/w/api.php'
#     params = {
#         'action': 'query',
#         'format': 'json',
#         'prop': 'info',
#         'pageids': page_id,
#         'intoken': 'protects',
#         'inprop': 'protection',
#         'formatversion': 2
#     }
#     response = requests.get(base_url, params=params)
#     data = response.json()
    
#     page = data['query']['pages'][0]
#     protections = page['protection']
    
#     if protections:
#         return r"$\checkmark$"
    
#     return r"$\times$"

def compare_digits(highest_number, other_number):
    highest_digits = len(str(highest_number))
    other_digits = len(str(other_number))
    
    if highest_digits == 5:
        if other_digits == 5:
            return ""
        elif other_digits == 4:
            return "\\phantom{0}"
        else:
            return "\\phantom{" + "0" * (highest_digits - other_digits) + ",}"
        
    if highest_digits == 4:
        if other_digits == 4:
            return ""
        elif other_digits == 3:
            return "\\phantom{0,}"
        else:
            return "\\phantom{" + "0" * (highest_digits - other_digits) + ",}"

    else:
        if highest_digits == other_digits:
            return ""
        elif highest_digits - other_digits > 0:
            return "\\phantom{" + "0" * (highest_digits - other_digits) + "}"
        else:
            return None  # Handle the case where the other_number has more digits than the highest_number

def get_protection_status(page_id):
    base_url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'info',
        'pageids': page_id,
        'intoken': 'protects',
        'inprop': 'protection',
        'formatversion': 2
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    page = data['query']['pages'][0]
    protections = page['protection']

    for protection in protections:
        if protection['type'] == 'edit':
            return r"$\checkmark$"

    return r"$\times$"

def get_protection_timestamps(page_id):
    base_url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'info',
        'pageids': page_id,
        'intoken': 'protects',
        'inprop': 'protection',
        'formatversion': 2
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    page = data['query']['pages'][0]
    protections = page['protection']

    timestamps = []

    for protection in protections:
        if(protection['type'] == 'edit'):
            title = page['title']
            revision_params = {
                'action': 'query',
                'format': 'json',
                'prop': 'revisions',
                'rvprop': 'timestamp',
                'rvlimit': 1,
                'rvdir': 'newer',
                'titles': title,
                'formatversion': 2
            }
            revision_response = requests.get(base_url, params=revision_params)
            revision_data = revision_response.json()
            revision = revision_data['query']['pages'][0]['revisions'][0]
            timestamp = revision['timestamp']
            timestamps.append(timestamp)

    return timestamps
        

def get_wikipedia_article_title(page_id):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info&pageids={page_id}&inprop=url"
    response = requests.get(url)
    data = response.json()

    page_info = data["query"]["pages"][str(page_id)]
    article_title = page_info["title"]

    return article_title


def analyize_pages(input_path, start_date, end_date, output_path):
    page_revisions = {}
    page_reverts = {}
    page_vandalism_reverts = {}
    total_revisions_for_all_pages = 0

    with gzip.open(input_path, "rb") as input_file, open(output_path + '.txt', "w") as output_file:
        tree = ET.parse(input_file)
        root = tree.getroot()

        for page in root.findall("page"):
            page_id = page.get("id")
            revisions = 0
            reverts = 0
            vandalism_reverts = 0

            for revision in page.findall("revision"):
                timestamp = revision.get("timestamp")

                # Extract the date portion from the timestamp
                revision_date = timestamp.split("T")[0]
                
                # Check if the revision is within the specified date range
                if start_date <= revision_date <= end_date:
                    revisions += 1

                    for reverted in revision.findall("reverted"):
                        reverts += 1

                        if (
                            reverted.get("withVandalismComment") is not None
                            and reverted.get("withVandalismComment") == "true"
                        ):
                            vandalism_reverts += 1

            page_revisions[page_id] = revisions
            page_reverts[page_id] = reverts
            page_vandalism_reverts[page_id] = vandalism_reverts
            total_revisions_for_all_pages += revisions
            
        sorted_pages_revisions = sorted(
            page_revisions.items(), key=lambda x: x[1], reverse=True
        )
        # sorted_pages_reverts = sorted(
        #     page_reverts.items(), key=lambda x: x[1], reverse=True
        # )
        # sorted_pages_vandalism_reverts = sorted(
        #     page_vandalism_reverts.items(), key=lambda x: x[1], reverse=True
        # )

    
    return sorted_pages_revisions, page_reverts, page_vandalism_reverts, total_revisions_for_all_pages, page_revisions
    
    
    

# Read the config file
with open('config.json', 'r') as file:
    config = json.load(file)

# Config
given_date = pd.Timestamp(config['given_date'])
file_name = config['input_file']
event_name_for_latex = config['event_name_for_latex']
base_file_name = file_name.rsplit(".", 2)[0]

input_directory = "..\data"
input_path = os.path.join(input_directory, file_name)

output_directory = "..\Events/"+ base_file_name + "/pages_analysis"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

weeks_before = 4
weeks_after = 4
start_date = given_date - pd.DateOffset(weeks=weeks_before)
end_date = given_date + pd.DateOffset(weeks=weeks_after)



given_date_string = given_date.strftime('%Y-%m-%d')
given_date_string_a_day_before = (given_date - pd.DateOffset(days=1)).strftime('%Y-%m-%d')
start_date_string = start_date.strftime('%Y-%m-%d')
end_date_string = end_date.strftime('%Y-%m-%d')
vertical_line_date = given_date


sorted_pages_revisions, page_reverts, page_vandalism_reverts, total_revisions_for_all_pages, page_revisions = analyize_pages(input_path, start_date_string, end_date_string, os.path.join(output_directory,"pages_stats_latex"))
page_revisions_before, page_reverts_before, page_vandalism_reverts_before, total_revisions_for_all_pages_before, page_revisions_before2 = analyize_pages(input_path, start_date_string, given_date_string_a_day_before, os.path.join(output_directory,"Before_pages_stats_latex"))
page_revisions_after, page_reverts_after, page_vandalism_reverts_after, total_revisions_for_all_pages_after, page_revisions_after2 = analyize_pages(input_path, given_date_string, end_date_string, os.path.join(output_directory,"After_pages_stats_latex"))

# print(dict(sorted_pages_revisions).get('70149799'))
# # print(page_revisions_before.get(70149799))
# print(get_wikipedia_article_title('70149799'))

pages_string = ""
before_period = start_date_string + " to " + given_date_string_a_day_before
after_period = given_date_string + " to " + end_date_string
all_period = start_date_string + " - " + end_date_string
caption = "Top 10 articles ranked by total edits during the "+event_name_for_latex+" on "+given_date_string+". Covers 8 weeks ("+all_period+"),  with 4 weeks before and after. Table shows counts of total, reverted, and vandalism-reverted edits for each article before and after the event. Includes protection status (\scalebox{0.8}{\\faLock}) and if the article was protected during the analysis period \scalebox{0.8}{(\\faAt)}. Summation row provides overall statistics for all 10 articles. Percentage contribution indicates edits proportion compared to total analysis edits."

table_string = r'''
\begin{table}[H]
\scriptsize
\setlength{\tabcolsep}{5.6pt}
\caption{'''

table_string += caption +"}\n\label{table:"+event_name_for_latex+" Top 10}"
table_string+= r'''
\centering
\begin{adjustbox}{width=\textwidth}
\begin{tabular}{@{}l@{\hspace{12pt}}cccccccccc@{}}
\toprule
\bfseries Top 10 Articles by Total Edits & \multicolumn{4}{c}{\bfseries Edits} & \multicolumn{2}{c}{\bfseries Reverts} & \multicolumn{2}{c}{\bfseries Vand.} & \multicolumn{2}{c}{\bfseries Protec.}\\
\cmidrule(r{\tabcolsep}){2-5}
\cmidrule(l{\tabcolsep}r{\tabcolsep}){6-7}
\cmidrule(l{\tabcolsep}r{\tabcolsep}){8-9}
\cmidrule(l{\tabcolsep}){10-11}
&  $\sum$ & \% & $\leftarrow$  & $\rightarrow$ & $\leftarrow$ & $\rightarrow$ & $\leftarrow$ & $\rightarrow$ & \faLock & \faAt\\
\midrule
'''
## to get total
counter = 0
revisions_total = 0
revisions_total_before = 0
revisions_total_after = 0
reverts_total = 0
reverts_total_before = 0
reverts_total_after = 0
vand_total = 0
vand_total_before = 0
vand_total_after = 0
contrib_total = 0
protected_total = 0
protected_during_total = 0

for page_id, revisions in sorted_pages_revisions:
    if counter >= 10:
        break

    reverts_counts = page_reverts.get(page_id)
    vand_counts = page_vandalism_reverts.get(page_id)
    revisions_before = dict(page_revisions_before).get(page_id)
    revisions_after = dict(page_revisions_after).get(page_id)
    reverts_before = dict(page_reverts_before).get(page_id)
    reverts_after = dict(page_reverts_after).get(page_id)
    vand_before = dict(page_vandalism_reverts_before).get(page_id)
    vand_after = dict(page_vandalism_reverts_after).get(page_id)
    
    contrib = (revisions / total_revisions_for_all_pages) * 100
    
    protection_status = get_protection_status(page_id)
    if(protection_status == r"$\checkmark$" ):
        protected_total +=1
        protection_timestamp = get_protection_timestamps(page_id)

        # Convert the dates to pandas Timestamp objects for comparison
        for item in protection_timestamp:
            protection_timestamp_date_only = pd.to_datetime(item.split("T")[0])
            # Check if any of the dates fall within the specified range
            if start_date <= protection_timestamp_date_only <= end_date:
                protected_during_total +=1
                protection_status_during = r"$\checkmark$"
            else:
                protection_status_during = r"$\times$"       
    else:
        protection_status_during = ""
    
    revisions_total += revisions
    revisions_total_before += revisions_before
    revisions_total_after += revisions_after
    reverts_total += reverts_counts
    vand_total += vand_counts
    reverts_total_before += reverts_before
    reverts_total_after += reverts_after
    vand_total_before += vand_before
    vand_total_after += vand_after
    contrib_total += (contrib)

    counter += 1
    
# highest_digits_edits = (revisions_total)
# highest_digits_edits_before = (sum(page_revisions.values()))
# highest_digits_edits_before = (sum(page_revisions.values()))
# highest_digits_reverts_before= (max(page_reverts_before.values()))
# highest_digits_vand_before = (max(page_vandalism_reverts_before.values()))

counter_pages = 0
for page_id, revisions in sorted_pages_revisions:
    if counter_pages >= 10:
        break
    
    article_title = get_wikipedia_article_title(page_id)
    revisions_before = dict(page_revisions_before).get(page_id)
    revisions_after = dict(page_revisions_after).get(page_id)
    reverts_before = dict(page_reverts_before).get(page_id)
    reverts_after = dict(page_reverts_after).get(page_id)
    vand_before = dict(page_vandalism_reverts_before).get(page_id)
    vand_after = dict(page_vandalism_reverts_after).get(page_id)
    
    protection_status = get_protection_status(page_id)
    if(protection_status == r"$\checkmark$" ):
        # protected_total +=1
        protection_timestamp = get_protection_timestamps(page_id)

        # Convert the dates to pandas Timestamp objects for comparison
        for item in protection_timestamp:
            protection_timestamp_date_only = pd.to_datetime(item.split("T")[0])
            # Check if any of the dates fall within the specified range
            if start_date <= protection_timestamp_date_only <= end_date:
                # protected_during_total +=1
                protection_status_during = r"$\checkmark$"
            else:
                protection_status_during = r"$\times$"       
    else:
        protection_status_during = ""

    contrib = (revisions / total_revisions_for_all_pages) * 100
    
    phantom_edits = compare_digits(revisions_total,revisions)
    phantom_edits_before = compare_digits(revisions_total_before,revisions_before)
    phantom_edits_after = compare_digits(revisions_total,revisions_after)
    phantom_reverts_before = compare_digits(reverts_total_before,reverts_before)
    phantom_reverts_after = compare_digits(reverts_total_after,reverts_after)
    phantom_vand_before = compare_digits(vand_total_before,vand_before)
    phantom_vand_after = compare_digits(vand_total_after,vand_after)
    phantom_contrib = compare_digits("{:.0f}".format(contrib_total),"{:.0f}".format(contrib))
    phantom_protec_status = compare_digits(protected_total,1)
    phantom_protec_during = compare_digits(protected_during_total,1)

    pages_string += (f"{article_title} & {phantom_edits}{revisions:,} & {phantom_contrib}{contrib:.0f}\% & {phantom_edits_before}{revisions_before:,} & {phantom_edits_after}{revisions_after:,} & {phantom_reverts_before}{reverts_before:,} & {phantom_reverts_after}{reverts_after:,} & {phantom_vand_before}{vand_before:,} & {phantom_vand_after}{vand_after:,} & {phantom_protec_status}{protection_status} & {phantom_protec_status}{protection_status_during}\\\\\n")
    
    counter_pages += 1

pages_string += r'''\midrule
$\sum$'''
pages_string += (f" & {revisions_total:,} & {contrib_total:.0f}\% & {revisions_total_before:,} & {revisions_total_after:,}  & {reverts_total_before:,} & {reverts_total_after:,} & {vand_total_before:,} & {vand_total_after:,} & {protected_total:,} & {protected_during_total:,}\\\\\n")


table_string += pages_string

table_string += r'''\bottomrule
\end{tabular}\end{adjustbox}\end{table}'''

# Open the output file in write mode
with open(os.path.join(output_directory,'../Latex_pages_table_v2.txt'), 'w') as file:
    file.write(table_string)


print("Latex Page text file generated...")