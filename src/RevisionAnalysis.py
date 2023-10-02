import gzip
import xml.etree.ElementTree as ET
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import json
import pingouin as pg

def get_asterisks(p_value):
    if p_value <= 0.001:
        return '***'
    elif p_value <= 0.01:
        return '**\phantom{*}'
    elif p_value <= 0.05:
        return '*\phantom{**}'
    else:
        return '\phantom{***}'

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
    
    

def get_data(input_file, start_date, end_date, edits):
    # Load the data from the txt file into a pandas DataFrame
    data = pd.read_csv(input_file, delimiter='\t')

    # Convert the date column to a pandas datetime object
    data['date'] = pd.to_datetime(data['date'])

    # Set the date column as the index
    data = data.set_index('date')

    
    # Reindex the DataFrames with a complete date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    data = data.reindex(date_range, fill_value=0)
    
    return data[edits].values


def calculate_absolute_difference(data_before, data_after):
    absolute_difference = abs(data_after - data_before)
    return absolute_difference

def calculate_revision_stats(input_file, start_date, end_date):
    # Load the data from the txt file into a pandas DataFrame
    data = pd.read_csv(input_file, delimiter='\t')

    # Convert the date column to a pandas datetime object
    data['date'] = pd.to_datetime(data['date'])

    # Select the data within the specified start and end dates
    data = data.loc[(data['date'] >= start_date) & (data['date'] <= end_date)]

    # Calculate the sum of revisions, reverts, and vandalism reverts for the selected period
    sum_revisions = data['#num-revisions'].sum()
    sum_reverts = data['#num-reverted-revisions'].sum()
    sum_vandalism_reverts = data['#num-vandalism-comment-reverted-revisions'].sum()

    return sum_revisions, sum_reverts, sum_vandalism_reverts

def calculate_revision_stats_registered_anonymous(input_file, start_date, end_date):
    # Load the data from the txt file into a pandas DataFrame
    data = pd.read_csv(input_file, delimiter='\t')

    # Convert the date column to a pandas datetime object
    data['date'] = pd.to_datetime(data['date'])

    # Select the data within the specified start and end dates
    data = data.loc[(data['date'] >= start_date) & (data['date'] <= end_date)]

    # Calculate the sum of revisions, reverts, and vandalism reverts for the selected period
    sum_revisions = data['#num-revisions'].sum()
    # sum_reverts = data['#num-reverted-revisions'].sum()
    # sum_vandalism_reverts = data['#num-vandalism-comment-reverted-revisions'].sum()
    
    return sum_revisions
# , sum_reverts, sum_vandalism_reverts



