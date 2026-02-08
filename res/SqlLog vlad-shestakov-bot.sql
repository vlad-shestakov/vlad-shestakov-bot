-- SqlLog vlad-shestakov-bot.sql 
--  \res\SqlLog vlad-shestakov-bot.sql

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
      ,c.image_link -- res\about_image.jpg
      ,c.image2_link
  from COMMANDS c
 where 1=1
   --and c.active = 1
 order by c.active desc, c.ord, c.id
;

select c.id , c.command , c.command_hint , c.message_head , c.active , c.ord , c.message_text , c.image_link , c.image2_link
  from COMMANDS c;
/*
|command|command_hint       |message_head     |active|ord  |message_text                  |image_link|
|-------|-------------------|-----------------|------|-----|------------------------------|----------|
|homelib|Домашняя библиотека|                 |1     |580  |                              |          |
|weather|Данные о погоде    |Данные о погоде: |1     |610  |/weather_today - Погода на...г|          |
|version|Версия бота        |                 |1     |9 999|                              |          |
 */
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


------------------------------------------------------------