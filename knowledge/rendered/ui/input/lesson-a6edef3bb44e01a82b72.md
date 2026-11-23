# 自定义 View 上的 android:* 属性只有被该类读取才生效：控件初值取运行时生效值

## 何时使用

界面实现阶段，把源布局中自定义控件的 XML 属性转换为目标组件初始状态时；联调修复判断是否为复刻缺陷时

## 适用情境

源布局在继承 View 的自定义控件（非 CheckBox/CompoundButton）上声明 android:checked 等框架属性，该类构造只读取自己的 styleable 属性；目标用状态变量表示勾选或开关的首显状态。

## 例外与边界

- 由 View 自己的构造读取的通用属性（android:background、padding、alpha、focusable、visibility 等）在任何继承 View 的自定义控件上都生效，layout_* 由父布局读取也生效，照常迁移；要逐个核是否被读取的，是定义在某个子类 styleable 里的属性（如 checked、enabled 这类由 CompoundButton、TextView 等读取的属性）

## 原因

框架属性写在自定义 View 上不会自动生效；照 XML 声明值设初值，首显状态会与 Android 实机相反。联调时若只对照 XML，还会把真实的复刻缺陷误记为“用户例外”。

## 做法

1. 转写自定义 View 的属性前查它的继承链和构造/init 实际读取的属性；未被读取的 android:* 属性不影响运行时，初值取字段默认值以及显示前的 setChecked 等调用。
2. 在注释里分开写“XML 声明值”和“运行时生效值”，依据写到读取该属性的代码行。
3. 用户描述与源 XML 不一致时，先核源控件的运行语义，再决定记为复刻缺陷还是新要求。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕android:checked 定义在 CompoundButton 等控件的 styleable 里，表示按钮的初始选中状态；只有读取这些 styleable 的控件会用到它
- 〔做法第 1 步〕CompoundButton 在构造里以 getBoolean(CompoundButton_checked, false) 读 checked 并调 setChecked；直接继承 View 的类没有这一步
