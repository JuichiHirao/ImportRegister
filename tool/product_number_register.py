import re
from db import mysql_control
from tool import fc2


class ProductNumberRegister:

    def __init__(self):
        self.makers = []

        self.db = mysql_control.DbMysql()
        self.makers = self.db.get_movie_maker()
        self.fc2 = fc2.Fc2()

        self.filter_makers = list(filter(lambda maker:
                                         len(maker.matchProductNumber.strip()) > 0
                                         and len(maker.matchStr) > 0, self.makers))

    def parse2(self, jav, is_check):

        p_number = ''
        sell_date = ''
        seller = ''
        is_nomatch = False
        match_maker = None
        # match = re.search('[0-9A-Za-z]*-[0-9A-Za-z]*', jav.title)
        if jav.id == 316:
            i = 0

        # jav.makerが存在する場合（ほぼAVRIP）
        ng_reason = 0
        if len(jav.maker.strip()) > 0:
            if jav.maker == jav.label:
                jav.label = ''
            # 「妄想族」のためにスラッシュは置換
            maker_name = jav.maker.replace('/', '／')

            # jav.makerで検索
            # find_filter_maker = filter(lambda maker: maker.name == maker_name, self.makers)
            find_filter_maker = filter(lambda maker: len(maker.matchName) > 0 and re.match(maker.matchName, maker_name),
                                       self.makers)
            find_list_maker = list(find_filter_maker)

            # jav.makerで1件だけ一致
            if len(find_list_maker) == 1:
                match_maker = find_list_maker[0]
                if re.search(match_maker.matchStr, jav.title, re.IGNORECASE) or re.search(
                        match_maker.matchProductNumber, jav.title, re.IGNORECASE):
                    print('OK メーカー完全一致と、タイトル内に製品番号一致 [' + jav.maker + ']' + jav.title)
                    if not is_check:
                        ng_reason = 1
                        self.db.update_jav_checked_ok(ng_reason, match_maker.id, jav)
                else:
                    print('NG メーカー完全一致だが、タイトル内に製品番号が一致しない [' + jav.maker + ']' + jav.title)
                    ng_reason = -1
                    is_nomatch = True

            # jav.makerが複数件一致した場合はさらに掘り下げる
            elif len(find_list_maker) > 1:
                find_filter_label = filter(lambda maker: re.search(maker.matchStr, jav.title, re.IGNORECASE),
                                           find_list_maker)
                find_list_label = list(find_filter_label)
                len_label = len(find_list_label)
                if len_label == 1:
                    match_maker = find_list_label[0]
                    print('OK メーカーと、タイトル内に製品番号一つだけ一致 [' + jav.maker + ':' + jav.label + ']' + jav.title)
                    if not is_check:
                        ng_reason = 2
                        self.db.update_jav_checked_ok(ng_reason, match_maker.id, jav)
                elif len_label > 1:
                    if len(jav.label) <= 0:
                        find_filter_label = filter(lambda maker: len(maker.label) == 0, find_list_label)
                    else:
                        find_filter_label = filter(lambda maker: maker.label == jav.label, find_list_maker)
                    find_list_label = list(find_filter_label)
                    if len(find_list_label) == 1:
                        match_maker = find_list_label[0]
                        print('OK メーカーと、タイトル内に製品番号複数一致 & label一致 [' + jav.maker + ':' + jav.label + ']' + jav.title)
                        if not is_check:
                            ng_reason = 3
                            self.db.update_jav_checked_ok(ng_reason, match_maker.id, jav)
                    else:
                        print('NG メーカーと、タイトル内に製品番号複数一致 [' + jav.maker + ']' + jav.title)
                        ng_reason = -2
                else:
                    # juyなど、Madonnaとマドンナで英語日本語でマッチしない場合はここにくる
                    print('NG ' + str(len(find_list_maker)) + ' メーカーには複数一致、製品番号に一致しない ID [' + str(
                        jav.id) + '] jav [' + jav.maker + ':' + jav.label + ']' + '  maker [' + find_list_maker[
                              0].name + ']' + jav.title)
                    ng_reason = -3
                    is_nomatch = True
                # print(str(len(find_list_maker)) + ' ' + jav.maker)
            else:
                print('maker exist no match, not register [' + jav.maker + ':' + jav.label + '] ' + jav.title)
                ng_reason = -4
                is_nomatch = True

            if match_maker:
                match = re.search(match_maker.matchStr + '[-]*[A-Za-z0-9]{2,5}', jav.title, flags=re.IGNORECASE)

                if match:
                    p_number = match.group().upper()
                else:
                    is_nomatch = True
                    print('メーカー[' + str(match_maker.id) + '] に一致したが、タイトル内に[' + match_maker.matchStr + '] の文字列がない ' + jav.title)
                    ng_reason = -5

        # javのメーカ名が無い場合
        else:
            '''
            find_filter_maker = filter(
                lambda maker: re.search(maker.matchStr, jav.title, flags=re.IGNORECASE)
                              and re.search(maker.matchProductNumber, jav.title,
                                            flags=re.IGNORECASE), self.filter_makers)
            '''
            # find_filter_maker = []
            find_list_maker = []
            for maker in self.filter_makers:
                if re.search(maker.matchStr, jav.title, flags=re.IGNORECASE) \
                        and re.search(maker.matchProductNumber, jav.title, flags=re.IGNORECASE):
                    find_list_maker.append(maker)

            # find_list_maker = list(find_filter_maker)
            match_maker = None
            p_number = ''
            if len(find_list_maker) == 1:
                match_maker = find_list_maker[0]
                m = re.search(match_maker.matchProductNumber, jav.title, flags=re.IGNORECASE)
                p_number = m.group().strip()
                if not match_maker.label:
                    match_maker.label = ''
                print(
                    'OK jav.maker無し 製品番号に1件だけ一致 [' + p_number + ']' + match_maker.name + ':' + match_maker.label + ' ' + jav.title)

                if match_maker.pNumberGen == 1:
                    m = re.search(match_maker.matchProductNumber, jav.title, flags=re.IGNORECASE)
                    m_m = re.search('\([0-9]{4}', match_maker.matchStr)
                    if m_m:
                        m_number = m_m.group()
                    else:
                        print("HEY動画のmakerのmatchStrの列が(4083|本生素人TV)の形式になっていません")
                        exit(-1)
                    p_number = m_number.replace('(', '') + '_' + m.group().replace('PPV', '')
                else:
                    p_number = m.group().strip()
                if not is_check:
                    ng_reason = 4
                    self.db.update_jav_checked_ok(ng_reason, match_maker.id, jav)
            elif len(find_list_maker) > 1:
                print(str(len(find_list_maker)) + ' many match ' + jav.title)
                ng_reason = -6
            elif len(find_list_maker) <= 0:
                # print(str(len(find_list_maker)) + ' no match ' + jav.title)
                is_nomatch = True
                ng_reason = -7

            if jav.isSite == 0:
                if match_maker is not None:
                    if match_maker.siteKind == 1:
                        seller, sell_date = self.fc2.get_info(p_number)
                        # print('    ' + seller + ' ' + sell_date)

        # HEY動画でAV9898など配信名しか入っていない場合の処理
        '''
        if ng_reason == -7:
            title_plus_file = jav.title + ' ' + jav.package
            find_filter_label = filter(lambda maker: re.search(maker.matchName, title_plus_file, re.IGNORECASE),
                                       self.makers)
            find_list_label = list(find_filter_label)
            if len(find_list_label) > 0:
                print(jav.title)
        '''

        if ng_reason < 0:
            if not is_check:
                self.db.update_jav_checked_ok(ng_reason, 0, jav)

        if is_nomatch:
            p_number = ''
            match = re.search('[0-9A-Za-z]*-[0-9A-Za-z]*', jav.title)

            if match:
                p_number = match.group().strip()
                p_maker = p_number.split('-')[0]
                find_filter_maker = filter(lambda maker: maker.matchStr == p_maker, self.makers)
                find_list_maker = list(find_filter_maker)
                if len(find_list_maker) == 1:
                    match_maker = find_list_maker[0]
                    print(
                        'OK 製品番号PARSE maker.matchStrに1件だけ一致 [' + p_maker + ']' + match_maker.name + ':' + match_maker.label)
                    if not is_check:
                        ng_reason = 5
                        self.db.update_jav_checked_ok(ng_reason, match_maker.id, jav)
                if len(find_list_maker) > 1:
                    print('NG 製品番号PARSE maker.matchStrに複数一致 [' + str(jav.id) + '] ' + jav.title)
                if len(find_list_maker) <= 0:
                    print('NG [' + str(jav.id) + '] is_nomatch メーカー[' + jav.maker + ':' + jav.label + ']  は、movie_makersに存在しない  ' + jav.title)

        return p_number, seller, sell_date, match_maker, ng_reason

    def parse(self, title):
        match = re.search('[0-9A-Za-z]*-[0-9A-Za-z]*', title)

        p_number = ''

        if match:
            p_number = match.group().strip()
        else:
            for maker in self.makers:
                if len(maker.matchStr) <= 0:
                    continue

                if re.search(maker.matchStr, title):
                    # print('match ' + p_number + ' ' + maker.name + ' ' + maker.matchStr)
                    m = re.search(maker.matchProductNumber, title, flags=re.IGNORECASE)
                    if m:
                        if len(str(m.group())) > 0:
                            p_number = m.group()
                if re.search('FC2 ', title):
                    m = re.search('[0-9]{6}', title)
                    if m:
                        p_number = m.group()

        # print('[' + p_number + '] ' + title)

        return p_number

    def batch(self):

        javs = self.db.get_javs_nothing_product_number()
        for jav in javs:

            p_number = self.parse(jav.title)

            if len(p_number) > 0:
                self.db.update_jav_product_number(jav.id, p_number)


if __name__ == '__main__':
    p_register = ProductNumberRegister()
    p_register.batch()
