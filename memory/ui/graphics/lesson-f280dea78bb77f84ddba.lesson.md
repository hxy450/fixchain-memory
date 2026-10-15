# 源端用文字字符或 emoji 充当图形时，按原字符用 Text 实现，不换成外形不同的系统符号

ID：`lesson-f280dea78bb77f84ddba` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为源端以 TextView/Text 字符（粗体“-”“+”、emoji）表现的按钮或图形写转换决策并选择目标组件时

## 适用情境

源端用 TextView 或 Compose Text 显示字面字符充当按钮图形（加减号），或 Text 直接显示 emoji（如星标、咖啡杯）；工程 skill 或规格有“图标优先用已验证的系统 symbol”“不把 emoji 塞进 Text 当图标”一类规则，写者准备改成 SymbolGlyph 或带圆圈的近似符号。

## 例外与边界

- 源端该处引用的是 drawable 或矢量图标资源：按源资源复制原图，不属本条

## 原因

字面字符是界面内容，外形由字体决定；换成 symbol 库里名称相近的图标（如带圆圈的 minus）会改变外形（如多出圆环、与相邻符号不对称）。symbol 类规则约束的是源端矢量图标资源的映射与名称合法性，不是要求替换源端的字面字符。

## 做法

1. 按源布局和截图确认字形外观（有无圆环、粗细、字号），按原字符用 Text 实现；短横也可用 Divider 或 Rect 画同形，symbol 库没有同形名称时不选外形不同的近似 symbol。
2. 规格提取时区分“源矢量图标映射”与“源界面字面文本”；与 symbol 类规则冲突时在规格中记录这一区分，不替换字符。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-0848ab137044cb92d1bc](../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：diagnosis, recommendation:6
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-6ba16d2344b52f8fca51](../../../store/cases/case-6ba16d2344b52f8fca51/3b128ce1f45adbd905d0ce25b9396eeee973d527b0b9ccad5c9a72d571e4534f.json) · 结论：diagnosis, recommendation:1
  卡片版本：`3b128ce1f45adbd905d0ce25b9396eeee973d527b0b9ccad5c9a72d571e4534f`
