# 本地数据与偏好

读到源端的数据库、JSON 解析、assets 预置数据、外部存储，或偏好 XML、SharedPreferences / DataStore，规格里写数据表、存储、设置页和偏好键时

## 子主题

- [设置页与偏好存储](prefs/index.md)（17 条）：读到 addPreferencesFromResource 加载的偏好 XML（Preference、SwitchPreference、ListPreference、EditTextPreference）、SharedPreferences / DataStore 的键和默认值、偏好标记控制的一次性引导，规格里写设置页、偏好表和首次进入行为时
- [数据库、JSON 与文件](storage/index.md)（16 条）：读到 SQLiteOpenHelper、Room @Entity、org.json、assets/ 下的预置 JSON 或 DB、种子数据类、外部存储公共目录和 MediaStore，规格里写数据表、逐列清单、建库时机、解析和下载导出时

## 触发族

- [带 String 重载或 Parcel 字符串写法的数值字段](numeric-field-string-overload/index.md)（1 条）：读到参考文档或 getter 给出模型字段是 `Double` / `Long`，同时有 `setX(String)` 重载，或 Parcel 里写 `String.valueOf(getX())`、读 `setX(in.readString())`；规格字段表把存储类型写成 string、建议目标用 `string | null` 存，或没写 String 入口的解析规则
