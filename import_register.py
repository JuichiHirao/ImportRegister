
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

        self.__set_files()

    def __set_files(self):

        self.files = glob.glob(self.register_path + '\*')
        # print(len(self.files))

    def __get_target_files(self, product_number, jav):

        re_pattern1 = re.compile('.*' + product_number + '.*', re.IGNORECASE)
        find_filter = filter(lambda file: re_pattern1.match(file), self.files)

        return list(find_filter)

    def __get_link_files(self, download_links):

        files = []
        for link in download_links.split(' '):
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
        for idx, jav in enumerate(javs):

            is_err = False
            idx = idx + 1

            if idx > 50:
                break

            if jav.productNumber is None:
                err_list.append('productNumber is None [' + str(jav.id) + '] ' + jav.title)
                is_err = True
                continue
            files = self.__get_target_files(jav.productNumber, jav)

            pathname_th = os.path.join(self.store_path, jav.thumbnail)
            if not os.path.isfile(pathname_th):
                err_list.append('not exist thumbnail ' + str(jav.id) + '[' + jav.thumbnail + '] ' + jav.title)
                is_err = True
                # print('not exist thumbnail [' + pathname + ']')
                continue

            pathname_p = os.path.join(self.store_path, jav.package)
            # print('pathname_p ' + pathname_p)
            if not os.path.isfile(pathname_p):
                err_list.append('not exist package ' + str(jav.id) + ' [' + jav.package + '] ' + jav.title)
                is_err = True
                # print('not exist package  [' + pathname + ']')
                continue

            if is_err:
                continue

            # ハイフンで区切ったメーカーを取得
            match_str = ''
            if '-' in jav.productNumber:
                match_str = jav.productNumber.split('-')[0]

            if len(match_str) > 0:
                repattern = re.compile(match_str, re.IGNORECASE)
                find_filter = filter(lambda maker: repattern.match(maker.matchStr), self.makers)
                find_list = list(find_filter)

                if len(find_list) == 1:
                    if jav.maker in find_list[0].label or jav.maker == find_list[0].name:
                        print(jav.title)
                    else:
                        print('confirm ' + jav.title)
                        print('  ' + str(find_list[0].name))
                elif len(find_list) > 1:
                    repattern_label = re.compile(jav.label, re.IGNORECASE)
                    if len(jav.label) == 0:
                        find_filter_label = filter(lambda maker: len(maker.label) == 0, find_list)
                    else:
                        find_filter_label = filter(lambda maker: maker.label == jav.label, find_list)
                    find_list_label = list(find_filter_label)
                    if len(find_list_label) == 1:
                        find_list = find_list_label
                    elif len(find_list_label) > 1:
                        err_list.append('many match ' + str(jav.id) + '  [' + jav.label + ']  ' + jav.title)
                        for maker in find_list_label:
                            m = repattern_label.match(maker.label)
                            err_list.append('    res ' + str(m.start()))
                            err_list.append('    [' + maker.get_maker() + ']')
                        is_err = True
                    else:
                        err_list.append('many match label no match ' + str(jav.id) + '  [' + match_str + ']  ' + jav.title)
                        is_err = True
                else:
                    err_list.append('no match ' + str(jav.id) + '  [' + match_str + ']  ' + jav.title)
                    is_err = True
            else:
                err_list.append('wrong match_str ' + str(jav.id) + '  [' + match_str + ']  ' + jav.title)
                is_err = True

            import_data = site_data.ImportData()
            is_movie, import_data.isSplit, import_data.isRar, is_err_extract = self.__parse_files(jav, files)

            if not is_movie:
                err_list.append('movie not found ' + str(jav.id) + '  [' + match_str + ']  ' + jav.title)
                for file in self.__get_link_files(jav.downloadLinks):
                    err_list.append('  ' + file)
                is_err = True

            if is_err_extract:
                err_list.append('error extract ' + str(jav.id) + '  [' + match_str + ']  ' + jav.title)
                is_err = True

            if is_err:
                continue

            import_data.postDate = jav.postDate
            import_data.copy_text = jav.title
            import_data.productNumber = jav.productNumber.upper()
            import_data.matchStr = match_str
            if len(find_list) == 1:
                import_data.kind = find_list[0].kind
                import_data.maker = find_list[0].get_maker()
            import_data.sellDate = jav.sellDate
            import_data.actress = jav.actress
            import_data.isNameOnly = True
            import_data.url = jav.url

            filename, ext = os.path.splitext(pathname_p)
            dest_p = os.path.join(self.register_path, import_data.productNumber + ext)
            # shutil.copy2(pathname_p, dest_p)
            print('  ' + dest_p + " <- " + pathname_p)

            filename, ext = os.path.splitext(pathname_th)
            dest_th = os.path.join(self.register_path, import_data.productNumber + 'big' + ext)
            # shutil.copy2(pathname_th, dest_th)
            print('  ' + dest_th + " <- " + pathname_th)
            # self.db.export_import(import_data)
            # self.db.update_jav_is_selection(jav.id, 9)

        for err in err_list:
            print(err)


if __name__ == '__main__':

    importRegister = ImportRegister()
    importRegister.arrange_execute()

