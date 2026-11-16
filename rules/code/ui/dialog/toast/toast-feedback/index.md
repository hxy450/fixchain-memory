# Toast 提示和结果反馈的形式

agent 会看到什么：读到源端用 Toast.makeText（LENGTH_SHORT / LONG）、AlertDialog 的去设置引导给校验失败、权限拒绝、写入成功等结果反馈；产物里时长写死、文案少了加工、改成页内错误行或整页错误态、失败一律 showToast，或该弹引导的地方仍弹源端 Toast

## 规矩

- rule-cfba082d6c4a｜源码混用 Toast 的 SHORT 和 LONG 时，Toast 封装带 duration 参数、逐处照源映射｜读到：源码 Toast.makeText(…, Toast.LENGTH_SHORT) 和 Toast.LENGTH_LONG 在同一文件或同一公共方法里混用；写错：目标 showToast({ message, duration }) 全部用同一个时长（如只定义一个 LONG 常量 3500），或公共 Toast 封装只有 message 参数、duration 写死
- rule-638fea17bef4｜源码对 Toast 文案做 toLowerCase 等加工时，getStringSync 取成 string 后照样加工｜读到：源码 Toast 文案先 getString(R.string.…) 再 .toLowerCase() 等字符串加工后拼接；写错：目标已用 resourceManager.getStringSync(...) 把资源取成 string，却删掉了 .toLowerCase()，直接用资源原文拼接
- rule-232d9948a670｜安卓校验失败用 toast 提示时，目标也用 showToast，页内错误行放固定位置｜读到：安卓确认或保存时的必填校验失败分支用 toast 提示（`Toast` 或封装的 `toast("…")`）后返回；写错：校验失败分支只给状态变量赋值（如 `errorMessage = '…'`）再 `return`，反馈只是追加在 `layoutWeight(1)` 内容区末尾的条件 `Text`，没有 `showToast`
- rule-0232620c4a32｜源端权限被拒时弹“去设置”引导，目标失败分支按失败类型分派，不一律 toast｜读到：源端权限回调拒绝后用 AlertDialog.Builder 弹“无法使用…／取消／去设置”，去设置跳 Settings.ACTION_APPLICATION_DETAILS_SETTINGS；只有启动器本身失败才 Toast；目标 ViewModel 的启动方法只返回 boolean，失败类型另存在一个字段里（含权限拒绝）；写错：宿主页的 if (!started) 分支一律 promptAction.showToast(...) 后返回，没读失败类型，没有去设置引导弹窗
- rule-70432d264295｜源端系统写入后 Toast「设置成功」而目标已降级为存相册时，各入口成功路径改弹引导｜读到：源端调用系统写入接口（如 WallpaperManager 设壁纸）后用 Toast 回执「设置成功/失败」；规格或已批决策把目标端改成 SaveButton 保存到相册、再引导用户手动设置；写错：目标入口的成功分支仍弹源端的「设置…成功」Toast，没有展示决策规定的引导
- rule-7962d306c6f0｜整页错误态只由列表加载失败且无数据驱动，不用聚合了次级动作的单一 errorMessage｜读到：规格把列表状态（Loading | Content | Empty | Error）和定位、权限等次级状态分成两套；验收条目写「权限拒绝后允许手动选择」「不支持时保留并提示」；写错：页面写成 errorMessage 非空即整页错误态（if (this.errorMessage) 渲染错误内容），而 ViewModel 把定位、权限、选择、列表等所有失败都写进同一个 errorMessage
- rule-51e9274bb95a｜Toast 的 LENGTH_SHORT/LONG 迁成 showToast 时长写 2000/3500｜读到：Toast.makeText(context, text, Toast.LENGTH_SHORT) 或 Toast.LENGTH_LONG，或经辅助方法传 Toast.LENGTH_LONG；写错：showToast({ message }) 没写 duration（落到默认 1500），或 duration 写成 1500 / 3000 这类估算值，注释写「短≈1.5s / 长≈3s」
- rule-381fa5a32c9d｜源调用继承自基类的方法时，读完基类实现，把开关守卫、默认值和参数照迁｜读到：源方法调用本类没定义、继承自基类的方法（如基类 Activity 里封装 Toast.makeText 的提示方法，调用时传 Toast.LENGTH_LONG），基类实现里先判偏好开关再显示；写错：目标直接换成平台调用 promptAction.showToast({ message })，没有基类实现里的偏好开关守卫，也没传源端给的时长
- rule-c1354522869b｜源端服务层弹 Toast 时，目标用 getLastWindow 加 showToast 复刻，不换成日志｜读到：Java 帮助类或服务里 `Toast.makeText(context, ..., ...).show()`（含 Handler(mainLooper).post 里弹出），如设定提醒后提示时间、未授权时再提示一次；写错：ArkTS 把 Toast 换成 hilog.info，注释写「服务层无后台 Toast 通道，降级日志」
- rule-9abd9796fe2b｜规格把 Toast 上移到调用层时，服务失败仍按 AC 写明的源端原文提示｜读到：规格 AC 写了服务两个失败分支各自的 Toast 原文：结果为空时一句固定文案，请求异常时显示异常的 message；写错：服务两种失败都只返回 ''，异常的 message 只进 console.error，页面弹自造的通用 $r('app.string.…') 文案
