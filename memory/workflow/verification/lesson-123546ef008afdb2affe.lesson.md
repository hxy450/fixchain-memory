# 引用安卓框架默认值时查框架定义，不凭记忆或估算

ID：`lesson-123546ef008afdb2affe` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，需要写出@android:color/*、主题默认窗口背景、对话框窗口宽度等框架默认值时

## 适用情境

源工程只引用框架资源名或依赖主题/框架默认，项目源码里没有该数值，目标端需要具体值。

## 原因

框架默认值不在项目源码中，凭记忆写或按观感估一个百分比容易出错，同一错误还会在多个页面重复，之后只有设备对照才能发现。

## 做法

1. 从框架资源或主题链取值，例如：@android:color/darker_gray为#AAAAAA；Theme.AppCompat.Light系未覆写windowBackground时窗口背景为#FAFAFA；AlertDialog面板宽为窗宽95%（横屏65%）再减两侧各16dp背景内缩。
2. 取到的值落到目标颜色/尺寸资源，多个页面复用同一资源。
3. 查不到时作为不确定项上报，不写估值。

来源支持：3 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-540ecdd38de3165e5d03](../../../store/cases/case-540ecdd38de3165e5d03/d1680892d4afde0858648aad9063ffbdea116cd79fb3574578d3ca210626908d.json) · 结论：diagnosis, recommendation:3
  卡片版本：`d1680892d4afde0858648aad9063ffbdea116cd79fb3574578d3ca210626908d`
- [case-86f157921e6dcf34d10e](../../../store/cases/case-86f157921e6dcf34d10e/624f2c713c2a3b1d609247a02f39a0a1d5ea8c62b365aeccc49134a52ac73802.json) · 结论：recommendation:1, recommendation:3
  卡片版本：`624f2c713c2a3b1d609247a02f39a0a1d5ea8c62b365aeccc49134a52ac73802`
- [case-f1328f25e2396630d2c2](../../../store/cases/case-f1328f25e2396630d2c2/1a0db1b1e1c45e05a8fdebc861b2bc09d36bd504ad4ace291f751e70022f3b11.json) · 结论：recommendation:1
  卡片版本：`1a0db1b1e1c45e05a8fdebc861b2bc09d36bd504ad4ace291f751e70022f3b11`
