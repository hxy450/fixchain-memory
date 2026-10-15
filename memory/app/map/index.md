# app/map

地图与定位 SDK 接入（如高德鸿蒙 SDK）：各产品单例的隐私与 Key 初始化、定位权限组的声明、申请与判定、逆地理编码补行政区名、定位结果到相机的接线与 WGS-84→GCJ-02 坐标转换、原生地图组件在 Swiper/Tabs 预构建页中的可见性生命周期与覆盖层触摸分工

[上一级](../index.md)

## 本级经验

- [APPROXIMATELY_LOCATION 与 LOCATION 成组声明、申请与判定：要精确定位也两项同申，任一授予就继续定位](lesson-b72e0d67fe27db2ae041.lesson.md)
  - 时机：定位能力实现阶段，编写定位权限的 module.json5 声明、运行期申请与申请结果判定时
  - 情境：目标同时申请 ohos.permission.APPROXIMATELY_LOCATION 与 ohos.permission.LOCATION；源端以 ACCESS_FINE_LOCATION 与 ACCESS_COARSE_LOCATION 一起请求；工程的权限辅助模板遍历 authResults、任一不为 0 即返回失败，通用权限表可能只列了 ohos.permission.LOCATION。
- [原生地图组件上叠放 ArkUI 控件时按地图是否需要手势写明 HitTestMode 分工](lesson-129b42655741e8c84a3a.lesson.md)
  - 时机：三方地图接入阶段，在高德 MapViewComponent 等原生 XComponent 地图之上叠放搜索栏、按钮等 ArkUI 覆盖层时
  - 情境：原生地图组件铺满页面并位于 Stack 最底层，上方叠放搜索栏、定位按钮、侧边栏等；参考工程真正承载地图的页面可能已为覆盖层或地图设了 hitTestBehavior，移植时只搬了地图组件与 adapter。
  - 例外：覆盖层下方不是原生地图、只是普通 ArkUI 内容时，按全尺寸覆盖容器的通用命中规则（lesson-4a4f8d845a204ffa244b）处理
- [原生地图组件放在 Swiper/Tabs 预构建的子页时，按选中可见性初始化或恢复、隐藏时暂停，只在 aboutToDisappear 完整释放](lesson-0e997c4e9745728b7db6.lesson.md)
  - 时机：三方地图接入阶段，把原生地图组件接入本工程已有页面，确定初始化、暂停、释放的挂载点时
  - 情境：目标页面作为 Swiper/Tabs 子页被宿主一次性预构建（在宿主文件里被直接实例化，而不是按路由压栈）；页面承载高德 MapViewComponent 等原生 XComponent 地图；SDK 或参考桥接把激活/暂停与完整释放分成不同接口。
  - 例外：页面经 Navigation 路由按需压栈、离开即销毁时，按页面自身生命周期初始化与释放
- [接入高德鸿蒙 SDK 的多个产品（地图、定位、搜索、导航）时，按产品单例分别设置隐私与 Key、分别初始化并判定就绪](lesson-9477f662ac13df03778c.lesson.md)
  - 时机：三方 SDK 移植阶段，按参考桥接类与 SDK 声明编写高德地图、定位、搜索、导航的初始化时
  - 情境：HarmonyOS 工程接入高德鸿蒙 SDK（map3d/location/search/navi 分包），各产品有自己的单例（MapsInitializer、AMapLocationManagerImpl、NaviSetting、ServiceSettings）；以另一工程的完整桥接类为参考裁剪成精简桥接，桥接可能被多个页面共用。
- [源定位 SDK 直接给行政区名、目标 LocationKit 只给坐标时，用 getAddressesFromLocation 逆地理编码补名称](lesson-a317e16cd9f46aa34962.lesson.md)
  - 时机：定位能力实现与规格阶段，把源端定位结果（如高德 AMapLocation 的 district/city）映射为目标服务接口与业务对象时
  - 情境：Android 定位 SDK 的回调直接带 district、city 等行政区名，业务据此展示或匹配本地数据；HarmonyOS geoLocationManager.getCurrentLocation 只返回坐标，目标服务接口只列了返回坐标的 locate()。
  - 例外：源端业务只消费坐标、不读行政区名时，无需补名称
- [用原生地图 SDK 替换占位地图时，把页面已有的定位出口接到相机与当前位置显示，地图就绪前暂存中心](lesson-b5e8609c6602b3828fa9.lesson.md)
  - 时机：三方地图接入阶段，用高德等原生地图组件替换占位地图、决定定位结果如何驱动地图相机与当前位置显示时；从参考桥接裁剪能力时
  - 情境：页面原先只有占位地图，定位按钮调用的地图 provider 只缓存中心坐标；参考工程的桥接类含 recenter/moveCamera、就绪前暂存中心与坐标适配器。
- [用高德鸿蒙 SDK 的 PoiQueryV2 搜索时 city 为必设参数：空值回退有效城市码，cityLimit 按源端查询设置](lesson-e4d79661c5168786a356.lesson.md)
  - 时机：三方 SDK 移植或搜索实现阶段，构造高德 PoiQueryV2 关键词或周边查询参数时
  - 情境：目标用高德鸿蒙 SDK search 包的 PoiQueryV2，其声明（PoiSearchV2.d.ets）写明 city 必须定义、不能为空；源端可能以空城市表示不限城市，页面也可能不传城市。
- [系统 geoLocationManager 定位结果（WGS-84）交给高德地图的相机中心或当前位置显示前，先转换为 GCJ-02](lesson-dc43237eaa6d11c43efd.lesson.md)
  - 时机：定位与地图接线阶段，把系统定位坐标交给高德等使用 GCJ-02 的地图 SDK 接口时
  - 情境：定位来源是 HarmonyOS geoLocationManager.getCurrentLocation（返回 WGS-84），底图与当前位置显示用高德鸿蒙 SDK（GCJ-02）；源端 Android 可能直接用高德定位 SDK，结果本就是 GCJ-02。
  - 例外：定位来源已是高德定位 SDK 等返回 GCJ-02 的接口，或坐标已在其他层转换过时，不再重复转换
