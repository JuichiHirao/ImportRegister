from db import mysql_control
import os
from data import site_data
import glob
import re
import rarfile
import shutil


class ImportRegister:

    def __init__(self):

        # rarfile.DEFAULT_CHARSET = "windows-1252"
        # rarfile.UNRAR_TOOL = 'unrar'
        rarfile.UNRAR_TOOL = r'C:\\Program Files (x86)\\UnrarDLL\\Examples\\MASM\\unrar'
        # rarfile.UNRAR_TOOL = r'C:\\SHARE\\unrar.exe'
        self.movie_extension = '.*\.avi$|.*\.wmv$|.*\.mpg$|.*ts$|.*divx$|.*mp4$' \
                               '|.*asf$|.*mkv$|.*rm$|.*rmvb$|.*m4v$|.*3gp$'

        self.store_path = "D:\DATA\jav-save"
        self.register_path = "D:\DATA\Downloads"

        self.db = mysql_control.DbMysql()
        self.makers = self.db.get_movie_maker()

        self.is_check = True
        # self.is_check = False
        self.__set_files()

    def __set_files(self):

        self.files = glob.glob(self.register_path + '\*')
        # print(len(self.files))

    def __get_target_files(self, jav):

        re_pattern1 = re.compile('.*' + jav.productNumber + '.*', re.IGNORECASE)
        find_filter = filter(lambda file: re_pattern1.match(file), self.files)

        find_list = list(find_filter)

        if len(find_list) > 0:
            return find_list

        files = []
        for link in jav.downloadLinks.split(' '):
            files.append(link.split('/')[-1].replace('.html', ''))

        return files

    def __parse_files(self, jav, file_list):

        is_rar = False
        is_movie = False
        is_split = False
        is_err_extract = False

        re_rar = re.compile('part1.rar$', re.IGNORECASE)
        re_movie = re.compile(self.movie_extension, re.IGNORECASE)

        for file in file_list:
            rar_file = ''
            extract_file = ''
            if re_rar.search(file):
                rar_file = os.path.basename(file)
                print('  rar   ' + rar_file)
                is_rar = True
                infolist = rarfile.RarFile(file).infolist()
                if len(infolist) == 1:
                    for f in rarfile.RarFile(file).infolist():
                        extract_file = f.filename
                        print('  extract ' + str(f.filename))

                if len(extract_file):
                    extract_pathname = os.path.join(self.register_path, extract_file)
                    if not os.path.exists(extract_pathname):
                        rarfile.RarFile(file).extractall()
                        print('  extracted rar [' + extract_file + ']')

            if re_movie.search(file):
                filename = os.path.basename(file)
                name, ext = os.path.splitext(filename)
                print('  movie ' + filename)
                if is_movie:
                    is_split = True
                is_movie = True

            if len(rar_file) > 0:
                if name in rar_file:
                    print('  extracted rar ' + rar_file)
                else:
                    is_err_extract = True

        result_tuple = (is_movie, is_split, is_rar, is_err_extract)
        print('  movie ' + str(is_movie) + '  split ' + str(is_split) + '  rar ' + str(is_rar) + '  err extract '
              + str(is_err_extract))

        return result_tuple

    def arrange_execute(self):

        javs = self.db.get_javs()

        err_list = []
        target_idx = 1
        for idx, jav in enumerate(javs):

            is_err = False

            if not jav.isSelection == 1:
                continue

            if jav.actress == '—-':
                jav.actress = ''

            if jav.isParse2 < 0:
                if jav.isParse2 == -1:
                    print('-1 ' + str(jav.id) + ' メーカー完全一致だが、タイトル内に製品番号が一致しない [' + jav.maker + ']' + jav.title)
                if jav.isParse2 == -2:
                    print('-2 ' + str(jav.id) + ' メーカーと、タイトル内に製品番号複数一致 [' + jav.maker + ']' + jav.title)
                if jav.isParse2 == -3:
                    print('-3 ' + str(jav.id) + ' メーカには複数一致、製品番号に一致しない ID [' + str(jav.id) + '] jav [' + jav.maker + ':' + jav.label + ']' + jav.title)
                if jav.isParse2 == -4:
                    print('-4 ' + str(jav.id) + ' maker exist no match, not register [' + jav.maker + ':' + jav.label + '] ' + jav.title)
                if jav.isParse2 == -5:
                    print('-5 ' + str(jav.id) + ' match maker other maker.matchStr [' + str(match_maker.id) + ']' + match_maker.matchStr + '  ' + jav.title)
                if jav.isParse2 == -6:
                    print('-6 ' + str(jav.id) + ' many match ' + jav.title)
                if jav.isParse2 == -7:
                    print('-7 ' + str(jav.id) + ' no match ' + jav.title)
                else:
                    print('-x ' + str(jav.id) + ' errno[' + str(jav.isParse2) + '] First error no ' + jav.title)

                # break

            if jav.makersId <= 0:
                continue

            if jav.productNumber is None or len(jav.productNumber) <= 0:
                err_list.append('productNumber is None [' + str(jav.id) + '] ' + jav.title)
                continue

            files = self.__get_target_files(jav)

            pathname_th = os.path.join(self.store_path, jav.thumbnail)
            if not os.path.isfile(pathname_th):
                err_list.append('not exist thumbnail ' + str(jav.id) + '[' + jav.thumbnail + '] ' + jav.title)
                continue

            pathname_p = os.path.join(self.store_path, jav.package)
            # print('pathname_p ' + pathname_p)
            if not os.path.isfile(pathname_p):
                err_list.append('not exist package ' + str(jav.id) + ' [' + jav.package + '] ' + jav.title)
                continue

            if jav.makersId > 0:
                find_filter = filter(lambda maker: maker.id == jav.makersId, self.makers)
                find_list = list(find_filter)

                if len(find_list) == 1:
                    match_maker = find_list[0]
                else:
                    err_list.append('jav.makersId [' + jav.makersId + '] がmakersに存在しません ' + jav.title)
                    continue

            if target_idx > 3:
                break
            target_idx = target_idx + 1

            print('[' + str(jav.id) + '] ' + jav.title)
            import_data = site_data.ImportData()
            is_movie, import_data.isSplit, import_data.isRar, is_err_extract = self.__parse_files(jav, files)

            if not is_movie:
                err_list.append('movie not found ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title)
                is_err = True

            if is_err_extract:
                err_list.append('error extract ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title)
                is_err = True

            if is_err:
                continue

            import_data.postDate = jav.postDate
            import_data.copy_text = jav.title
            import_data.productNumber = jav.productNumber.upper()
            import_data.matchStr = match_maker.matchStr
            import_data.kind = match_maker.kind
            import_data.maker = match_maker.get_maker(jav.label)
            import_data.sellDate = jav.sellDate
            # import_data.actress = jav.actress
            import_data.tag = jav.actress
            import_data.isNameOnly = True
            import_data.url = jav.url
            import_data.rating = jav.rating

            filename, ext = os.path.splitext(pathname_p)
            dest_p = os.path.join(self.register_path, import_data.productNumber + ext)
            if not self.is_check:
                shutil.copy2(pathname_p, dest_p)
            print('  ' + dest_p + " <- " + pathname_p)

            filename, ext = os.path.splitext(pathname_th)
            dest_th = os.path.join(self.register_path, import_data.productNumber + 'big' + ext)
            if not self.is_check:
                shutil.copy2(pathname_th, dest_th)
            print('  ' + dest_th + " <- " + pathname_th)
            if not self.is_check:
                self.db.export_import(import_data)
                self.db.update_jav_is_selection(jav.id, 9)

        for err in err_list:
            print(err)


if __name__ == '__main__':
    importRegister = ImportRegister()
    importRegister.arrange_execute()
