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
