import requests
from bs4 import BeautifulSoup

def scrape_dsa_event_pgs(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Narrow to main container
        container = soup.find('div', id ='action_head')
        if not container:
            print(f"❌ No action_head found at {url}")
            return None

        # Extract title
        title_tag = container.find('h2', class_='entry-title js-entry-title')
        title = title_tag.get_text(strip=True) if title_tag else ''

        # Extract h4s
        date_time_tag = container.find('h4', class_='event_date')
        location_tag = container.find('h4', class_='event_location js-event_location')
        contact_tag = container.find('h4', class_='event_contact')

        date_time = date_time_tag.get_text(strip=True)[6:] if date_time_tag else ''
        parts = date_time.split('•')
        date = parts[0].strip()
        time = parts[1].strip()
        location_name_address = location_tag.get_text(strip=True)[9:] if location_tag else ''
        parts = location_name_address.split('•')
        location_name = parts[0].strip()
        address = parts[1].strip()
        contact = contact_tag.get_text(strip=True)[18:] if contact_tag else ''

        # Extract description of event
        deeper_container = container.find('div', class_='action_description clearfix')
        description_tag = deeper_container.find('p')
        sign_up_link_tag = deeper_container.find('a', href=True)

        description = description_tag.get_text(strip=True) if description_tag else ''
        sign_up_link = sign_up_link_tag.get_text(strip=True) if sign_up_link_tag else ''
   

        return {
            "title": title,
            "date": date,
            "time": time,
            "location_name": location_name,
            "address": address,
            "contact": contact,
            "url": url,
            "description": description,
            "sign_up_link": sign_up_link
        }

    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return None
    
################# Scrape data from linktree and event pages ###################
# URL of the Linktree page
linktree_url = 'https://linktr.ee/jaxdsa'
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the linktree page content
response = requests.get(linktree_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

relevant_div = soup.select('div.mb-4.flex.flex-col.gap-4 a')

#extract all event links
all_dsa_event_links = []
for link in relevant_div: 
    text = link.get_text(strip=True)
    href = link['href']
    all_dsa_event_links.append({"title": text, "url": href})

#extract event data from event page 
dsa_event_data = []
for item in all_dsa_event_links:
    url = item["url"]  
    print(f"Scraping: {url}")
    event = scrape_dsa_event_pgs(url)
    if event:
        dsa_event_data.append(event)

########################Send data to spreadsheet################################
#connecting to sheet- import google sheets API library and load credential
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'event-scrapper-dsa.json'  # filepath for json credentials
#if located in same folder as script then just the name of the file is needed 
SPREADSHEET_ID = '1kvs0UEPlUaPICdJ3uGFV1Jxm7O_Q8OjgY6R2WC5tpQ8'
# spreadsheet ID is value between d/ and /edit in the spreadsheet URL 
RANGE_NAME = 'Events!A1'  # sheet name (look at tab at bottom) and starting location

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('sheets', 'v4', credentials=creds)

#read headers from spreadsheet
header_result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range="Events!1:1"
).execute()

header_row = header_result['values'][0]  # list of column headers
print(header_row)

#format data appropriately
org_name = "DSA"
rows_to_append = []

for event in dsa_event_data:
    row = [""] * len(header_row) # blank row with correct num of columns to fill in with data 

    full_event = {
        "Organization": org_name,
        "Event Title": event.get("title", ""),
        "Date": event.get("date", ""),
        "Time": event.get("time", ""),
        "Location_Name": event.get("location_name", ""),
        "Address":event.get("address", ""),
        "Contact": event.get("contact", ""),
        "Link": event.get("url", ""),
        "Description": event.get("description",""),
        "Sign_up_link": event.get("sign_up_link","")
    }

    print(full_event.items())

    # Fill in only the columns that match your sheet's headers
    for key, value in full_event.items():
        print(key,value)
        if key in header_row:
            idx = header_row.index(key)
            row[idx] = value

    rows_to_append.append(row)

#Send off to sheets!
body = {'values': rows_to_append}

result = service.spreadsheets().values().append(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME,
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body=body
).execute()

print(f"{result.get('updates').get('updatedCells')} cells written to sheet.")