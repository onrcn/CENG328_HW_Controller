import pandas as pd

def sort_csv(input_file='students_submissions.csv'):
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    df_sorted = df.sort_values(by='Student Name')
    return df_sorted

def convert_to_html(input_file='students_submissions.csv', output_file='sorted_submissions.html'):
    df = sort_csv(input_file)

    # Replace newline characters with <br> for HTML
    df = df.replace({'\n': '<br>'}, regex=True)

    # Ensure all entries in the 'Compiled' column are strings
    df['Compiled'] = df['Compiled'].astype(str)

    # Add internal borders for the "Compiled" column
    df['Compiled'] = df['Compiled'].str.replace('True', '<span style="border: 1px solid green; padding: 2px;">True</span>', regex=False)
    df['Compiled'] = df['Compiled'].str.replace('False', '<span style="border: 1px solid red; padding: 2px;">False</span>', regex=False)

    # Convert the DataFrame to an HTML table with added CSS
    html_table = df.to_html(index=False, classes='table table-striped', border=0, escape=False)

    # Define HTML structure with inline CSS
    html_string = f'''
    <html>
    <head>
    <style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
    }}
    h2 {{
        text-align: center;
        color: #333;
    }}
    .table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
    }}
    .table th, .table td {{
        padding: 12px 15px;
        border: 1px solid #dddddd;
    }}
    .table th {{
        background-color: #007bff;
        color: #ffffff;
    }}
    .table tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
    .table tr:hover {{
        background-color: #d1e7fd;
    }}
    </style>
    </head>
    <body>
    <h2>Student Submissions</h2>
    {html_table}
    </body>
    </html>
    '''

    # Write the HTML string to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_string)

    print(f'HTML table saved to {output_file}')

if __name__ == '__main__':
    convert_to_html()

