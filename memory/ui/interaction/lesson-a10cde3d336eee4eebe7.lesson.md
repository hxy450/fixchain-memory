# 根级键盘快捷键不假定聚焦的输入框会吞掉全部按键事件

ID：`lesson-a10cde3d336eee4eebe7` · 版本：1

[本主题](index.md)

## 何时使用

实现根级硬件键盘快捷键（媒体控制、导航），并要求输入框聚焦时放行时

## 适用情境

源 onKeyUp 在当前焦点为 EditText 时放行；目标在入口页根组件 onKeyEvent 统一处理按键。

## 原因

聚焦的 TextInput 只消费字符键按下，抬起事件仍冒泡到根；只按抬起处理会在输入时触发快捷键（修复期真机验证）。

## 做法

1. 按源端“输入框聚焦时放行”写显式判据，例如只处理根上同时收到过按下的抬起事件。

## 可选检查

- 改动后在输入框内键入快捷键字母、在框外按快捷键各验证一次

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-f32c19bb6ab1caffe063](../../../store/cases/case-f32c19bb6ab1caffe063/6b3630e43c34ed4aaf2bd5f287c045fa02405eb14bef13d4f1c7a2f04ca1f5b6.json) · 结论：recommendation:4
  卡片版本：`6b3630e43c34ed4aaf2bd5f287c045fa02405eb14bef13d4f1c7a2f04ca1f5b6`
