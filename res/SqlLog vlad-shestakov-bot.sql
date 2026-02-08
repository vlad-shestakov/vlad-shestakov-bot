-- SqlLog vlad-shestakov-bot-priv.sql 
--  D:\R_STUDIO\PRG\python\2025-03-25-vlad-shestakov-bot-priv\vlad-shestakov-bot-priv\res\SqlLog vlad-shestakov-bot-priv.sql

------------------------------------------------------------

select * 
  from databasechangelog
-- order by 1
;

------------------------------------------------------------


select c.id
      ,c.command 
      ,c.command_hint
      ,c.active
      ,c.ord 
      ,c.message_head
      ,c.message_text
      ,c.image_link, c.image2_link
  from COMMANDS c
 where 1=1
   --and c.active = 1
 order by c.active desc, c.ord, c.id
;

/*
|id |command       |command_hint                                    |active|ord  |message_head                                    |message_text                                                                                                                                                                                                                                                                                                                                                                                                                                                 |image_link                       |image2_link                  |
|---|--------------|------------------------------------------------|------|-----|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|-----------------------------|
|1  |little_spb_map|Карта передач "Малые родины большого Петербурга"|1     |300  |Карта передач "Малые родины большого Петербурга"|<a href="https://yandex.ru/maps/2/saint-petersburg/?ll=30.419000%2C59.931000&mode=usermaps&um=constructor%3Afee6272492e823f8e5e2f502163e5ccda6440b6fe6f4308e280f8c99f668734b&z=12">Карта передач</a>¶¶<a href="https://tvspb.ru/programs/2675276">Сайт-страница проекта</a>¶Плейлист <a href="https://vkvideo.ru/playlist/-23702661_52">VK Видео</a>¶Плейлист <a href="https://www.youtube.com/playlist?list=PLepwnVVdj5NwRNlF9UgWUVo4VYZW9Gbkf">YouTube</a>¶|res\images\little_spb_cover.jpg  |res\images\little_spb_map.jpg|
|7  |spb_chat      |Чат "Свидетели Питера"                          |1     |320  |Чат "Свидетели Питера"                          |Жизнь в Питере и отдых и можно совместить, поделиться впечатлениями - полезной информацией,  где отдохнуть, куда сходить.¶¶https://t.me/+t20wzzasKi5hOTQ6                                                                                                                                                                                                                                                                                                    |res\images\chat_spb_cover.jpg    |                             |
|6  |lab38_chat    |Юмористический чат - "Лаборатория 38" (18+)     |1     |500  |Юмористический чат - "Лаборатория 38" (18+)     |https://t.me/+qqCYZnBCPD8yNGEy                                                                                                                                                                                                                                                                                                                                                                                                                               |                                 |                             |
|8  |github        |Проекты на GitHub                               |1     |550  |Проекты на GitHub                               |https://github.com/vlad-shestakov                                                                                                                                                                                                                                                                                                                                                                                                                            |res\images\github_cover.png      |                             |
|9  |homelib       |Домашняя библиотека (beta)                      |1     |580  |                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                 |                             |
|4  |version       |Версия бота                                     |1     |9 999|                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                 |                             |
|5  |learning_log  |Приложение "Журнал обучения"                    |0     |5 500|Приложение "Журнал обучения"                    |Позволяет пользователям авторизоваться и хранить заметки по произвольным темам.¶¶Ссылка на приложение: http://vladshestakov.ru:8010/                                                                                                                                                                                                                                                                                                                         |res\images\learning_log_cover.jpg|                             |
 */


SELECT c.message_head, c.message_text, c.image_link, c.image2_link, c.id
                            FROM COMMANDS c
                            WHERE c.active = 1
                              AND UPPER(c.command) = UPPER('map_spb')
                            LIMIT 1

-- /learning_log
SELECT c.message_head, c.message_text, c.image_link, c.image2_link
                        FROM COMMANDS c
                        WHERE c.active = 1
                          AND UPPER('/' || c.command) = UPPER('/learning_log')
                        LIMIT 1
;
select c.command 
      ,c.message_text
      ,c.image_link 
      ,c.image2_link 
      ,c.id
  from COMMANDS c
 where 1=1
   and c.active = 1
   and upper(c.command) = upper('learning_log')
 limit 1
 ;

