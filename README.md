## Асинхронный парсер сайта https://jut.su.

![Parser pic](parser.png)

### Настройки
Все настроки необходимо проводить в файле **.env**

* **TARGET_URL** - указывай ссылку на тайтл (ссылка, где именно серии);
* **ONE_TARGET_URL** - тут можешь прописать ссылку на какой-то конкретный эпизод. 
Чтобы скачивать все эпизоды оставляй пустым;
* **PATH_SAVE** - путь куда будут сохраняться файлы.
По умолчанию создается папка Download и в нее будут скачиваться тайтлы;
* **MAIN_URL** -  этот параметр скорее всего не будет меняться ближайшее время. 
Но если все же домен сменится, нужно изменить на новыйй ( По умолчанию https://jut.su);
* **COUNT_THREADS** - кол-во потоков скачивания;
* **CHUNK_SIZE** - размер чанков скачивания;
* **MAX_QUALITY** - максимальное качество, в котором будут скачиваться видео; 
По умолчанию 360, но можешь поменять вплоть до 1080;
* **USER_AGENT** - этот параметр нужен для подмена браузера в запросах;

### Справка
Для запуска парсера сначала нужно установить python3 (разрабатывал на python3.12).
Далее устанавливай все библиотеки из файла **requirements.txt** и 
меняй настройки в файле **.env**. 

Открывай CMD или консоль, переходи в директорию парсера и запускай.<br>
- python main.py


