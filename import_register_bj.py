# import glob
import os
import re
import rarfile
import shutil
import glob
from javcore import common
from javcore import data
from javcore import db
from javcore import site
from send2trash import send2trash


class ImportRegisterBj:

    def __init__(self):

        # rarfile.DEFAULT_CHARSET = "windows-1252"
        # rarfile.UNRAR_TOOL = 'unrar'
        rarfile.UNRAR_TOOL = r'C:\\Program Files (x86)\\UnrarDLL\\Examples\\MASM\\unrar'
        # rarfile.UNRAR_TOOL = r'C:\\SHARE\\unrar.exe'
        self.movie_extension = '.*\.avi$|.*\.wmv$|.*\.mpg$|.*ts$|.*divx$|.*mp4$' \
                               '|.*asf$|.*mkv$|.*rm$|.*rmvb$|.*m4v$|.*3gp$|.*flv'

        self.register_path = "D:\DATA\Downloads\TEMP"
        if not os.path.exists(self.register_path):
            print('not exist path store_path [' + self.register_path + ']')
            exit(-1)

        self.store_path = "C:\mydata\\bj-jpeg"
        if not os.path.exists(self.store_path):
            print('not exist path store_path [' + self.store_path + ']')
            exit(-1)

        self.import_dao = db.import_dao.ImportDao()
        self.bj_dao = db.bj.BjDao()
        self.wiki = site.wiki.SougouWiki()

        self.is_check = True
        # self.is_check = False
        # self.target_max = 200
        # self.__set_files()

    def arrange_execute(self):

        bjs = self.bj_dao.get_all()

        # print('count bjs [{}]'.format(len(bjs)))
        err_list = []
        target_idx = 1
        bj_parser = common.BjParser()
        idx2 = 0
        for idx, bj in enumerate(bjs):

            is_err = False
            if not bj.isSelection == 1:
                continue

            bj.parse(bj_parser)
            bj.print()

            for thumbnail_info in bj.thumbnailInfoList:
                pathname = os.path.join(self.store_path, thumbnail_info.filename)
                if not os.path.isfile(pathname):
                    err_list.append('[' + str(bj.id) + '] JPEGが存在しない [' + pathname + ']')

            rar_pathname = os.path.join(self.register_path, bj.rar_filename)
            size = 0
            if not os.path.isfile(rar_pathname):
                err_list.append('[' + str(bj.id) + '] RARが存在しない [' + rar_pathname + ']')
                is_err = True
            else:
                size = os.path.getsize(rar_pathname)
                print('  OK ' + rar_pathname)

            base_pathname = os.path.join(self.register_path, bj.basename)

            if not os.path.exists(base_pathname):
                file_list = glob.glob(os.path.join(self.register_path, bj.basename + '*'))
                is_exist = False
                for file in file_list:
                    if re.search(self.movie_extension, file, re.IGNORECASE):
                        # err_list.append('[{}] DIRなしで動画が存在する [{}] {}'.format(bj.id, base_pathname, file_list))
                        is_exist = True
                        break

                if is_exist is False:
                    err_list.append('[' + str(bj.id) + '] DIRが存在しない [' + base_pathname + ']')
                    is_err = True
            else:
                print('  OK ' + base_pathname)

            if is_err:
                continue

            for thumbnail_info in bj.thumbnailInfoList:
                src_pathname = os.path.join(self.store_path, thumbnail_info.filename)
                dest_pathname = os.path.join(self.register_path, thumbnail_info.dest_filename)
                if not self.is_check:
                    shutil.copy2(src_pathname, dest_pathname)
                else:
                    print('  {} -> {}'.format(src_pathname, dest_pathname))

            import_data = data.ImportData()
            import_data.title = bj.title
            import_data.postDate = bj.postDate
            import_data.copy_text = bj.base_filename
            import_data.productNumber = bj.basename
            import_data.kind = 5
            import_data.actress = bj.actress
            import_data.isNameOnly = True
            import_data.url = bj.url
            import_data.rating = bj.rating
            import_data.tag = bj.tag
            import_data.maker = bj.postedIn
            import_data.size = size

            if not self.is_check:
                self.import_dao.export_import(import_data)
                self.bj_dao.update_is_selection(bj.id, 9)

            if target_idx > self.target_max:
                break

            target_idx = target_idx + 1

        for err in err_list:
            print(err)

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
