import os
import sys
import stat
import pwd
import grp
import shutil
from datetime import datetime


def get_permissions(mode):
    """ファイルモードからls -l形式のパーミッション文字列を生成"""
    perms = [
        stat.filemode(mode),  # -rw-r--r-- みたいな文字列を取得
    ]
    return ''.join(perms)


def format_ls_line(path, filename):
    """1行分のls -l形式の文字列を作成"""
    full_path = os.path.join(path, filename)
    st = os.stat(full_path)

    permissions = get_permissions(st.st_mode)
    hard_links = 1  # 固定（必要に応じてst.st_nlinkに変更可能）
    owner = pwd.getpwuid(st.st_uid).pw_name
    group = grp.getgrgid(st.st_gid).gr_name
    size = st.st_size
    modified_time = datetime.fromtimestamp(st.st_mtime).strftime('%b %d %H:%M')

    return f"{permissions} {hard_links} {owner} {group} {size} {modified_time} {filename}"


def save_ls_result(monitor_path, test_evidence_path):
    """ls -l結果をエビデンスディレクトリに保存"""
    dir_name = os.path.basename(os.path.abspath(monitor_path))
    ls_file = os.path.join(test_evidence_path, f"{dir_name}_ls結果_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    with open(ls_file, 'w', encoding='utf-8') as f:
        for item in sorted(os.listdir(monitor_path)):  # ls -l では並びが一定のためソート
            ls_line = format_ls_line(monitor_path, item)
            f.write(ls_line + '\n')

    print(f"ls結果を保存: {ls_file}")


def move_files(monitor_path, test_evidence_path):
    """監視ディレクトリのファイルをエビデンスディレクトリに移動"""
    dir_name = os.path.basename(os.path.abspath(monitor_path))

    for item in os.listdir(monitor_path):
        item_path = os.path.join(monitor_path, item)

        if os.path.isfile(item_path):
            new_file_name = f"{dir_name}_{item}"
            new_file_path = os.path.join(test_evidence_path, new_file_name)
            shutil.move(item_path, new_file_path)
            print(f"ファイル移動: {item_path} -> {new_file_path}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <監視ディレクトリ> <エビデンスディレクトリ> <テスト名>")
        sys.exit(1)

    monitor_path = sys.argv[1]
    evidence_path = sys.argv[2]
    test_name = sys.argv[3]

    if not os.path.exists(monitor_path):
        print(f"監視ディレクトリが存在しません: {monitor_path}")
        sys.exit(1)

    # テスト名ディレクトリをエビデンスディレクトリ配下に作成
    test_evidence_path = os.path.join(evidence_path, test_name)
    os.makedirs(test_evidence_path, exist_ok=True)

    save_ls_result(monitor_path, test_evidence_path)
    move_files(monitor_path, test_evidence_path)


if __name__ == "__main__":
    main()
