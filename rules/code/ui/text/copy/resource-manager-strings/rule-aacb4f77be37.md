# 组件内取字符串资源用 getHostContext() 判空后取 resourceManager

审的是：代码
触发（任一种）：
- 读到：源端 activity.getString(R.string.…) / getResources().getString(…) 拼进文本或 setContentDescription；写错的样子：写成 this.getUIContext().getResourceManager().getStringSync(…)，UIContext 没有 getResourceManager
适用范围：在组件里解析字符串资源时
做法：
- 链式调用逐跳核对：const ctx = this.getUIContext().getHostContext(); 为 undefined 时走兜底（如返回空串），否则 ctx.resourceManager.getStringSync($r('app.string.…'))
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getHostContext(): Context | undefined：UIContext 取宿主 Context，可能为 undefined，要先判空（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getHostContext）
- resourceManager: resmgr.ResourceManager：Context 上的资源管理器（出处：鸿蒙 SDK 的 ets/api/application/Context.d.ts，Context.resourceManager）
- getStringSync(resource: Resource): string：同步取字符串资源（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
来源：1 张卡，1 个应用
- case-a3c9f45c1b4dd1fb77b8（AntennaPod）：做法第 1 步 ← 建议 4、诊断
