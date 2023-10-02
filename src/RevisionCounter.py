import gzip
import xml.etree.ElementTree as ET
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import requests
import json

def count_revisions(input_path, revision_counts, filter_geolocated=False):
    # open the output file in write mode
    with open(revision_counts, "w") as output_file:
        # write the header row
        output_file.write("date\t#num-revisions\t#num-reverted-revisions\t#num-vandalism-comment-reverted-revisions\n")
        
        # open the input file using gzip and parse the XML
        with gzip.open(input_path, "rb") as input_file:
            tree = ET.parse(input_file)
            # get the root element and loop through its child elements
            root = tree.getroot()
            all_revisions = 0
            all_reverted = 0
            all_vand = 0

            for page in root.findall("page"):
                # loop through the revision elements and update the counters
                for revision in page.findall("revision"):
                    if filter_geolocated and not revision.findall("geolocated"):
                        continue
                    
                    # initialize counters for the metrics
                    all_revisions += 1
                    num_revisions = 1
                    num_reverted_revisions = 0
                    num_vandalism_comment_reverted_revisions = 0    
                    date = revision.get("timestamp")[:10]
                    
                    for reverted in revision.findall("reverted"):
                        num_reverted_revisions = 1
                        all_reverted += 1
                        if reverted.get("withVandalismComment") is not None and reverted.get("withVandalismComment") == "true":
                            num_vandalism_comment_reverted_revisions = 1
                            all_vand += 1
                                
                    # write the metrics for this page to the output file
                    output_file.write(f"{date}\t{num_revisions}\t{num_reverted_revisions}\t{num_vandalism_comment_reverted_revisions}\n")         
                    
    return all_revisions, all_reverted, all_vand        

       
