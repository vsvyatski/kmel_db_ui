#!/usr/bin/env /usr/bin/python3

import argparse
import logging
import struct

log = logging.getLogger(__name__)
FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
log.setLevel(logging.DEBUG)

DUMP_TITLE = False
DUMP_GENRE = False
DUMP_PERFORMER = False
DUMP_ALBUM = False
DUMP_PLAYLIST = False


(
    signature,
    u1,

    title_count,
    title_entry_size,

    genre_count,
    genre_entry_size,

    performer_count,
    performer_entry_size,

    album_count,
    album_entry_size,

    playlist_count,
    playlist_entry_size,

    u2,
    u3,

    main_index_offset,
    title_offset,
    shortdir_offset,
    shortfile_offset,
    longdir_offset,
    longfile_offset,

    alpha_title_order_offset,

    genre_index_offset,
    genre_name_offset,
    genre_title_offset,

    genre_title_order_offset,

    performer_index_offset,
    performer_name_offset,
    performer_title_offset,

    performer_title_order_offset,

    album_index_offset,
    album_name_offset,
    album_title_offset,

    album_title_order_offset,
    u8,

    playlist_index_offset,
    playlist_name_offset,
    playlist_title_offset,

    u9,
    u10,
    u11,
    u12,
    sub_index_offset,
    end
) = list(range(43))

# file_offsets is a dictionary of tuples containing the file offset,
# format and name of the DB file header
file_offsets = {
    signature:              (0x00, "<4s", "signature"),
    u1:                     (0x04, "<HH", "u1"),
    title_count:            (0x08, "<H", "title_count"),
    title_entry_size:       (0x0a, "<H", "title_entry_size"),
    genre_count:            (0x0c, "<H", "genre_count"),
    genre_entry_size:       (0x0e, "<H", "genre_entry_size"),
    performer_count:        (0x10, "<H", "performer_count"),
    performer_entry_size:   (0x12, "<H", "performer_entry_size"),
    album_count:            (0x14, "<H", "album_count"),
    album_entry_size:       (0x16, "<H", "album_entry_size"),
    playlist_count:         (0x18, "<H", "playlist_count"),
    playlist_entry_size:    (0x1a, "<H", "playlist_entry_size"),
    u2:                     (0x1c, "<H", "u2"),
    u3:                     (0x1e, "<H", "u3"),
    main_index_offset:      (0x40, "<I", "main_index_offset"),
    title_offset:           (0x44, "<I", "title_offset"),
    shortdir_offset:        (0x48, "<I", "shortdir_offset"),
    shortfile_offset:       (0x4c, "<I", "shortfile_offset"),
    longdir_offset:         (0x50, "<I", "longdir_offset"),
    longfile_offset:        (0x54, "<I", "longfile_offset"),
    alpha_title_order_offset: (0x58, "<I", "alpha_title_order_offset"),
    genre_index_offset:     (0x5c, "<I", "genre_index_offset"),
    genre_name_offset:      (0x60, "<I", "genre_name_offset"),
    genre_title_offset:     (0x64, "<I", "genre_title_offset"),
    genre_title_order_offset: (0x68, "<I", "genre_title_order_offset"),
    performer_index_offset: (0x6c, "<I", "performer_index_offset"),
    performer_name_offset:  (0x70, "<I", "performer_name_offset"),
    performer_title_offset: (0x74, "<I", "performer_title_offset"),
    performer_title_order_offset: (0x78, "<I", "performer_title_order_offset"),
    album_index_offset:     (0x7c, "<I", "album_index_offset"),
    album_name_offset:      (0x80, "<I", "album_name_offset"),
    album_title_offset:     (0x84, "<I", "album_title_offset"),
    album_title_order_offset: (0x88, "<I", "album_title_order_offset"),
    u8:                     (0x8c, "<I", "u8"),
    playlist_index_offset:  (0x90, "<I", "playlist_index_offset"),
    playlist_name_offset:   (0x94, "<I", "playlist_name_offset"),
    playlist_title_offset:  (0x98, "<I", "playlist_title_offset"),
    u9:                     (0x9c, "<I", "u9"),
    u10:                    (0xa0, "<I", "u10"),
    u11:                    (0xa4, "<I", "u11"),
    u12:                    (0xa8, "<I", "u12"),
    sub_index_offset:                    (0xac, "<I", "sub_index_offset")
}

STRING_ENCODING = "utf_16_le"

INDEX_FORMAT = "<HHHHIIIHHIHHIHHIHHIHHII"


def debug_title(debug):
    if DUMP_TITLE:
        log.debug(debug)


def debug_genre(debug):
    if DUMP_GENRE:
        log.debug(debug)


def debug_performer(debug):
    if DUMP_PERFORMER:
        log.debug(debug)


def debug_album(debug):
    if DUMP_ALBUM:
        log.debug(debug)


def debug_playlist(debug):
    if DUMP_PLAYLIST:
        log.debug(debug)


def dump_table(bfr, start, mid, end):
    print('\nProcessed: {}'.format(mid - start))

    count = 0
    for index in range(start, mid):
        if (count % 16 == 0):
            print('\n0x{:08x}: '.format(count), end='')
        print('{:02x} '.format(bfr[index]), end='')
        count += 1

    print('\n\nUnprocessed: {}'.format(end - mid))

    count = 0
    for index in range(mid, end):
        if (count % 16 == 0):
            print('\n0x{:08x}: '.format(count), end='')
        print('{:02x} '.format(bfr[index]), end='')
        count += 1

    print()


