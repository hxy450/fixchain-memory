# 同一偏好键在不同读点用不同缺省值时按读点保留，不收敛成键常量上的单一默认

## 何时使用

偏好键表与访问器设计阶段，以及页面实现中修改某个偏好读取的缺省值时

## 适用情境

源端同一键在不同调用点以不同 defValue 读取（如过滤逻辑读 false、菜单显隐读 true）；目标准备在键常量或单一访问器里集中定义一个默认值，键表或规格摘要只写了一个缺省。

## 例外与边界

- 源端启动时调用 PreferenceManager.setDefaultValues 把偏好 XML 里各项的 android:defaultValue 写入存储的，这些键在首次启动后已经有值，读点缺省只在写入之前起作用；目标要在首次启动时同样写入这批初值，读点缺省照样按读点保留，不能拿 XML 初值替换读点缺省，也不能因为保留了读点缺省就省掉初值写入。

## 原因

SharedPreferences.getX(key, defValue) 的缺省值属于读点：键未写入时各读点得到各自的缺省。收敛成单一默认后，键缺失状态下有的读点结果反转，下游再按键常量注释“纠正”原本正确的读点。

## 做法

1. 建键表时逐读点列出 defValue：有分歧的键保留调用方显式缺省（或按读点命名的访问器），并在键常量注释里列出全部读点及其缺省值。
2. 修改某读点的缺省值前，回到该读点的源码行核对，不以规格摘要或键常量注释里的单一缺省为准。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Preferences.getSync(key, defValue) 的缺省值由每次调用传入：找不到键时返回这次调用给的 defValue
- 〔原因〕Preferences.getSync 读到的值为 null 或不是 ValueType 格式时返回 defValue，不抛错
- 〔原因〕安卓 SharedPreferences.getBoolean(key, defValue) 在键不存在时返回调用方给的 defValue；该键存的不是 boolean 时抛 ClassCastException
