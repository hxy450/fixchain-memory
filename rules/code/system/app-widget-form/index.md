# 桌面小部件迁成的 ArkTS 卡片

agent 会看到什么：读到 AppWidgetProvider、appwidget-provider 的 minWidth / minHeight、RemoteViews 布局，或卡片数据流（运行标志加条目）；产物里 FormExtensionAbility 读的状态来源、form_config.json 的 designWidth 和卡片里的字号、图标尺寸

## 规矩

- rule-8f385af71a29｜源端状态跨进程读不到时，选语义相同的持久投影，不借名称相近的派生值｜读到：规格的卡片数据流是 combine(运行标志, items)，并写明 FormExtensionAbility 与主 UIAbility 不共享内存、状态源只能是 RDB + preferences；写错：FormExtensionAbility 侧用另一个派生值（如「最近一次同步时间在 N 秒内」）代替「worker 正在运行」，注释写「源：X」而 X 与所用的值定义不同
- rule-3ac623f846a9｜小部件转 ArkTS 卡片时文字按源 sp 写 fp、图标随空间分配，不按 designWidth 放大｜读到：源小部件布局按钮 match_parent / wrap_content，android:drawableTop 放图标，android:textSize 用 sp；appwidget-provider 的 minWidth / minHeight 很小；写错：ArkTS 卡片里图标写成固定的大 width / height（vp），Text 的 fontSize 放大成源值的倍数，理由是 designWidth 720 要放大；桌面上文字被截断