def calculate_date_summation(file, output_file):
    date_summation = output_file

    # Dictionaries to store the sum of revisions for each column and date
    date_counts = {'#num-revisions': {}, '#num-reverted-revisions': {}, '#num-vandalism-comment-reverted-revisions': {}}

    # Read the input file and calculate the sum of revisions for each column and date
    with open(file, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        # Skip the header row
        next(reader)
        for row in reader:
            date = row[0]
            num_revisions = int(row[1])
            num_reverted_revisions = int(row[2])
            num_vandalism_comment_reverted_revisions = int(row[3])
            # Add the counts for each column and date
            date_counts['#num-revisions'][date] = date_counts['#num-revisions'].get(date, 0) + num_revisions
            date_counts['#num-reverted-revisions'][date] = date_counts['#num-reverted-revisions'].get(date, 0) + num_reverted_revisions
            date_counts['#num-vandalism-comment-reverted-revisions'][date] = date_counts['#num-vandalism-comment-reverted-revisions'].get(date, 0) + num_vandalism_comment_reverted_revisions

    # Write the output to a tab-separated text file
    with open(date_summation, 'w') as outfile:
        outfile.write('date\t#num-revisions\t#num-reverted-revisions\t#num-vandalism-comment-reverted-revisions\n')
        for date in sorted(date_counts['#num-revisions'].keys()):
            outfile.write('{}\t{}\t{}\t{}\n'.format(date, date_counts['#num-revisions'][date], date_counts['#num-reverted-revisions'][date], date_counts['#num-vandalism-comment-reverted-revisions'][date]))
            

def calculate_sums_by_user_type(filename):
    all_revisions = 0
    all_reverted = 0
    all_vand = 0

    with open(filename, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        next(reader)  # Skip the header row
        for row in reader:
            date = row[0]
            num_revisions = int(row[1])
            num_reverted_revisions = int(row[2])
            num_vandalism_comment_reverted_revisions = int(row[3])
            all_revisions += num_revisions
            all_reverted += num_reverted_revisions
            all_vand += num_vandalism_comment_reverted_revisions

    return all_revisions, all_reverted, all_vand


def revision_counter_by_user_type(input_path):
    # Count revisions by type and date
    anonymous_revisions_count = {}
    anonymous_reverted_count = {}
    anonymous_vandalism_reverted_count = {}
    registered_revisions_count = {}
    registered_reverted_count = {}
    registered_vandalism_reverted_count = {}

    # Open the compressed file using gzip
    with gzip.open(input_path, 'rt', encoding='utf-8') as file:
        # Parse the XML content
        root = ET.fromstring(file.read())

        # Count revisions
        for page in root.findall('page'):
            for revision in page.findall('revision'):
                timestamp = revision.get("timestamp")
                # Extract the date portion from the timestamp
                revision_date = timestamp.split("T")[0]
                # Check if the revision is within the specified date range
                contributor = revision.get('contributor')
                if contributor.startswith('ip:'):
                    user_type = 'anonymous'
                elif contributor.startswith('id:'):
                    user_type = 'registered'
                else:
                    continue  # Skip revisions with unknown contributor type

                # Update the revisions count for the user type and date
                if user_type == 'anonymous':
                    if revision_date in anonymous_revisions_count:
                        anonymous_revisions_count[revision_date] += 1
                    else:
                        anonymous_revisions_count[revision_date] = 1

                    for reverted in revision.findall("reverted"):
                        if revision_date in anonymous_reverted_count:
                            anonymous_reverted_count[revision_date] += 1
                        else:
                            anonymous_reverted_count[revision_date] = 1

                        if reverted.get("withVandalismComment") is not None and reverted.get("withVandalismComment") == "true":
                            if revision_date in anonymous_vandalism_reverted_count:
                                anonymous_vandalism_reverted_count[revision_date] += 1
                            else:
                                anonymous_vandalism_reverted_count[revision_date] = 1
                    
                elif user_type == 'registered':
                    if revision_date in registered_revisions_count:
                        registered_revisions_count[revision_date] += 1
                    else:
                        registered_revisions_count[revision_date] = 1

                    for reverted in revision.findall("reverted"):
                        if revision_date in registered_reverted_count:
                            registered_reverted_count[revision_date] += 1
                        else:
                            registered_reverted_count[revision_date] = 1

                        if reverted.get("withVandalismComment") is not None and reverted.get("withVandalismComment") == "true":
                            if revision_date in registered_vandalism_reverted_count:
                                registered_vandalism_reverted_count[revision_date] += 1
                            else:
                                registered_vandalism_reverted_count[revision_date] = 1
                                

    # Sort the dates in ascending order
    sorted_anonymous_dates = sorted(anonymous_revisions_count.keys())
    sorted_registered_dates = sorted(registered_revisions_count.keys())

    # Write anonymous revisions counts to a text file in sorted order
    with open(os.path.join(output_directory,"ANONYMOUS_by_date_counts.txt"), 'w') as output_file_anonymous:
        output_file_anonymous.write("date\t#num-revisions\t#num-reverted-revisions\t#num-vandalism-comment-reverted-revisions\n")
        for date in sorted_anonymous_dates:
            num_revisions = anonymous_revisions_count[date]
            num_reverted_revisions = anonymous_reverted_count.get(date, 0)
            num_vandalism_comment_reverted_revisions = anonymous_vandalism_reverted_count.get(date, 0)
            output_file_anonymous.write(f"{date}\t{num_revisions}\t{num_reverted_revisions}\t{num_vandalism_comment_reverted_revisions}\n")

    # Write registered revisions counts to a text file in sorted order
    with open(os.path.join(output_directory,"REGISTERED_by_date_counts.txt"), 'w') as output_file_registered:
        output_file_registered.write("date\t#num-revisions\t#num-reverted-revisions\t#num-vandalism-comment-reverted-revisions\n")
        for date in sorted_registered_dates:
            num_revisions = registered_revisions_count[date]
            num_reverted_revisions = registered_reverted_count.get(date, 0)
            num_vandalism_comment_reverted_revisions = registered_vandalism_reverted_count.get(date, 0)
            output_file_registered.write(f"{date}\t{num_revisions}\t{num_reverted_revisions}\t{num_vandalism_comment_reverted_revisions}\n")
    
def registered_users_count_trial3(input_path, output_path_anonymous, output_path_registered):
    # Count revisions by type and date
    anonymous_revisions_count = {}
    registered_revisions_count = {}

    # Open the compressed file using gzip
    with gzip.open(input_path, 'rt', encoding='utf-8') as file:
        # Parse the XML content
        root = ET.fromstring(file.read())

        # Count revisions
        for page in root.findall('page'):
            for revision in page.findall('revision'):
                timestamp = revision.get("timestamp")
                # Extract the date portion from the timestamp
                revision_date = timestamp.split("T")[0]
                # Check if the revision is within the specified date range
                contributor = revision.get('contributor')
                if contributor.startswith('ip:'):
                    user_type = 'anonymous'
                elif contributor.startswith('id:'):
                    user_type = 'registered'
                else:
                    continue  # Skip revisions with unknown contributor type

                # Update the revisions count for the user type and date
                if user_type == 'anonymous':
                    if revision_date in anonymous_revisions_count:
                        anonymous_revisions_count[revision_date] += 1
                    else:
                        anonymous_revisions_count[revision_date] = 1
                elif user_type == 'registered':
                    if revision_date in registered_revisions_count:
                        registered_revisions_count[revision_date] += 1
                    else:
                        registered_revisions_count[revision_date] = 1
                        
    # Sort the dates in ascending order
    sorted_anonymous_dates = sorted(anonymous_revisions_count.keys())
    sorted_registered_dates = sorted(registered_revisions_count.keys())

    # Write anonymous revisions counts to a text file in sorted order
    with open(output_path_anonymous, 'w') as output_file_anonymous:
        output_file_anonymous.write("date\t#num-revisions\n")
        for date in sorted_anonymous_dates:
            count = anonymous_revisions_count[date]
            output_file_anonymous.write(f"{date}\t{count}\n")

    # Write registered revisions counts to a text file in sorted order
    with open(output_path_registered, 'w') as output_file_registered:
        output_file_registered.write("date\t#num-revisions\n")
        for date in sorted_registered_dates:
            count = registered_revisions_count[date]
            output_file_registered.write(f"{date}\t{count}\n")
            

# Read the config file
with open('config.json', 'r') as file:
    config = json.load(file)

# Config
file_name = config['input_file']

base_file_name = file_name.rsplit(".", 2)[0]

input_directory = "..\data"
input_path = os.path.join(input_directory, file_name)

output_directory = "..\Events/"+ base_file_name +"/counts"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Count all revisions
all_date_counts = os.path.join(output_directory,"by_date_counts_NOT_summed.txt")
all_revisions, all_reverts, all_vand = count_revisions(input_path, all_date_counts)
calculate_date_summation(all_date_counts, os.path.join(output_directory,"by_date_counts.txt"))

# Count geolocated revisions
geolocated_counts = os.path.join(output_directory,"GEOLOCATED_by_date_counts_NOT_summed.txt")
all_geo_revisions, all_geo_reverts, all_geo_vand = count_revisions(input_path, geolocated_counts, filter_geolocated=True)
calculate_date_summation(geolocated_counts, os.path.join(output_directory, "GEOLOCATED_by_date_counts.txt"))


# # all_reg_revisions, all_reg_reverts, all_reg_vand, all_anon_revisions, all_anon_reverts, all_anon_vand = 
# revision_counter_by_user_type(input_path)
anonymous_date_summation = os.path.join(output_directory,'ANONYMOUS_by_date_counts.txt')
registered_date_summation = os.path.join(output_directory,'REGISTERED_by_date_counts.txt')

registered_users_count_trial3(input_path, anonymous_date_summation, registered_date_summation)

# Example usage:
# registered_counts = os.path.join(output_directory,"REGISTERED_by_date_counts.txt")
# anonymous_counts = os.path.join(output_directory,"ANONYMOUS_by_date_counts.txt")
# all_reg_revisions, all_reg_reverts, all_reg_vand = calculate_sums_by_user_type(registered_counts)
# all_anon_revisions, all_anon_reverts, all_anon_vand = calculate_sums_by_user_type(anonymous_counts)


with open(os.path.join(output_directory, "total_counts.txt"), "w") as output_file:
    output_file.write("##########\t#Revisions\t#Reverts\t#Vandalism Reverts\n")
    output_file.write("Total:\t" + str(all_revisions) + "\t" + str(all_reverts) + "\t" + str(all_vand)+"\n")
    output_file.write("Geoloacted revisions:\t" + str(all_geo_revisions) + "\t" + str(all_geo_reverts) + "\t" + str(all_geo_vand)+"\n")
    # output_file.write("Registered revisions:\t" + str(all_reg_revisions) + "\t" + str(all_reg_reverts) + "\t" + str(all_reg_vand)+"\n")
    # output_file.write("Anonymous revisions:\t" + str(all_anon_revisions) + "\t" + str(all_anon_reverts) + "\t" + str(all_anon_vand)+"\n")

print("Revision Counting Done...")