class MainIndexEntry(object):
    def __init__(self, values, index_number):
        self.index_number = index_number
        self.genre = values[0]
        self.performer = values[1]
        self.album = values[2]

        self.u1 = values[3]
        if self.u1 != 0x0000:
            log.warning("Unexpected main index u1 value")

        self.u2 = values[4]
        if self.u2 != 0xffffffff:
            log.warning("Unexpected main index u2 value")

        self.u3 = values[5]
        if self.u3 != 0x80000000:
            log.warning("Unexpected main index u3 value")

        self.u4 = values[6]
        if self.u4 != 0x80000000:
            log.warning("Unexpected main index u4 value")

        self.title_length = values[7]
        self.title_char = values[8]
        self.title_offset = values[9]
        if self.title_char != 0x02:
            log.warning("Unexpected title char value")

        # log.debug("Title length:{} offset:{}".format(
        #     self.title_length, self.title_offset))

        self.shortdir_length = values[10]
        self.shortdir_char = values[11]
        self.shortdir_offset = values[12]
        if self.shortdir_char != 0x01:
            log.warning("Unexpected shortdir char value")

        self.shortfile_length = values[13]
        self.shortfile_char = values[14]
        self.shortfile_offset = values[15]
        if self.shortfile_char != 0x01:
            log.warning("Unexpected shortfile char value")

        self.longdir_length = values[16]
        self.longdir_char = values[17]
        self.longdir_offset = values[18]
        if self.longdir_char != 0x02:
            log.warning("Unexpected longdir char value")

        self.longfile_length = values[19]
        self.longfile_char = values[20]
        self.longfile_offset = values[21]
        if self.longfile_char != 0x02:
            log.warning("Unexpected longfile char value")

        self.u5 = values[22]
        if self.u5 != 0x00000000:
            log.warning("Unexpected main index u5 value")

    def set_genre(self, genre):
        self.genre = genre
        # log.debug(self.genre)

    def set_performer(self, performer):
        self.performer = performer
        # log.debug(self.performer)

    def set_album(self, album):
        debug_album('{} setting album {}'.format(
            self.__class__.__name__, album))
        self.album = album

    def set_title(self, title):
        self.title = title
        # log.debug("Title:{}".format(self.title))

    def set_shortdir(self, shortdir):
        self.shortdir = shortdir
        # log.debug("\tShortdir:{}".format(self.shortdir))

    def set_shortfile(self, shortfile):
        self.shortfile = shortfile
        # log.debug("\tShortfile:{}".format(self.shortfile))

    def set_longdir(self, longdir):
        self.longdir = longdir
        # log.debug("\tLongdir:{}".format(self.longdir))

    def set_longfile(self, longfile):
        self.longfile = longfile
        # log.debug("\tLongfile:{}".format(self.longfile))

    def __str__(self):
        return "Title {}- '{}'; genre {:04x}; performer {:04x}; album {:04x}".format(
            self.index_number, self.title, self.genre, self.performer, self.album)


class BaseIndexEntry(object):

    FORMAT = "<HHIHHHH"
    SIZE = struct.calcsize(FORMAT)
    NAME_CHAR_LENGTH = 2
    __isfrozen = False

    def __setattr__(self, key, value):
        '''Only allow new attributes if not frozen.'''
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        '''Freeze the class such that new attributes cannot be added.'''
        self.__isfrozen = True

    def __init__(self, index_number):
        self.index_number = index_number
        self.name = ''
        self.name_length = 0
        self.name_offset = 0

        self.counts = []

        self._album_count = 0
        self._dir_count = 0
        self._genre_count = 0
        self._performer_count = 0

        self.titles = []
        self.titles_count = 0
        self.titles_offset = 0

        self.performer_albums = {}
        self.performer_titles = {}
        self.album_titles = {}

    @property
    def album_count(self):
        return self._album_count

    @property
    def dir_count(self):
        return self._dir_count

    @property
    def genre_count(self):
        return self._genre_count

    @property
    def performer_count(self):
        return self._performer_count

    def set_name(self, name):
        self.name = name
        # log.debug("{} name: '{}'".format(
        #     self.__class__.__name__, self.name))

    def set_titles(self, titles, entries):
        self.titles = titles
        self.titles_count = len(self.titles)

        # log.debug("\t{} titles: {}".format(
        #     self.__class__.__name__, self.titles))

        # Count things

        self.counts = []
        dirlist = []
        genlist = []
        self.performer_albums = {}
        self.performer_titles = {}
        self.album_titles = {}
        for title in self.titles:
            self.counts.append(
                (entries[title].genre,
                    entries[title].performer,
                    entries[title].album))

            if entries[title].longdir not in dirlist:
                dirlist.append(entries[title].longdir)
            if entries[title].genre not in genlist:
                genlist.append(entries[title].genre)

            if entries[title].performer not in self.performer_albums.keys():
                self.performer_albums[entries[title].performer] = \
                    [entries[title].album]
                self.performer_titles[entries[title].performer] = [title]
            else:
                if entries[title].album not in \
                        self.performer_albums[entries[title].performer]:

                    self.performer_albums[entries[title].performer].append(
                        entries[title].album)

                if title not in \
                        self.performer_titles[entries[title].performer]:

                    self.performer_titles[entries[title].performer].append(
                        title)

            if entries[title].album not in self.album_titles.keys():
                self.album_titles[entries[title].album] = [title]
            else:
                if title not in self.album_titles[entries[title].album]:
                    self.album_titles[entries[title].album].append(title)

        self._dir_count = len(dirlist)
        self._genre_count = len(genlist)
        self._performer_count = len(self.performer_albums)
        self._album_count = len(self.album_titles)

        # log.debug("\t{} performer albums {}".format(
        #     self.__class__.__name__, self.performer_albums))
        # log.debug("\t{} performer titles {}".format(
        #     self.__class__.__name__, self.performer_titles))
        # log.debug("\t{} album titles {}".format(
        #     self.__class__.__name__, self.album_titles))

    def read_from_buffer(self, bfr, offset):

        values = struct.unpack_from(
            self.FORMAT,
            bfr,
            offset)

        self.name_length = values[0]

        name_char_length = values[1]
        if name_char_length != self.NAME_CHAR_LENGTH:
            log.warning("Unexpected {} name character length".format(
                self.__class__.__name__))

        self.name_offset = values[2]

        zero1 = values[3]
        if zero1 != 0x00:
            log.warning("Unexpected {} zero1 value".format(
                self.__class__.__name__))

        self.titles_count = values[4]

        self.titles_offset = values[5]

        zero2 = values[6]
        if zero2 != 0x00:
            log.warning("Unexpected {} zero2 value".format(
                self.__class__.__name__))

    def __str__(self):
        contents = "{}: '{}', titles: {}".format(
            self.__class__.__name__, self.name, str(self.titles))
        return contents


class GenreIndexEntry(BaseIndexEntry):

    def __init__(self, index_number):
        super(GenreIndexEntry, self).__init__(index_number)
        self._freeze()

    def __str__(self):
        contents = "Genre {}- '{}'; titles_offset {:04x}; dir_count {:04x}; performer_count {:04x}; album_count {:04x}".format(
            self.index_number, self.name, self.titles_offset, self.dir_count, self.performer_count, self.album_count)
        return contents


