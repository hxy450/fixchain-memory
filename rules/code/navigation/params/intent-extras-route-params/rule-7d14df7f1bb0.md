# 源页从 Intent 或首页缓存拿列表数据时，目标 Param 或共享运行时给出等价来源，不留静态占位

审的是：代码
触发（任一种）：
- 读到：源 Activity/Fragment 用 `bundle.getSerializable(...)` 取首页数据对象给列表赋值，或从首页缓存读数据（如 15 日列表）再按下标请求详情；写错的样子：目标页面的 Param 只有城市、编码、经纬度等标识，列表初始化为空数组且没有任何赋值来源，或写成几条固定占位；forward-ref 只登记了加载函数
适用范围：迁移页面入参和页面间数据交接时
做法：
- 读源页的全部 extras 和缓存读取（Serializable 数据对象、SharedPreferences 首页缓存），在目标 Param 或共享运行时里给出等价来源，例如详情页从首页运行时取同一份列表数据
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 详情页和趋势页改为从首页运行时填充同一份 15 日列表：修复后的数据交接（出处：卡里修好并验证过）
- public Serializable getSerializable(@Nullable String key)（API 33 起标 deprecated，改用 getSerializable(String, Class)）：源端取 Serializable 入参的两种写法，搜源码时两种都要看（出处：android.os.Bundle#getSerializable）
针对本应用要查的：
- 源页面的全部入参和缓存读取：源工程里该页 Activity/Fragment（.kt/.java）的 onCreate、loadData 一类方法，搜 getSerializable、getParcelable、getStringExtra 和 SharedPreferences 读取；每个入参或缓存值在目标 Param 或共享运行时里找到对应来源，列表不能只有初始化
来源：1 张卡，1 个应用
- case-e7af91622703010ed47f（app_hnaccurateweather_live_android）：做法第 1 步 ← 诊断、建议 3；取值 1 ← 诊断
