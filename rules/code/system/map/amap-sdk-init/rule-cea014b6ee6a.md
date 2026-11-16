# 裁剪高德 SDK 初始化时，ServiceSettings 等各产品单例都保留隐私两步和 setApiKey

审的是：代码
触发（任一种）：
- 读到：参考桥接类的初始化注释写「每个产品各自保存隐私状态，创建任何地图、定位、导航或搜索对象前必须提供全部状态」，并对 MapsInitializer、AMapLocationManagerImpl、NaviSetting、ServiceSettings 各调用 updatePrivacyShow / updatePrivacyAgree；写错的样子：移植后的初始化只给 MapsInitializer 和 AMapLocationManagerImpl 设了隐私，ServiceSettings 只剩 setApiKey，没有 updatePrivacyShow / updatePrivacyAgree
适用范围：鸿蒙工程接入高德鸿蒙 SDK（地图、定位、导航、搜索分包），参照现成桥接类写初始化时
做法：
- 对本工程要用的每个产品单例（MapsInitializer、AMapLocationManagerImpl、NaviSetting、ServiceSettings）照参考各写全三步：updatePrivacyShow、updatePrivacyAgree、设置 Key（搜索是 ServiceSettings.getInstance().setApiKey(<key>)），参数照参考实现里同一产品的那几行
- 这几步放在创建任何地图、定位、导航或搜索对象之前完成
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 每个高德产品各自保存隐私状态，创建任何地图、定位、导航或搜索对象前必须分别提供：只给地图、定位设隐私不能覆盖搜索（出处：卡里修好并验证过（参考桥接类的初始化注释））
- ServiceSettings 单独设置隐私、Key、语言和 HTTPS：修好后的搜索初始化（出处：卡里修好并验证过）
未核实：updatePrivacyShow、updatePrivacyAgree 在 ServiceSettings 上是静态调用还是实例调用、参数是什么，没能对照高德鸿蒙 SDK 的声明
来源：1 张卡，1 个应用
- case-15e27ba62ddc28121b8e（android-panorama-map-vest7）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；取值 1 ← 诊断；取值 2 ← 诊断
