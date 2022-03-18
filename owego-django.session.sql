SELECT * FROM auth_user
JOIN authtoken_token at ON at.user_id=auth_user.id

DELETE FROM authtoken_token
WHERE user_id=1

SELECT * FROM owegoapi_owegouser

SELECT * FROM owegoapi_bill

SELECT * FROM owegoapi_note

UPDATE owegoapi_note SET bill_id = 2 WHERE id=1