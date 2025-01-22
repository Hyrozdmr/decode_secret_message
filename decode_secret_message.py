import requests
from bs4 import BeautifulSoup

def decode_secret_message(doc_url):
    print("Fetching the document...")
    response = requests.get(doc_url)

    if response.status_code != 200:
        print(f"Failed to fetch document. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    print("Parsing the document...")

    table = soup.find('table')

    if not table:
        print("No table found in the document.")
        return

    # Initialise a 100x100 grid with empty spaces
    grid = [[' ' for _ in range(100)] for _ in range(100)]

    # Parse each row in the table
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        try:
            # Check for sufficient cells in the row
            if len(cells) < 3:
                print("Skipping row with insufficient cells.")
                continue

            # Assign x, char, y based on the observed row structure
            x = int(cells[0].text.strip())
            char = cells[1].text.strip()
            y = int(cells[2].text.strip())

            # Debugging output to check parsed values
            print(f"Parsed: x={x}, char='{char}', y={y}")

            # Place the character in the grid if it's valid
            if char and char not in {'░'}:
                grid[y][x] = char
        except ValueError as error:
            print(f"ValueError encountered: {error}. Skipping row.")
            continue
        except IndexError as error:
            print(f"IndexError encountered: {error}. Skipping row.")
            continue

    # Print the decoded message (non-empty rows only)
    print("Decoded message:")
    for row in grid:
        line = ''.join(row)
        if line.strip():  # Print only rows with content
            print(line)

# URL to the Google Doc
doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
decode_secret_message(doc_url)
