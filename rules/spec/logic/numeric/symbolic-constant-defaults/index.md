# 引用别处 const val 符号的默认值

agent 会看到什么：读到 Room 实体字段的初值、SharedPreferences.getLong / getInt 的缺省值写的是别的文件里 const val 定义的大写常量符号，不是字面量；规格表的默认值、偏好缺省值一栏写成 -1 这类具体数，没注明取自哪个常量

## 规矩

- rule-a0b4566633f0｜源端默认值写的是符号常量时，规格先查到 const val 定义再填数，查不到写符号名标待核｜读到：Room 实体 @PrimaryKey(autoGenerate = true) var id: Long = 某个大写常量，或 SharedPreferences.getLong(key, 某个大写常量)：默认值是引用别的文件里 const val 的符号，不是字面量；写错：规格表的默认值、偏好缺省值一栏写成 -1 这类具体数，没有注明取自哪个常量定义，和源定义的值不一致
