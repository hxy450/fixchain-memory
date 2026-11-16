# 页面收到配置重建事件时按安卓重建时序处理，不只靠 onAreaChange 刷新文案

审的是：代码
触发（任一种）：
- 读到：源 View 在构造时新建输入监听、按 firstRun 一类一次性状态决定是否显示帮助，绘制时经 `getResources().getString` 取文案；Activity 没声明 `android:configChanges`；写错的样子：页面只订阅 save / load 两路事件，或只在 `onAreaChange` 里重算布局时顺带刷新文案，没有配置变化的处理入口
适用范围：目标页面承接源端随配置变化重建的 Activity 和 View 时
做法：
- 订阅 Ability 发出的重建事件，处理函数按安卓重建时序依次执行：关闭确认框等对话框 → save → 新建输入控制器 → 重置一次性状态（帮助显示重新按 firstRun 取）→ load → 重读资源文案并重算布局
- 不要依赖尺寸回调：onAreaChange 只在组件大小或位置变化时触发，切语言不会触发
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：组件大小或位置变化结束时回调，和配置变化无关（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- 只靠 onAreaChange 刷新文案时，切语言后画布仍是旧语言，帮助文案和确认框也保留；改成重建事件按时序处理后正常：尺寸回调接不住配置变化（出处：卡里修好并验证过）
针对本应用要查的：
- 源端重建时哪些对象重新构造、哪些状态重置、哪些文案重读：源 View 的构造函数、onSizeChanged、onDraw，以及 Activity 的 onCreate / onSaveInstanceState；逐项列出，按 save → 构造 → load → 重读资源 的先后排进处理函数
来源：1 张卡，1 个应用
- case-f879e05d3c9a16396341（2048）：做法第 1 步 ← 诊断、建议 3；做法第 2 步 ← 建议 3、诊断；取值 2 ← 诊断
