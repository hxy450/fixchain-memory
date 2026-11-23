# 被第三方拉起并回传结果的入口：setResult+finish 映射为一次 terminateSelfWithResult，最终状态确定后从唯一出口回传

## 何时使用

功能实现与接线阶段，移植源 Activity 响应第三方带结果请求（如 ACTION_IMAGE_CAPTURE、ACTION_VIDEO_CAPTURE）的结果回传、输出位置与限制参数时；判定这类入口的平台缺口时

## 适用情境

源端以 setResult(RESULT_OK/RESULT_CANCELED, data)+finish() 回传，可能在多处调用 setResult（后一次覆盖前一次，finish 幂等），并按 EXTRA_OUTPUT、时长/大小/质量限制或内联数据分支处理；目标由 Want 拉起，结果经 UIAbilityContext.terminateSelfWithResult 以 AbilityResult 一次性返回。

## 例外与边界

- 写调用方给的输出 URI 依赖调用方在 Want 的 flags 里临时授予写权限（FLAG_AUTH_WRITE_URI_PERMISSION）；打开或写入失败时按取消回传，不改写到本应用自选的位置再报成功。
- 只有经 startAbilityForResult 拉起时结果才会回到调用方；普通拉起的同一入口照样走唯一出口结束，不另写一条只 terminateSelf 的分支。

## 原因

只调用 terminateSelf 时调用方收不到结果码与数据；把多处 setResult 直译成一次性终止回调会先到先终止，结果回传两次或空结果先以成功结束；写入分支各自收尾时，带调用方输出位置的分支写完不回传。以上游临时实现推断“平台无数据通道”，还会把没有回传数据的请求报成成功。

## 做法

1. 结果出口写成 terminateSelfWithResult({ resultCode, want: { uri, parameters } })；resultCode 取当前契约约定的成功与取消值，规格未另定时沿用源端 RESULT_OK=-1、RESULT_CANCELED=0 并写进契约。
2. 列出源端全部 setResult/finish 调用点，合并为一个在最终状态确定后调用的出口；空输出或失败按取消返回。
3. 每个请求分支按“写入完成 → 回传 → 结束”串起，先等保存完成再结束，带调用方输出位置的分支写完也走结果出口；结果通道经查证确实无法携带的数据（如内联位图）按取消返回并释放资源，不报成功。
4. 启动 Want 里的输出位置与时长、大小、质量限制注入到实际执行写入或录制的组件；写调用方提供的 URI 时打开其 fd 写入，失败清理不删除调用方的资产。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕UIAbilityContext.terminateSelfWithResult 销毁 UIAbility 自身，只有当它是经 startAbilityForResult 拉起时才把 AbilityResult 返回给调用方，仅支持主线程调用；terminateSelf 只销毁自身、不回传结果
- 〔做法第 1、2 步〕安卓 Activity.RESULT_OK 为 -1（操作成功），RESULT_CANCELED 为 0（操作取消）
- 〔适用情境 / 做法第 2 步〕安卓 Activity.setResult 只把结果码和数据记在 Activity 上，多次调用以最后一次为准，finish 时才把记下的结果交回调用方
- 〔做法第 4 步〕MediaStore.EXTRA_VIDEO_QUALITY 是整数：0 表示低质量（面向彩信），1 表示高质量
- 〔做法第 4 步〕MediaStore.EXTRA_DURATION_LIMIT 是允许的最长录制时长，单位秒；EXTRA_SIZE_LIMIT 是允许的最大大小，注释没写单位
- 〔适用情境 / 做法第 3 步〕ACTION_IMAGE_CAPTURE 没带 EXTRA_OUTPUT 时，小尺寸图片以 Bitmap 放在结果的 extra 里返回；带了 EXTRA_OUTPUT 时，全尺寸图片写到 EXTRA_OUTPUT 给的 content resolver Uri
- 〔做法第 4 步〕fs.openSync 的 path 可以是应用沙箱路径或文件 URI；不传 mode 时以只读方式打开
- 〔做法第 4 步〕OpenMode.TRUNC 在文件存在且以有写权限的方式打开时把文件长度裁剪为零
