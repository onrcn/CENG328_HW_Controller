# /scripts/convert_to_html.py
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')


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

    # Create the HTML string with references to the external CSS and JS files
    html_string = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Submissions</title>
        <link rel="stylesheet" href="../static/style.css">
    </head>
    <body>
        <h2>Student Submissions</h2>
        <div id="table-container">{html_table}</div>
        <button id="saveButton" class="save-button">Save Changes</button>
        <button id="addQuestionButton" class="add-question-button">Add Question</button>
        <script src="../static/script.js"></script>
    </body>
    </html>
    '''

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
