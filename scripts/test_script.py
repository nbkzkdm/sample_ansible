import os
import sys
import shutil


def copy_test_files(test_name, dest_dir):
    # 実行中のスクリプトの絶対パスからベースディレクトリを計算
    print(f"test_name '{test_name}', dest_dir: {dest_dir}", flush=True)
    script_path = os.path.abspath(sys.argv[0])
    base_dir = os.path.dirname(script_path)

    # `test/` ディレクトリの絶対パスを計算
    test_dir = os.path.abspath(os.path.join(base_dir, "..", "test", test_name))

    # コピー先ディレクトリの作成
    os.makedirs(dest_dir, exist_ok=True)

    if not os.path.exists(test_dir):
        print(f"Test directory '{test_dir}' does not exist.", flush=True)
        sys.exit(1)

    # ファイルをコピー
    for file_name in os.listdir(test_dir):
        src_path = os.path.join(test_dir, file_name)
        dest_path = os.path.join(dest_dir, file_name)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied: {src_path} -> {dest_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 test_script.py <test_name> <dest_dir>", flush=True)
        sys.exit(1)

    test_name = sys.argv[1]
    dest_dir = sys.argv[2]

    copy_test_files(test_name, dest_dir)
