ALTER TABLE movie_import ADD product_number VARCHAR(255) AFTER url;

ALTER TABLE import ADD rating TINYINT DEFAULT 0 AFTER jav_url;
ALTER TABLE bj ADD rating TINYINT DEFAULT 0 AFTER is_downloads;
ALTER TABLE bj ADD size TINYINT DEFAULT 0 AFTER rating;
ALTER TABLE bj DROP size;
ALTER TABLE import ADD size BIGINT DEFAULT 0 AFTER rating;
ALTER TABLE import DROP size;
ALTER TABLE jav ADD download_files TEXT AFTER download_links;

INSERT INTO movie_makers(name, label, kind, match_str, match_product_number)
  VALUES('ゲインコーポレーション', '', 1, 'DMDG', '');
INSERT INTO movie_makers(name, label, kind, match_str, match_product_number)
  VALUES('MGS', 'ゲリラ', 1, '302GEBB', '');
INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number)
  VALUES('SODクリエイト', 'SODクリエイト', 'ハメ撮り人生相談', 1, 'TIGR', '');

SELECT * FROM jav WHERE product_number = 'GEGE-021';
UPDATE jav SET is_selection = 19 WHERE id = 969;
UPDATE jav SET is_selection = 19 WHERE id = 968;
UPDATE jav SET is_selection = 19 WHERE id = 729;
UPDATE jav SET is_selection = 19 WHERE id = 619;

SELECT * FROM jav WHERE is_selection = 1 ORDER BY post_date;

SELECT count(*) FROM jav WHERE product_number is null or product_number = '';

SELECT * FROM jav WHERE is_selection not in (-1, 9, 19) ORDER BY post_date DESC;

SELECT * FROM maker where match_str like 'KTR%';

INSERT INTO maker(name, match_name, label, kind, match_str, match_product_number)
  VALUES('親父の個撮', '親父の個撮', '', 1, 'OYJ', '');
INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('MGS', 'MGS', '俺の素人', 1, 'ORE', '', 0, null, null, 0, 'MANUAL2018-09-15');

INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('パコパコ団とゆかいな仲間たち', 'パコパコ団とゆかいな仲間たち', 'HHグループ', 1, 'PKPD', '', 0, null, null, 0, 'MANUAL2018-09-16');

SELECT * FROM jav WHERE download_files is not null order by id;

SELECT * FROM jav WHERE is_selection = 1 ORDER BY post_date;

INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('ブリット', 'ブリット', '', 1, 'EQ', '', 0, null, null, 0, 'MANUAL2018-09-24');
INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('IMPACT', 'IMPACT', '', 2, 'IMPVE', '', 0, null, null, 0, null);

INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('MGS', 'MGS', '黒船', 1, '302URF', '', 0, null, null, 0, 'MANUAL2018-10-08');

SELECT COUNT(*) FROM jav WHERE is_selection = 1;

INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('dl.getchu.com', 'dl.getchu.com', '', 1, 'GETCHU', 'GETCHU-[0-9]{6}', 0, null, null, 0, 'MANUAL2018-10-20');

SELECT * FROM jav WHERE id in (6767, 6768, 6769, 6867);
UPDATE jav SET maker = 'SODクリエイト', label = 'SOD Star' WHERE id in (6767, 6768, 6769, 6867);

SELECT * FROM jav WHERE id in (3510);

SELECT * FROM jav WHERE id in (6927, 6925, 6926, 3510);

INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('マーキュリー', '	MERCURY（マーキュリー）', '', 1, 'NINE', '', 0, null, null, 0, 'MANUAL2018-10-29');
INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('プラネットプラス', '	', '', 1, 'SUSS', '', 0, null, null, 0, 'MANUAL2018-11-01');

ALTER TABLE import CHANGE jav_package package varchar(255);
ALTER TABLE import CHANGE jav_thumbnail thumbnail varchar(255);
ALTER TABLE import DROP jav_sell_date;
ALTER TABLE import DROP jav_actress;
ALTER TABLE import DROP jav_maker;
ALTER TABLE import DROP jav_label;
ALTER TABLE jav ADD detail TEXT AFTER makers_id;

ALTER TABLE import ADD download_files TEXT AFTER makers_id;

ALTER TABLE import ADD download_files TEXT AFTER thumbnail;

INSERT INTO scraping.maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('PreStige', 'プレステージ', 'KANBi', 1, '336KNB', '', 0, '', 0, 0, 'MANUAL 2018-11-10');

INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('SITE', 'HimeMix', 'HimeMix', 1, 'HimeMix', '[0-9]{4}', 0, null, null, 0, 'MANUAL 2018-11-10');
INSERT INTO scraping.maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('AROUND', 'AROUND', '', 1, 'ARSO', '', 0, null, null, 0, 'MANUAL 2018-11-10');
INSERT INTO scraping.maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('MGS', 'ゲリラ', '', 1, '302GEGR', '', 0, null, null, 0, 'MANUAL 2018-11-20');

UPDATE jav SET maker = 'ホットエンターテイメント', label = '人妻' WHERE id in (9805,9804,9803,9802,9798)
UPDATE jav SET maker = 'ブリット', label = '悪戯' WHERE id in (9807)
UPDATE jav SET sell_date = '2018-10-10' WHERE id in (9805,9804,9803,9802,9798,9807)


SELECT * FROM jav WHERE title like '%sdmu%' ORDER BY post_date DESC;
SELECT * FROM jav WHERE title like '%star%' ORDER BY post_date DESC;
UPDATE jav, (SELECT maker as maker_o, label as label_o FROM jav WHERE id = 10922) as tmp
  SET jav.maker = tmp.maker_o, jav.label = tmp.label_o
  WHERE jav.id = 9844;

SELECT * FROM jav WHERE title like '%gs-18%' ORDER BY post_date DESC;
UPDATE jav, (SELECT maker as maker_o, label as label_o FROM jav WHERE id = 9125) as tmp
  SET jav.maker = tmp.maker_o, jav.label = tmp.label_o
  WHERE jav.id = 10038;
-- update table_001,( select max(col_01) as col_01_max from table_001 )  set col_01=col_01+1 where col_01 = col_01_max;

SELECT * FROM maker WHERE match_str = 'GIGL' OR name like 'ハイカラ%';
SELECT * FROM maker WHERE match_str = 'HARU';
SELECT * FROM maker WHERE match_str = 'CWM';
SELECT * FROM jav WHERE id = 11290;

INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, replace_words, p_number_gen, deleted, registered_by)
  VALUES ('PreStige', 'PreStige', 'FULLSAIL BEST', 1, 'FSB', '', 0, null, null, 0, 'MANUAL 2018-11-30');

SELECT * FROM jav WHERE id = 10067;
INSERT INTO maker (name, match_name, label, kind, match_str, match_product_number, site_kind, p_number_gen, replace_words, registered_by)
  VALUES ('HEY動画', 'HEY動画', 'おやじのハメ撮り', 3, '(4191|おやじのハメ撮り)', 'PPV[0-9]{3}', 0, 1, 'PPV', 'MANUAL 2018-12-02');

SELECT * FROM maker WHERE created_at >= '2018-12-11';
SELECT * FROM maker WHERE name like '%TOKYO%';
