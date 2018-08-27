import re


class JavData:

    def __init__(self):
        self.id = -1
        self.url = ''
        self.title = ''
        self.postDate = None
        self.package = ''
        self.thumbnail = ''
        self.sellDate = None
        self.actress = ''
        self.maker = ''
        self.label = ''
        self.downloadLinks = ''
        self.productNumber = ''
        self.isSelection = False
        self.isParse2 = False
        self.makersId = 0
        self.rating = 0
        self.isSite = 0
        self.createdAt = None
        self.updatedAt = None

    def get_date(self, line=''):
        arr = line.split('：')
        if len(arr) >= 2:
            result = re.search(".*[/-].*/.*", arr[1].strip())
            if result:
                return arr[1].strip()

        return ''

    def get_text(self, line=''):
        arr = line.split('：')
        if len(arr) >= 2:
            return arr[1].strip()

        return ''

    def print(self):
        print('【' + self.title + '】')
        print('  date     [' + str(self.sellDate) + ']')
        print('  actress  [' + self.actress + ']')
        print('  maker    [' + self.maker + ']')
        print('  label    [' + self.label + ']')
        print('  post     [' + str(self.postDate) + ']')
        print('  url      [' + self.url + ']')
        print('  p_number [' + self.productNumber + ']')
        print(' ')


class Jav2Data:

    def __init__(self):
        self.id = -1
        self.title = ''
        self.downloadLinks = ''
        self.kind = ''
        self.url = ''
        self.detail = ''
        self.createdAt = None
        self.updatedAt = None


class BjData:

    def __init__(self):
        self.id = -1
        self.title = ''
        self.postDate = None
        self.thumbnails = ''
        self.thumbnailsCount = 0
        self.downloadLink = ''
        self.url = ''
        self.postedIn = ''
        self.isDownloads = 0
        self.isSelection = 0
        self.createdAt = None
        self.updatedAt = None

    def print(self):
        print('【' + self.title + '】')
        print('  post_data     [' + str(self.postDate) + ']')
        print('  th count      [' + str(self.thumbnailsCount) + '] ' + self.thumbnails)
        print('  download_link [' + self.downloadLink + ']')
        print('  posted_in     [' + self.postedIn + ']')
        print('  url           [' + self.url + ']')
        print(' ')


class MovieMakerData:

    def __init__(self):
        self.id = -1
        self.name = ''
        self.label = ''
        self.kind = 0
        self.matchStr = ''
        self.matchProductNumber = ''
        self.replaceWords = ''
        self.registeredBy = ''
        self.createdAt = None
        self.updatedAt = None

    def get_maker(self, javLabel):

        if self.id == 835:
            return self.name + '：' + javLabel

        if not self.label or len(self.label) <= 0:
            return self.name

        return self.name + '：' + self.label

    def print(self):
        print('【' + self.name + ':' + self.label + '】')
        print('  kind    [' + str(self.kind) + ']')
        print('  match   [' + self.matchStr + ']')
        print('  match_p [' + self.matchProductNumber + ']')
        print('  created [' + str(self.createdAt) + ']')
        print('  updated [' + str(self.updatedAt) + ']')
        print(' ')


class ImportData:

    def __init__(self):
        self.id = -1
        self.copy_text = ''
        self.kind = 0
        self.matchStr = ''
        self.productNumber = ''
        self.sellDate = None
        self.maker = ''
        self.title = ''
        self.actress = ''
        self.isRar = False
        self.tag = False
        self.filename = ''
        self.hd_kind = 0
        self.isSplit = False
        self.isNameOnly = False
        self.url = ''
        self.postDate = None
        self.rating = 0


