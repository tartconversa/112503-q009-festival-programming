# 影展候补需求估计与跨厅加场

影展分轮、候补、拷贝与调场资料。所有时间为场馆当地时间，座位数中无障碍席位是子集。团体可以申报可接受的多场，接受回执时间与收到时间分别记录。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- shows.csv 的字段为 show、title、room、start、capacity、access_seats、round、state。
- releases.csv 的字段为 release、show、at、supply、taken、state。
- groups.csv 的字段为 group、size、access、indivisible、preferred、received。
- tickets.csv 的字段为 receipt、group、show、kind、event_at、received、hold_until。
- copies.csv 的字段为 copy、title、format、feature、valid_from、valid_to、currently_at。
- room_paths.csv 的字段为 origin、destination、travel_minutes、formats、access_features。
- changes.csv 的字段为 change、show、reported、effective、kind。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
