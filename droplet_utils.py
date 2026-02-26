import base64
import os
from io import StringIO

import digitalocean
import paramiko

from logger_config import logger
from pathlib import Path
from typing import Dict, List


def get_ssh_key():
    """Load SSH private key from environment variable (base64 encoded or raw PEM) and return paramiko key object."""
    raw_value = os.getenv("DROPLET_SSH_PRIVATE_KEY")
    if not raw_value:
        return None

    ssh_private_key = None
    raw_value = raw_value.strip().replace("\r\n", "\n").replace("\r", "\n")

    try:
        to_decode = raw_value.replace("\n", "").replace(" ", "")
        if to_decode and len(to_decode) % 4:
            to_decode += "=" * (4 - len(to_decode) % 4)
        if to_decode:
            decoded = base64.b64decode(to_decode, validate=False)
            ssh_private_key = decoded.decode("utf-8", errors="replace")
    except Exception:
        pass

    if not ssh_private_key and raw_value.lstrip().startswith("-----"):
        ssh_private_key = raw_value

    if not ssh_private_key:
        logger.error("Could not parse DROPLET_SSH_PRIVATE_KEY (neither valid base64 nor PEM)")
        return None

    try:
        key_file = StringIO(ssh_private_key)
        return paramiko.Ed25519Key.from_private_key(key_file)
    except Exception:
        pass
    try:
        key_file = StringIO(ssh_private_key)
        return paramiko.RSAKey.from_private_key(key_file)
    except Exception as e:
        logger.error(f"Failed to load SSH key as Ed25519 or RSA: {str(e)}")
    return None


def get_droplet_info(droplet_ip: str) -> dict:
    """
    Get droplet information from DigitalOcean API.
    
    Args:
        droplet_ip: IP address of the droplet
    
    Returns:
        Dict containing droplet information or None if not found
    """
    try:
        do_token = os.getenv("DIGITALOCEAN_API_PAT")
        if not do_token:
            logger.warning("DigitalOcean API token not found, skipping droplet info")
            return None
        
        manager = digitalocean.Manager(token=do_token)
        droplets = manager.get_all_droplets()
        
        for droplet in droplets:
            if droplet.ip_address == droplet_ip:
                return {
                    "id": droplet.id,
                    "name": droplet.name,
                    "size": droplet.size_slug,
                    "region": droplet.region["slug"],
                    "status": droplet.status,
                    "created_at": droplet.created_at
                }
        
        logger.warning(f"Droplet with IP {droplet_ip} not found in DigitalOcean account")
        return None
        
    except Exception as e:
        logger.error(f"Error getting droplet info for {droplet_ip}: {str(e)}")
        return None

def get_available_droplet_ips(env_var_name: str = "AVAILABLE_IPS") -> List[str]:
    """
    Get list of available droplet IPs from environment variable.
    
    Args:
        env_var_name: Environment variable name containing droplet IPs
    
    Returns:
        List of droplet IP addresses
    """
    droplet_ips_str = os.getenv(env_var_name, "")
    if not droplet_ips_str:
        return []
    
    # Support both comma-separated and space-separated IPs
    droplet_ips = [ip.strip() for ip in droplet_ips_str.replace(',', ' ').split() if ip.strip()]
    logger.info(f"Found {len(droplet_ips)} droplet IPs: {droplet_ips}")
    return droplet_ips

def upload_files_to_droplet(local_dir: str, droplet_ip: str, remote_dir: str = "/root/task") -> bool:
    """
    Upload files from local directory to droplet via SSH.
    
    Args:
        local_dir: Local directory containing files to upload
        droplet_ip: IP address of the droplet
        remote_dir: Remote directory to upload files to
    
    Returns:
        True if successful, False otherwise
    """
    ssh_key = get_ssh_key()
    if not ssh_key:
        logger.error("Failed to load SSH key for droplet (set DROPLET_SSH_PRIVATE_KEY in env)")
        return False

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            droplet_ip,
            username="root",
            pkey=ssh_key,
            timeout=30
        )

        # Create remote directory
        ssh.exec_command(f"mkdir -p {remote_dir}")
        
        # Create SFTP client
        sftp = ssh.open_sftp()
        
        # Upload all files recursively
        local_path = Path(local_dir)
        for file_path in local_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(local_path)
                remote_file_path = f"{remote_dir}/{relative_path.as_posix()}"
                
                # Create remote directory if needed
                remote_file_dir = "/".join(remote_file_path.split("/")[:-1])
                ssh.exec_command(f"mkdir -p {remote_file_dir}")
                
                # Upload file
                sftp.put(str(file_path), remote_file_path)
                
                # Make shell scripts executable
                if file_path.suffix == ".sh":
                    ssh.exec_command(f"chmod +x {remote_file_path}")
                
                logger.info(f"Uploaded: {relative_path}")
        
        sftp.close()
        ssh.close()
        
        logger.info(f"Successfully uploaded files to {droplet_ip}:{remote_dir}")
        return True
        
    except Exception as e:
        logger.error(f"Error uploading files to droplet {droplet_ip}: {str(e)}")
        return False

def execute_script_on_droplet(droplet_ip: str, run_script: str) -> bool:
    """
    Execute a script on a droplet via SSH.
    
    Args:
        droplet_ip: IP address of the droplet
        run_script: Path to the script to execute
    
    Returns:
        True if successful, False otherwise
    """
    ssh_key = get_ssh_key()
    if not ssh_key:
        logger.error("Failed to load SSH key for droplet (set DROPLET_SSH_PRIVATE_KEY in env)")
        return False

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            droplet_ip,
            username="root",
            pkey=ssh_key,
            timeout=30
        )

        # Execute the script
        logger.info(f"Executing {run_script} on droplet {droplet_ip}...")
        stdin, stdout, stderr = ssh.exec_command(f"bash {run_script}")

        # Wait for completion and get output
        stdout_data = stdout.read().decode()
        stderr_data = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()

        if stdout_data:
            print(f"Script output:\n{stdout_data}")
            logger.info(f"Script output:\n{stdout_data}")
        if stderr_data:
            print(f"Script errors:\n{stderr_data}")
            logger.info(f"Script errors:\n{stderr_data}")

        if exit_status == 0:
            print(f"{run_script} executed successfully on {droplet_ip}")
            logger.info(f"{run_script} executed successfully on {droplet_ip}")
            ssh.close()
            return True
        else:
            print(f"{run_script} failed with exit status: {exit_status}")
            logger.error(f"{run_script} failed with exit status: {exit_status}")
            ssh.close()
            return False

    except Exception as e:
        print(f"Error executing script on droplet {droplet_ip}: {str(e)}")
        logger.error(f"Error executing script on droplet {droplet_ip}: {str(e)}")
        return False
