from db import mysql_control
import os
from data import site_data
import glob
import re
import rarfile
import shutil

from tool import product_number_register


class ImportRegister:

    def __init__(self):

        # rarfile.DEFAULT_CHARSET = "windows-1252"
        # rarfile.UNRAR_TOOL = 'unrar'
        rarfile.UNRAR_TOOL = r'C:\\Program Files (x86)\\UnrarDLL\\Examples\\MASM\\unrar'
        # rarfile.UNRAR_TOOL = r'C:\\SHARE\\unrar.exe'
        self.movie_extension = '.*\.avi$|.*\.wmv$|.*\.mpg$|.*ts$|.*divx$|.*mp4$' \
                               '|.*asf$|.*mkv$|.*rm$|.*rmvb$|.*m4v$|.*3gp$'
        self.rar_extension = '.*\.rar$'

        self.store_path = "D:\DATA\jav-save"
        self.register_path = "D:\DATA\Downloads"

        self.db = mysql_control.DbMysql()
        self.makers = self.db.get_movie_maker()

        self.is_recover_check = True
        # self.is_recover_check = False
        self.is_check = True
        # self.is_check = False

        self.target_max = 20
        self.__set_files()

    def __set_files(self):

        self.files = glob.glob(self.register_path + '\*')
        # print(len(self.files))

    def __get_target_files(self, jav):

        idx = 0
        if jav.id == 5744:
            idx = idx + 1
        files = []
        re_pattern1 = re.compile('.*' + jav.productNumber + '.*', re.IGNORECASE)
        find_filter = filter(lambda file: re_pattern1.match(file), self.files)
        find_list = list(find_filter)

        re_movie = re.compile(self.movie_extension, re.IGNORECASE)
        re_rar = re.compile(self.rar_extension, re.IGNORECASE)
        for data in find_list:
            if re_movie.search(data):
                files.append(data)
            if re_rar.search(data):
                files.append(data)

        if len(files) <= 0:
            for link in jav.downloadLinks.split(' '):
                link_filename = link.split('/')[-1].replace('.html', '')
                pathname = os.path.join(self.register_path, link_filename)
                if os.path.isfile(pathname):
                    files.append(pathname)
                else:
                    # [030718] XXXX
                    search_file = re.search('\[[0-3][0-9][0-1][0-9][1-2][0-9]\]', link_filename)
                    if search_file:
                        replace_filename = link_filename.replace(search_file.group(), '').strip()
                        replace_pathname = os.path.join(self.register_path, replace_filename)
                        if os.path.isfile(replace_pathname):
                            files.append(replace_filename)

        return files

    def __parse_files(self, jav, file_list):

        is_rar = False
        movie_size = 0
        is_split = False
        is_err_extract = False

        re_rar = re.compile('part1.rar$', re.IGNORECASE)
        re_movie = re.compile(self.movie_extension, re.IGNORECASE)

        movie_count = 0
        for file in file_list:
            rar_file = ''
            extract_file = ''
            if re_rar.search(file):
                rar_file = os.path.basename(file)
                print('  rar   ' + rar_file)
                is_rar = True
                rar_pathname = os.path.join(self.register_path, rar_file)
                if not os.path.exists(rar_pathname):
                    print('  rarファイルが存在しない [' + rar_pathname + ']')
                    is_err_extract = True
                    continue
                else:
                    rar_archive = rarfile.RarFile(rar_pathname)
                    rar_infolist = rar_archive.infolist()
                    if len(rar_infolist) >= 1:
                        for f in rar_infolist:
                            extract_file = f.filename

                            extract_pathname = os.path.join(self.register_path, extract_file)
                            if not os.path.exists(extract_pathname):
                                is_err_extract = True
                                print('  rarファイルが解凍されていない [' + extract_file + ']' + file)
                            else:
                                if extract_pathname not in file_list:
                                    file_list.append(extract_pathname)

            if re_movie.search(file):
                filename = os.path.basename(file)
                name, ext = os.path.splitext(filename)
                print('  movie ' + filename)
                size_pathname = os.path.join(self.register_path, file)
                if os.path.isfile(size_pathname):
                    size = os.path.getsize(size_pathname)
                    movie_size = movie_size + size

                re_movie = re.compile(self.movie_extension, re.IGNORECASE)
                if re_movie.search(file):
                    movie_count += 1

        if movie_count > 1:
            is_split = True

        result_tuple = (movie_size, is_split, is_rar, is_err_extract)
        print('  movie_size ' + str(movie_size) + '  split ' + str(is_split) + '  rar ' + str(is_rar) + '  err extract '
              + str(is_err_extract))

        return result_tuple

    def __get_title_from_copytext(self, copy_text, product_number, match_maker):

        hankaku = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        zenkaku = ['１', '２', '３', '４', '５', '６', '７', '８', '９', '０']
        title = ''
        movie_kind = ''

        if match_maker.replaceWords is not None and len(match_maker.replaceWords) > 0:
            words = match_maker.replaceWords.split(' ')
            for word in words:
                copy_text = re.sub(word, '', copy_text)
            '''
            if ' ' in match_maker.replaceWords:
                words = ' '.split(match_maker.replaceWords)
                for word in ' '.split(match_maker.replaceWords):
                    copy_text = re.sub(word, '', copy_text)
            else:
                copy_text = re.sub(match_maker.replaceWords, '', copy_text)
            '''

        match_search = re.search('[\[]*FHD[\]]*', copy_text)
        if match_search:
            title = copy_text.replace(match_search.group(), '').replace(product_number.upper(), '', )\
                .replace(product_number.lower(), '', )
            movie_kind = ' FHD'
        else:
            title = copy_text.replace(product_number, '').strip()

        if len(movie_kind) > 0:
            title = title.strip() + movie_kind

        match_maker_name = re.search(match_maker.matchName, title)
        if match_maker_name:
            title = title.replace(match_maker_name.group(), '')

        return title.strip()

    def recover_p_number_register(self, jav, tool):

        jav.productNumber, seller, sell_date, match_maker, ng_reason = tool.parse2(jav, self.is_recover_check)
        print(jav.productNumber + ' title [' + jav.title + ']')
        if match_maker is None:
            print('no match maker '  ' title [' + jav.title + ']')

        if not self.is_recover_check:
            self.db.update_jav_product_number(jav.id, jav.productNumber)

    def arrange_execute(self):

        javs = self.db.get_javs()

        err_list = []
        target_idx = 1
        p_number_tool = product_number_register.ProductNumberRegister()
        for idx, jav in enumerate(javs):

            is_err = False

            if not jav.isSelection == 1:
                continue

            if jav.actress == '—-':
                jav.actress = ''

            if jav.isParse2 < 0:
                if jav.isParse2 == -1:
                    print('-1 ' + str(jav.id) + ' メーカー完全一致だが、タイトル内に製品番号が一致しない [' + jav.maker + ']' + jav.title)
                elif jav.isParse2 == -2:
                    print('-2 ' + str(jav.id) + ' メーカーと、タイトル内に製品番号複数一致 [' + jav.maker + ']' + jav.title)
                elif jav.isParse2 == -3:
                    print('-3 ' + str(jav.id) + ' メーカには複数一致、製品番号に一致しない ID [' + str(jav.id) + '] jav [' + jav.maker + ':' + jav.label + ']' + jav.title)
                elif jav.isParse2 == -4:
                    print('-4 ' + str(jav.id) + ' maker exist no match, not register [' + jav.maker + ':' + jav.label + '] ' + jav.title)
                elif jav.isParse2 == -5:
                    print('-5 ' + str(jav.id) + 'メーカー[' + jav.maker + ':' + jav.label + '] に一致したが、タイトル内にmatchStrの文字列がない ' + jav.title)
                elif jav.isParse2 == -6:
                    print('-6 ' + str(jav.id) + ' many match ' + jav.title)
                elif jav.isParse2 == -7:
                    print('-7 ' + str(jav.id) + ' no match ' + jav.title)
                else:
                    print('-x ' + str(jav.id) + ' errno[' + str(jav.isParse2) + '] First error no ' + jav.title)

                self.recover_p_number_register(jav, p_number_tool)

                # break

            if jav.makersId <= 0:
                continue

            if jav.productNumber is None or len(jav.productNumber) <= 0:
                err_list.append('productNumber is None [' + str(jav.id) + '] ' + jav.title)
                continue

            files = self.__get_target_files(jav)

            is_exist = False
            for thumbnail in jav.thumbnail.split(' '):
                pathname_th = os.path.join(self.store_path, thumbnail)
                if os.path.isfile(pathname_th):
                    jav.thumbnail = thumbnail
                    is_exist = True
                    break

            if not is_exist:
                err_list.append('not exist thumbnail ' + str(jav.id) + '[' + jav.thumbnail + '] ' + jav.title)
                continue

            pathname_p = os.path.join(self.store_path, jav.package)
            # print('pathname_p ' + pathname_p)
            if not os.path.isfile(pathname_p):
                err_list.append('not exist package ' + str(jav.id) + ' [' + jav.package + '] ' + jav.title)
                continue

            find_filter = filter(lambda maker: maker.id == jav.makersId, self.makers)
            find_list = list(find_filter)

            if len(find_list) == 1:
                match_maker = find_list[0]
            else:
                err_list.append('jav.makersId [' + jav.makersId + '] がmakersに存在しません ' + jav.title)
                continue

            if target_idx < 0 or target_idx > self.target_max:
                break

            target_idx = target_idx + 1

            import_data = site_data.ImportData()
            import_data.title = self.__get_title_from_copytext(jav.title, jav.productNumber, match_maker)
            print('[' + str(jav.id) + '] [' + import_data.title + ']  ' + jav.title)

            movie_size, import_data.isSplit, import_data.isRar, is_err_extract = self.__parse_files(jav, files)

            if movie_size <= 0:
                if is_err_extract:
                    err_list.append('err_extract ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title)
                else:
                    err_list.append('movie not found ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title)
                is_err = True

            if is_err_extract:
                err_list.append('error extract ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title)
                is_err = True

            if is_err:
                continue

            import_data.postDate = jav.postDate
            import_data.copy_text = jav.title
            if match_maker.name == 'SITE':
                import_data.productNumber = jav.productNumber.lower()
            else:
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
            import_data.size = movie_size

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
