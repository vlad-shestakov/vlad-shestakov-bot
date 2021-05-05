drop table posts;
drop table users;

----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL, 
  age INTEGER,
  gender TEXT,
  nationality TEXT
);

CREATE TABLE IF NOT EXISTS posts (
  id SERIAL PRIMARY KEY, 
  title TEXT NOT NULL, 
  description TEXT NOT NULL, 
  user_id INTEGER REFERENCES users(id)
);


----------------------------------------------------
INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');

INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('Владимир', 39, 'male', 'Russia');



----------------------------------------------------
INSERT INTO
  posts (title, description, user_id)
VALUES
  ('Happy', 'I am feeling very happy today', 1),
  ('Hot Weather', 'The weather is very hot today', 2),
  ('Help', 'I need some help with my work', 2),
  ('Great News', 'I am getting married', 1),
  ('Interesting Game', 'It was a fantastic game of tennis', 5),
  ('Пост', 'Кто-нибудь хочет еще этих мягких французских булок?', 6),
  ('Party', 'Anyone up for a late-night party today?', 3);
  

select * from users;
select * from posts;