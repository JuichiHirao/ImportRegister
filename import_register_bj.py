from db import mysql_control
import os
from data import site_data
import re
import rarfile
import shutil


class ImportRegisterBj:

    def __init__(self):

        # rarfile.DEFAULT_CHARSET = "windows-1252"
        # rarfile.UNRAR_TOOL = 'unrar'
        rarfile.UNRAR_TOOL = r'C:\\Program Files (x86)\\UnrarDLL\\Examples\\MASM\\unrar'
        # rarfile.UNRAR_TOOL = r'C:\\SHARE\\unrar.exe'
        self.movie_extension = '.*\.avi$|.*\.wmv$|.*\.mpg$|.*ts$|.*divx$|.*mp4$' \
                               '|.*asf$|.*mkv$|.*rm$|.*rmvb$|.*m4v$|.*3gp$'

        self.register_path = "D:\DATA\Downloads\TEMP"
        if not os.path.exists(self.register_path):
            print('not exist path store_path [' + self.register_path + ']')
            exit(-1)

        self.store_path = "D:\DATA\\bj-jpeg"
        if not os.path.exists(self.store_path):
            print('not exist path store_path [' + self.store_path + ']')
            exit(-1)
        self.db = mysql_control.DbMysql()

        # self.is_check = True
        self.is_check = False
        self.target_max = 30;
        # self.__set_files()

    def arrange_execute(self):

        bjs = self.db.get_bj()

        err_list = []
        target_idx = 1
        for idx, bj in enumerate(bjs):

            is_err = False

            if not bj.isSelection == 1:
                continue

            bj.print()

            jpeg_links = []
            for jpeg_link in bj.thumbnails.split(' '):
                pathname = os.path.join(self.store_path, jpeg_link.split('/')[-1])
                if not os.path.exists(pathname):
                    err_list.append('[' + bj.id + '] JPEGが存在しない [' + pathname + ']')
                else:
                    jpeg_links.append(pathname)

            rar_filename = bj.downloadLink.split('/')[-1]
            rar_pathname = os.path.join(self.register_path, rar_filename)
            size = 0
            if not os.path.exists(rar_pathname):
                err_list.append('[' + bj.id + '] RARが存在しない [' + rar_pathname + ']')
                is_err = True
            else:
                size = os.path.getsize(rar_pathname)
                print('  OK ' + rar_pathname)

            base_name = rar_filename.replace('.rar', '')
            base_pathname = os.path.join(self.register_path, base_name)

            if not os.path.exists(base_pathname):
                err_list.append('[' + bj.id + '] RARが存在しない [' + rar_pathname + ']')
                is_err = True
            else:
                print('  OK ' + base_pathname)

            if is_err:
                break

            tag = ''
            actress = self.__get_actress(bj.title, bj.postedIn)
            if len(actress) > 0:
                print('    actress [' + actress + ']')
                tag = 'KOREAN BJ ' + actress
                tag = tag.replace('BJ BJ ', 'BJ ')
                target_name = base_name + ' ' + bj.title + ' ' + actress
            else:
                target_name = base_name + ' ' + bj.title
            print('  ' + target_name)

            idx = 1
            if len(jpeg_links) == 1:
                idx = 0
            for jpeg in jpeg_links:
                suffix = ''
                if idx > 0:
                    suffix = '_' + str(idx)

                dest_pathname = os.path.join(self.register_path, target_name + suffix + '.jpg')
                if not self.is_check:
                    shutil.copy2(jpeg, dest_pathname)
                else:
                    print('      ' + dest_pathname + ' <-- ' + jpeg)

                idx = idx + 1

            import_data = site_data.ImportData()
            import_data.title = bj.title
            import_data.postDate = bj.postDate
            import_data.copy_text = target_name
            import_data.productNumber = base_name
            import_data.kind = 5
            import_data.actress = actress
            import_data.isNameOnly = True
            import_data.url = bj.url
            import_data.rating = bj.rating
            import_data.tag = tag
            import_data.maker = bj.postedIn
            import_data.size = size

            if not self.is_check:
                self.db.export_import(import_data)
                self.db.update_bj_is_selection(bj.id, 9)

            if target_idx > self.target_max:
                break

            target_idx = target_idx + 1

    def __get_actress(self, title, posted_in):
        actress = ''
        if '201' in title and "KOREAN BJ" in title:
            match = re.search('[A-Z ]* 201', title)
            if match:
                replace_str = match.group().replace(' 201', '')
                actress = posted_in.replace(replace_str, '').strip()
                print('    ' + replace_str + '  ' + actress)
            else:
                print('    not match')

        return actress


if __name__ == '__main__':
    importRegister = ImportRegisterBj()
    importRegister.arrange_execute()
