import os
import sys
import json
import psycopg2
from datetime import datetime


def load_db_settings():
    """db_setting.jsonからDB接続情報を読み込む"""
    with open('db_setting.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_sql_path(test_name, sql_file, subtest=None):
    """SQLファイルのパスを生成"""
    if subtest:
        return os.path.join("sql", test_name, subtest, sql_file)
    else:
        return os.path.join("sql", test_name, sql_file)


def get_log_path(evidence_dir, test_name, sql_file, subtest=None):
    """ログファイルの保存パスを生成"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_dir = os.path.join(evidence_dir, test_name)

    if subtest:
        base_dir = os.path.join(base_dir, subtest)

    os.makedirs(base_dir, exist_ok=True)

    log_file_name = f"{os.path.splitext(sql_file)[0]}_{timestamp}.log"
    return os.path.join(base_dir, log_file_name)


def run_sql_and_log(test_name, sql_file, evidence_dir, subtest=None):
    db_settings = load_db_settings()

    sql_path = get_sql_path(test_name, sql_file, subtest)
    log_path = get_log_path(evidence_dir, test_name, sql_file, subtest)

    if not os.path.exists(sql_path):
        print(f"SQLファイルが見つかりません: {sql_path}")
        sys.exit(1)

    try:
        conn = psycopg2.connect(
            host=db_settings['db_host'],
            port=db_settings['db_port'],
            database=db_settings['db_name'],
            user=db_settings['db_user'],
            password=db_settings['db_password']
        )
        cursor = conn.cursor()

        with open(sql_path, 'r', encoding='utf-8') as f:
            sql = f.read()

        # 実行SQLログ出力
        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write(f"-- Executed SQL ({sql_file}) --\n")
            log_file.write(sql + "\n\n")

            cursor.execute(sql)

            # 実行結果ログ出力（SELECTの場合のみ）
            if cursor.description:  # SELECT結果がある場合のみログ出力
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

                log_file.write("-- Query Results --\n")
                log_file.write("\t".join(columns) + "\n")
                for row in rows:
                    log_file.write("\t".join(map(str, row)) + "\n")

            conn.commit()
            print(f"SQL実行ログ保存: {log_path}")

    except Exception as e:
        print(f"SQL実行エラー: {e}")
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"\n-- Error --\n{str(e)}\n")
        sys.exit(1)

    finally:
        cursor.close()
        conn.close()


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python execute_sql.py <test_name> <sql_file> <evidence_dir> [<subtest>]")
        sys.exit(1)

    test_name = sys.argv[1]
    sql_file = sys.argv[2]
    evidence_dir = sys.argv[3]
    subtest = sys.argv[4] if len(sys.argv) == 5 else None

    run_sql_and_log(test_name, sql_file, evidence_dir, subtest)


if __name__ == '__main__':
    main()
