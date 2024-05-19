# /scripts/convert_to_html.py
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

print()
print()
print()
print(f"BASE_DIR: {BASE_DIR}")
print(f"DATA_DIR: {DATA_DIR}")
print(f"STATIC_DIR: {STATIC_DIR}")
print()
print()
print()


def sort_csv(input_file=os.path.join(DATA_DIR, 'students_submissions.csv')):
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    df_sorted = df.sort_values(by='Student Name')
    return df_sorted


def convert_to_html(input_file=os.path.join(DATA_DIR, 'students_submissions.csv'), output_file=os.path.join(DATA_DIR, 'sorted_submissions.html')):
    df = sort_csv(input_file)

    # Replace newline characters with <br> for HTML
    df = df.replace({'\n': '<br>'}, regex=True)

    # Fill NaN values with empty strings
    df = df.fillna('')

    # Ensure all entries in the 'Compiled' column are strings
    df['Compiled'] = df['Compiled'].astype(str)

    # Add internal borders for the "Compiled" column
    df['Compiled'] = df['Compiled'].str.replace(
        'True', '<span style="border: 1px solid green; padding: 2px;">True</span>', regex=False)
    df['Compiled'] = df['Compiled'].str.replace(
        'False', '<span style="border: 1px solid red; padding: 2px;">False</span>', regex=False)

    # Convert the DataFrame to an HTML table with added CSS
    html_table = df.to_html(
        index=False, classes='table table-striped', border=0, escape=False)

    with open(os.path.join(STATIC_DIR, 'index.html'), 'r', encoding='utf-8') as file:
        html_template = file.read()

    html_string = html_template.replace(
        '<div id="table-container"></div>', f'<div id="table-container">{html_table}</div>')

    # Write the HTML string to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_string)

    print(f'HTML table saved to {output_file}')


def convert_to_excel(input_file=os.path.join(DATA_DIR, 'students_submissions.csv'), output_file=os.path.join(DATA_DIR, 'sorted_submissions.xlsx')):
    df = sort_csv(input_file)
    df.to_excel(output_file, index=False)
    print(f'Excel file saved to {output_file}')


if __name__ == '__main__':
    convert_to_html()
    convert_to_excel()
