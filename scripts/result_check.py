import os
import sys
import re


def normalize_content(content):
    """改行とインデントを無視した文字列に変換"""
    return re.sub(r'\s+', '', content)


def compare_files(expected_file, actual_file):
    """ファイル内容を比較（改行・インデント無視）"""
    with open(expected_file, 'r', encoding='utf-8') as f1, open(actual_file, 'r', encoding='utf-8') as f2:
        expected_content = normalize_content(f1.read())
        actual_content = normalize_content(f2.read())
    return expected_content == actual_content


def compare_directories(test_name, target_dir, number):
    print(f"test_name '{test_name}', target_dir: {target_dir}, number: {number}", flush=True)
    """指定ディレクトリのファイルと、期待されるディレクトリのファイルを比較"""
    base_dir = os.path.join(".", "test_expected", test_name)
    # str(number)

    if not os.path.exists(base_dir):
        print(f"Expected directory '{base_dir}' does not exist.", flush=True)
        sys.exit(1)

    pattern = re.compile(f'{str(number)}_.*')

    expected_dir = None
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path) and pattern.match(item):
            expected_dir = full_path
            break
    print(f"Expected directory '{expected_dir}'", flush=True)

    if not os.path.exists(expected_dir):
        print(f"Expected directory '{expected_dir}' does not exist.", flush=True)
        sys.exit(1)

    if not os.path.exists(target_dir):
        print(f"Target directory '{target_dir}' does not exist.", flush=True)
        sys.exit(1)

    expected_files = {f for f in os.listdir(expected_dir) if os.path.isfile(os.path.join(expected_dir, f))}
    actual_files = {f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))}

    if expected_files != actual_files:
        print("File names do not match!", flush=True)
        print("Expected:", expected_files, flush=True)
        print("Actual:", actual_files, flush=True)
        sys.exit(1)

    for file in expected_files:
        expected_file_path = os.path.join(expected_dir, file)
        actual_file_path = os.path.join(target_dir, file)

        if not compare_files(expected_file_path, actual_file_path):
            print(f"File '{file}' does not match!", flush=True)
            sys.exit(1)

    print("All files match!")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <test_name> <target_directory> <number>", flush=True)
        sys.exit(1)

    test_name = sys.argv[1]
    target_directory = sys.argv[2]
    number = sys.argv[3]

    compare_directories(test_name, target_directory, number)
