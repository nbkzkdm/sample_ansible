# sample_ansible

>  ansible-playbook playbook.yml --extra-vars "test_name=test_01 dest_path=test_output"


``` shell
ansible-playbook playbook.yml | tee ansible_output.log
ANSIBLE_STDOUT_CALLBACK=json ansible-playbook playbook.yml > ansible_output.json
```