/us - Список пользователей (чтение из БД)
/po - Список постов (чтение из БД)
/ver  - Версия

/LearningLog - приложение "Журнал обучения"

------------------------------------------------------------

map_spb

Карта передач «Малые родины большого Петербурга»

Карта с выпусками передачи «Малые родины большого Петербурга».

Сайт-страница проекта
  https://yandex.ru/maps/2/saint-petersburg/?ll=30.419000%2C59.931000&mode=usermaps&um=constructor%3Afee6272492e823f8e5e2f502163e5ccda6440b6fe6f4308e280f8c99f668734b&z=12
Плейлист ВК Видео
  https://vkvideo.ru/playlist/-23702661_52
Плейлист YouTube
  https://www.youtube.com/playlist?list=PLepwnVVdj5NwRNlF9UgWUVo4VYZW9Gbkf
  
res\images\little_spb_cover.jpg
***

posts
id
header
text
image_link
image2_link

select c.* from commands c;

***
CREATE TABLE IF NOT EXISTS commands (
    id            SERIAL PRIMARY KEY,
    command       VARCHAR(255),
    command_hint  VARCHAR(255),
    header        VARCHAR(255),
    text          TEXT,
    image_link    VARCHAR(255),
    image2_link   VARCHAR(255)
);

ALTER TABLE public.commands ADD ord int4 NULL;

ALTER TABLE public.commands ADD active int DEFAULT 0 NOT NULL;

ALTER TABLE public.commands ALTER COLUMN command SET NOT NULL;

CREATE UNIQUE INDEX commands_command_uk_idx ON public.commands (command);

ALTER TABLE public.commands RENAME COLUMN "header" TO message_head;
ALTER TABLE public.commands RENAME COLUMN "text" TO message_text;

***

Создал карту с выпусками передачи «Малые родины большого Петербурга». Это специальный проект телеканала «Санкт-Петербург» об исторических районах города, 
с их настроением, культурной средой и знаковыми архитектурными объектами.
Собрано порядка 230 роликов.

Передача хорошая, но не все топонимы знакомы. Приезжаешь на район и не всегда можно быстро нагуглить нужный выпуск.

Моя карта с выпусками передачи - yandex.ru/maps/?um=c...

В Яндекс картах можно создавать свои карты, делиться ими. Данные можно обновлять интерактивно, либо через импорт/экспорт простого эксела.

Сайт-страница проекта
  https://yandex.ru/maps/2/saint-petersburg/?ll=30.419000%2C59.931000&mode=usermaps&um=constructor%3Afee6272492e823f8e5e2f502163e5ccda6440b6fe6f4308e280f8c99f668734b&z=12
Плейлист ВК Видео
  https://vkvideo.ru/playlist/-23702661_52
Плейлист YouTube
  https://www.youtube.com/playlist?list=PLepwnVVdj5NwRNlF9UgWUVo4VYZW9Gbkf

@spb_rodin 
 #topspb_tv #малыеродины
#типичныйпетербург #типичныйспб


yandex.ru/maps/?um=c...


------------------------------------------------------------


select * 
  from public.users;
/*
|id |name     |age|gender|nationality|
|---|---------|---|------|-----------|
|1  |James    |25 |male  |USA        |
|2  |Leila    |32 |female|France     |
|3  |Brigitte |35 |female|England    |
|4  |Mike     |40 |male  |Denmark    |
|5  |Elizabeth|21 |female|Canada     |
|6  |Владимир |39 |male  |Russia     |
 */

select * 
  from public.posts;

/*
|id |title           |description                                        |user_id|
|---|----------------|---------------------------------------------------|-------|
|1  |Happy           |I am feeling very happy today                      |1      |
|2  |Hot Weather     |The weather is very hot today                      |2      |
|3  |Help            |I need some help with my work                      |2      |
|4  |Great News      |I am getting married                               |1      |
|5  |Interesting Game|It was a fantastic game of tennis                  |5      |
|6  |Пост            |Кто-нибудь хочет еще этих мягких французских булок?|6      |
|7  |Party           |Anyone up for a late-night party today?            |3      |
 */

------------------------------------------------------------