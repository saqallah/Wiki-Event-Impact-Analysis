import os
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import json

def plot_revisions(event_name_for_latex, input_file, geolocated_input_file, anonymous_input_file, registered_input_file, start_date, end_date, vertical_line_date, interval_by_days, graph_name):
    # Load the data from the txt file into a pandas DataFrame
    data = pd.read_csv(input_file, delimiter='\t')
    geolocated_data = pd.read_csv(geolocated_input_file, delimiter='\t')
    anonymous_data = pd.read_csv(anonymous_input_file, delimiter='\t')
    registered_data = pd.read_csv(registered_input_file, delimiter='\t')
    
    # Convert the date column to a pandas datetime object
    data['date'] = pd.to_datetime(data['date'])
    geolocated_data['date'] = pd.to_datetime(geolocated_data['date'])
    anonymous_data['date'] = pd.to_datetime(anonymous_data['date'])
    registered_data['date'] = pd.to_datetime(registered_data['date'])
    
    # Set the date column as the index
    data = data.set_index('date')
    geolocated_data = geolocated_data.set_index('date')
    anonymous_data = anonymous_data.set_index('date')
    registered_data = registered_data.set_index('date')
    
    # Reindex the DataFrames with a complete date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    data = data.reindex(date_range, fill_value=0)
    geolocated_data = geolocated_data.reindex(date_range, fill_value=0)
    anonymous_data = anonymous_data.reindex(date_range, fill_value=0)
    registered_data = registered_data.reindex(date_range, fill_value=0)
    
    # Create a new figure and axis object
    fig, ax = plt.subplots(figsize=(20, 5))
    
    # Plot the #num-revisions data
    ax.plot(data.index, data['#num-revisions'], label='Total Edits', color='cornflowerblue')
    # ax.plot(geolocated_data.index, geolocated_data['#num-revisions'], label='Geolocated Edits', color='purple')
    ax.plot(anonymous_data.index, anonymous_data['#num-revisions'], label='Anonymous Edits', color='darkorange')
    # ax.plot(registered_data.index, registered_data['#num-revisions'], label='Registered Revisions', color='green')
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), fontsize='large',  framealpha=0.0)

    # Set the y-axis label
    ax.set_ylabel('Count', fontname='Arial', fontsize='medium')

    # Set the title of the plot
    ax.set_title('Edits over Time', fontname='Arial', fontsize='large')

    # Format the date labels on the x-axis to show only the month and day
    date_fmt = mdates.DateFormatter('%a %y-%m-%d')  # Include day of the week
    ax.xaxis.set_major_formatter(date_fmt)
    
    # Set the x-axis label
    ax.set_xlabel('Date (Day YY-MM-DD)', fontname='Arial', fontsize='medium')

    # Set the frequency of the x-axis ticks to show every day
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval_by_days))

    # Add a grid to the plot
    ax.grid(True, alpha=0.75, linestyle='dotted')

    # Set the background color of the plot
    ax.set_facecolor('#F8F8F8')

    # Rotate the x-axis labels vertically
    plt.xticks(rotation='vertical', fontsize='small')
    
    yticks = list(range(0, max(data['#num-revisions'].max(), geolocated_data['#num-revisions'].max()) + 10, 10))
    ax.set_yticks(yticks)
    ax.tick_params(axis='y', labelsize='small')
    
    # Set the range for the x-axis
    ax.set_xlim(start_date, end_date)
    
    # Add a title inside the plot
    ax.text(0.02, 0.95, (event_name_for_latex + "\n" + vertical_line_date.strftime('%Y-%m-%d')), transform=ax.transAxes,
        horizontalalignment='left', verticalalignment='top',
        fontsize=16)
    
    # Add a vertical line to highlight the specific date
    ax.axvline(pd.Timestamp(vertical_line_date), color='k', linestyle='--', alpha=0.5)
    # Save the plot as a PNG image
    plt.savefig(os.path.join(output_directory,graph_name + '.png'), dpi=300, bbox_inches='tight')
    
    ## save to all plots folder
    # plt.savefig(os.path.join(output_all_plots,graph_name + '.png'), dpi=300, bbox_inches='tight')

    # Show the plot
    # plt.show()



