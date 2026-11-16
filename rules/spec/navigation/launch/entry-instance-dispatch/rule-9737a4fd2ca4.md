# 源 standard、目标 singleton 时，规格单列「已运行时收到新 want」场景

审的是：规格
触发（任一种）：
- 读到：源 Activity 没设 `android:launchMode`（standard），每个外部 intent 都新建 Activity，在 `onCreate` 读 `getIntent()` 并 `setResult`；规格把目标 `launchType` 定为 singleton；写错的样子：规格服务层只写 `onCreate` / `aboutToAppear` 里解析 want，没有「已运行时再收到外部 want（onNewWant）」的条目
适用范围：规格提取阶段处理被第三方拉起、要回传结果的 Activity 时
做法：
- 单列「已运行时收到新拉起 want」场景并写出验收：新 want 带 revision；页面或 VM 观察到后先结束旧的相机、录像和保存，再重新应用启动参数；旧请求的结果失效
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- launchMode 的 standard 是默认值，通常每次启动都新建一个 Activity 实例：源端每个外部请求都有新的 getIntent 和结果通道（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，launchMode 的 standard（按应用的 compileSdk 取对应平台））
- launchType：singleton 仅第一次启动创建实例，缺省就是 singleton；multiton 每次新建：目标默认单实例，后续请求走已运行的实例（出处：module-configuration-file.md，abilities标签）
- onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void：已运行的 UIAbility 再次被拉起（热启动）时回调，新 want 从这里到达（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onNewWant）
来源：1 张卡，1 个应用
- case-7621afac5fee30a13731（opencamera-hmos）：做法第 1 步 ← 建议 3