class PerformerIndexEntry(BaseIndexEntry):

    def __init__(self, index_number):
        super(PerformerIndexEntry, self).__init__(index_number)
        self._freeze()

    def __str__(self):
        contents = "Performer {}- '{}'; titles_offset {:04x}; dir_count {:04x}; genre_count {:04x}; album_count {:04x}".format(
            self.index_number, self.name, self.titles_offset, self.dir_count, self.genre_count, self.album_count)
        return contents


class AlbumIndexEntry(BaseIndexEntry):

    def __init__(self, index_number):
        super(AlbumIndexEntry, self).__init__(index_number)
        self._freeze()

    def __str__(self):
        contents = "Album {}- '{}'; titles_offset {:04x}; dir_count {:04x}; performer_count {:04x}; genre_count {:04x}".format(
            self.index_number, self.name, self.titles_offset, self.dir_count, self.performer_count, self.genre_count)
        return contents


class PlaylistIndexEntry(BaseIndexEntry):

    def __init__(self, index_number):
        super(PlaylistIndexEntry, self).__init__(index_number)
        self._freeze()


class SubIndexEntry(object):
    def __init__(self, index, values):
        self.index = index
        self.offset = values[0]
        self.size = values[1]
        self.count = values[2]

    def __str__(self):
        return 'Sub-index {}: offset 0x{:08x}, size {}, count {}\n'.format(
            self.index,
            self.offset,
            self.size,
            self.count)


