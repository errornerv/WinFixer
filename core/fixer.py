import subprocess
import os
import shutil
from .logger import log

def run_command(command, shell=True, critical=True):
    try:
        log(f"Running command: {command}")
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode == 0:
            log(f"✅ Success: {result.stdout.strip()}")
            return True, result.stdout
        else:
            error_msg = result.stderr.strip() if result.stderr else "No error message available."
            log(f"❌ Error: {error_msg}", level="error")
            log(f"Return code: {result.returncode}", level="error")
            return False, result.stderr
    except Exception as e:
        log(f"❌ Exception while running command: {e}", level="error")
        return False, str(e)

def reset_network_adapter():
    commands = [
        ('netsh winsock reset', True),
        ('netsh int ip reset', True),
        ('ipconfig /release', False),
        ('ipconfig /renew', False),
        ('ipconfig /flushdns', True)
    ]
    success = True
    restart_required = False
    for cmd, critical in commands:
        cmd_success, output = run_command(cmd, critical=critical)
        if cmd == 'netsh winsock reset' and "You must restart the computer" in output:
            restart_required = True
            log("System restart required to complete Winsock reset. Stopping further commands.", level="info")
            break
        if not cmd_success:
            success = False
            if critical:
                log("Critical command failed, stopping network reset.", level="error")
                break
    if not success and not restart_required:
        log("Failed to reset network. Check if app is running as Administrator.", level="error")
    elif success and not restart_required:
        log("Network reset completed successfully.", level="info")
    if restart_required:
        log("Please restart your computer to apply the network reset changes.", level="info")
    return success, restart_required

def clear_icon_cache():
    commands = [
        'taskkill /f /im explorer.exe',
        'del /a /q "%localappdata%\\IconCache.db"',
        'del /a /f /q "%localappdata%\\Microsoft\\Windows\\Explorer\\iconcache*"',
        'start explorer.exe'
    ]
    restart_required = False
    success = True
    for cmd in commands:
        cmd_success, output = run_command(cmd)
        if "start explorer.exe" in cmd and cmd_success:
            restart_required = True
        if not cmd_success:
            success = False
            break
    if success:
        log("Icon cache cleared successfully.", level="info")
    else:
        log("Failed to clear icon cache.", level="error")
    if restart_required:
        log("Explorer was restarted to clear the icon cache.", level="info")
    return success, restart_required

def delete_temp_files():
    temp_paths = [
        os.path.expandvars(r"%temp%"),
        r"C:\Windows\Temp"
    ]
    success = True
    for path in temp_paths:
        try:
            if os.path.exists(path):
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path, ignore_errors=True)
                        log(f"Deleted: {item_path}", level="info")
                    except Exception as e:
                        log(f"Failed to delete {item_path}: {e}", level="error")
                        success = False
            else:
                log(f"Path not found: {path}", level="warning")
        except Exception as e:
            log(f"Error accessing {path}: {e}", level="error")
            success = False
    if success:
        log("Temporary files deleted successfully.", level="info")
    else:
        log("Failed to delete some temporary files.", level="error")
    return success

def disk_cleanup():
    cmd = "cleanmgr /sagerun:1"
    success, _ = run_command(cmd)
    if success:
        log("Disk cleanup completed successfully.", level="info")
    else:
        log("Disk cleanup failed.", level="error")
    return success

def run_sfc_scan():
    cmd = "sfc /scannow"
    success, _ = run_command(cmd)
    if success:
        log("SFC scan completed successfully.", level="info")
    else:
        log("SFC scan failed.", level="error")
    return success