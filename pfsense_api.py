import paramiko
import config

def execute_ssh(cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(config.ROUTER_IP, username=config.ROUTER_USER, password=config.ROUTER_PASS, timeout=3)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode('utf-8').strip()
        ssh.close()
        return result
    except Exception as e:
        print(f"SSH Error: {e}")
        return ""

def add_captive_user(username, password):
    php_script = f"""<?php
require_once('config.inc');
require_once('auth.inc');
$u = array();
$u['name'] = '{username}';
$u['bcrypt-hash'] = password_hash('{password}', PASSWORD_DEFAULT);
$u['priv'] = array('user-services-captiveportal-login');
if (!is_array($config['system']['user'])) {{ $config['system']['user'] = array(); }}
$config['system']['user'][] = $u;
write_config('SmartGateway: Added user {username} from Python');
local_sync_accounts();
?>"""
    cmd = f"cat << 'EOF' > /tmp/add_user.php\n{php_script}\nEOF\nphp /tmp/add_user.php"
    execute_ssh(cmd)

def del_captive_user(username):
    php_script = f"""<?php
require_once('config.inc');
require_once('auth.inc');
if (is_array($config['system']['user'])) {{
    foreach ($config['system']['user'] as $key => $user) {{
        if ($user['name'] == '{username}') {{
            unset($config['system']['user'][$key]);
            break;
        }}
    }}
    write_config('SmartGateway: Deleted user {username} from Python');
    local_sync_accounts();
}}
?>"""
    cmd = f"cat << 'EOF' > /tmp/del_user.php\n{php_script}\nEOF\nphp /tmp/del_user.php"
    execute_ssh(cmd)
    
def reboot_router():
    # คำสั่งนี้จะส่งไปที่ Router แล้วมันอาจจะตัดการเชื่อมต่อทันที เลยต้องใส่ try/except กัน Error โชว์
    try:
        execute_ssh("reboot")
    except Exception:
        pass