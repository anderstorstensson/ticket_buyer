import requests
from bs4 import BeautifulSoup
import time
import webbrowser  # Import the webbrowser module
import re
from playsound import playsound

# Function to check the webpage
def check_ticket_status():
    url = "https://secure.onreg.com/onreg2/_bibexchange_/?eventid=6736&language=us" # 2025
    response = requests.get(url,verify=False)

    # If request is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the relevant part of the page; this will depend on the page's structure
        # Assuming 'In Progress' status is inside a <button> tag
        button = soup.find('btn button_cphhalf')
        # Find all <tr> elements that likely contain ticket information
        rows = soup.find_all('tr')

        # Extract information from each row
        for row in rows:
            # Extract all <td> elements from the current row
            columns = row.find_all('td')

            if len(columns) == 4:  # Ensure there are enough columns to match your example
                event_name = columns[0].text.strip()  # Event name (e.g., "CPH Half 2024")
                bib_number = columns[1].text.strip()  # Bib number (e.g., "11208")
                price = columns[2].text.strip()  # Price (e.g., "575.00 DKK")

                # Extract the <a> element within the last <td> element
                button = columns[3].find('a', class_='btn button_cphhalf')
                if "button_cphhalf" in str(columns[3]):
                    button_text = columns[3].text.strip()  # Get the text inside the button
                    button_classes = " ".join(columns[3].get('class', []))  # Get all classes as a string

                    # Print the extracted information
                    print(f"Event: {event_name}")
                    print(f"  Bib Number: {bib_number}")
                    print(f"  Price: {price}")
                    print(f"  Button Text: '{button_text}'")
                    print("\n")

                    if 'in progress' not in button_text.lower() :
                        # Change this to any alert mechanism you prefer
                        print("Tickets are available!")
                        with open('html_content.html', 'w') as file:
                            file.write(str(response.content))

                        with open('Button.html', 'w') as file:
                            file.write(str(columns[3]))

                        content = str(columns[3])
                        match = re.search( r'href="([^"]*)"', content)
                        if match:
                            href = match.group(1)
                        else:
                            href = ""

                        href = href.replace('amp;','')
                        url = f"https://secure.onreg.com/onreg2/_bibexchange_/{href}" # 2025


                        webbrowser.open_new_tab(url)

                        try:
                            playsound('alarm.wav')
                        except:
                            try:
                                playsound('alarm.wav')
                            except Exception as e:
                                print(e)
                                playsound('alarm.wav')

                        return True
                        break
                    else:
                        return False
    else:
        print("Failed to fetch the webpage.")
        return False

# Main loop to repeatedly check
def main():
    while True:
        if check_ticket_status():
            break  # Exit the loop if tickets are available

        # Wait for a while before checking again
        time.sleep(1)  # Check every 60 seconds

if __name__ == "__main__":
    main()
