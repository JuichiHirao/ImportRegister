import glob
import os
import re
import rarfile
import shutil
from javcore import data
from javcore import db
from send2trash import send2trash


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

        self.import_dao = db.import_dao.ImportDao()
        self.bj_dao = db.bj.BjDao()

        self.is_check = True
        # self.is_check = False
        self.target_max = 30;
        # self.__set_files()

    def arrange_execute(self):

        bjs = self.bj_dao.get_all()

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

            dest_register_path = ''
            if 'VIDEOS' in bj.postedIn:
                dest_register_path = os.path.abspath(os.path.join(self.register_path, os.pardir))
            else:
                dest_register_path = self.register_path

            idx = 1
            if len(jpeg_links) == 1:
                idx = 0
            for jpeg in jpeg_links:
                suffix = ''
                if idx > 0:
                    suffix = '_' + str(idx)

                dest_pathname = os.path.join(dest_register_path, target_name + suffix + '.jpg')
                if not self.is_check:
                    shutil.copy2(jpeg, dest_pathname)
                else:
                    print('      ' + dest_pathname + ' <-- ' + jpeg)

                idx = idx + 1

            import_data = data.ImportData()
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

            if 'VIDEOS' in bj.postedIn:
                video_dir_pathname = os.path.join(self.register_path, base_name)
                # rar_pathname
                if os.path.exists(video_dir_pathname):
                    files = glob.glob(video_dir_pathname + '\*')
                    re_movie = re.compile(self.movie_extension, re.IGNORECASE)
                    mov_files = []
                    for file_data in files:
                        if re_movie.search(file_data):
                            mov_files.append(file_data)
                    if len(mov_files) >= 1:
                        if len(mov_files) == 1:
                            extension = os.path.splitext(os.path.basename(mov_files[0]))[1]
                            movie_dest_pathname = os.path.join(dest_register_path, base_name + extension.lower())

                            if not self.is_check:
                                shutil.copy2(mov_files[0], movie_dest_pathname)
                            print('      ' + movie_dest_pathname + ' <-- ' + mov_files[0])
                        else:
                            for movie_idx, mov_file in enumerate(mov_files):
                                extension = os.path.splitext(os.path.basename(mov_file))[1]
                                movie_dest_pathname = os.path.join(dest_register_path, base_name + '_' + str(movie_idx+1) + extension.lower())
                                if not self.is_check:
                                    shutil.copy2(mov_file, movie_dest_pathname)
                                print('      ' + movie_dest_pathname + ' <-- ' + mov_file)

                    if not self.is_check:
                        send2trash(video_dir_pathname)
                        send2trash(rar_pathname)

                    if 'UNCENSORED' in bj.title:
                        import_data.tag = 'UNCENSORED'

            if not self.is_check:
                self.import_dao.export_import(import_data)
                self.bj_dao.update_is_selection(bj.id, 9)

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
