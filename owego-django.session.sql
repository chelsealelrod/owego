SELECT * FROM auth_user
JOIN authtoken_token at ON at.user_id=auth_user.id

DELETE FROM owegoapi_note
WHERE id=8

SELECT * FROM owegoapi_owegouser

SELECT * FROM owegoapi_bill

SELECT * FROM owegoapi_category

SELECT * FROM owegoapi_tag

SELECT * FROM owegoapi_note

UPDATE owegoapi_note SET bill_id = 2 WHERE id=1