def plot_reverts(event_name_for_latex, input_file, geolocated_input_file, start_date, end_date, vertical_line_date, graph_name):
    # Load the data from the txt file into a pandas DataFrame
    data = pd.read_csv(input_file, delimiter='\t')
    geolocated_data = pd.read_csv(geolocated_input_file, delimiter='\t')

    # Convert the date column to a pandas datetime object
    data['date'] = pd.to_datetime(data['date'])
    geolocated_data['date'] = pd.to_datetime(geolocated_data['date'])

    # Set the date column as the index
    data = data.set_index('date')
    geolocated_data = geolocated_data.set_index('date')

    # Reindex the DataFrames with a complete date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    data = data.reindex(date_range, fill_value=0)
    geolocated_data = geolocated_data.reindex(date_range, fill_value=0)

    # Create a new figure and axis object
    fig, ax = plt.subplots(figsize=(20, 5))

    # Plot the #num-reverted-revisions data as bars
    ax.bar(data.index, data['#num-reverted-revisions'], label='Total Reverted Edits',color='cornflowerblue') #color='lightsteelblue')

    # # Plot the geolocated revisions
    # ax.bar(geolocated_data.index, geolocated_data['#num-reverted-revisions'], label='Geolocated Reverted Edits', color='cornflowerblue')

    # # Plot the geolocated revisions
    # ax.bar(geolocated_data.index, geolocated_data['#num-vandalism-comment-reverted-revisions'], label='Geolocated Vandalism Reverted Edits', color='darkorange')

    # Plot the #num-vandalism-comment-reverted-revisions data as bars
    ax.bar(data.index, data['#num-vandalism-comment-reverted-revisions'], label='Vandalism Reverted Edits', color='darkorange') #color='wheat')

    # # Add a legend to the plot
    # ax.legend(loc='best', fontsize='small')
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), fontsize='large', framealpha=0.0)

    # Set the y-axis label
    ax.set_ylabel('Count', fontname='Arial', fontsize='medium')

    # Set the title of the plot
    ax.set_title('Reverted Edits over Time', fontname='Arial', fontsize='large')

    # Format the date labels on the x-axis to show only the month and day
    date_fmt = mdates.DateFormatter('%a  %y-%m-%d')  # Include day of the week
    ax.xaxis.set_major_formatter(date_fmt)

    # Set the x-axis label
    ax.set_xlabel('Date (Day YY-MM-DD)', fontname='Arial', fontsize='medium')

    # Set the frequency of the x-axis ticks to show every day
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

    # Set the frequency of the y-axis ticks to show every 2
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))

    # Add a grid to the plot
    ax.grid(True, alpha=0.75, linestyle='dotted')

    # Set the background color of the plot
    ax.set_facecolor('#F8F8F8')

    # Rotate the x-axis labels vertically
    plt.xticks(rotation='vertical', fontsize='small')

    # Add a vertical line to highlight the specific date
    ax.axvline(pd.Timestamp(vertical_line_date), color='k', linestyle='--', alpha=0.5)

    # Set the range for the x-axis
    ax.set_xlim(start_date - pd.DateOffset(days=1), end_date + pd.DateOffset(days=1))

    # Add a vertical line to highlight the specific date
    ax.axvline(pd.Timestamp(vertical_line_date), color='k', linestyle='--', alpha=0.5)
    
    # Add a title inside the plot
    ax.text(0.02, 0.95, (event_name_for_latex + "\n" + vertical_line_date.strftime('%Y-%m-%d')), transform=ax.transAxes,
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)  # , fontweight='bold')

    # Save the plot as a PNG image
    plt.savefig(os.path.join(output_directory,graph_name + '.png'), dpi=300, bbox_inches='tight')
    # plt.savefig(os.path.join(output_all_plots,graph_name + '.png'), dpi=300, bbox_inches='tight')

    # Show the plot
    # plt.show()


# Read the config file
with open('config.json', 'r') as file:
    config = json.load(file)

# Config
given_date = pd.Timestamp(config['given_date'])
event_name_for_latex = config['event_name_for_latex']
file_name = config['input_file']

base_file_name = file_name.rsplit(".", 2)[0]
input_directory = "..\data"
name_for_plotting = file_name.rsplit("_", 1)[0]


weeks_before = 4
weeks_after = 4
start_date_year = given_date- pd.DateOffset(months=6)
end_date_year = given_date + pd.DateOffset(months=6)
start_date = given_date - pd.DateOffset(weeks=weeks_before)
end_date = given_date + pd.DateOffset(weeks=weeks_after)


given_date_string = given_date.strftime('%Y-%m-%d')
given_date_string_a_day_before = (given_date - pd.DateOffset(days=1)).strftime('%Y-%m-%d')
start_date_string = start_date.strftime('%Y-%m-%d')
end_date_string = end_date.strftime('%Y-%m-%d')
start_date_yearly_string = start_date_year.strftime('%Y-%m-%d')
end_date_yearly_string = end_date_year.strftime('%Y-%m-%d')
vertical_line_date = given_date

