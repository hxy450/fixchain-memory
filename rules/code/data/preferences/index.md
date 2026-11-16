# 偏好存储

源端有 SharedPreferences、MMKV 的读写，目标端有 preferences 的封装、putSync / flush 和它用的 Context 时

## 触发族

- [SharedPreferences 迁成 preferences 的偏好存储](shared-preferences/index.md)（9 条）：源端 SharedPreferences / MMKV 的读写、Editor 累积后 commit、Application.onCreate 里按标记门控的初始化、存进偏好的 bean，对应目标 preferences 封装的 init 位置、putSync / flush 和存进去的 JSON
- [MMKV 里持久化的界面切换状态](mmkv-view-state/index.md)（1 条）：读过的源码切换视图时把位置写进 MMKV 的键、启动时读回恢复；交回的 ViewModel 只改内存状态不写 preferences，或页面在偏好加载完之前就读了默认值
- [preferences 用的 Context](preferences-context/index.md)（1 条）：交回的修复把 preferences 的 context 从 getApplicationContext() 换成 UIAbilityContext（this.context），理由写「更可靠」，没核对两者的 preferencesDir
- [偏好读点的缺省值、读取类型和读取时机](pref-read-point-default/index.md)（6 条）：读到源端在各处用 getBoolean / getString / getInt(键, 缺省值) 读同一偏好（各读点缺省值不同、传 null 区分缺键、按字符串值域读、在点击回调里现读）；产物里 getSync 的缺省值和类型、有没有 hasSync 判缺键，以及是在回调里现读还是 aboutToAppear 读一次缓存
