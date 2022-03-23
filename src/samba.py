import os
import traceback
from pathlib import Path

from loguru import logger as log
from smb.SMBConnection import SMBConnection


class SMBClient(object):
    smb: SMBConnection

    def __init__(self, user_name: str, passwd: str, ip: str, port: int = 139):
        self.status = False
        self.user_name = user_name
        self.passwd = passwd
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            self.smb = SMBConnection(self.user_name, self.passwd, 'py_smb', '', use_ntlm_v2=True)
            self.smb.connect(self.ip, self.port)
            self.status = self.smb.auth_result
        except Exception as e:
            log.error(e)
            self.smb.close()

    def disconnect(self):
        if self.status:
            self.smb.close()

    def list_shared_folders(self):
        return [s.name for s in self.smb.listShares()]

    def has_shared_folder(self, folder_name: str) -> bool:
        return folder_name in self.list_shared_folders()

    def list_objects(self, shared_folder: str, dir_name: str) -> list:
        objects = list()
        for obj in self.smb.listPath(shared_folder, dir_name):
            objects.append(obj)
        return objects

    def list_dirs(self, shared_folder: str, dir_name: str) -> list:
        objs = self.list_objects(shared_folder, dir_name)
        return [obj.filename for obj in objs if obj.isDirectory is True]

    def list_files(self, shared_folder: str, dir_name: str) -> list:
        objs = self.list_objects(shared_folder, dir_name)
        return [obj.filename for obj in objs if obj.isDirectory is False]

    def download(self, shared_folder: str, remote_dir: str, file_names: str, local_dir: str):
        for file_name in file_names:
            with open(os.path.join(local_dir, file_name), 'w') as file_obj:
                self.smb.retrieveFile(shared_folder, os.path.join(remote_dir, file_name), file_obj)

    def upload_file(self, shared_folder: str, smb_dir: str, local_file_path: str):
        with open(local_file_path, 'rb') as file:
            p = Path(local_file_path)
            remote_path = os.path.join(smb_dir, p.name)
            return self.smb.storeFile(shared_folder, remote_path, file)

    def upload_folder(self, shared_folder, smb_dir, local_folder_path):
        """TODO"""
        pass

    def mkdir(self, shared_folder: str, path: str):
        paths = path.split('/')
        try:
            for i, sub_dir in enumerate(paths):
                parent_dir = '/'.join(paths[:i])
                cur_path = os.path.join(parent_dir, sub_dir)
                if sub_dir not in self.list_dirs(shared_folder, parent_dir):
                    if sub_dir in self.list_files(shared_folder, parent_dir):
                        msg = f'There is a file with the same name={sub_dir} in {parent_dir}.'
                        raise FileExistsError(msg)
                    elif sub_dir == cur_path:
                        continue
                    else:
                        self.smb.createDirectory(shared_folder, cur_path)
        except Exception as e:
            log.error(f'Make dir {path} Failed! detail: {str(e)}')
            log.error(traceback.format_exc())

    def show_file_attr(self, shared_folder: str, path: str, file_obj: str):
        file_attr, file_size = self.smb.retrieveFile(shared_folder, path, file_obj)
        return file_attr, file_size
