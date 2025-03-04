# sample_ansible

vagrant init centos/stream9 --box-version 20250210.0


## 最新のパッケージ情報を更新
sudo dnf update -y

## EPELリポジトリを有効化
sudo dnf install -y epel-release

## Vimインストール

sudo dnf install -y vim
echo "set number" >> ~/.vimrc

## Ansible をインストール
sudo dnf install -y ansible
ansible --version
ansible-galaxy collection install community.postgresql


python3 --version
sudo dnf install python3-pip -y
pip3 install ansible
pip3 --version
python3 -m pip install --upgrade pip
pip3 --version
pip3 install ansible
pip3 install ansible-navigator
pip3 install ansible-builder
ansible-navigator --version
ansible-builder --version

sudo dnf install postgresql-devel -y
sudo dnf install python3-devel -y
sudo dnf install gcc -y
pip3 install psycopg2

pip3 install psycopg2-binary


>  ansible-playbook playbook.yml --extra-vars "test_name=test_01 dest_path=test_output"
>  ansible-playbook playbook.yml --extra-vars "test_name=test_01 dest_path=test_output evidence=evidence"


``` shell
ansible-playbook playbook.yml | tee ansible_output.log
ANSIBLE_STDOUT_CALLBACK=json ansible-playbook playbook.yml > ansible_output.json
```

``` yaml
- name: Run ls -l and save output to a file
  shell: ls -l /path/to/directory > /path/to/output/result.txt
```

``` yaml
- name: Run ls -l and save output using tee
  command: ls -l /path/to/directory | tee /path/to/output/result.txt
```

[Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)

``` shell
$ ansible-playbook --help
usage: ansible-playbook [-h] [--version] [-v] [--private-key PRIVATE_KEY_FILE] [-u REMOTE_USER] [-c CONNECTION] [-T TIMEOUT] [--ssh-common-args SSH_COMMON_ARGS] [--sftp-extra-args SFTP_EXTRA_ARGS] [--scp-extra-args SCP_EXTRA_ARGS]
                        [--ssh-extra-args SSH_EXTRA_ARGS] [-k | --connection-password-file CONNECTION_PASSWORD_FILE] [--force-handlers] [--flush-cache] [-b] [--become-method BECOME_METHOD] [--become-user BECOME_USER]
                        [-K | --become-password-file BECOME_PASSWORD_FILE] [-t TAGS] [--skip-tags SKIP_TAGS] [-C] [-D] [-i INVENTORY] [--list-hosts] [-l SUBSET] [-e EXTRA_VARS] [--vault-id VAULT_IDS]
                        [--ask-vault-password | --vault-password-file VAULT_PASSWORD_FILES] [-f FORKS] [-M MODULE_PATH] [--syntax-check] [--list-tasks] [--list-tags] [--step] [--start-at-task START_AT_TASK]
                        playbook [playbook ...]

Ansible playbook を実行し、対象ホスト上で定義されたタスクを実行する。

positional arguments:
  playbook              Playbook(s)

optional arguments:
  --ask-vault-password, --ask-vault-pass
                        ask for vault password
  --become-password-file BECOME_PASSWORD_FILE, --become-pass-file BECOME_PASSWORD_FILE
                        Become password file
  --connection-password-file CONNECTION_PASSWORD_FILE, --conn-pass-file CONNECTION_PASSWORD_FILE
                        Connection password file
  --flush-cache         clear the fact cache for every host in inventory
  --force-handlers      run handlers even if a task fails
  --list-hosts          outputs a list of matching hosts; does not execute anything else
  --list-tags           list all available tags
  --list-tasks          list all tasks that would be executed
  --skip-tags SKIP_TAGS
                        only run plays and tasks whose tags do not match these values
  --start-at-task START_AT_TASK
                        start the playbook at the task matching this name
  --step                one-step-at-a-time: confirm each task before running
  --syntax-check        perform a syntax check on the playbook, but do not execute it
  --vault-id VAULT_IDS  the vault identity to use
  --vault-password-file VAULT_PASSWORD_FILES, --vault-pass-file VAULT_PASSWORD_FILES
                        vault password file
  --version             show program's version number, config file location, configured module search path, module location, executable location and exit
  -C, --check           don't make any changes; instead, try to predict some of the changes that may occur
  -D, --diff            when changing (small) files and templates, show the differences in those files; works great with --check
  -K, --ask-become-pass
                        ask for privilege escalation password
  -M MODULE_PATH, --module-path MODULE_PATH
                        prepend colon-separated path(s) to module library (default={{ ANSIBLE_HOME ~ "/plugins/modules:/usr/share/ansible/plugins/modules" }})
  -e EXTRA_VARS, --extra-vars EXTRA_VARS
                        set additional variables as key=value or YAML/JSON, if filename prepend with @
  -f FORKS, --forks FORKS
                        specify number of parallel processes to use (default=5)
  -h, --help            show this help message and exit
  -i INVENTORY, --inventory INVENTORY, --inventory-file INVENTORY
                        specify inventory host path or comma separated host list. --inventory-file is deprecated
  -k, --ask-pass        ask for connection password
  -l SUBSET, --limit SUBSET
                        further limit selected hosts to an additional pattern
  -t TAGS, --tags TAGS  only run plays and tasks tagged with these values
  -v, --verbose         Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv.

Connection Options:
  control as whom and how to connect to hosts

  --private-key PRIVATE_KEY_FILE, --key-file PRIVATE_KEY_FILE
                        use this file to authenticate the connection
  --scp-extra-args SCP_EXTRA_ARGS
                        specify extra arguments to pass to scp only (e.g. -l)
  --sftp-extra-args SFTP_EXTRA_ARGS
                        specify extra arguments to pass to sftp only (e.g. -f, -l)
  --ssh-common-args SSH_COMMON_ARGS
                        specify common arguments to pass to sftp/scp/ssh (e.g. ProxyCommand)
  --ssh-extra-args SSH_EXTRA_ARGS
                        specify extra arguments to pass to ssh only (e.g. -R)
  -T TIMEOUT, --timeout TIMEOUT
                        override the connection timeout in seconds (default=10)
  -c CONNECTION, --connection CONNECTION
                        connection type to use (default=smart)
  -u REMOTE_USER, --user REMOTE_USER
                        connect as this user (default=None)

Privilege Escalation Options:
  control how and which user you become as on target hosts

  --become-method BECOME_METHOD
                        privilege escalation method to use (default=sudo), use `ansible-doc -t become -l` to list valid choices.
  --become-user BECOME_USER
                        run operations as this user (default=root)
  -b, --become          run operations with become (does not imply password prompting)
```

* テスト名
* 監視ディレクトリ
* 成功ディレクトリ
* エラーディレクトリ
* 履歴ディレクトリ
* テスト結果ディレクトリ

1. 成功ディレクトリの内容を削除
2. エラーディレクトリの内容を削除
3. 履歴ディレクトリの内容を削除
4. 監視ディレクトリに何もないこと確認
5. 監視ディレクトリにファイル配置
6. 成功ディレクトリに配置のファイルの確認
7. エラーディレクトリに配置のファイルの確認
8. 履歴ディレクトリに配置のファイルの確認
9. 監視ディレクトリに何もないこと確認
10. テスト結果ディレクトリにエビデンス格納

``` shell
- name: Remove all files in target directory
  file:
    path: "{{ item }}"
    state: absent
  with_fileglob:
    - "{{ target_directory }}/*"

- name: Remove all subdirectories in target directory
  file:
    path: "{{ item }}"
    state: absent
  with_fileglob:
    - "{{ target_directory }}/*/"
  when: target_directory is defined
```



