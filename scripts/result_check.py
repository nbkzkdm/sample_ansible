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


def find_expected_directory(base_dir, number):
    """指定番号に該当する期待ディレクトリを探す（<number>_ で始まるディレクトリ）"""
    pattern = re.compile(f'{re.escape(str(number))}_.*')

    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path) and pattern.match(item):
            return full_path

    print(f"Expected directory with prefix '{number}_' not found in '{base_dir}'.", flush=True)
    sys.exit(1)


def compare_directories(test_name, sub_dir, target_dir, number):
    print(f"test_name: '{test_name}', sub_dir: '{sub_dir}', target_dir: '{target_dir}', number: {number}", flush=True)

    # 期待ディレクトリのパス（test_expected/test_name/sub_dir）
    expected_base_dir = os.path.join("test_expected", test_name, sub_dir)

    if not os.path.exists(expected_base_dir):
        print(f"Expected base directory '{expected_base_dir}' does not exist.", flush=True)
        sys.exit(1)

    # <number>_ で始まるディレクトリを検索
    expected_dir = find_expected_directory(expected_base_dir, number)

    print(f"Expected directory: '{expected_dir}'", flush=True)

    if not os.path.exists(target_dir):
        print(f"Target directory '{target_dir}' does not exist.", flush=True)
        sys.exit(1)

    # ファイル一覧取得
    expected_files = [os.path.join(expected_dir, f) for f in os.listdir(expected_dir)
                      if os.path.isfile(os.path.join(expected_dir, f))]
    actual_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir)
                    if os.path.isfile(os.path.join(target_dir, f))]

    if len(expected_files) != len(actual_files):
        print("File counts do not match!", flush=True)
        print(f"Expected file count: {len(expected_files)}, Actual file count: {len(actual_files)}", flush=True)
        sys.exit(1)

    # ファイル内容の突合せ（名前一致は無視、順不同で内容一致を確認）
    unmatched_expected = expected_files.copy()
    unmatched_actual = actual_files.copy()

    for expected_file in expected_files:
        matched = False
        for actual_file in actual_files:
            if compare_files(expected_file, actual_file):
                matched = True
                unmatched_expected.remove(expected_file)
                unmatched_actual.remove(actual_file)
                break

    if unmatched_expected or unmatched_actual:
        print("Some files did not match!", flush=True)
        print(f"Unmatched expected files: {unmatched_expected}", flush=True)
        print(f"Unmatched actual files: {unmatched_actual}", flush=True)
        sys.exit(1)

    print("All files match!")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 script.py <test_name> <subDir> <target_directory> <number>", flush=True)
        sys.exit(1)

    test_name = sys.argv[1]
    sub_dir = sys.argv[2]
    target_directory = sys.argv[3]
    number = sys.argv[4]

    compare_directories(test_name, sub_dir, target_directory, number)
