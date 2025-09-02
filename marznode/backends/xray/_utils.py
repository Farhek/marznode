"""xray utilities"""

import re
import subprocess
from typing import Dict


def get_version(xray_path: str) -> str | None:
    """
    get xray version by running its executable
    :param xray_path:
    :return: xray version
    """
    cmd = [xray_path, "version"]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
    match = re.match(r"^Xray (\d+\.\d+\.\d+)", output)
    if match:
        return match.group(1)
    return None


def get_x25519(xray_path: str, private_key: str = None) -> Dict[str, str] | None:
    """
    get x25519 public key using the private key
    :param xray_path:
    :param private_key:
    :return: x25519 publickey
    """
    cmd = [xray_path, "x25519"]
    if private_key:
        cmd.extend(["-i", private_key])
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")

    # Try old style output
    match_old = re.search(r"Private key:\s*([^\n]+)\nPublic key:\s*([^\n]+)", output)
    if match_old:
        return {"private_key": match_old.group(1), "public_key": match_old.group(2)}

    # Try new style output (since v25.x)
    match_new_priv = re.search(r"PrivateKey:\s*([^\n]+)", output)
    match_new_pub  = re.search(r"Password:\s*([^\n]+)", output)
    if match_new_priv and match_new_pub:
        return {"private_key": match_new_priv.group(1), "public_key": match_new_pub.group(1)}


    return None
