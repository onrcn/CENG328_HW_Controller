import os
import csv
import shutil
import subprocess
import magic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
SUBMISSIONS_DIR = os.path.join(BASE_DIR, '..', 'submissions')
ARCHIVES_DIR = os.path.join(BASE_DIR, '..', 'archives')


def csv_create(base_dir=SUBMISSIONS_DIR, csv_file=os.path.join(DATA_DIR, "students_submissions.csv")):
    students_info = []

    for folder_name in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, folder_name)):
            parts = folder_name.split('_')
            student_name = parts[0]
            unique_id = parts[1]
            students_info.append(
                [student_name, unique_id, "", "", "", "", "", ""])

    headers = ["Student Name", "Unique Identifier", "Folder Structure",
               "Compiled", "Compile Log", "Error Log", "Changed Files", "Deleted Files"]

    with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(students_info)

    print(f"CSV file '{csv_file}' created successfully.")


def determine_file_type(file_path):
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        return file_type
    except subprocess.CalledProcessError as e:
        print(f"Error determining file type: {e}")
        return ""


def extract_archive(file_path, destination_dir):
    file_type = determine_file_type(file_path)
    try:
        extracted = False
        if file_type == "application/zip" or file_path.endswith('.zip'):
            shutil.unpack_archive(file_path, destination_dir)
            extracted = True
        elif "rar" in file_type or file_path.endswith('.rar'):
            os.makedirs(destination_dir, exist_ok=True)
            subprocess.run(['unrar', 'x', '-o+', '-y',
                           file_path, destination_dir], check=True)
            extracted = True

        if not extracted:
            if file_path.endswith('.rar'):
                new_file_path = file_path.replace('.rar', '.zip')
                os.rename(file_path, new_file_path)
                shutil.unpack_archive(new_file_path, destination_dir)
                extracted = True
            elif file_path.endswith('.zip'):
                new_file_path = file_path.replace('.zip', '.rar')
                os.rename(file_path, new_file_path)
                os.makedirs(destination_dir, exist_ok=True)
                subprocess.run(['unrar', 'x', '-o+', '-y',
                               new_file_path, destination_dir], check=True)
                extracted = True

        if not extracted:
            raise ValueError(f"Unsupported archive type for file {file_path}")
    except Exception as e:
        print(f"Error extracting {file_path}: {e}")
        raise


def is_source_code(file_path):
    file_type = determine_file_type(file_path)
    file_types = ["text/x-c", "text/x-c++src", "text/x-csrc",
                  "text/x-c++hdr", "text/x-chdr", "text/x-csrc"]
    return file_type in file_types


def clean_up_folder(folder_path):
    deleted_files_log = []
    changed_files_log = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file == "input.txt":
                continue
            new_file_path = None
            if not is_source_code(file_path):
                try:
                    if file.endswith('.txt') and 'c' in file_path:
                        new_file_path = file_path.replace('.txt', '.c')
                    elif file.endswith('.txt') and 'cpp' in file_path:
                        new_file_path = file_path.replace('.txt', '.cpp')
                    elif file.endswith('.rar'):
                        new_file_path = file_path.replace('.rar', '.zip')
                    elif file.endswith('.zip'):
                        new_file_path = file_path.replace('.zip', '.rar')

                    if new_file_path:
                        os.rename(file_path, new_file_path)
                        changed_files_log.append(
                            f"{file} -> {os.path.basename(new_file_path)}")
                    else:
                        os.remove(file_path)
                        deleted_files_log.append(file)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    return deleted_files_log, changed_files_log


def find_all_source_files(student_folder):
    source_files = []
    for root, dirs, files in os.walk(student_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if is_source_code(file_path):
                source_files.append(file_path)
    return source_files


def compile_check(source_files):
    compile_results = {}
    compile_logs = {}
    error_logs = {}
    for file_path in source_files:
        if os.path.isfile(file_path):  # Ensure it's a file
            if file_path.endswith('.cpp'):
                compile_command = f"g++ \"{file_path}\" -o \"{file_path}.out\""
            else:
                compile_command = f"gcc \"{file_path}\" -o \"{file_path}.out\""
            try:
                result = subprocess.run(
                    compile_command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    compile_results[file_path] = True
                    compile_logs[file_path] = result.stdout
                else:
                    compile_results[file_path] = False
                    error_logs[file_path] = result.stderr
            except Exception as e:
                compile_results[file_path] = False
                error_logs[file_path] = str(e)
    return compile_results, compile_logs, error_logs


def ensure_input_txt(student_folder, root_input_txt):
    student_input_txt = os.path.join(student_folder, "input.txt")
    if not os.path.exists(student_input_txt):
        shutil.copy(root_input_txt, student_input_txt)


def log_folder_structure(folder_path):
    folder_structure = []
    for root, dirs, files in os.walk(folder_path):
        level = root.replace(folder_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        folder_structure.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            folder_structure.append(f"{subindent}{file}")
    return "\n".join(folder_structure)


def update_csv_with_errors(base_dir=SUBMISSIONS_DIR, csv_file=os.path.join(DATA_DIR, "students_submissions.csv"), check_input_txt=True):
    with open(csv_file, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        rows = list(reader)

    root_input_txt = os.path.join(DATA_DIR, "input.txt")

    for row in rows[1:]:
        student_folder = os.path.join(
            base_dir, f"{row[0]}_{row[1]}_assignsubmission_file_")
        if os.path.isdir(student_folder):
            try:
                archive_files = [f for f in os.listdir(
                    student_folder) if f.endswith(('.zip', '.rar', '.tar.gz'))]
                for archive_file in archive_files:
                    archive_path = os.path.join(student_folder, archive_file)
                    try:
                        extract_archive(archive_path, student_folder)
                        os.remove(archive_path)
                    except Exception as e:
                        row[5] += f"{archive_file}: {e}; "

                initial_structure = log_folder_structure(student_folder)
                row[2] = initial_structure

                if check_input_txt:
                    ensure_input_txt(student_folder, root_input_txt)

                deleted_files_log, changed_files_log = clean_up_folder(
                    student_folder)
                row[7] = ", ".join(deleted_files_log)
                row[6] = ", ".join(changed_files_log)

                source_files = find_all_source_files(student_folder)
                if source_files:
                    compile_results, compile_logs, error_logs = compile_check(
                        source_files)
                    row[3] = "\n".join(
                        [f"{k}: {v}" for k, v in compile_results.items()])
                    row[4] = "\n".join(
                        [f"{k}: {v}" for k, v in compile_logs.items()])
                    row[5] = "\n".join(
                        [f"{k}: {v}" for k, v in error_logs.items()])
                else:
                    row[3] = "No source files found"
                    row[4] = "N/A"
                    row[5] = ""

            except Exception as e:
                row[5] += str(e)

    with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def first_control(check_input_txt=True):
    csv_create()
    update_csv_with_errors(check_input_txt=check_input_txt)
    print("First control finished.")


if __name__ == "__main__":
    first_control(check_input_txt=False)