def analyse_revisions(input_file, geoloacted_input_file, anonymous_input_file, registered_input_file , given_date, start_date, end_date, output_file):
    sum_revisions, sum_reverts, sum_vandalism_reverts = calculate_revision_stats(input_file, start_date, end_date)
    sum_revisions_before, sum_reverts_before, sum_vandalism_reverts_before = calculate_revision_stats(input_file, start_date, given_date - pd.DateOffset(days=1))
    sum_revisions_after, sum_reverts_after, sum_vandalism_reverts_after = calculate_revision_stats(input_file, given_date, end_date)

    geoloacted_sum_revisions, geoloacted_sum_reverts, geoloacted_sum_vandalism_reverts = calculate_revision_stats(geoloacted_input_file, start_date, end_date)
    geoloacted_sum_revisions_before, geoloacted_sum_reverts_before, geoloacted_sum_vandalism_reverts_before = calculate_revision_stats(geoloacted_input_file, start_date, given_date - pd.DateOffset(days=1))
    geoloacted_sum_revisions_after, geoloacted_sum_reverts_after, geoloacted_sum_vandalism_reverts_after = calculate_revision_stats(geoloacted_input_file, given_date, end_date)
    
    anonymous_sum_revisions = calculate_revision_stats_registered_anonymous(anonymous_input_file, start_date, end_date)
    anonymous_sum_revisions_before = calculate_revision_stats_registered_anonymous(anonymous_input_file, start_date, given_date - pd.DateOffset(days=1))
    anonymous_sum_revisions_after = calculate_revision_stats_registered_anonymous(anonymous_input_file, given_date, end_date)
    
    registered_sum_revisions = calculate_revision_stats_registered_anonymous(registered_input_file, start_date, end_date)
    registered_sum_revisions_before = calculate_revision_stats_registered_anonymous(registered_input_file, start_date, given_date - pd.DateOffset(days=1))
    registered_sum_revisions_after = calculate_revision_stats_registered_anonymous(registered_input_file, given_date, end_date)
    
    # Calculate the percentage increase in revisions, reverts, and vandalism reverts
    revision_increase_percentage = ((sum_revisions_after - sum_revisions_before) / sum_revisions_before) * 100
    reverts_increase_percentage = ((sum_reverts_after - sum_reverts_before) / sum_reverts_before) * 100
    vandalism_reverts_increase_percentage = ((sum_vandalism_reverts_after - sum_vandalism_reverts_before) / sum_vandalism_reverts_before) * 100
    
    registered_revisions_increase_percentage = ((registered_sum_revisions_after - registered_sum_revisions_before) / registered_sum_revisions_before) * 100
    anonymous_revisions_increase_percentage = ((anonymous_sum_revisions_after - anonymous_sum_revisions_before) / anonymous_sum_revisions_before) * 100
    
    # Calculate the percentage increase in revisions, reverts, and vandalism reverts
    geoloacted_revision_increase_percentage = ((geoloacted_sum_revisions_after - geoloacted_sum_revisions_before) / geoloacted_sum_revisions_before) * 100
    geoloacted_reverts_increase_percentage = ((geoloacted_sum_reverts_after - geoloacted_sum_reverts_before) / geoloacted_sum_reverts_before) * 100
    geoloacted_vandalism_reverts_increase_percentage = ((geoloacted_sum_vandalism_reverts_after - geoloacted_sum_vandalism_reverts_before) / geoloacted_sum_vandalism_reverts_before) * 100
    
    
    # calculate percentage of revisions being registered users
    revisions_being_registered = (registered_sum_revisions / sum_revisions) * 100
    revisions_being_registered_before = (registered_sum_revisions_before / sum_revisions_before) * 100
    revisions_being_registered_after = (registered_sum_revisions_after / sum_revisions_after) * 100
    
    # calculate percentage of revisions being anonymous users
    revisions_being_anonymous = (anonymous_sum_revisions / sum_revisions) * 100
    revisions_being_anonymous_before = (anonymous_sum_revisions_before / sum_revisions_before) * 100
    revisions_being_anonymous_after = (anonymous_sum_revisions_after / sum_revisions_after) * 100
    
    # calculate percentage of revisions being geoloacted
    revisions_being_geoloacted = (geoloacted_sum_revisions / sum_revisions) * 100
    revisions_being_geoloacted_before = (geoloacted_sum_revisions_before / sum_revisions_before) * 100
    revisions_being_geoloacted_after = (geoloacted_sum_revisions_after / sum_revisions_after) * 100
    
    reverts_being_geoloacted = (geoloacted_sum_reverts / sum_reverts) * 100
    reverts_being_geoloacted_before = (geoloacted_sum_reverts_before / sum_reverts_before) * 100
    reverts_being_geoloacted_after = (geoloacted_sum_reverts_after / sum_reverts_after) * 100
    
    vandalism_reverts_being_geoloacted = (geoloacted_sum_vandalism_reverts / sum_vandalism_reverts) * 100
    vandalism_reverts_being_geoloacted_before = (geoloacted_sum_vandalism_reverts_before / sum_vandalism_reverts_before) * 100
    vandalism_reverts_being_geoloacted_after = (geoloacted_sum_vandalism_reverts_after / sum_vandalism_reverts_after) * 100
    
    reverts_being_vandalism = (sum_vandalism_reverts/sum_reverts)*100
    reverts_being_vandalism_before = (sum_vandalism_reverts_before/sum_reverts_before)*100
    reverts_being_vandalism_after = (sum_vandalism_reverts_after/sum_reverts_after)*100
   
    # Calculate the absolute difference in revisions, reverts, and vandalism reverts
    revision_abs_difference = calculate_absolute_difference(sum_revisions_before, sum_revisions_after)
    reverts_abs_difference = calculate_absolute_difference(sum_reverts_before, sum_reverts_after)
    vandalism_reverts_abs_difference = calculate_absolute_difference(sum_vandalism_reverts_before, sum_vandalism_reverts_after)
    
    registered_abs_difference = calculate_absolute_difference(registered_sum_revisions_before, registered_sum_revisions_after)
    anonymous_abs_difference = calculate_absolute_difference(anonymous_sum_revisions_before, anonymous_sum_revisions_after)
    
    # Open the output file in write mode
    with open(output_file +'.txt', 'w') as file:
        file.write("Revisions\n")
        file.write("#Element\t#Total\t#Geoloacted\t#Registered\t#Anonymous\n")
        file.write("Whole_Period\t{:,}\t{:,}\t{:,}\t{:,}\n".format(sum_revisions, geoloacted_sum_revisions, registered_sum_revisions, anonymous_sum_revisions))
        file.write("Percentage\t\t{:.2f}\t{:.2f}\t{:.2f}\n".format(revisions_being_geoloacted, revisions_being_registered, revisions_being_anonymous))
        file.write("Before\t{:,}\t{:,}\t{:,}\t{:,}\n".format(sum_revisions_before, geoloacted_sum_revisions_before, registered_sum_revisions_before, anonymous_sum_revisions_before))
        file.write("Percentage\t\t{:.2f}%\t{:.2f}%\t{:.2f}%\n".format(revisions_being_geoloacted_before, revisions_being_registered_before, revisions_being_anonymous_before))
        file.write("After\t{:,}\t{:,}\t{:,}\t{:,}\n".format(sum_revisions_after, geoloacted_sum_revisions_after, registered_sum_revisions_after, anonymous_sum_revisions_after))
        file.write("Percentage\t\t{:.2f}%\t{:.2f}%\t{:.2f}%\n".format(revisions_being_geoloacted_after, revisions_being_registered_after, revisions_being_anonymous_after))

        if (sum_revisions != (sum_revisions_before + sum_revisions_after)):
            file.write("Number Of revisions don't match with the before and after\n")
                
        file.write("\n\nReverts\n")
        file.write("#Element\t#Total\t#Geoloacted\t#Registered\t#Anonymous\n")
        file.write("Whole_Period\t{:,}\t{:,}\n".format(sum_reverts, geoloacted_sum_reverts))
        file.write("Percentage\t\t{:.2f}\n".format(reverts_being_geoloacted))
        file.write("Before\t{:,}\t{:,}\n".format(sum_reverts_before, geoloacted_sum_reverts_before))
        file.write("Percentage\t\t{:.2f}%\n".format(reverts_being_geoloacted_before))
        file.write("After\t{:,}\t{:,}\n".format(sum_reverts_after, geoloacted_sum_reverts_after))
        file.write("Percentage\t\t{:.2f}%\n".format(reverts_being_geoloacted_after))
        
        if (sum_reverts != (sum_reverts_before + sum_reverts_after)):
            file.write("Number Of reverts don't match with the before and after\n")
            
        file.write("\n\nVandalism\n")
        file.write("#Element\t#Total\t#Geoloacted\t#Registered\t#Anonymous\n")
        file.write("Whole_Period\t{:,}\t{:,}\n".format(sum_vandalism_reverts, geoloacted_sum_vandalism_reverts))
        file.write("Percentage\t\t{:.2f}\n".format(vandalism_reverts_being_geoloacted))
        file.write("Before\t{:,}\t{:,}\n".format(sum_vandalism_reverts_before, geoloacted_sum_vandalism_reverts_before))
        file.write("Percentage\t\t{:.2f}%\n".format(vandalism_reverts_being_geoloacted_before))
        file.write("After\t{:,}\t{:,}\n".format(sum_vandalism_reverts_after, geoloacted_sum_vandalism_reverts_after))
        file.write("Percentage\t\t{:.2f}%\n".format(vandalism_reverts_being_geoloacted_after))
        
        file.write("\n\nIncreasement\n")
        file.write("#Element\t#Total\t#Geoloacted\t#Registered\t#Anonymous\n")
        file.write("Revisions\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\n".format(revision_increase_percentage, geoloacted_revision_increase_percentage, registered_revisions_increase_percentage, anonymous_revisions_increase_percentage))
        file.write("Reverts\t{:.2f}\t{:.2f}\n".format(reverts_increase_percentage, geoloacted_reverts_increase_percentage))
        file.write("Reverts\t{:.2f}\t{:.2f}\n".format(vandalism_reverts_increase_percentage, geoloacted_vandalism_reverts_increase_percentage))


        if (sum_vandalism_reverts != (sum_vandalism_reverts_before + sum_vandalism_reverts_after)):
            file.write("Number Of vandalism reverts don't match with the before and after\n")
        
        # Geoloacted 
        if (geoloacted_sum_revisions != (geoloacted_sum_revisions_before + geoloacted_sum_revisions_after)):
            file.write("Number Of geoloacted revisions don't match with the before and after\n")
            
        if (geoloacted_sum_reverts != (geoloacted_sum_reverts_before + geoloacted_sum_reverts_after)):
            file.write("Number Of geoloacted reverts don't match with the before and after\n")
        

        if (geoloacted_sum_vandalism_reverts != (geoloacted_sum_vandalism_reverts_before + geoloacted_sum_vandalism_reverts_after)):
            file.write("Number Of geoloacted vandalism reverts don't match with the before and after\n")


        if (sum_revisions != (registered_sum_revisions + anonymous_sum_revisions)):
            file.write("Number Of registered and anonymous revisions don't match with all revisions\n")
            
        if (anonymous_sum_revisions != (anonymous_sum_revisions_before + anonymous_sum_revisions_after)):
            file.write("Number Of anonymous revisions don't match with the before and after\n")
            
        if (registered_sum_revisions != (registered_sum_revisions_before + registered_sum_revisions_after)):
            file.write("Number Of registered revisions don't match with the before and after\n")
        
    before_event_edits = get_data(date_summation, start_date, given_date_a_day_before, '#num-revisions')
    after_event_edits = get_data(date_summation, given_date, end_date, '#num-revisions')
    
    before_event_reg_edits = get_data(registered_input_file, start_date, given_date_a_day_before, '#num-revisions')
    after_event_reg_edits = get_data(registered_input_file, given_date, end_date, '#num-revisions')

    before_event_reverts = get_data(date_summation,start_date, given_date_a_day_before, '#num-reverted-revisions')
    after_event_reverts = get_data(date_summation,given_date, end_date, '#num-reverted-revisions')

    before_event_vand = get_data(date_summation,start_date, given_date_a_day_before, '#num-vandalism-comment-reverted-revisions')
    after_event_vand = get_data(date_summation,given_date, end_date, '#num-vandalism-comment-reverted-revisions')
    
    # Perform Welch's t-test
    ttest_edits = pg.ttest(before_event_edits, after_event_edits)
    
    # Perform Welch's t-test
    ttest_reg_edits = pg.ttest(before_event_reg_edits, after_event_reg_edits)

    # Perform Welch's t-test
    ttest_reverts = pg.ttest(before_event_reverts, after_event_reverts)

    # Perform Welch's t-test
    ttest_vand = pg.ttest(before_event_vand, after_event_vand)
    
        
    p_value_edits = get_asterisks(ttest_edits['p-val'].values[0])
    
    p_value_reg_edits = get_asterisks(ttest_reg_edits['p-val'].values[0])

    p_value_reverts = get_asterisks(ttest_reverts['p-val'].values[0])

    p_value_vand = get_asterisks(ttest_vand['p-val'].values[0])

        

    table_string = r'''
\begin{{table}}[H]
\scriptsize
\caption{{Analysis of edits during the {table_event_name} on {given_date_string}. Table shows total, registered, reverted, and vandalism-reverted edits for related articles. Covers 8 weeks ({start_date} - {end_date}), 4 before and 4 after the event. Counts provided for both periods, with absolute difference, relative change,  and Cohen’s \textit{{d}}, with one to three asterisks (*) indicating \textit{{p}}-values less or equal to 0.05, 0.01, and 0.001.}}
\label{{table:{table_event_name}}}
\setlength{{\tabcolsep}}{{5.6pt}}
\centering
\begin{{tabular}}{{@{{}}l@{{\hspace{{12pt}}}}cccccc@{{}}}}
\toprule
\bfseries Edits Analysis & \multicolumn{{3}}{{c}}{{\bfseries Counts}} & \multicolumn{{3}}{{c}}{{\bfseries Change}}\\ 
\cmidrule(r{{\tabcolsep}}){{2-4}}
\cmidrule(l{{\tabcolsep}}){{5-7}}
& {{$\sum$}} & {{$\leftarrow$}} & {{$\rightarrow$}} & {{Abs.}} & {{Rel.}} & {{\textit{{d}}}}\\
\midrule
{{Total Edits}} & {total_edits} & {before_total} & {after_total} & {abs_total} & {change_total_percentage}\% & {cohens_d_edits}{p_value_edits}\\
{{Registered Edits}} & {reg_edits_phan}{registered_users_total} & {reg_edits_phan_before}{registered_users_before} & {reg_edits_phan_after}{registered_users_after}  & {reg_edits_phan_abs}{abs_registered} & {reg_edits_phan_change}{change_registered_users_percentage}\% & {cohens_d_reg_edits}{p_value_reg_edits}\\
{{Reverted Edits}} & {reverts_phan}{reverted_edits_total} & {reverts_phan_before}{reverted_edits_before}  & {reverts_phan_after}{reverted_edits_after} & {reverts_phan_abs}{abs_reverts} & {reverts_phan_change}{change_reverted_edits_percentage}\% & {cohens_d_reverts}{p_value_reverts}\\
{{Vandalism Reverted Edits}} & {vand_phan}{vandalism_reverted_total}  & {vand_phan_before}{vandalism_reverted_before} & {vand_phan_after}{vandalism_reverted_after}  & {vand_phan_abs}{abs_vandalism_reverts} & {vand_phan_change}{change_vandalism_reverted_percentage}\% & {cohens_d_vand}{p_value_vand}\\
\bottomrule
\end{{tabular}}\end{{table}}



For all events table:
{{table_event_name}} & {total_edits} & {before_total} & {after_total} & {change_total_percentage}\% & {reverted_edits_before}  & {reverted_edits_after} & {change_reverted_edits_percentage}\% & {vandalism_reverted_before} & {vandalism_reverted_after} & {change_vandalism_reverted_percentage}\%\\
'''
    
    # Create the dictionary with the necessary keys and values
    format_dict = {
    'table': table_string,
    'total_edits': "{:,}".format(sum_revisions),
    'geolocated_total': "{:,}".format(geoloacted_sum_revisions),
    'geolocated_percentage': "{:.0f}".format(revisions_being_geoloacted),
    'registered_users_total': "{:,}".format(registered_sum_revisions),
    'registered_users_percentage': "{:.0f}".format(revisions_being_registered),
    'reverted_edits_total': "{:,}".format(sum_reverts),
    'geolocated_reverted': "{:,}".format(geoloacted_sum_reverts),
    'geolocated_reverted_percentage': "{:.0f}".format(reverts_being_geoloacted),
    'vandalism_reverted_total': "{:,}".format(sum_vandalism_reverts),
    'geolocated_vandalism_reverted': "{:,}".format(geoloacted_sum_vandalism_reverts),
    'geolocated_vandalism_reverted_percentage': "{:.0f}".format(vandalism_reverts_being_geoloacted),
    
    
    'before_total': "{:,}".format(sum_revisions_before),
    'geolocated_before': "{:,}".format(geoloacted_sum_revisions_before),
    'geolocated_before_percentage': "{:.0f}".format(revisions_being_geoloacted_before),
    'registered_users_before': "{:,}".format(registered_sum_revisions_before),
    'registered_users_before_percentage': "{:.0f}".format(revisions_being_registered_before),
    'reverted_edits_before': "{:,}".format(sum_reverts_before),
    'geolocated_reverted_before': "{:,}".format(geoloacted_sum_reverts_before),
    'geolocated_reverted_before_percentage': "{:.0f}".format(reverts_being_geoloacted_before),
    'vandalism_reverted_before': "{:,}".format(sum_vandalism_reverts_before),
    'geolocated_vandalism_reverted_before': "{:,}".format(geoloacted_sum_vandalism_reverts_before),
    'geolocated_vandalism_reverted_before_percentage': "{:.0f}".format(vandalism_reverts_being_geoloacted_before),
    
    
    'after_total': "{:,}".format(sum_revisions_after),
    'geolocated_after': "{:,}".format(geoloacted_sum_revisions_after),
    'geolocated_after_percentage': "{:.0f}".format(revisions_being_geoloacted_after),
    'registered_users_after': "{:,}".format(registered_sum_revisions_after),
    'registered_users_after_percentage': "{:.0f}".format(revisions_being_registered_after),
    'reverted_edits_after': "{:,}".format(sum_reverts_after),
    'geolocated_reverted_after': "{:,}".format(geoloacted_sum_reverts_after),
    'geolocated_reverted_after_percentage': "{:.0f}".format(reverts_being_geoloacted_after),
    'vandalism_reverted_after': "{:,}".format(sum_vandalism_reverts_after),
    'geolocated_vandalism_reverted_after': "{:,}".format(geoloacted_sum_vandalism_reverts_after),
    'geolocated_vandalism_reverted_after_percentage': "{:.0f}".format(vandalism_reverts_being_geoloacted_after),
    
    
    'change_total_percentage': "{:,.0f}".format(revision_increase_percentage),
    'change_geolocated_percentage': "{:,.0f}".format(geoloacted_revision_increase_percentage),
    'change_registered_users_percentage': "{:,.0f}".format(registered_revisions_increase_percentage),
    'change_reverted_edits_percentage': "{:,.0f}".format(reverts_increase_percentage),
    'change_geolocated_reverted_percentage': "{:,.0f}".format(geoloacted_reverts_increase_percentage),
    'change_vandalism_reverted_percentage': "{:,.0f}".format(vandalism_reverts_increase_percentage),
    'change_geolocated_vandalism_reverted_percentage': "{:,.0f}".format(geoloacted_vandalism_reverts_increase_percentage),
    
    'reverts_being_vandalism': "{:.0f}".format(reverts_being_vandalism),
    'reverts_being_vandalism_before': "{:.0f}".format(reverts_being_vandalism_before),
    'reverts_being_vandalism_after': "{:.0f}".format(reverts_being_vandalism_after),

    
    'abs_total': "{:,}".format(revision_abs_difference),
    'abs_registered': "{:,}".format(registered_abs_difference),
    'abs_reverts': "{:,}".format(reverts_abs_difference),
    'abs_vandalism_reverts': "{:,}".format(vandalism_reverts_abs_difference),
    
    'table_event_name': "{}".format(event_name_for_latex),
    'given_date_string': "{}".format(given_date_string),
    'start_date': "{}".format(start_date_string),
    'end_date': "{}".format(end_date_string),
    
    'p_value_edits' : "{}".format(p_value_edits),
    'cohens_d_edits' : "{}".format(round(ttest_edits['cohen-d'].values[0],2)),
    
    'p_value_reg_edits' : "{}".format(p_value_reg_edits),
    'cohens_d_reg_edits' : "{}".format(round(ttest_reg_edits['cohen-d'].values[0],2)),

    'p_value_reverts' : "{}".format(p_value_reverts),
    'cohens_d_reverts' : "{}".format(round(ttest_reverts['cohen-d'].values[0],2)),

    'p_value_vand' : "{}".format(p_value_vand),
    'cohens_d_vand' : "{}".format(round(ttest_vand['cohen-d'].values[0],2)),
    
    'reg_edits_phan' : "{}".format(compare_digits(sum_revisions,registered_sum_revisions)),
    'reverts_phan' : "{}".format(compare_digits(sum_revisions,sum_reverts)),
    'vand_phan' : "{}".format(compare_digits(sum_revisions,sum_vandalism_reverts)),
    
    'reg_edits_phan_before' : "{}".format(compare_digits(sum_revisions_before,registered_sum_revisions_before)),
    'reverts_phan_before' : "{}".format(compare_digits(sum_revisions_before,sum_reverts_before)),
    'vand_phan_before' : "{}".format(compare_digits(sum_revisions_before,sum_vandalism_reverts_before)),
    
    'reg_edits_phan_after' : "{}".format(compare_digits(sum_revisions_after,registered_sum_revisions_after)),
    'reverts_phan_after' : "{}".format(compare_digits(sum_revisions_after,sum_reverts_after)),
    'vand_phan_after' : "{}".format(compare_digits(sum_revisions_after,sum_vandalism_reverts_after)),
    
    'reg_edits_phan_abs' : "{}".format(compare_digits(revision_abs_difference,registered_abs_difference)),
    'reverts_phan_abs' : "{}".format(compare_digits(revision_abs_difference,reverts_abs_difference)),
    'vand_phan_abs' : "{}".format(compare_digits(revision_abs_difference,vandalism_reverts_abs_difference)),
    
    'reg_edits_phan_change' : "{}".format(compare_digits("{:.0f}".format(revision_increase_percentage),"{:.0f}".format(registered_revisions_increase_percentage))),
    'reverts_phan_change' : "{}".format(compare_digits("{:.0f}".format(revision_increase_percentage),"{:.0f}".format(reverts_increase_percentage))),
    'vand_phan_change' : "{}".format(compare_digits("{:.0f}".format(revision_increase_percentage),"{:.0f}".format(vandalism_reverts_increase_percentage))),
    }

    # print(len(str("{:.0f}".format(revision_increase_percentage))))
    # print(len(str("{:.0f}".format(vandalism_reverts_increase_percentage))))
    # Format the table string with the dictionary
    table_string = table_string.format(**format_dict)

    # Open the output file in write mode
    with open("..\Events/"+ base_file_name+ '/Latex_stats_table.txt', 'w') as file:
        # Write the modified LaTeX code as a raw string
        file.write(rf"{table_string}")
        
