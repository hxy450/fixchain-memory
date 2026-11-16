# 源端地图 SDK 的 MapView 和定位坐标

agent 会看到什么：读到源端布局或代码里有第三方地图 SDK 的 MapView、AMapLocationClient 定位后 moveCamera / addMarker / setMyLocationEnabled，产物里是占位地图区、Unavailable 适配器、只有生命周期的地图桥接，或没做坐标转换就交给地图的定位结果

## 规矩

- rule-c7f54bc9899a｜规格要求真实地图且没计划占位时，不能把 Unavailable 适配器当唯一实现｜读到：规格要求页面初始化地图、添加 marker、移动相机、点击逆地理编码（API 候选为 AMap 地图 SDK），计划 placeholders_planned 为空；写错：能力注册表默认且唯一的地图实现是 Unavailable 适配器（initialize 恒返回 Unavailable），页面的地图区是灰底 Stack 或「暂无数据」，没有 marker / polyline 模型
- rule-589e2628ad73｜源端是地图 SDK 的 MapView 区域时，目标落成真实地图组件并绑定定位坐标｜读到：源布局里有第三方地图 SDK 的 MapView（如 com.tencent.tencentmap.mapsdk.maps.MapView），代码在定位回调里 addMarker 当前位置并 moveCamera 到真实坐标；写错：定位成功分支写成白色 Blank / Row 加 marker Image 的 Stack，没有任何地图组件，也没把定位坐标绑到相机和 marker
- rule-7114e4475ddc｜用原生地图 SDK 替换占位地图时，把定位结果接到相机和蓝点，就绪前暂存中心｜读到：源端 AMapLocationClient 定位后 aMap.moveCamera(CameraUpdateFactory.newLatLngZoom(...)) 并开启 MyLocation（MyLocationStyle、setMyLocationEnabled）；写错：新增的地图桥接只有初始化和生命周期（getMapAsync 存 map、resume / pause / release），注释写只保留生命周期；页面定位按钮仍只调缓存型 provider 的 center()，没有 moveCamera / setMyLocationEnabled
- rule-0d877dad2d86｜系统定位坐标交给高德地图前，用 CoordinateConverter(CoordType.GPS) 转成 GCJ-02｜读到：源端用 AMapLocationClient 定位，定位结果直接就是高德地图用的坐标；写错：目标的定位来源换成 geoLocationManager.getCurrentLocation，拿到的经纬度直接交给高德地图的 moveCamera / 当前位置标记，没有坐标转换，中心和蓝点偏移
