ALTER TABLE movie_import ADD product_number VARCHAR(255) AFTER url;

ALTER TABLE import ADD rating TINYINT DEFAULT 0 AFTER jav_url;

INSERT INTO movie_makers(name, label, kind, match_str, match_product_number)
  VALUES('ゲインコーポレーション', '', 1, 'DMDG', '');
INSERT INTO movie_makers(name, label, kind, match_str, match_product_number)
  VALUES('MGS', 'ゲリラ', 1, '302GEBB', '');
