def extract_financial_data_from_table(table_tag):
    # Get all headers
    headers = table_tag.find_all('th')

    # Get the first row
    first_row = table_tag.find_all('tr')[1]

    # Create the dictionary
    data = {}
    for header, cell in zip(headers[1:], first_row.find_all('td')):
        data[header.get_text()] = cell.get_text()

    return data
