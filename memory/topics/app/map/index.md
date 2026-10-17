# app/map

地图与定位接入：SDK 单例初始化与就绪、定位权限成组、坐标系与行政区名补齐、原生地图组件生命周期

[上一级](../index.md)

## 本级经验

- [占位地图换原生地图时接定位出口并转换坐标系](lesson-b5e8609c6602b3828fa9.lesson.md) · 阶段：execute · 信号：moveCamera, newLatLngZoom, MyLocationStyle, setMyLocationEnabled
- [定位只给坐标时用逆地理编码取行政区名，不留空名](lesson-a317e16cd9f46aa34962.lesson.md) · 阶段：spec/execute · 信号：geoLocationManager.getAddressesFromLocation, geoLocationManager.getCurrentLocation, AMapLocation, subLocality
- [精确与模糊定位权限成组声明申请，任一授予即继续定位](lesson-b72e0d67fe27db2ae041.lesson.md) · 阶段：execute · 信号：ohos.permission.APPROXIMATELY_LOCATION, ohos.permission.LOCATION, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
- [预构建子页中原生地图可见时初始化、隐藏暂停、卸载释放](lesson-0e997c4e9745728b7db6.lesson.md) · 阶段：execute · 信号：MapViewComponent, XComponent, HitTestMode.Transparent, HitTestMode.None
- [高德各单例分别设隐私与密钥，PoiQueryV2 必填城市](lesson-9477f662ac13df03778c.lesson.md) · 阶段：execute · 信号：PoiQueryV2, updatePrivacyShow, updatePrivacyAgree, setApiKey