class DBfile(object):
    def __init__(self, filename):

        # Open the file, read it into a buffer, close it
        f = open(filename, 'rb')
        self.db = f.read()
        f.close()

        # self.details holds the offsets for everything
        self.details = []
        for index in range(end):
            self.details.append(
                struct.unpack_from(
                    file_offsets[index][1],
                    self.db,
                    file_offsets[index][0]))

        debug_album('Album count: {}'.format(self.details[album_count][0]))

        self.parse_u2()
        self.parse_u3()
        self.parse_main_index()
        self.parse_alpha_ordered_titles()
        self.parse_genres()
        self.parse_genre_ordered_titles()
        self.parse_performers()
        self.parse_performer_ordered_titles()
        self.parse_albums()
        self.parse_album_ordered_titles()
        self.parse_u8()
        self.parse_playlists()
        self.parse_u9()
        self.parse_u10()
        self.parse_u11()
        self.parse_u12()
        self.parse_sub_indices()

    def parse_u2(self):
        # log.debug("Parsing u2")
        if self.details[u2][0] != 0x0001:
            log.warning("Unexpected u2 value")

    def parse_u3(self):
        # log.debug("Parsing u3")
        if self.details[u3][0] != 0x0014:
            log.warning("Unexpected u3 value")

    def parse_main_index(self):
        # log.debug("Parsing main index")
        self.entries = []
        if self.details[title_entry_size][0] != struct.calcsize(INDEX_FORMAT):
            log.warning("Unexpected index size")
        current = self.details[main_index_offset][0]
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from(INDEX_FORMAT, self.db, current)
            main_index_entry = MainIndexEntry(value, len(self.entries))

            title_start = self.details[title_offset][0] + \
                main_index_entry.title_offset
            title_end = title_start + \
                main_index_entry.title_length - \
                main_index_entry.title_char
            title = self.db[title_start:title_end].decode(STRING_ENCODING)

            main_index_entry.set_title(title)

            shortdir_start = self.details[shortdir_offset][0] + \
                main_index_entry.shortdir_offset
            shortdir_end = shortdir_start + \
                main_index_entry.shortdir_length - \
                main_index_entry.shortdir_char
            shortdir = self.db[shortdir_start:shortdir_end].decode('ascii')
            main_index_entry.set_shortdir(shortdir)

            shortfile_start = self.details[shortfile_offset][0] + \
                main_index_entry.shortfile_offset
            shortfile_end = shortfile_start + \
                main_index_entry.shortfile_length - \
                main_index_entry.shortfile_char
            shortfile = self.db[shortfile_start:shortfile_end].decode('ascii')
            # print('test1', self.db[shortfile_start:shortfile_end])
            main_index_entry.set_shortfile(shortfile)

            longdir_start = self.details[longdir_offset][0] + \
                main_index_entry.longdir_offset
            longdir_end = longdir_start + \
                main_index_entry.longdir_length - \
                main_index_entry.longdir_char
            longdir = self.db[longdir_start:longdir_end].decode(
                STRING_ENCODING)
            main_index_entry.set_longdir(longdir)

            longfile = self.db[
                self.details[longfile_offset][0] + main_index_entry.longfile_offset:
                self.details[longfile_offset][0] + main_index_entry.longfile_offset + main_index_entry.longfile_length - main_index_entry.longfile_char].decode(STRING_ENCODING)
            main_index_entry.set_longfile(longfile)

            self.entries.append(main_index_entry)
            current += self.details[title_entry_size][0]

    def parse_alpha_ordered_titles(self):
        debug_title("Parsing alpha_ordered_titles")
        # log.debug("alpha_ordered_titles offset: {:08x}".format(
        #     self.details[alpha_title_order_offset][0]))
        current = self.details[alpha_title_order_offset][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            debug_title("\tT(alpha)- {}: {}".format(
                value[0],
                self.entries[value[0]]))
            # TODO: Check alpha order
            current += increment
        if current != self.details[genre_index_offset][0]:
            log.warning("Unexpected alpha_ordered_titles end offset")

    def parse_genres(self):
        # log.debug("Parsing genres")
        self.genres = []

        if self.details[genre_entry_size][0] != GenreIndexEntry.SIZE:
            log.warning("Unexpected genre index size")

        current = self.details[genre_index_offset][0]

        for index in range(self.details[genre_count][0]):
            genre_index_entry = GenreIndexEntry(len(self.genres))
            genre_index_entry.read_from_buffer(self.db, current)

            name = self.db[
                self.details[genre_name_offset][0] + genre_index_entry.name_offset:
                self.details[genre_name_offset][0] + genre_index_entry.name_offset + genre_index_entry.name_length - genre_index_entry.NAME_CHAR_LENGTH].decode(STRING_ENCODING)
            genre_index_entry.set_name(name)

            titles = []
            titles_current = self.details[genre_title_offset][0] + genre_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(genre_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            genre_index_entry.set_titles(titles, self.entries)
            #log.debug("Titles: ", titles)

            self.genres.append(genre_index_entry)
            current += self.details[genre_entry_size][0]

    def parse_genre_ordered_titles(self):
        # log.debug("Parsing genre_ordered_titles")
        # log.debug("genre_ordered_titles offset: {:08x}".format(
        #     self.details[genre_title_order_offset][0]))
        current = self.details[genre_title_order_offset][0]
        increment = struct.calcsize("<H")
        verify = 0
        for index in range(self.details[title_count][0]):

            value = struct.unpack_from(
                "<H",
                self.db,
                current)

            # log.debug("\tT(G)- {} {}".format(
            #     value[0],
            #     self.entries[value[0]]))

            if self.entries[value[0]].genre >= verify:
                verify = self.entries[value[0]].genre
            else:
                log.warning("genre_ordered_titles out of order")
            current += increment
        if current != self.details[performer_index_offset][0]:
            log.warning("Unexpected genre_ordered_titles end offset")

    def parse_performers(self):
        # log.debug("Parsing performers")
        self.performers = []
        if self.details[performer_entry_size][0] != PerformerIndexEntry.SIZE:
            log.warning("Unexpected performer index size")
        current = self.details[performer_index_offset][0]
        for index in range(self.details[performer_count][0]):
            performer_index_entry = PerformerIndexEntry(len(self.performers))
            performer_index_entry.read_from_buffer(self.db, current)

            name = self.db[
                self.details[performer_name_offset][0] + performer_index_entry.name_offset:
                self.details[performer_name_offset][0] + performer_index_entry.name_offset + performer_index_entry.name_length - performer_index_entry.NAME_CHAR_LENGTH].decode(STRING_ENCODING)
            performer_index_entry.set_name(name)

            titles = []
            titles_current = self.details[performer_title_offset][0] + performer_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(performer_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            performer_index_entry.set_titles(titles, self.entries)
            #log.debug("Titles: ", titles)

            self.performers.append(performer_index_entry)
            current += self.details[performer_entry_size][0]

    def parse_performer_ordered_titles(self):
        # log.debug("Parsing performer_ordered_titles")
        # log.debug("performer_ordered_titles offset: {:08x}".format(
        #     self.details[performer_title_order_offset][0]))
        current = self.details[performer_title_order_offset][0]
        increment = struct.calcsize("<H")
        verify = 0
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            # log.debug("\tT(P)- {} {}".format(
            #     value[0], self.entries[value[0]]))
            if self.entries[value[0]].performer >= verify:
                verify = self.entries[value[0]].performer
            else:
                log.warning("performer_ordered_titles out of order")
            current += increment

        # Check that we end up where we expect to be
        if current != self.details[album_index_offset][0]:
            log.warning("Unexpected performer_ordered_titles end offset")

    def parse_albums(self):
        debug_album("Parsing albums")

        self.albums = []

        # Check that the entry size is as expected
        if self.details[album_entry_size][0] != AlbumIndexEntry.SIZE:
            log.warning("Unexpected album index size")

        # Get the start of the data
        current = self.details[album_index_offset][0]

        titles_increment = struct.calcsize("<H")

        # Iterate through the number of expected albums
        for index in range(self.details[album_count][0]):

            # Create an Album Index Entry and read from the current file location
            album_index_entry = AlbumIndexEntry(len(self.albums))
            album_index_entry.read_from_buffer(self.db, current)

            # Get the name of the album
            name_start = self.details[album_name_offset][0] + \
                album_index_entry.name_offset
            name_end = name_start + \
                album_index_entry.name_length - \
                album_index_entry.NAME_CHAR_LENGTH
            name = self.db[name_start:name_end].decode(STRING_ENCODING)
            album_index_entry.set_name(name)

            debug_album('Created album with name: {}'.format(name))

            titles = []
            titles_current = self.details[album_title_offset][0] + \
                album_index_entry.titles_offset
            for titles_index in range(album_index_entry.titles_count):
                titles.append(struct.unpack_from(
                    "<H",
                    self.db,
                    titles_current)[0])
                titles_current += titles_increment
            album_index_entry.set_titles(titles, self.entries)

            debug_album('\tSet album titles to {}'.format(titles))

            self.albums.append(album_index_entry)
            current += self.details[album_entry_size][0]

        if titles_current != self.details[album_title_order_offset][0]:
            log.warning("Unexpected album_title_offset end")
            log.warning("\t0x{:04x} != 0x{:04x}".format(
                titles_current, self.details[album_title_order_offset][0]))

            # dump_table(
            #     bfr=self.db,
            #     start=self.details[album_title_offset][0],
            #     mid=titles_current,
            #     end=self.details[album_title_order_offset][0])

            # Check for differences with the first time around.
            for album_index_entry in self.albums:
                titles = []
                second_current = titles_current + \
                    album_index_entry.titles_offset

                for titles_index in range(album_index_entry.titles_count):
                    titles.append(struct.unpack_from(
                        "<H",
                        self.db,
                        second_current)[0])
                    second_current += titles_increment
                if titles != album_index_entry.titles:
                    log.warning('Differences in: {}'.format(
                        album_index_entry.name))
                    log.warning('Second {} != Original {}'.format(
                        titles,
                        album_index_entry.titles))
                    for t in titles:
                        log.warning(self.entries[t])
                    for t in album_index_entry.titles:
                        log.warning(self.entries[t])

        # Check that we end up where we expect to be
        if current != self.details[album_name_offset][0]:
            log.warning("Unexpected album_index_offset end")

    def parse_album_ordered_titles(self):
        debug_album("Parsing album_ordered_titles")
        debug_album("\talbum_ordered_titles offset: {:08x}".format(
            self.details[album_title_order_offset][0]))

        # Get the offset
        current = self.details[album_title_order_offset][0]

        increment = struct.calcsize("<H")

        verify = 0
        for index in range(self.details[title_count][0]):
            title_index = struct.unpack_from(
                "<H",
                self.db,
                current)[0]

            title = self.entries[title_index]

            debug_album("\tAlbum Ordered {}".format(title))

            # Make sure that the album number increases by 1
            if title.album == verify:
                pass
            elif title.album == verify + 1:
                verify = title.album
            else:
                log.warning("album_ordered_titles out of order")

            current += increment

        # Check that we end up where we expect to be
        if current != self.details[playlist_index_offset][0]:
            log.warning("Unexpected album_ordered_titles end offset")

    def parse_u8(self):
        # log.debug("Parsing u8")
        # log.debug("u8 offset: {:08x}".format(
        #     self.details[u8][0]))
        if self.details[u8][0] != 0x00000000:
            log.warning("Unexpected value for u8 offset")

    def parse_playlists(self):
        # log.debug("Parsing playlists")
        self.playlists = []

        if self.details[playlist_entry_size][0] != PlaylistIndexEntry.SIZE:
            log.warning("Unexpected playlist index size")

        current = self.details[playlist_index_offset][0]
        for index in range(self.details[playlist_count][0]):
            playlist_index_entry = PlaylistIndexEntry(len(self.playlists))
            playlist_index_entry.read_from_buffer(self.db, current)

            name_start = self.details[playlist_name_offset][0] + \
                playlist_index_entry.name_offset
            name_end = name_start + \
                playlist_index_entry.name_length - \
                playlist_index_entry.NAME_CHAR_LENGTH
            name = self.db[name_start:name_end].decode(STRING_ENCODING)

            playlist_index_entry.set_name(name)

            titles = []
            titles_current = self.details[playlist_title_offset][0] + \
                playlist_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(playlist_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            playlist_index_entry.set_titles(titles, self.entries)

            self.playlists.append(playlist_index_entry)
            current += self.details[playlist_entry_size][0]

    def parse_u9(self):
        # log.debug("Parsing u9")
        # log.debug("u9 offset: {:08x}".format(self.details[u9][0]))
        current = self.details[u9][0]
        increment = struct.calcsize("<HHHHHHHHHH")
        value = struct.unpack_from("<HHHHHHHHHH", self.db, current)
        if value != (65535, 65535, 0, 0, 2, 2, 0, 0, 0, 0):
            log.warning("Unexpected u9 values")
        current += increment

        # Check that we end up where we expect to be
        if current != self.details[u10][0]:
            log.warning("Unexpected u9 end offset")

    def parse_u10(self):
        # log.debug("Parsing u10")
        # log.debug("u10 offset: {:08x}".format(self.details[u10][0]))
        current = self.details[u10][0]
        increment = struct.calcsize("<H")
        value = struct.unpack_from("<H", self.db, current)
        if value != (0,):
            log.warning("Unexpected u10 value")
        current += increment

        # Check that we end up where we expect to be
        if current != self.details[u11][0]:
            log.warning("Unexpected u10 end offset")

    def parse_u11(self):
        # log.debug("Parsing u11")
        # log.debug("u11 offset: {:08x}".format(self.details[u11][0]))
        current = self.details[u11][0]
        increment = struct.calcsize("<I")
        for index in range(self.details[album_count][0]):
            value = struct.unpack_from("<I", self.db, current)
            if value[0] != 0x00:
                log.warning("Unexpected u11 value {}".format(value[0]))
            current += increment

        # Check that we end up where we expect to be
        if current != self.details[u12][0]:
            log.warning("Unexpected u11 end offset")

    def parse_u12(self):
        # log.debug("Parsing u12")
        # log.debug("u12 offset: {:08x}".format(self.details[u12][0]))
        current = self.details[u12][0]
        increment = struct.calcsize("<I")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<I", self.db, current)
            if value[0] != 0x00:
                log.warning("Unexpected u12 value {}".format(value[0]))
            current += increment

        # Check that we end up where we expect to be
        if current != self.details[sub_index_offset][0]:
            log.warning("Unexpected u12 end offset")

    def parse_sub_indices(self):
        # log.debug("Parsing sub indices")
        # log.debug("sub_index_offset: {:08x}".format(
        #     self.details[sub_index_offset][0]))
        current = self.details[sub_index_offset][0]

        # this seems to be the offset of some data
        data_start_offset = struct.unpack_from("<I", self.db, current)
        if data_start_offset[0] != 0x6c:
            log.warning("Unexpected sub index data_start_offset")

        data_start = current + data_start_offset[0]
        current += struct.calcsize("<I")
        increment = struct.calcsize("<IHH")
        num = 0

        self.sub_index_entries = []

        # read the index up to the beginning of the data
        while current < data_start:

            # seems to be an offset, size, count
            sub_index_entry = SubIndexEntry(
                num,
                struct.unpack_from("<IHH", self.db, current))

            # log.debug("UNK13 Index 0x%x @ 0x%x: Offset 0x%x, Size 0x%x, Count 0x%x" %(num,
            #     current,
            #     sub_index_entry.offset,
            #     sub_index_entry.size,
            #     sub_index_entry.count))

            self.sub_index_entries.append(sub_index_entry)
            current += increment
            num += 1

        self.parse_subindex_t0()
        self.parse_subindex_t1()
        self.parse_subindex_t2()
        self.parse_subindex_t3()
        self.parse_subindex_t4()
        self.parse_subindex_t5()
        self.parse_subindex_t6()
        self.parse_subindex_t7()
        self.parse_subindex_t8()
        self.parse_subindex_t9()
        self.parse_subindex_t10()
        self.parse_subindex_t11()
        self.parse_subindex_t12()

    def parse_subindex_t0(self):
        # log.debug("sub index t0 - genre performers offsets and counts")

        # Expect number of genres - 1
        if self.sub_index_entries[0].count != self.details[genre_count][0] - 1:
            log.warning("Unexpected sub index  count 0")

        current = self.sub_index_entries[0].offset
        increment = struct.calcsize("<HHHH")

        u13t1_offset = 0
        for index in range(self.sub_index_entries[0].count):

            t0gennum, t0t1off, t0numperf, t0zero = struct.unpack_from(
                "<HHHH",
                self.db,
                current)

#             log.debug('''
# \tu13s[0][0x{:04x}] Name: {}:
# \t\tgenre number: 0x{:04x},
# \t\tu13t1_offset: 0x{:04x},
# \t\tnumber of performers: 0x{:04x}
# \t\tzero: 0x{:04x}'''.format(
#                 index,
#                 self.genres[t0gennum].name,
#                 t0gennum,
#                 t0t1off,
#                 t0numperf,
#                 t0zero))

            if t0t1off != u13t1_offset:
                log.warning("Unexpected u13t0 value 1")

            # Check that we have it right.
            if t0numperf != self.genres[t0gennum].performer_count:
                log.warning("Unexpected u13t0 value 2")

            if t0numperf != len(self.genres[t0gennum].performer_albums):
                log.warning("Unexpected u13t0 value 2")

            u13t1_full_offset = (t0t1off * increment) + \
                self.sub_index_entries[1].offset

            for performer in sorted(self.genres[t0gennum].performer_albums):

                # log.debug("\t\tperformer {:04x} albums {}".format(
                #     performer,
                #     self.genres[t0gennum].performer_albums[performer]))

                t1perfnum, t1t2off, t1numalb, t1zero = struct.unpack_from(
                    "<HHHH",
                    self.db,
                    u13t1_full_offset)

                if t1perfnum != performer:
                    log.warning('''
Expected t1perfnum 0x{:04x}, got performer 0x{:04x}'''.format(
                        t1perfnum, performer))

                if t1numalb != len(
                        self.genres[t0gennum].performer_albums[performer]):
                    log.warning("Arrgh1! ")

                u13t2_full_offset = (
                    t1t2off * increment +
                    self.sub_index_entries[2].offset)

                for album in sorted(
                        self.genres[t0gennum].performer_albums[performer]):

                    t2albnum, t2t3off, t2numtit, t2zero = struct.unpack_from(
                        "<HHHH",
                        self.db,
                        u13t2_full_offset)

                    # log.debug("\t\t\talbum 0x{:04x} titles 0x{:04x}".format(
                    #     t2albnum, t2numtit))

                    if t2albnum != album:
                        log.warning('''
Expected t2albnum 0x{:04x}, got album 0x{:04x}'''.format(
                            t2albnum, album))

                    u13t3_full_offset = (
                        t2t3off * struct.calcsize("<H") +
                        self.sub_index_entries[3].offset)

                    for title in range(t2numtit):
                        t3_value = struct.unpack_from(
                            "<H",
                            self.db,
                            u13t3_full_offset)

                        # log.debug("\t\t\t\t title 0x{:04x} {}".format(
                        #     t3_value[0],
                        #     self.entries[t3_value[0]]))

                        if self.entries[t3_value[0]].genre != t0gennum:
                            log.warning('''
Genre wrong 0x{:04x} != 0x{:04x}'''.format(
                                self.entries[t3_value[0]].genre,
                                t0gennum))

                        if self.entries[t3_value[0]].performer != performer:
                            log.warning('''
Performer wrong 0x{:04x} != 0x{:04x}'''.format(
                                self.entries[t3_value[0]].performer,
                                performer))

                        if self.entries[t3_value[0]].album != album:
                            log.warning('''
Album wrong 0x{:04x} != 0x{:04x}'''.format(
                                self.entries[t3_value[0]].album,
                                album))

                        u13t3_full_offset += struct.calcsize("<H")

                    u13t2_full_offset += increment

                u13t1_full_offset += increment

            # Check that last value is always zero
            if t0zero != 0x00:
                log.warning("Unexpected u13t0 value 3")

            u13t1_offset += t0numperf
            current += increment

    def parse_subindex_t1(self):
        # log.debug("u13t1 - genre performer albums offsets and counts")
        current = self.sub_index_entries[1].offset
        increment = struct.calcsize("<HHHH")
        total = 0

        for index in range(self.sub_index_entries[1].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            # log.debug("\tperformer: {:04x}, total: {:04x}, num albums: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t1 value 1")

            if value[3] != 0x00:
                log.warning("Unexpected u13t1 value 3")
            total += value[2]
            current += increment

    def parse_subindex_t2(self):
        # log.debug("u13t2 - genre performer album titles offsets and counts")
        current = self.sub_index_entries[2].offset
        increment = struct.calcsize("<HHHH")
        total = self.genres[0].titles_count
        for index in range(self.sub_index_entries[2].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            # log.debug("\talbum: {:04x}, total: {:04x}, ?: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t2 value 1")
            if value[3] != 0x00:
                log.warning("Unexpected u13t2 value 3")
            total += value[2]
            current += increment

    def parse_subindex_t3(self):
        # log.debug("u13t3 - genre_ordered_titles")

        # Check it points to the earlier table
        if self.sub_index_entries[3].offset != \
                self.details[genre_title_order_offset][0]:
            log.warning("Unexpected sub index offset 3")

        # Check it has the same count as earlier
        if self.sub_index_entries[3].count != \
                self.details[title_count][0]:
            log.warning("Unexpected sub index count 3")

    def parse_subindex_t4(self):
        # log.debug("u13t4 - genre albums offsets and counts")

        if self.sub_index_entries[4].count != self.details[genre_count][0] - 1:
            log.warning("Unexpected sub index count 4")

        current = self.sub_index_entries[4].offset
        increment = struct.calcsize("<HHHH")
        total_albums = 0
        for index in range(self.sub_index_entries[4].count):

            value = struct.unpack_from("<HHHH", self.db, current)

#             log.debug('''
# \tgenre number: 0x{:04x},
# \t\tu13t5_offset: 0x{:04x},
# \t\tnumber of albums: 0x{:04x}
# \t\tzero: 0x{:04x}'''.format(value[0], value[1], value[2], value[3]))

            if value[1] != total_albums:
                log.warning("Unexpected u13t4 value 1")

            # Check that we have it right.
            if value[2] != self.genres[value[0]].album_count:
                log.warning('''
\tUnexpected u13t4 value 2, expected {} got {}'''.format(
                    self.genres[value[0]].album_count,
                    value[2]))

            u13t5_full_offset = value[1] * increment + self.sub_index_entries[5].offset

            for album in sorted(self.genres[value[0]].album_titles):
                # log.debug("\t\talbum {:04x} titles {}".format(
                #     album, self.genres[value[0]].album_titles[album]))

                t5albnum, t5t6off, t5numtit, t5zero = struct.unpack_from(
                    "<HHHH",
                    self.db,
                    u13t5_full_offset)

                if t5albnum != album:
                    log.warning('''
\tArrgh3 album {:04x} != t5_value {:04x}'''.format(album, t5albnum))

                if t5numtit != len(self.genres[value[0]].album_titles[album]):
                    log.warning('''
\tExpected t5numtit 0x{:04x}, got 0x{:04x}'''.format(
                        len(self.genres[value[0]].album_titles[album]),
                        t5numtit))

                u13t6_full_offset = (
                    (t5t6off * struct.calcsize("<H")) +
                    self.sub_index_entries[6].offset)

                for title in range(t5numtit):

                    t6_value = struct.unpack_from(
                        "<H",
                        self.db,
                        u13t6_full_offset)

                    # log.debug("\t\t\t title {:04x} {}".format(t6_value[0], self.entries[t6_value[0]]))

                    if self.entries[t6_value[0]].genre != value[0]:
                        log.warning("Genre wrong")
                    if self.entries[t6_value[0]].album != album:
                        log.warning("Album wrong")
                    u13t6_full_offset += struct.calcsize("<H")

#                u13t6_full_offset = t5t6off*increment + self.sub_index_entries[6].offset
#                for album in sorted(self.genres[value[0]].performer_albums[performer]):
#                    t6_value = struct.unpack_from("<HHHH", self.db, u13t6_full_offset)
#                    log.debug("\t\t\talbum {:04x} titles {:04x}".format(t6_value[0], t6_value[2]))
#                    if t6_value[0] != album:
#                        log.warning("Arrgh5")
#
#                    u13t6_full_offset += increment

                u13t5_full_offset += increment

            # Check that the last value is always zero
            if value[3] != 0x00:
                log.warning("Unexpected u13t4 value 3")

            total_albums += value[2]
            current += increment

    def parse_subindex_t5(self):
        # log.debug("u13t5 - genre album titles offsets and counts")

# Not always true - albums may contain just genre 0000, or more than one genre
#        if self.sub_index_entries[5].count != self.details[album_count][0] - 1:
#            log.warning("Unexpected sub index count 5 expected: {:04x}, got: {:04x}".format(self.details[album_count][0] - 1, self.sub_index_entries[5].count))

        # running total in value[1]
        current = self.sub_index_entries[5].offset
        increment = struct.calcsize("<HHHH")
        total = self.genres[0].titles_count
        for index in range(self.sub_index_entries[5].count):
            value = struct.unpack_from("<HHHH", self.db, current)
#            log.debug("\talbum number: {:04x}, title total: {:04x}, number of titles: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t5 value 1")
            if value[3] != 0x00:
                log.warning("Unexpected u13t5 value 3")
            total += value[2]
            current += increment

    def parse_subindex_t6(self):
        # log.debug("u13t6 - genre titles")

        # Check it points to the earlier table
        if self.sub_index_entries[6].offset != \
                self.details[genre_title_offset][0]:
            log.warning("Unexpected sub index offset 6")

        # Check it has the same count as earlier
        if self.sub_index_entries[6].count != \
                self.details[title_count][0]:
            log.warning("Unexpected sub index count 6")

    def parse_subindex_t7(self):
        # log.debug("u13t7 - performer albums offsets and counts")

        if self.sub_index_entries[7].count != self.details[performer_count][0] - 1:
            log.warning("Unexpected sub index count 7")

        current = self.sub_index_entries[7].offset
        increment = struct.calcsize("<HHHH")
        total_albums = 0
        for index in range(self.sub_index_entries[7].count):
            value = struct.unpack_from("<HHHH", self.db, current)

            # log.debug("\tperformer number: {:04x}, u13t8_offset: {:04x}, number of albums: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))

            if value[1] != total_albums:
                log.warning("Unexpected u13t7 value 1")

            if value[2] != self.performers[value[0]].album_count:
                log.warning(
                    "Unexpected u13t7 value 2, expected {} got {}".format(
                        self.performers[value[0]].album_count,
                        value[2]))

            u13t8_full_offset = value[1] * increment + self.sub_index_entries[8].offset
            for album in sorted(self.performers[value[0]].album_titles):

                # log.debug("\t\talbum {:04x} titles {}".format(
                #     album,
                #     self.performers[value[0]].album_titles[album]))

                t8_value = struct.unpack_from(
                    "<HHHH",
                    self.db,
                    u13t8_full_offset)

                if t8_value[0] != album:
                    log.warning(
                        "Arrgh6 album {:04x} != t8_value {:04x}".format(
                            album,
                            t8_value[0]))

                if t8_value[2] != len(
                        self.performers[value[0]].album_titles[album]):
                    log.warning("Arrgh7")

                u13t9_full_offset = t8_value[1] * struct.calcsize("<H") + \
                    self.sub_index_entries[9].offset

                for title in range(t8_value[2]):
                    t9_value = struct.unpack_from(
                        "<H",
                        self.db,
                        u13t9_full_offset)

                    # log.debug("\t\t\t title {:04x} {}".format(
                    #     t9_value[0], self.entries[t9_value[0]]))

                    if self.entries[t9_value[0]].performer != value[0]:
                        log.warning("Performer wrong")
                    if self.entries[t9_value[0]].album != album:
                        log.warning("Album wrong")
                    u13t9_full_offset += struct.calcsize("<H")

                u13t8_full_offset += increment

            # Check that the last value is always zero
            if value[3] != 0x00:
                log.warning("Unexpected u13t7 value 3")

            total_albums += value[2]
            current += increment

    def parse_subindex_t8(self):
        # log.debug("u13t8 - performer album titles offsets and counts")
        current = self.sub_index_entries[8].offset
        increment = struct.calcsize("<HHHH")
        total = 0
        for index in range(self.sub_index_entries[8].count):
            value = struct.unpack_from("<HHHH", self.db, current)
#            log.debug("\talbum: {:04x}, u13t9_offset: {:04x}, number of titles: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning(
                    "Unexpected u13t8 value[1](offset) {} !=  total {}".format(
                        value[1],
                        total))
            if value[3] != 0x00:
                log.warning("Unexpected u13t8 value 3")
            total += value[2]
            current += increment

    def parse_subindex_t9(self):
        # log.debug("u13t9 - performer titles")
        if self.sub_index_entries[9].offset != self.details[performer_title_offset][0]:
            log.warning("Unexpected sub index offset 9")
        if self.sub_index_entries[9].count != self.details[title_count][0]:
            log.warning("Unexpected sub index count 9")

    def parse_subindex_t10(self):
        # log.debug("u13t10 - genre performers offsets and counts")
        if self.sub_index_entries[10].count != self.details[genre_count][0] - 1:
            log.warning("Unexpected sub index count 10")
        current = self.sub_index_entries[10].offset
        t0_current = self.sub_index_entries[0].offset
        increment = struct.calcsize("<HHHH")
        total_performers = 0
        for index in range(self.sub_index_entries[10].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            value0 = struct.unpack_from("<HHHH", self.db, t0_current)

            # log.debug("\tgenre number: {:04x}, u13t11_offset: {:04x}, number of performers: {:04x} {:04x}".format(
            #     value[0], value[1], value[2], value[3]))

            if value[1] != total_performers:
                log.warning("Unexpected u13t10 value 1")

            if value[2] != self.genres[value[0]].performer_count:
                log.warning("Unexpected u13t10 value 2")

            u13t11_full_offset = value[1] * increment + self.sub_index_entries[11].offset
            for performer in sorted(self.genres[value[0]].performer_titles):

                # log.debug("\t\tperformer {:04x} titles {}".format(
                #     performer,
                #     self.genres[value[0]].performer_titles[performer]))

                t11_value = struct.unpack_from(
                    "<HHHH", self.db, u13t11_full_offset)
                if t11_value[0] != performer:
                    log.warning("Performer wrong {:04x} {:04x}".format(
                        performer, t11_value[0]))
                if t11_value[2] != len(
                        self.genres[value[0]].performer_titles[performer]):
                    log.warning("Title length wrong")

                u13t12_full_offset = t11_value[1] * struct.calcsize("<H") + \
                    self.sub_index_entries[12].offset
                for title in range(t11_value[2]):
                    t12_value = struct.unpack_from(
                        "<H",
                        self.db,
                        u13t12_full_offset)

                    # log.debug("\t\t\t title {:04x} {}".format(
                    #     t12_value[0], self.entries[t12_value[0]]))

                    if self.entries[t12_value[0]].genre != value[0]:
                        log.warning("Genre wrong")
                    if self.entries[t12_value[0]].performer != performer:
                        log.warning("Performer wrong")
                    u13t12_full_offset += struct.calcsize("<H")

                u13t11_full_offset += increment

            # Check that last value is always zero
            if value[3] != 0x00:
                log.warning("Unexpected u13t10 value 3")

            # this table is a duplicate of table 0
            if value != value0:
                log.warning("Unexpected u13t10 doesn't match t0 {} {}".format(
                    value, value0))

            total_performers += value[2]
            current += increment
            t0_current += increment

    def parse_subindex_t11(self):
        # log.debug("u13t11 - genre performer titles offsets and counts")
        # running total in value[1]
        current = self.sub_index_entries[11].offset
        increment = struct.calcsize("<HHHH")
        total = self.genres[0].titles_count
        for index in range(self.sub_index_entries[11].count):
            value = struct.unpack_from("<HHHH", self.db, current)
#            log.debug("\tperformer: {:04x}, u13t12_offset: {:04x}, title: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t11 value 1")
            if value[3] != 0x00:
                log.warning("Unexpected u13t11 value 3")
            total += value[2]
            current += increment

        # check that we read to the end of the file
        if current != len(self.db):
            log.warning("Unexpected end of sub index table 11")

    def parse_subindex_t12(self):
        # log.debug("u13t12 - genre_ordered_titles")
        if self.sub_index_entries[12].offset != self.details[genre_title_order_offset][0]:
            log.warning("Unexpected sub index offset 12")
        if self.sub_index_entries[12].count != self.details[title_count][0]:
            log.warning("Unexpected sub index count 12")

    def show_titles(self):
        print("\nTitles:")
        for index in range(self.details[title_count][0]):
            print("\t{}".format(self.entries[index]))

    def show_genres(self):
        print("\nGenres:")
        for index in range(self.details[genre_count][0]):
            print(self.genres[index])
            for title_index in range(self.genres[index].titles_count):
                print("\t\t0x{:04x}: {}".format(
                    index,
                    self.entries[self.genres[index].titles[title_index]]))

    def show_performers(self):
        print("\nPerformers:")
        for index in range(self.details[performer_count][0]):
            print(self.performers[index])
            for title_index in range(self.performers[index].titles_count):
                print("\t\t0x{:04x}: {}".format(
                    index,
                    self.entries[self.performers[index].titles[title_index]]))

    def show_albums(self):
        print("\nAlbums:")
        for index in range(self.details[album_count][0]):
            print(self.albums[index])
            for title_index in range(self.albums[index].titles_count):
                print("\t\t0x{:04x}: {}".format(
                    index,
                    self.entries[self.albums[index].titles[title_index]]))

    def show_playlists(self):
        print("\nPlaylists:")
        for index in range(self.details[playlist_count][0]):
            print("\tPlaylist- 0x{:04x}: '{}'".format(
                index, self.playlists[index].name))
            for title_index in range(self.playlists[index].titles_count):
                print("\t\t0x{:04x}: {}".format(
                    index,
                    self.entries[self.playlists[index].titles[title_index]]))

    def __str__(self):
        contents = "\n"
        for index in range(title_count, main_index_offset):
            contents += "{:30s}: 0x{:08x}\n".format(
                file_offsets[index][2], self.details[index][0])

        for index in range(main_index_offset, sub_index_offset):

            # Handle u8
            this_offset = self.details[index][0]
            next_offset = self.details[index + 1][0]
            if next_offset == 0:
                next_offset = self.details[index + 2][0]
            table_length = next_offset - this_offset
            if this_offset == 0:
                table_length = 0

            contents += "{:30s}: 0x{:08x} to 0x{:08x} 0x{:08x}\n".format(
                file_offsets[index][2],
                this_offset,
                next_offset,
                table_length)

        for index in range(sub_index_offset, end):
            contents += "{:30s}: 0x{:08x}\n".format(
                file_offsets[index][2], self.details[index][0])

        for sub_index_entry in self.sub_index_entries:
            contents += '{}'.format(sub_index_entry)

        return contents

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Read a kenwood database")
    parser.add_argument(
        "-d",
        "--dump",
        dest="dump",
        action="store",
        nargs="*",
        default=[],
        help="specify what to dump to stdout " +
        "(title, genre, performer, album, playlist)")
    parser.add_argument(
        "-i", "--input",
        dest="inputfile",
        action="store", default="kenwood.dap", help="specify input file")

    args = parser.parse_args()

    dump_all = False
    if args.dump == []:
        dump_all = True

    if dump_all or "title" in args.dump:
        DUMP_TITLE = True

    if dump_all or "genre" in args.dump:
        DUMP_GENRE = True

    if dump_all or "performer" in args.dump:
        DUMP_PERFORMER = True

    if dump_all or "album" in args.dump:
        DUMP_ALBUM = True

    if dump_all or "playlist" in args.dump:
        DUMP_PLAYLIST = True

    db = DBfile(args.inputfile)

    if dump_all or DUMP_TITLE:
        db.show_titles()
    if dump_all or DUMP_GENRE:
        db.show_genres()
    if dump_all or DUMP_PERFORMER:
        db.show_performers()
    if dump_all or DUMP_ALBUM:
        db.show_albums()
    if dump_all or DUMP_PLAYLIST:
        db.show_playlists()

    log.debug(db)