input_path = os.path.join(input_directory, file_name)

# specify input file paths
input_directory = "..\Events/"+ base_file_name +"/counts"
date_summation = os.path.join(input_directory,"by_date_counts.txt")
geoloacted_date_summation = os.path.join(input_directory,"GEOLOCATED_by_date_counts.txt")
anonymous_date_summation = os.path.join(input_directory,"ANONYMOUS_by_date_counts.txt")
registered_date_summation = os.path.join(input_directory,"REGISTERED_by_date_counts.txt")

output_directory = "..\Events/"+ base_file_name + "/plots"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# output_all_plots = "..\Events/all_plots"
# if not os.path.exists(output_all_plots):
#     os.makedirs(output_all_plots)

#Plotting
plot_revisions(event_name_for_latex, date_summation, geoloacted_date_summation, anonymous_date_summation, registered_date_summation, start_date, end_date, vertical_line_date, 1, 'revisions_plot_'+name_for_plotting)
plot_revisions(event_name_for_latex, date_summation, geoloacted_date_summation, anonymous_date_summation, registered_date_summation, start_date_year, end_date_year, vertical_line_date, 14, 'revisions_plot_yearly_'+name_for_plotting)
plot_reverts(event_name_for_latex, date_summation, geoloacted_date_summation, start_date, end_date, vertical_line_date, 'reverts_plot_'+ name_for_plotting)

print("Revision Plotting Done...")

plotting_text = r'''
\begin{{figure}}[p]
  \centering
  \subfloat[Total and anonymous edits over an 8 weeks analysis period.]{{\includegraphics[width=\textwidth, keepaspectratio]{{Figures/Events/{4_weeks_name}.png}}\label{{fig:{4_Weeks_label}}}}}
  \hfill
  \subfloat[Total and anonymous edits over a 12 months analysis period.]{{\includegraphics[width=\textwidth, keepaspectratio]{{Figures/Events/{6_months_name}.png}}\label{{fig:{6_months_label}}}}}
  \hfill
  \subfloat[Reverted edits and reverted-vandalism edits over an 8 weeks analysis period.]{{\includegraphics[width=\textwidth, keepaspectratio]{{Figures/Events/{reverts_4_weeks_name}.png}}\label{{fig:{reverts_4_weeks_label}}}}}
  \caption{{Edits, reverted edits, including anonymous edits and vandalism-reverted edits during the {event_name} on {event_date}. Plots (a) and (c) cover an 8-week period ({start_date} - {end_date}), with 4 weeks before and after. Plot (b) covers a 12-month period ({start_date_yearly} - {end_date_yearly}), with 6 months before and after.}}
  \label{{fig:{both_label}}}
\end{{figure}}'''

# \begin{{figure}}[H]
#   \begin{{center}}
#   \includegraphics[width=\textwidth, keepaspectratio]{{Figures/Events/{reverts_4_weeks_name}.png}}
#   \end{{center}}
#   \caption{{Number of reverted edits over time, including vandalism-reverted edits during the {event_name} on {event_date}. Covers 8 weeks ({start_date} - {end_date}), 4 before and 4 after.}}
#   \label{{fig:{reverts_4_weeks_label}}}
# \end{{figure}}
# Create the dictionary with the necessary keys and values
format_dict = {
'4_weeks_name': "{}".format('revisions_plot_'+ name_for_plotting),
'4_Weeks_label': "{}".format('revisions_plot_'+ name_for_plotting),
'6_months_name': "{}".format('revisions_plot_yearly_'+ name_for_plotting),
'6_months_label': "{}".format('revisions_plot_yearly_'+ name_for_plotting),
'both_label':"{}".format('edits_plot_'+ name_for_plotting),
'event_name':"{}".format(event_name_for_latex),
'event_date': "{}".format(given_date_string),
'start_date': "{}".format(start_date_string),
'end_date': "{}".format(end_date_string),
'start_date_yearly': "{}".format(start_date_yearly_string),
'end_date_yearly': "{}".format(end_date_yearly_string),

'reverts_4_weeks_name': "{}".format('reverts_plot_'+ name_for_plotting),
'reverts_4_weeks_label': "{}".format('reverts_plot_'+ name_for_plotting),
}

# Format the table string with the dictionary
plotting_text = plotting_text.format(**format_dict)
    

# Open the output file in write mode
with open("..\Events/"+ base_file_name+ '/Latex_plotting_text.txt', 'w') as file:
    # Write the modified LaTeX code as a raw string
    file.write(rf"{plotting_text}")