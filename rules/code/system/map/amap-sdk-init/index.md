# 高德 SDK 各产品单例的初始化

agent 会看到什么：读到参考桥接对 MapsInitializer、AMapLocationManagerImpl、NaviSetting、ServiceSettings 各自 updatePrivacyShow / updatePrivacyAgree / setApiKey，产物里是移植后的地图桥接初始化：哪些单例设了隐私、是否放在同一个 try 里共用一个就绪标志

## 规矩

- rule-cea014b6ee6a｜裁剪高德 SDK 初始化时，ServiceSettings 等各产品单例都保留隐私两步和 setApiKey｜读到：参考桥接类的初始化注释写「每个产品各自保存隐私状态，创建任何地图、定位、导航或搜索对象前必须提供全部状态」，并对 MapsInitializer、AMapLocationManagerImpl、NaviSetting、ServiceSettings 各调用 updatePrivacyShow / updatePrivacyAgree；写错：移植后的初始化只给 MapsInitializer 和 AMapLocationManagerImpl 设了隐私，ServiceSettings 只剩 setApiKey，没有 updatePrivacyShow / updatePrivacyAgree
- rule-837fa391c898｜高德各单例分别初始化、分别判成败，搜索就绪不和 MapsInitializer.initialize 同一个 try｜写错：桥接的初始化把 MapsInitializer.initialize、定位和 ServiceSettings 的设置放在同一个 try 里，用同一个就绪标志决定搜索能不能用，任何一步抛错搜索都静默返回 []
