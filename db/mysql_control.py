import yaml
import mysql.connector
from data import site_data


class DbMysql:

    def __init__(self, table_name=''):
        self.max_time = 0
        self.user = ''
        self.password = ''
        self.hostname = ''
        self.dbname = ''
        self.cursor = None

        self.conn = self.get_conn()

        # テーブル名が指定されていた場合は取得済みの回数を設定
        if len(table_name) > 0:
            self.table_name = table_name
            max_time = self.db.prepare("SELECT max(times) FROM " + table_name)
            for row in max_time():
                self.max_time = int(row[0])

        self.cursor = self.conn.cursor()

    def get_conn(self):

        with open('credentials.yml') as file:
            obj = yaml.load(file)
            self.user = obj['user']
            self.password = obj['password']
            self.hostname = obj['hostname']
            self.dbname = obj['dbname']

        return mysql.connector.connect(user=self.user, password=self.password,
                                       host=self.hostname, database=self.dbname)

    def exist_title_and_kind(self, title, kind, table_name):
        sql = 'SELECT title FROM ' + table_name + ' WHERE title = %s and kind = %s'

        self.cursor.execute(sql, (title, kind, ))
        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        exist_flag = False

        if rs is not None:
            for row in rs:
                exist_flag = True
                break

        self.conn.commit()

        return exist_flag

    def exist_title(self, title, table_name):
        sql = 'SELECT title FROM ' + table_name + ' WHERE title = %s '

        self.cursor.execute(sql, (title, ))
        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        exist_flag = False

        if rs is not None:
            for row in rs:
                exist_flag = True
                break

        self.conn.commit()

        return exist_flag

    def get_url_javs(self):

        # sql = 'SELECT id, url FROM jav WHERE download_links = "" ORDER BY post_date'
        # sql = 'SELECT id, url FROM jav WHERE package IS NULL AND download_links IS NULL AND id = 1884 ORDER BY post_date desc'
        sql = 'SELECT id, url FROM jav WHERE package IS NULL AND download_links IS NULL ORDER BY post_date'

        self.cursor.execute(sql)

        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        javs = []
        for row in rs:
            jav = site_data.JavData()
            jav.id = row[0]
            jav.url = row[1]
            javs.append(jav)

        self.conn.commit()

        return javs

    def get_movie_maker(self):

        sql = 'SELECT id ' \
                + '  ,name, label, kind, match_str' \
                + '  ,match_product_number, replace_words, registered_by ' \
                + '  ,created_at, updated_at ' \
                + '  FROM maker ' \
                + '  WHERE deleted = 0 ' \
                + '  ORDER BY id'

        self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        makers = []
        for row in rs:
            maker = site_data.MovieMakerData()
            maker.id = row[0]
            maker.name = row[1]
            maker.label = row[2]
            maker.kind = row[3]
            maker.matchStr = row[4]
            maker.matchProductNumber = row[5]
            maker.replaceWords = row[6]
            maker.registeredBy = row[7]
            maker.createdAt = row[8]
            maker.updatedAt = row[9]
            makers.append(maker)

        self.conn.commit()

        return makers

    def __get_sql_select(self):
        sql = 'SELECT id, title, post_date, package ' \
                '  , thumbnail, sell_date, actress, maker ' \
                '  , label, download_links, url, is_selection' \
                '  , product_number, rating, is_site ' \
                '  , is_parse2, makers_id ' \
                '  , created_at, updated_at ' \
                '  FROM jav '

        return sql

    def __get_list(self, rs):

        javs = []
        for row in rs:
            jav = site_data.JavData()
            jav.id = row[0]
            jav.title = row[1]
            jav.postDate = row[2]
            jav.package = row[3]
            jav.thumbnail = row[4]
            jav.sellDate = row[5]
            jav.actress = row[6]
            jav.maker = row[7]
            jav.label = row[8]
            jav.downloadLinks = row[9]
            jav.url = row[10]
            jav.isSelection = row[11]
            jav.productNumber = row[12]
            jav.rating = row[13]
            jav.isSite = row[14]
            jav.isParse2 = row[15]
            jav.makersId = row[16]
            jav.createdAt = row[17]
            jav.updatedAt = row[18]
            javs.append(jav)

        return javs

    def get_bj(self):
        sql = 'SELECT id' \
                '  , title, post_date, thumbnails, thumbnails_count ' \
                '  , download_link, url, posted_in, is_selection ' \
                '  , is_downloads, rating ' \
                '  , created_at, updated_at ' \
                '  FROM bj '
                # '  WHERE id in (121, 134, 202, 205, 206) '

        sql = sql + '  ORDER BY post_date'

        self.cursor.execute(sql)

        rs = self.cursor.fetchall()
        bjs = []
        for row in rs:
            bj = site_data.BjData()
            bj.id = row[0]
            bj.title = row[1]
            bj.postDate = row[2]
            bj.thumbnails = row[3]
            bj.thumbnailsCount = row[4]
            bj.downloadLink = row[5]
            bj.url = row[6]
            bj.postedIn = row[7]
            bj.isSelection = row[8]
            bj.isDownloads = row[9]
            bj.rating = row[10]
            bj.createdAt = row[11]
            bj.updatedAt = row[12]
            bjs.append(bj)

        return bjs

    def get_javs(self):

        sql = self.__get_sql_select()
        sql = sql + '  ORDER BY post_date'

        self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        javs = self.__get_list(rs)

        return javs

    def get_javs_nothing_product_number(self):

        sql = 'SELECT id, title, post_date' \
                '  , thumbnail, sell_date, actress, maker ' \
                '  , label, download_links, url, is_selection' \
                '  , created_at, updated_at ' \
                '  FROM jav ' \
                '  WHERE product_number IS NULL or LENGTH(product_number) <= 0 ' \
                '  ORDER BY post_date'

        self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        javs = []
        for row in rs:
            jav = site_data.JavData()
            jav.id = row[0]
            jav.title = row[1]
            jav.postDate = row[2]
            jav.thumbnail = row[3]
            jav.sellDate = row[4]
            jav.actress = row[5]
            jav.maker = row[6]
            jav.label = row[7]
            jav.downloadLinks = row[8]
            jav.url = row[9]
            jav.isSelection = row[10]
            jav.createdAt = row[11]
            jav.updatedAt = row[12]
            javs.append(jav)

        self.conn.commit()

        return javs

    def get_url_bjs(self):

        sql = 'SELECT id, thumbnails FROM bj WHERE is_downloads IS NULL OR is_downloads = 0 ORDER BY post_date'

        self.cursor.execute(sql)

        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        bjs = []
        for row in rs:
            bj = site_data.BjData()
            bj.id = row[0]
            bj.thumbnails = row[1]
            bjs.append(bj)

        self.conn.commit()

        return bjs

    def update_bj(self, bjData):

        sql = 'UPDATE bj ' \
                '  SET is_downloads = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (bjData.isDownloads, bjData.id))
        print("bj isDownloads update id [" + str(bjData.id) + "]")

        self.conn.commit()

    def update_bj_is_selection(self, id, is_selection):

        sql = 'UPDATE bj ' \
                '  SET is_selection = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (is_selection, id))
        print("bj update id [" + str(id) + "]")

        self.conn.commit()

    def update_jav_is_selection(self, id, is_selection):

        sql = 'UPDATE jav ' \
                '  SET is_selection = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (is_selection, id))
        print("jav update id [" + str(id) + "]")

        self.conn.commit()

    def update_jav_product_number(self, id, product_number):

        sql = 'UPDATE jav ' \
                '  SET product_number = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (product_number, id))
        print("jav update id [" + str(id) + "]")

        self.conn.commit()

    def update_jav(self, javData):

        sql = 'UPDATE jav ' \
                '  SET package = %s ' \
                '    , thumbnail = %s ' \
                '    , download_links = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (javData.package, javData.thumbnail, javData.downloadLinks, javData.id))
        print("jav update id [" + str(javData.id) + "]")

        self.conn.commit()

    def export_import(self, importData):

        sql = 'INSERT INTO import(copy_text, jav_post_date ' \
                ', kind, match_product, product_number, sell_date ' \
                ', maker, title, actresses, rar_flag ' \
                ', tag, filename, hd_kind, movie_file_id' \
                ', split_flag, name_only_flag, jav_url, rating ' \
                ', size) ' \
                ' VALUES(%s, %s' \
                ', %s, %s, %s, %s' \
                ', %s, %s, %s, %s' \
                ', %s, %s, %s, %s' \
                ', %s, %s, %s, %s' \
                ', %s)'

        self.cursor.execute(sql, (importData.copy_text, importData.postDate
                            , importData.kind, importData.matchStr, importData.productNumber, importData.sellDate
                            , importData.maker, importData.title, importData.actress, importData.isRar
                            , importData.tag, importData.filename, importData.hd_kind, 0
                            , importData.isSplit, importData.isNameOnly, importData.url, importData.rating
                            , importData.size))

        self.conn.commit()

    def export_jav(self, javData):

        sql = 'INSERT INTO jav (title, post_date ' \
                ', sell_date, actress, maker, label, url, product_number) ' \
                ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'

        self.cursor.execute(sql, (javData.title, javData.postDate
                            , javData.sellDate, javData.actress
                            , javData.maker, javData.label
                            , javData.url, javData.productNumber))

        self.conn.commit()

    def export_jav2(self, jav2Data):

        sql = 'INSERT INTO jav2 (title, download_links, kind, url, detail)' \
                ' VALUES(%s, %s, %s, %s, %s)'

        self.cursor.execute(sql, (jav2Data.title, jav2Data.downloadLinks, jav2Data.kind, jav2Data.url, jav2Data.detail))

        self.conn.commit()

    def export_bj(self, bjData):

        sql = 'INSERT INTO bj(title, post_date ' \
                ', thumbnails, thumbnails_count, download_link, url, posted_in) ' \
                ' VALUES(%s, %s, %s, %s, %s, %s, %s)'

        self.cursor.execute(sql, (bjData.title, bjData.postDate
                            , bjData.thumbnails, bjData.thumbnailsCount
                            , bjData.downloadLink, bjData.url
                            , bjData.postedIn))

        self.conn.commit()