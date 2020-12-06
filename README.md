# exe

exe parser on Python

Аналог dumpbin, readelf, objdump

## Примеры запука:
* python3 pydump.py -path PATH -x -- выведет все заголовки файла
* python3 pydump.py -path PATH -d -- Режим дизассемблера

### CLI режим
* -x -- выводит все заголовки
* -f -- file header
* -o -- optional header
* -s -- sections header
* -e -- export table (если он есть)
* -i -- import table (если он есть)

### CUI режим
Запуск CUI python3 pydump.py -path PATH
- в [ ] указаны текущие секции
- section_name_1 > text.txt -- дизассемблирует секцию и запишет опкоды в указанный файл
- section_name_1 >> text.txt -- дизассемблирует секцию и допишет опкоды в конец указанного файла
- section_name [0 - 1024] -- выведет на экран указанный промежуток команд
- section_name [0 - 1024] > text.txt -- дизассемблирует секцию и запишет указанный промежуток опкодов в указанный файл