# Read the config file
with open('config.json', 'r') as file:
    config = json.load(file)

# Retrieve the variables
given_date = pd.Timestamp(config['given_date'])
file_name = config['input_file']
base_file_name = file_name.rsplit(".", 2)[0]
event_name_for_latex = config['event_name_for_latex']
 
# specify input file paths
input_directory = "..\Events/"+ base_file_name +"/counts"
date_summation = os.path.join(input_directory,"by_date_counts.txt")
geoloacted_date_summation = os.path.join(input_directory,"GEOLOCATED_by_date_counts.txt")
anonymous_date_summation = os.path.join(input_directory,"ANONYMOUS_by_date_counts.txt")
registered_date_summation = os.path.join(input_directory,"REGISTERED_by_date_counts.txt")

output_directory = "..\Events/"+ base_file_name +"/analysis_results"
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
given_date_a_day_before = (given_date - pd.DateOffset(days=1))

analyse_revisions(date_summation, geoloacted_date_summation, anonymous_date_summation, registered_date_summation, given_date, start_date, end_date, os.path.join(output_directory,'revisions_stats'))

print("Revision Analysis Done...")


# geo_before_event_edits = get_data(geoloacted_date_summation, start_date, given_date_a_day_before, '#num-revisions')
# geo_after_event_edits = get_data(geoloacted_date_summation, given_date, end_date, '#num-revisions')

# geo_before_event_reverts = get_data(geoloacted_date_summation,start_date, given_date_a_day_before, '#num-reverted-revisions')
# geo_after_event_reverts = get_data(geoloacted_date_summation,given_date, end_date, '#num-reverted-revisions')

# geo_before_event_vand = get_data(geoloacted_date_summation,start_date, given_date_a_day_before, '#num-vandalism-comment-reverted-revisions')
# geo_after_event_vand = get_data(geoloacted_date_summation,given_date, end_date, '#num-vandalism-comment-reverted-revisions')

# # Perform Welch's t-test
# ttest_edits = pg.ttest(geo_before_event_edits, geo_after_event_edits)
# print(ttest_edits)
# print(get_asterisks(ttest_edits['p-val'].values[0]))

# # Perform Welch's t-test
# ttest_reverts = pg.ttest(geo_before_event_reverts, geo_after_event_reverts)
# print(ttest_edits)
# print(get_asterisks(ttest_reverts['p-val'].values[0]))


# # Perform Welch's t-test
# ttest_vand = pg.ttest(geo_before_event_vand, geo_after_event_vand)

# print(ttest_vand)
# print(get_asterisks(ttest_vand['p-val'].values[0]))