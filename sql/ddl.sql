ALTER TABLE movie_import ADD product_number VARCHAR(255) AFTER url;

ALTER TABLE import ADD rating TINYINT DEFAULT 0 AFTER jav_url;
ALTER TABLE bj ADD rating TINYINT DEFAULT 0 AFTER is_downloads;
ALTER TABLE bj ADD size TINYINT DEFAULT 0 AFTER rating;
ALTER TABLE bj DROP size;
ALTER TABLE import ADD size BIGINT DEFAULT 0 AFTER rating;
ALTER TABLE import DROP size;

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


SELECT count(*) FROM jav WHERE product_number is null or product_number = '';

SELECT * FROM jav WHERE is_selection not in (-1, 9, 19) ORDER BY post_date DESC;

SELECT * FROM maker where match_str like 'KTR%';

INSERT INTO maker(name, match_name, label, kind, match_str, match_product_number)
  VALUES('親父の個撮', '親父の個撮', '', 1, 'OYJ', '');

