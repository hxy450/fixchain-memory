# 系统定位坐标交给高德地图前，用 CoordinateConverter(CoordType.GPS) 转成 GCJ-02

审的是：代码
触发（任一种）：
- 读到：源端用 AMapLocationClient 定位，定位结果直接就是高德地图用的坐标；写错的样子：目标的定位来源换成 geoLocationManager.getCurrentLocation，拿到的经纬度直接交给高德地图的 moveCamera / 当前位置标记，没有坐标转换，中心和蓝点偏移
适用范围：定位来源是系统 geoLocationManager、底图是高德（GCJ-02）时
做法：
- 进入相机和蓝点前先转换：用高德 SDK 的 CoordinateConverter，坐标类型设 CoordType.GPS，把 WGS-84 转成 GCJ-02；或用等价的 WGS-84→GCJ-02 适配函数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 本模块获取到的坐标均为 WGS-84 坐标系，使用其它坐标系要先转换：geoLocationManager 给的是 WGS-84（出处：location-guidelines.md，开发步骤）
- function getCurrentLocation(request?: CurrentLocationRequest | SingleLocationRequest): Promise<Location>：系统定位接口（出处：鸿蒙 SDK 的 ets/api/@ohos.geoLocationManager.d.ts，geoLocationManager.getCurrentLocation）
- 加 CoordinateConverter(GPS) 转换后中心点与蓝点不再偏移：修复后的转换（出处：卡里修好并验证过）
针对本应用要查的：
- 高德鸿蒙 SDK 里 CoordinateConverter 的用法：目标工程依赖的高德鸿蒙地图包 oh_modules 下的 .d.ts，按 CoordinateConverter、CoordType 搜；照声明写构造、设坐标类型 GPS、取转换结果的调用
未核实：卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-f9c6cd0dc22c13bdcdd8（android-panorama-map-vest7）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
