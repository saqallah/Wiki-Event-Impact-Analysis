import gzip
import xml.etree.ElementTree as ET
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import requests
import json

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
#         return "Protected"
    
#     return "Not protected"

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
            return r"Protected"

    return r"NOT protected"



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

        sorted_pages_revisions = sorted(
            page_revisions.items(), key=lambda x: x[1], reverse=True
        )
        sorted_pages_reverts = sorted(
            page_reverts.items(), key=lambda x: x[1], reverse=True
        )
        sorted_pages_vandalism_reverts = sorted(
            page_vandalism_reverts.items(), key=lambda x: x[1], reverse=True
        )

        output_file.write("All pages with their revisions:\n")
        for page_id, revisions in sorted_pages_revisions:
            article_title = get_wikipedia_article_title(page_id)
            protection_status = get_protection_status(page_id)
            timestamps = get_protection_timestamps(page_id)
            output_file.write(f"Page ID: {page_id}, Article Title: {article_title}, Revisions: {revisions}, Protection status: {protection_status}, TimeStamp: {timestamps}\n")

        # output_file.write("\nAll pages with their reverts:\n")
        # for page_id, reverts in sorted_pages_reverts:
        #     article_title = get_wikipedia_article_title(page_id)
        #     protection_status = get_protection_status(page_id)
        #     output_file.write(f"Page ID: {page_id}, Article Title: {article_title}, Reverts: {reverts}, Protection status: {protection_status}\n")

        # output_file.write("\nAll pages with their vandalism reverts:\n")
        # for page_id, vandalism_reverts in sorted_pages_vandalism_reverts:
        #     article_title = get_wikipedia_article_title(page_id)
        #     protection_status = get_protection_status(page_id)
        #     output_file.write(f"Page ID: {page_id}, Article Title: {article_title}, Vandalism Reverts: {vandalism_reverts}, Protection status: {protection_status}\n")

        total_revisions = sum(page_revisions.values())
        total_reverts = sum(page_reverts.values())
        total_vandalism_reverts = sum(page_vandalism_reverts.values())

        output_file.write("\nTotal revisions for all pages: {}\n".format(total_revisions))
        output_file.write("Total reverts for all pages: {}\n".format(total_reverts))
        output_file.write("Total vandalism reverts for all pages: {}\n".format(total_vandalism_reverts))

    print("Write operation completed.")

# Read the config file
with open('config.json', 'r') as file:
    config = json.load(file)

# Config
given_date = pd.Timestamp(config['given_date'])
file_name = config['input_file']
base_file_name = file_name.rsplit(".", 2)[0]


input_directory = "..\data"
input_path = os.path.join(input_directory, file_name)

output_directory = "..\Events/"+ base_file_name + "/pages_analysis"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

weeks_before = 4
weeks_after = 4
## for analyzing one day only
start_date = given_date
end_date = given_date
# start_date = given_date - pd.DateOffset(weeks=weeks_before)
# end_date = given_date + pd.DateOffset(weeks=weeks_after)

given_date_string = given_date.strftime('%Y-%m-%d')
given_date_string_a_day_before = (given_date - pd.DateOffset(days=1)).strftime('%Y-%m-%d')
start_date_string = start_date.strftime('%Y-%m-%d')
end_date_string = end_date.strftime('%Y-%m-%d')
vertical_line_date = given_date

analyize_pages(input_path, start_date_string, end_date_string, os.path.join(output_directory,"pages_stats"))
# analyize_pages(input_path, start_date_string, given_date_string_a_day_before, os.path.join(output_directory,"Before_pages_stats"))
# analyize_pages(input_path, given_date_string, end_date_string, os.path.join(output_directory,"After_pages_stats"))

print("Page Analysis Done...")