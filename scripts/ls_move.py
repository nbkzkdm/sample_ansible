import os
import sys
import shutil
import subprocess
from datetime import datetime


def save_ls_result_with_subprocess(monitor_path, test_evidence_path, prefix):
    """ls -l結果をsubprocessで取得し、エビデンスディレクトリに保存"""
    dir_name = os.path.basename(os.path.abspath(monitor_path))
    ls_file = os.path.join(test_evidence_path, f"{prefix}_{dir_name}_ls結果_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    try:
        # subprocessでls -lの結果を取得
        result = subprocess.run(['ls', '-l', monitor_path], capture_output=True, text=True, check=True)
        with open(ls_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)

        print(f"ls結果を保存: {ls_file}")

    except subprocess.CalledProcessError as e:
        print(f"lsコマンドの実行に失敗しました: {e}")
        sys.exit(1)


def move_files(monitor_path, test_evidence_path, prefix):
    """監視ディレクトリのファイルをエビデンスディレクトリに移動"""
    dir_name = os.path.basename(os.path.abspath(monitor_path))

    for item in os.listdir(monitor_path):
        item_path = os.path.join(monitor_path, item)

        if os.path.isfile(item_path):
            new_file_name = f"{prefix}_{dir_name}_{item}"
            new_file_path = os.path.join(test_evidence_path, new_file_name)
            shutil.move(item_path, new_file_path)
            print(f"ファイル移動: {item_path} -> {new_file_path}")


def main():
    if len(sys.argv) < 6:
        print("Usage: python script.py <監視ディレクトリ> <エビデンスディレクトリ> <テスト名> <サブテスト名>")
        sys.exit(1)

    monitor_path = sys.argv[1]
    evidence_path = sys.argv[2]
    test_name = sys.argv[3]
    sub_test_name = sys.argv[4]
    prefix = sys.argv[5]

    if not os.path.exists(monitor_path):
        print(f"監視ディレクトリが存在しません: {monitor_path}")
        sys.exit(1)

    # テスト名/サブテスト名ディレクトリをエビデンスディレクトリ配下に作成
    test_evidence_path = os.path.join(evidence_path, test_name, sub_test_name)
    os.makedirs(test_evidence_path, exist_ok=True)

    save_ls_result_with_subprocess(monitor_path, test_evidence_path, prefix)
    move_files(monitor_path, test_evidence_path, prefix)


if __name__ == "__main__":
    main()
