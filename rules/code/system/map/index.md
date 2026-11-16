# 地图与定位

源端有高德等地图 SDK 的 MapView、AMapLocationClient、POI 搜索和 SDK 初始化，目标端有地图组件或桥接、定位结果和占位的地图区时

## 触发族

- [高德 POI 搜索和定位接口的调用](amap-poi-location/index.md)（4 条）：读到高德的 PoiSearchV2 / PoiQueryV2、InputtipsQuery 或 AMapLocation 的 district / city；产物里查询对象带的参数、定位后的地名，以及手头没有 SDK 时服务层用什么顶替
- [源布局里的原生地图（MapView / AMapNaviView）](native-map-view/index.md)（5 条）：读过的源码里 MapView / AMapNaviView 铺满全屏作底层，桥接分出 onResume / onPause / onDestroy 三个接口，或决策台账写三方地图不迁 SDK；交回的地图被改成固定高的地图卡、静态图冒充的假地图，页面被整页重写，或只在 onReady / onDisAppear 里创建和释放
- [源端地图 SDK 的 MapView 和定位坐标](map-view-location/index.md)（4 条）：读到源端布局或代码里有第三方地图 SDK 的 MapView、AMapLocationClient 定位后 moveCamera / addMarker / setMyLocationEnabled，产物里是占位地图区、Unavailable 适配器、只有生命周期的地图桥接，或没做坐标转换就交给地图的定位结果
- [高德 SDK 各产品单例的初始化](amap-sdk-init/index.md)（2 条）：读到参考桥接对 MapsInitializer、AMapLocationManagerImpl、NaviSetting、ServiceSettings 各自 updatePrivacyShow / updatePrivacyAgree / setApiKey，产物里是移植后的地图桥接初始化：哪些单例设了隐私、是否放在同一个 try 里共用一个就绪标志
