import os
import json
import shutil
from loguru import logger
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import base64

from Crypto.Cipher import AES
from base64 import b64encode, b64decode

GLOBAL_ENCRYPT_KEY = "whoisyourdaddya?"

class Crypt:
    def __init__(self, salt='SlTKeYOpHygTYkP3'):
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf-8'), AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc.encode('utf8'))
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf8'), AES.MODE_CFB, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)
    
class Encoder:
    def encode(self, data_string):
        data_string_bytes = data_string.encode()
        base64_bytes = base64.b64encode(data_string_bytes)
        base64_string = base64_bytes.decode()
        return base64_string

    def decode(self, base64_string):
        base64_bytes = base64_string.encode()

        data_string_bytes = base64.b64decode(base64_bytes)
        data_string = data_string_bytes.decode()
        return data_string

class MetaBase:
    data_field = 'RPGGOMetadata'

    def __init__(self, filepath, encrypt=False):
        self.filepath = filepath
        self.encrypt = encrypt

    def execute(self):
        pass


class MetaWriter(MetaBase):
    def execute(self, json_data_file):
        # clone the original file to avoid overwriting
        filename, file_extension = os.path.splitext(self.filepath)
        clone_filepath = filename + "_clone" + file_extension
        shutil.copyfile(self.filepath, clone_filepath)

        with open(json_data_file, 'r', encoding="utf-8-sig") as f:
            s_data = f.read()
        
        json_data = json.loads(s_data)
        data_string = json.dumps(json_data, ensure_ascii=False, indent=4)

        if self.encrypt:
            encoded_data_str = Crypt().encrypt(data_string, GLOBAL_ENCRYPT_KEY)
        else:
            encoded_data_str = Encoder().encode(data_string)

        metadata = PngInfo()
        metadata.add_itxt(self.data_field, encoded_data_str)

        targetImage = Image.open(self.filepath)

        targetImage.save(clone_filepath, pnginfo=metadata)


class MetaReader(MetaBase):
    def execute(self):
        import pprint
        targetImage = Image.open(self.filepath)

        metadata = targetImage.info.get(self.data_field)
        if self.encrypt:
            decoded_data_str = Crypt().decrypt(metadata, GLOBAL_ENCRYPT_KEY)
        else:
            decoded_data_str = Encoder().decode(metadata)
        logger.debug(decoded_data_str)
        #userdata=json.loads(metadata)
        #pprint.pprint(metadata)