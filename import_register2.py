import os
import glob
import re
import rarfile
from javcore import data
from javcore import db
from javcore import tool
from javcore import common
from javcore import site


class ImportRegister:

    def __init__(self):

        self.env = common.Environment()
        # rarfile.DEFAULT_CHARSET = "windows-1252"
        # rarfile.UNRAR_TOOL = 'unrar'
        # rarfile.UNRAR_TOOL = r'C:\\Program Files (x86)\\UnrarDLL\\Examples\\MASM\\unrar'
        rarfile.UNRAR_TOOL = r'C:\\myapp\\unrar'
        # rarfile.UNRAR_TOOL = r'C:\\SHARE\\unrar.exe'
        self.movie_extension = '.*\.avi$|.*\.wmv$|.*\.mpg$|.*ts$|.*divx$|.*mp4$' \
                               '|.*asf$|.*mkv$|.*rm$|.*rmvb$|.*m4v$|.*3gp$'
        self.rar_extension = '.*\.rar$'

        self.store_path = self.env.get_image_path()
        self.register_path = self.env.get_register_path()

        self.jav_dao = db.jav.JavDao()
        self.maker_dao = db.maker.MakerDao()
        self.import_dao = db.import_dao.ImportDao()

        self.wiki = site.wiki.SougouWiki()
        self.mgs = site.mgs.Mgs()
        self.import_parser = common.ImportParser()
        self.auto_maker_parser = common.AutoMakerParser()

        self.makers = self.maker_dao.get_all()

        self.p_number_tool = tool.p_number.ProductNumber()
        self.copy_text = common.CopyText(False)

        self.is_check = True
        # self.is_check = False

        self.target_max = 80
        # self.target_max = 4
        self.__set_files()

    def __set_files(self):

        self.files = glob.glob(self.register_path + '\*')
        # print(len(self.files))

    def __get_target_files(self, jav):

        idx = 0
        if jav.id == 2013:
            idx = idx + 1

        files = []
        if jav.downloadFiles and len(jav.downloadFiles.strip()) > 0:
            download_files = jav.downloadFiles.split(' ')
            if len(download_files) == 1:
                pathname = os.path.join(self.register_path, download_files[0])
                if os.path.isfile(pathname):
                    files.append(download_files[0])
            elif len(download_files) > 1:
                for file in download_files:
                    pathname = os.path.join(self.register_path, file)
                    if os.path.isfile(pathname):
                        files.append(file)

        if len(files) > 0:
            return files

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
                                rar_archive.extractall(path=self.register_path, members=rar_infolist)
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
        msg_list = []

        if is_err_extract:
            msg_list.append('rar未解凍')
        if is_split:
            msg_list.append('分割ファイル')
        if is_rar:
            msg_list.append('RARFILE')
        if jav.isSite == 0:
            msg_list.append('isSite未実行')
        if jav.searchResult is None:
            msg_list.append('searchResult None')
        else:
            msg_list.append(jav.searchResult)

        if len(msg_list) >= 1:
            print('、'.join(msg_list))

        return result_tuple

    def arrange_execute(self):

        javs = self.jav_dao.get_all()

        err_list = []
        target_idx = 1
        for idx, jav in enumerate(javs):

            is_err = False

            if not jav.isSelection == 1:
                continue

            if jav.actress == '—-':
                jav.actress = ''

            if target_idx < 0 or target_idx > self.target_max:
                break

            target_idx = target_idx + 1

            if jav.isParse2 < 0:
                print('[' + str(jav.id) + '] isParse2に' + str(jav.isParse2) + 'のデータが見つかったため処理終了')
                exit(-1)

            if jav.makersId <= 0:
                print('makerIdが未設定のデータ発見 id [' + str(jav.id) + '] したため処理終了')
                exit(-1)

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
                err_list.append('not exist thumbnail ' + str(jav.id) + ' [' + jav.thumbnail + '] ' + jav.title)
                # continue

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
                find_list = self.maker_dao.get_where_agreement(' WHERE id = %s', (jav.makersId, ))
                if not len(find_list) == 1:
                    err_list.append('jav.makersId [' + str(jav.makersId) + '] がmakersに存在しません ' + jav.title)
                continue

            import_data = data.ImportData()
            import_data.title = self.copy_text.get_title(jav.title, jav.productNumber, match_maker)
            print('[' + str(jav.id) + '] [' + import_data.title + ']  ' + jav.title)

            movie_size, import_data.isSplit, import_data.isRar, is_err_extract = self.__parse_files(jav, files)

            if movie_size <= 0:
                if is_err_extract:
                    err_list.append('err_extract ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title)
                else:
                    err_list.append('movie not found ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title)
                is_err = True
            if is_err_extract:
                err_list.append('error extract ' + str(jav.id) + '  [' + match_maker.matchStr + ']  ' + jav.title + str(files[0]))
                is_err = True
            # if is_err:
            #     continue

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
            import_data.tag = self.import_parser.get_actress(jav)
            # print('tag [' + import_data.tag + ']')
            import_data.isNameOnly = True
            import_data.package = jav.package
            import_data.thumbnail = jav.thumbnail
            import_data.downloadFiles = jav.downloadFiles
            import_data.url = jav.url
            import_data.rating = jav.rating
            import_data.size = movie_size
            import_data.filename = self.import_parser.get_filename(import_data)
            print('  filename : ' + import_data.filename + '')
            import_data.detail = jav.detail
            import_data.searchResult = jav.searchResult
            import_data.javId = jav.id

            if not self.is_check:
                self.import_dao.export_import(import_data)
                self.jav_dao.update_is_selection(jav.id, 9)

        for err in err_list:
            print(err)


if __name__ == '__main__':
    importRegister = ImportRegister()
    importRegister.arrange_execute()
