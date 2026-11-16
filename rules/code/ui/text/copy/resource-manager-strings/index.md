# 代码里经 resourceManager 取文案

agent 会看到什么：目标代码里手里是 $r(…)、Resource 或 ResourceStr 而要的是 string 的地方：resourceManager.getStringSync / getStringByNameSync / getStringArrayValueSync 的传参、getHostContext() 取上下文、typeof 收窄，或构建报 Resource 不能赋给 string；源端对应 getString、getResources().getString

## 规矩

- rule-58379494f7b0｜编译修复遇 Resource 不能赋给 string 时，用 getStringSync 解析本地化文本，不用枚举名｜读到：构建日志报 `Type 'Resource' is not assignable to type 'string'`（如 PopupOptions.message），源端是 stringResource(nameResId) 的本地化提示；写错：修复把 message 改成枚举的 rawName / name，本地化名称退化为英文枚举名
- rule-e63023383177｜已移植的 getter 返回 ResourceStr 而状态是 string 时，解析资源，不回退成占位字符串｜读到：目标侧已移植的 getter 返回 ResourceStr，空值时给的是 $r('app.string.…') 资源；写错：组件状态（@Local 字段）声明成 `string`，因类型不合改读原始字段或回退成占位字符串，没解析资源
- rule-b96530c7757c｜ResourceStr 传给 accessibilityText 时先用 typeof 收窄再调用｜读到：目标页面里的 `@Local` 状态字段或方法参数声明为 `ResourceStr`，参照的修饰链模板来自字段类型是 `Resource` 的其他页面；写错：把 ResourceStr 字段直接传进 `.accessibilityText(...)`，编译报 10505001（没有匹配的重载）
- rule-aacb4f77be37｜组件内取字符串资源用 getHostContext() 判空后取 resourceManager｜读到：源端 activity.getString(R.string.…) / getResources().getString(…) 拼进文本或 setContentDescription；写错：写成 this.getUIContext().getResourceManager().getStringSync(…)，UIContext 没有 getResourceManager
- rule-19cdc7b52705｜代码内取文案用 getStringSync($r(…).id) 按 id 取，不传 Resource 对象｜读到：安卓自绘 View 里用 getResources().getString(R.string.*) 取文案，再交给 canvas.drawText 或 paint.measureText；写错：代码内取字符串写成 resourceManager.getStringSync($r('app.string.*'))，传的是 Resource 对象而不是它的 .id
- rule-1726cde681da｜有应用内语言切换时，resourceManager 取串、数组、复数、颜色一律传 $r(...).id｜读到：工程用 i18n.System.setAppPreferredLanguage 做应用内语言切换，既有取串辅助写成 resourceManager.getStringSync(res.id)；写错：新写的取值传 Resource 对象：getStringArrayValue($r('app.strarray.…'))、getStringSync(resource)、getColorSync($r('app.color.…'))，没带 .id
- rule-7e99c4e9f0b1｜HAR 页面把按名取资源改写成静态 $r 时，先确认名字在本模块或已声明依赖里｜读到：HAR 页面用 `getStringByNameSync(name)` 或封装的按名取字符串函数取文案；写错：改写成 `$r('app.string.X')`，而 X 只在壳模块、AppScope 或未依赖的模块里定义
- rule-5910abbde8fe｜strarray 作显示文本时，读出后对 '@string/' 前缀逐项 getStringByNameSync｜读到：strarray.json 条目是 "@string/…"，或工程注释约定「strarray 内 @string/ 引用经 getStringByNameSync 解析」；写错：共享的 strArray 助手直接 return resourceManager.getStringArrayValueSync(res)，没有处理 '@string/' 前缀，弹层显示原始资源名
