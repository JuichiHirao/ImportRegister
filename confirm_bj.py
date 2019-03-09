import re
from javcore import db


class TagCheck:

    def __init__(self):

        self.bj_dao = db.bj.BjDao()
        self.bjs = self.bj_dao.get_where_agreement('WHERE id >= 1791')

        self.import_dao = db.import_dao.ImportDao()

        self.bj_dao = db.bj.BjDao()

    def execute(self):

        for bj in self.bjs:
            actress = self.__get_actress(bj.title, bj.postedIn)
            if len(actress) > 0:

                rar_filename = bj.downloadLink.split('/')[-1]
                base_name = rar_filename.replace('.rar', '')
                imports = self.import_dao.get_where_agreement('WHERE product_number = \'' + base_name + '\'')

                if len(actress) > 0:
                    # print('    actress [' + actress + ']')
                    tag = 'KOREAN BJ ' + actress
                    tag = tag.replace('BJ BJ ', 'BJ ')
                    # print(str(bj.id) + ' ' + tag)
                    if imports is not None:
                        if tag != imports[0].tag:
                            print(str(imports[0].id) + ' [' + tag + '] <- [' + imports[0].tag + ']')
                            self.import_dao.update_tag(tag, imports[0].id)
                    # else:
                    #     print('import nothing ' + base_name + '')
            # else:
            #     print('nothing ' + str(bj.id) + ' ' + bj.postedIn)

    def __get_actress(self, title, posted_in):
        actress = ''
        if '201' in title and "KOREAN BJ" in title:
            match = re.search('[A-Z ]*[\s]{0,1}201', title)
            if match:
                replace_str = match.group().replace('201', '').strip()
                actress = posted_in.replace(replace_str, '').strip()

        return actress


if __name__ == '__main__':
    tag_check = TagCheck()
    tag_check.execute()
