from typing import Any, Dict
from base64 import b64decode
import json

from nacl.public import SealedBox


def decrypt_res(encrypted_res: Dict[str, str], key_pair: SealedBox) -> Dict[str, Any]:
    logs = {}

    for user_id_hash, encrypted_user_data in encrypted_res.items():
        base64_decoded = b64decode(encrypted_user_data)
        decrypted_bytes = key_pair.decrypt(base64_decoded)
        user_data = json.loads(decrypted_bytes.decode())
        logs[user_id_hash] = user_data

    return logs
