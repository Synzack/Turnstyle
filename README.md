# Turnstyle
Ansible Scripts to Deploy an example Turnstile Page. 

Corresponding blog post: https://specterops.io/blog/2026/05/28/dont-jump-the-turnstile-lessons-from-the-field/

For educational purposes and authorized engagments.

## How To Configure

1. Update `config.py` with your SITE_KEY, SECRET_KEY, SECRET_URL, SERVICE_NAME, and SERVICE_ICON (URL)
2. Update `app.py` with your app_name, domain_name, and turnstile_landing_page
```
- name: Deploy TurnStyle
  hosts: all
  become: yes
  vars:
    app_name: "<app name>"
    domain_name: "<domain>"
    turnstile_landing_page: "</landing-page>
```
3. Deploy with `ansible-playbook` 
```
ansible-playbook turnstyle.yml -i <target>
```
