import xml.etree.ElementTree as ET
import gzip
import time
import wikipedia
import requests
import os


def get_max_search_results(search_words):
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_words,
        "format": "json",
        "sroffset": 0,
        "srlimit": 1
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    if "query" in data and "searchinfo" in data["query"]:
        search_info = data["query"]["searchinfo"]
        if "totalhits" in search_info:
            return int(search_info["totalhits"])
    return 0



word_to_search = "Legalization of cannabis in Canada"
output_name = word_to_search.replace(" ", "_")
print(output_name)

num_of_articles = 50
#article_names = []
article_names = wikipedia.search(word_to_search, results= num_of_articles)
print(article_names)


article_ids = []
  
for name in article_names:
    api_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info&titles=" + name
    response = requests.get(api_url)
    try:
        page_id = list(response.json()["query"]["pages"].values())[0]["pageid"]
        article_ids.append(page_id)
    except KeyError:
        print(f"No pageid found for article: {name}")

print(article_ids)

# # for article_id in article_ids:
# #     url = "http://en.wikipedia.org/wiki?curid=" + str(page_id)
# #     print(url)
# # ## http://en.wikipedia.org/wiki?curid=42085878

# Define a dictionary that maps ID ranges to filenames
id_range_to_file = {
    range(10, 41242): "enwiki-20230101-stub-meta-history1.xml.gz",
    range(41243, 151573): "enwiki-20230101-stub-meta-history2.xml.gz",
    range(151574, 311328): "enwiki-20230101-stub-meta-history3.xml.gz",
    range(311330, 558390): "enwiki-20230101-stub-meta-history4.xml.gz",
    range(558393, 958045): "enwiki-20230101-stub-meta-history5.xml.gz",
    range(958048, 1483661): "enwiki-20230101-stub-meta-history6.xml.gz",
    range(1483662, 2134111): "enwiki-20230101-stub-meta-history7.xml.gz",
    range(2134116, 2936258): "enwiki-20230101-stub-meta-history8.xml.gz",
    range(2936265, 4045399): "enwiki-20230101-stub-meta-history9.xml.gz",
    range(4045403, 5399356): "enwiki-20230101-stub-meta-history10.xml.gz",
    range(5399372, 7054856): "enwiki-20230101-stub-meta-history11.xml.gz",
    range(7054862, 9172787): "enwiki-20230101-stub-meta-history12.xml.gz",
    range(9172789, 11659678): "enwiki-20230101-stub-meta-history13.xml.gz",
    range(11659683, 14324602): "enwiki-20230101-stub-meta-history14.xml.gz",
    range(14324603, 17460148): "enwiki-20230101-stub-meta-history15.xml.gz",
    range(17460155, 20570376): "enwiki-20230101-stub-meta-history16.xml.gz",
    range(20570398, 23716196): "enwiki-20230101-stub-meta-history17.xml.gz",
    range(23716198, 27121847): "enwiki-20230101-stub-meta-history18.xml.gz",
    range(27121880, 31308441): "enwiki-20230101-stub-meta-history19.xml.gz",
    range(31308447, 35522426): "enwiki-20230101-stub-meta-history20.xml.gz",
    range(35522434, 39996241): "enwiki-20230101-stub-meta-history21.xml.gz",
    range(39996250, 44788921): "enwiki-20230101-stub-meta-history22.xml.gz",
    range(44788989, 50564548): "enwiki-20230101-stub-meta-history23.xml.gz",
    range(50564555, 57025645): "enwiki-20230101-stub-meta-history24.xml.gz",
    range(57025665, 62585846): "enwiki-20230101-stub-meta-history25.xml.gz",
    range(62585868, 63975837): "enwiki-20230101-stub-meta-history26.xml.gz",
    range(63975922, 72638791): "enwiki-20230101-stub-meta-history27.xml.gz"
}


specific_ids = []
for integer in article_ids:
    string = str(integer)
    specific_ids.append(string)

print(specific_ids)


specific_ids_sorted = sorted(specific_ids)

# Create an empty list to store the selected pages
selected_pages = []

# Create a dictionary to map specific IDs to file names
id_to_file = {}

# Iterate over the specific IDs and find the corresponding file names
for id in specific_ids_sorted:
    for id_range, file_name in id_range_to_file.items():
        if int(id) in id_range:
            # Add the ID and file name to the dictionary
            if file_name not in id_to_file:
                id_to_file[file_name] = [id]
            else:
                id_to_file[file_name].append(id)
            break

# Print the resulting dictionary
print(id_to_file)

# Iterate over the files that contain the specific IDs and extract the pages
for file_name, ids in id_to_file.items():
    count_ids = len(ids)
    
    # Get the full path of the file
    file_path = os.path.join('../enwiki-20230101-geolocated-data', file_name)
    # Open the gzip file and parse the XML
    with gzip.open(file_path, 'rb') as f:
        # Record the start time
        start_time = time.time()
        # Create an incremental parser
        context = ET.iterparse(f, events=("start", "end"))
        # Get the root element
        _, root = next(context)
        # Loop through all of the "page" elements in the tree
        print(f"Searching {file_name}...") # Print statement to indicate which file is being searched
        print(f"for these {ids}")
        # Keep track of the number of IDs found
        num_ids_found = 0
        for event, page in context:
            if event == "end" and page.tag == "page":
                page_id = page.get("id")
                # Check if the "id" attribute matches one of the specific IDs
                if page_id in ids:
                    # Append the entire "page" element to the list of selected pages
                    selected_pages.append(page)
                    print(f"{page_id} found")
                    # Increment the number of IDs found
                    num_ids_found += 1
                    # Remove the found ID from the list to avoid unnecessary comparisons
                    ids.remove(page_id)
                    #print how many left
                    print(str(num_ids_found) +" IDs found, " + str(len(ids)) + " left")
                    # If all the specific IDs have been found, break out of the loop
                    if num_ids_found == count_ids:
                        break
                # Clear the page element to reduce memory usage
                root.clear()
                
        # Record the end time and print the elapsed time
        end_time = time.time()
        print("Elapsed time for Parsing: {:.2f} seconds".format(end_time - start_time))
        # If all the specific IDs have been found, break out of the loop
        if num_ids_found == len(specific_ids):
            break

# Create a new XML tree with a root element "pages"
new_root = ET.Element("pages")
# Append all of the selected pages to the new tree
for page in selected_pages:
    new_root.append(page)


output_directory = "..\data/"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
    
# Create a new compressed file and write the new XML tree to it
# with gzip.open(word_to_search +"_"+ str(num_of_articles)+".xml.gz", "wb") as f:
with gzip.open(os.path.join(output_directory, output_name+"_"+ str(num_of_articles)+".xml.gz"), "wb") as f:
    tree = ET.ElementTree(new_root)
    tree.write(f, encoding="utf-8", xml_declaration=True)
