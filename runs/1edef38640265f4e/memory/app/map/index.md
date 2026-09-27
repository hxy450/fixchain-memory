# app/map

地图与定位 SDK 接入（如高德鸿蒙 SDK）：各产品单例的隐私与 Key 初始化、查询参数契约、定位权限组判定、定位结果到相机与坐标系转换、原生地图组件在 Tab 页中的生命周期与触摸分工

[上一级](../index.md)

## 本级经验

- [APPROXIMATELY_LOCATION 与 LOCATION 按一组判定：任一授予就继续定位，不套用“全部授予”的通用权限模板](lesson-b72e0d67fe27db2ae041.lesson.md)
  - 时机：定位能力实现阶段，编写定位权限申请结果的判定逻辑时
  - 情境：目标同时申请 ohos.permission.APPROXIMATELY_LOCATION 与 ohos.permission.LOCATION；工程 skill 提供通用的权限辅助模板（遍历 authResults，任一不为 0 即返回失败）；功能规格只要求两项权限都声明、都处理。
- [原生地图组件接入 Swiper/Tabs 预构建的页面：可见时初始化或恢复、隐藏时暂停、卸载才释放，并显式写出地图与覆盖层的触摸分工](lesson-0e997c4e9745728b7db6.lesson.md)
  - 时机：三方地图接入阶段，把参考工程的原生地图组件接入本工程已有页面，确定初始化、暂停、释放的挂载点与触摸分工时
  - 情境：目标页面作为 Swiper/Tabs 子页被宿主一次性预构建；页面在高德 MapViewComponent 等原生 XComponent 地图之上叠放搜索栏、按钮等 ArkUI 覆盖层；参考桥接把激活/暂停与完整释放分成不同接口。
- [用原生地图 SDK 替换占位地图时，把页面已有的定位出口接到相机与当前位置显示，并在系统定位与高德底图之间做坐标转换](lesson-b5e8609c6602b3828fa9.lesson.md)
  - 时机：三方地图接入阶段，用高德等原生地图组件替换占位地图、决定定位结果如何驱动地图相机与当前位置显示时；从参考桥接裁剪能力时
  - 情境：页面原先只有占位地图，定位按钮调用的地图 provider 只缓存中心坐标；定位来源是系统 geoLocationManager（WGS-84），新底图为高德（GCJ-02）；参考工程的桥接类含 recenter/moveCamera、就绪前暂存中心与坐标适配器。
- [裁剪高德鸿蒙 SDK 桥接时按产品单例分别设置隐私与 Key、分别判定就绪；PoiQueryV2 的 city 不能为空](lesson-9477f662ac13df03778c.lesson.md)
  - 时机：三方 SDK 移植阶段，按参考桥接类与 SDK 声明编写高德地图、定位、搜索的初始化与查询参数时
  - 情境：HarmonyOS 工程接入高德鸿蒙 SDK（map3d/location/search/navi 分包），以另一工程的完整桥接类为参考，裁剪成本工程的精简桥接，并用 PoiQueryV2 做关键词或周边搜索。
