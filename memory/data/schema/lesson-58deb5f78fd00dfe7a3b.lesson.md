# 源端以 Cursor.getString 读数值列时复刻 CursorWindow 的文本转换（REAL 按 %g），不直接换成 getString

ID：`lesson-58deb5f78fd00dfe7a3b` · 版本：1

[本主题](index.md)

## 何时使用

数据层实现阶段，把 SQLite Cursor 读取（尤其以 cursor.getString 读数值列）转成 relationalStore ResultSet 读取时

## 适用情境

源端以 cursor.getString(i) 读取 REAL 或 INTEGER 列，再交给模型的 String 入口解析或直接显示；目标准备一对一改成 resultSet.getString(columnIndex)。

## 原因

Android CursorWindow 在 getString 读数值列时做文本转换（出处：AOSP android_database_CursorWindow.cpp 的 nativeGetString）：INTEGER 转十进制整数文本，REAL 按 C 的 %g 格式转文本（六位有效数字，超出范围用指数形式），读回值因此被截到六位有效数字，后续解析出的数值也随之舍入。relationalStore 的 getString 不做这一转换（观察到返回全精度文本），一对一替换会让读回的文本与数值都和源端不同。

## 做法

1. 源端用 getString 读数值列时，目标先用 getColumnType/getColumnTypeSync（API 18+）判定列类型：REAL 用 getDouble 取值后按 C %g 规则格式化（六位有效数字、去掉尾随零、指数阈值同 %g），INTEGER 用 getLong 后转十进制文本，TEXT 才直接 getString；封装成共享读取函数供各 DAO 复用。
2. 数值字段写库时按数值绑定：模型值为空串或不可解析时写 NULL，不把字符串原样绑定成 TEXT。

## 可选检查

- 对格式有疑问时，用多位小数、很小与很大的 REAL 值对照 C printf("%g") 的输出

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-5e7f81b1b1ef0753d249](../../../store/cases/case-5e7f81b1b1ef0753d249/203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b.json) · 结论：diagnosis, recommendation:5
  卡片版本：`203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b`
