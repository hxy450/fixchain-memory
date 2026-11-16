# 布局控件带 onClick 绑定或按状态选图时，onClick 要复刻处理器分支的副作用，不能只取反换图

审的是：代码
触发（任一种）：
- 读到：布局 XML 里控件写 android:onClick="@{…}" 数据绑定，或 android:src 按 ViewModel 状态三元切换；实际行为写在 Fragment/Activity 统一点击处理器的 when 分支和 ViewModel 里；写错的样子：对应 ArkUI 组件的 .onClick 里只把 @State 布尔取反并换图，没有处理器分支里的偏好写入、振动、音频播放或面板打开
适用范围：界面迁移时，安卓布局里声明了点击绑定或数据绑定状态的控件迁成 ArkUI 组件并写事件逻辑
做法：
- 按控件 id 或状态名在统一点击处理器的分支和 ViewModel 里找到对应代码，逐项列出副作用：播放哪个音频、振动多少毫秒、写哪个偏好键、打开哪个面板
- 在 .onClick 里除了切状态换图，逐项写出这些副作用：偏好写入用 preferences 的 putSync(源端键, 值) 后 flush()；振动写 vibrator.startVibration({ type: 'time', duration: 源端毫秒数 }, { usage: … })；按源端条件播放按键音
- 开关状态的初值用 getSync(源端键, 源端默认值) 从偏好读出，默认值与源端 ViewModel 读偏好时给的一致，不另定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- putSync(key: string, value: ValueType): void：Preferences 同步写入一个键值，要再调 flush 才落盘（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.putSync）
- flush(): Promise<void>：把 Preferences 写到文件（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.flush）
- getSync(key: string, defValue: ValueType): ValueType：同步读一个键，键不存在时返回 defValue（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.getSync）
- function getPreferencesSync(context: Context, options: Options): Preferences：取得 Preferences 实例（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferencesSync）
- function startVibration(effect: VibrateEffect, attribute: VibrateAttribute): Promise<void>：触发振动，需要 ohos.permission.VIBRATE（出处：鸿蒙 SDK 的 ets/api/@ohos.vibrator.d.ts，vibrator.startVibration）
- VibrateTime { type: 'time'; duration: number }，duration 单位 ms：按时长振动的 effect，源端毫秒数直接填 duration（出处：鸿蒙 SDK 的 ets/api/@ohos.vibrator.d.ts，VibrateTime.duration）
- type Usage = 'unknown' | 'alarm' | 'ring' | 'notification' | 'communication' | 'touch' | 'media' | 'physicalFeedback' | 'simulateReality'：VibrateAttribute.usage 是必填项，取值在这些里选（出处：鸿蒙 SDK 的 ets/api/@ohos.vibrator.d.ts，vibrator.Usage）
针对本应用要查的：
- 每个控件点击后的副作用和偏好键、默认值：源工程里布局 onClick 绑定指向的 Fragment/Activity 处理器（按控件 id 搜 when 分支），以及 ViewModel 里初始化状态的那段；逐个分支记下调用的播放、振动、偏好读写和面板操作，偏好读取处的第二个参数就是默认值
未核实：偏好持久化的写法卡里没有上机验证；卡里振动先试 preset 'haptic.effect.soft' 再回退定时振动，真机震感被系统设置拦截，未确认；usage 取哪一个卡里没写
来源：1 张卡，1 个应用
- case-a224386ed55020afec18（android-train-ticket-vest7）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 诊断
