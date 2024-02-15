import requests
from bs4 import BeautifulSoup as bs
import csv
import sys

def parse(url):
    """
    Parse URL, then return bs object
    """
    response = requests.get(url)
    return bs(response.content, "html.parser")

def extract_location_details(cells):
    """
    Extract location details from cells
    """
    location_code = cells[0].text
    location = cells[1].text.strip()
    a_tag = cells[0].find("a")
    if a_tag and "href" in a_tag.attrs:
        location_url_suffix = a_tag["href"]
        location_url = f"https://volby.cz/pls/ps2017nss/{location_url_suffix}"
        return location_code, location, location_url
    return None, None, None

def extract_voting_data(location_soup):
    """
    Extract voting data from location soup
    """
    registered_voters = location_soup.find("td", headers="sa2").text.replace("\xa0", " ")
    envelopes = location_soup.find("td", headers="sa3").text.replace("\xa0", " ")
    valid_votes = location_soup.find("td", headers="sa6").text.replace("\xa0", " ")

    votes = []
    for vote_header in ["t1sb3", "t2sb3"]:
        vote_cells = location_soup.find_all("td", headers=vote_header)
        for vote_cell in vote_cells:
            vote = vote_cell.text.replace("\xa0", " ")
            if vote != "-":
                votes.append(vote)

    return registered_voters, envelopes, valid_votes, votes

def get_data_from_link(link):
    """
    Extracting data from link
    """
    data = []
    soup = parse(link)
    for row in soup.find_all("tr")[2:]:   
        cells = row.find_all("td")
        if len(cells) >   1:
            location_code, location, location_url = extract_location_details(cells)
            if location_code and location and location_url:
                location_soup = parse(location_url)
                registered_voters, envelopes, valid_votes, votes = extract_voting_data(location_soup)
                row_data = [location_code, location, registered_voters, envelopes, valid_votes] + votes
                data.append(row_data)
    return data

def write_to_csv(filename, header, data):
    """
    Writes the data to the CSV file
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for row in data:
            csvwriter.writerow(row)

def main(link, filename):
    """
    Main function for scraping
    """
    first_link = parse(link).find("td", "cislo").a["href"]
    first_link_url = f"https://volby.cz/pls/ps2017nss/{first_link}"
    parties = [party.text for party in parse(first_link_url).find_all("td", "overflow_name")]
    
    header = ["Code", "Location", "Registered Voters", "Envelopes", "Valid Votes"] + parties
    data = get_data_from_link(link)
    
    write_to_csv(filename, header, data)

if __name__ == "__main__":
    """
    Validate arguments
    """
    while True:
        if len(sys.argv) != 3:
            print("Error: Run with two arguments!")
            print("scraper.py 'URL' 'filename.csv'")
            sys.exit()
        elif not sys.argv[1].startswith("https://"):
            print("Error: Invalid URL format!")
            sys.exit()
        elif not sys.argv[2].endswith(".csv"):
            print("Error: Invalid output file format!")
            sys.exit()
        else:
            print(f"DOWNLOADING DATA FROM SELECTED URL: {sys.argv[1]}")
            break

    link = sys.argv[1]
    filename = sys.argv[2]
    main(link, filename)
    print("YOUR WEB SCRAPING IS COMPLETED")
