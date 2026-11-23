# 源端以 Cursor.getString 读数值列时复刻 CursorWindow 的文本转换（REAL 按 %g），不直接换成 getString

## 何时使用

数据层实现阶段，把 SQLite Cursor 读取（尤其以 cursor.getString 读数值列）转成 relationalStore ResultSet 读取时

## 适用情境

源端以 cursor.getString(i) 读取 REAL 或 INTEGER 列，再交给模型的 String 入口解析或直接显示；目标准备一对一改成 resultSet.getString(columnIndex)。

## 例外与边界

- 源端 getString 读到 NULL 字段返回的是 null：共享读取函数先用 isColumnNull 判空并原样返回 null，不把 NULL 格式化成 '0'、'0.0' 或空串；源端用 getDouble、getInt 等数值方法读的列不在这条范围内，照原方法迁移。

## 原因

Android CursorWindow 在 getString 读数值列时做文本转换（出处：AOSP android_database_CursorWindow.cpp 的 nativeGetString）：INTEGER 转十进制整数文本，REAL 按 C 的 %g 格式转文本（六位有效数字，超出范围用指数形式），读回值因此被截到六位有效数字，后续解析出的数值也随之舍入。relationalStore 的 getString 不做这一转换（观察到返回全精度文本），一对一替换会让读回的文本与数值都和源端不同。

## 做法

1. 源端用 getString 读数值列时，目标先用 getColumnType/getColumnTypeSync（API 18+）判定列类型：REAL 用 getDouble 取值后按 C %g 规则格式化（六位有效数字、去掉尾随零、指数阈值同 %g），INTEGER 用 getLong 后转十进制文本，TEXT 才直接 getString；封装成共享读取函数供各 DAO 复用。
2. 数值字段写库时按数值绑定：模型值为空串或不可解析时写 NULL，不把字符串原样绑定成 TEXT。

## 可选检查

- 对格式有疑问时，用多位小数、很小与很大的 REAL 值对照 C printf("%g") 的输出

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕安卓 CursorWindow.getString 读 FLOAT 列时按 printf 的 %g 格式化成文本，读 INTEGER 列按 %lld 转十进制文本，NULL 列返回 null，BLOB 列抛 SQLiteException
- 〔原因〕HarmonyOS 6.1.1(24) 上 relationalStore 的 ResultSet.getString 读 REAL 列返回全精度文本，不按 %g 截成六位有效数字
- 〔做法第 2 步〕REAL 列被绑定成 TEXT '' 落库时，`col IS NOT NULL AND col != 0` 一类条件把该行算作有值
