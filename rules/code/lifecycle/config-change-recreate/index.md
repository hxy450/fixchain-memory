# 未声明 android:configChanges 时的配置变化重建

agent 会看到什么：读过的 AndroidManifest.xml 里 Activity 没写 android:configChanges（或不含 orientation），旋转、改配置时安卓会重建页面，构造时的一次性状态和代码设置的视图状态随之复位；交回的 EntryAbility 没有 onConfigurationUpdate、页面没有配置变化的处理入口，或代码设的视图状态写成 @State 旋转后不复位

## 规矩

- rule-e639080e43b2｜未声明 configChanges 的 Activity，目标 Ability 要在配置变化时通知页面重建｜读到：`AndroidManifest.xml` 里 Activity 没有 `android:configChanges`，Activity 有 `onSaveInstanceState` / `savedInstanceState` 恢复分支；写错：`EntryAbility` 只在 `onForeground` / `onBackground` 发 save / load 事件，没有 `onConfigurationUpdate`，也没订阅 `display.on('change')`；注释写「冷启即 load 即进程恢复」
- rule-31ceec31f658｜页面收到配置重建事件时按安卓重建时序处理，不只靠 onAreaChange 刷新文案｜读到：源 View 在构造时新建输入监听、按 firstRun 一类一次性状态决定是否显示帮助，绘制时经 `getResources().getString` 取文案；Activity 没声明 `android:configChanges`；写错：页面只订阅 save / load 两路事件，或只在 `onAreaChange` 里重算布局时顺带刷新文案，没有配置变化的处理入口
- rule-f083c3f5c83a｜源端旋转会重建且视图状态由代码设置时，目标在方向变化时把它复位到初值｜读到：AndroidManifest 的 android:configChanges 不含 orientation；点击监听里 setBackgroundResource(...) 改视图，没存进 onSaveInstanceState；写错：目标把它写成页内 @State，旋转后保持不变
- rule-4480dae9123f｜目标的横竖翻转或配置变化分支，要重放源端新实例 onCreate 恢复分支和 onResume 的效果｜读到：源 Activity 没有 android:configChanges，onCreate 的 savedInstanceState 分支调刷新显示的方法，onResume 复位导航或计数字段；写错：目标页的横竖翻转分支或 onConfigurationUpdate 转发回调只关通关类弹窗、重算视口，没有调对应的刷新显示方法、没有复位那些字段
- rule-20d79cf27756｜转屏不重建的目标页，依赖宽度的一次性计算挂到 onAreaChange 宽度变化上｜读到：源端 Compose 在 BoxWithConstraints 里读 maxWidth，用带键的 LaunchedEffect(key) 算格数或列数；AndroidManifest 的 Activity 没有 android:configChanges；写错：onAreaChange 只在首次测量时发计算事件（如“上次值 < 0”守卫），之后只由键对应的 @Monitor 触发，转屏只重绘
- rule-d00ea897a406｜目标页配置变化时，仍开着的托管弹层改用重建后的内容和回调，不原样保留｜读到：源 DialogFragment 的 listener、路径、标题经 setter 注入，所在 Activity 没有 android:configChanges；规格写了重建后按钮只关闭、列表回默认；写错：onConfigurationUpdate 转发到页面的回调、mediaquery 或 onAreaChange 的横竖翻转分支里只关内联弹窗，注释写「托管弹层按契约保留」，openCustomDialog 打开的弹层继续持有原回调和参数；或页面根本没订阅配置变化
- rule-a1e3eb9ca26b｜重放源端重建效果时，先执行 onCreate 体内的写语句，再触发组合副作用对应的判定｜读到：源 Activity onCreate 先 setContent（组合内 LifecycleEventEffect(ON_CREATE) 读状态做判定），之后才写同一状态（如计数自增）；写错：配置变化重放里先同步 emit 事件让订阅方重新判定、后执行自增，注释写「源序 setContent 判定先于自增」
- rule-6f8521907e5a｜onConfigurationUpdate 重放先比配置指纹，没变就返回，变了先落新指纹再重放｜读到：源 Activity 没声明 android:configChanges，配置真实变化才整窗重建并重跑 attachBaseContext / onCreate；规格的重放签名带变化域（如 onConfigurationReplay(change: ConfigurationChange)）；写错：onConfigurationUpdate(newConfig) 每次回调都无条件执行重放清单，没有基线、没有字段比较
- rule-9eb4859246f7｜移植按屏幕配置计算的框架算法时，屏幕尺寸放进 @Local 状态并随转屏刷新｜读到：源端用 ActionBarPolicy.getMaxActionButtons 这类读 Configuration 屏幕 dp 的框架算法，Activity 没声明 android:configChanges，转屏重建后重算；写错：目标在普通方法里直接读 display.getDefaultDisplaySync() 计算，结果不依赖任何 @Local/@State，转屏后上栏数不变
