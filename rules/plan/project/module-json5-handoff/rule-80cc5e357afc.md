# 移交 module.json5 配置缺口时，按所用 skill 的检查清单抄全，含后台播放两项

审的是：计划与派工
触发（任一种）：
- 读到：所用 skill 的 module.json5 检查清单要求 backgroundModes: [audioPlayback] 和 ohos.permission.KEEP_BACKGROUND_RUNNING；派工的写盘边界不许改 module.json5；写错的样子：交给收尾者的 module.json5 移交项（deferred-work）只列 skills 和运行时权限（如 ohos.permission.MICROPHONE），没有 backgroundModes: [audioPlayback] 和 ohos.permission.KEEP_BACKGROUND_RUNNING
适用范围：worker 不能改 module.json5、把配置缺口登记成移交项交给收尾者时
做法：
- 移交项从所用 skill 的 module.json5 检查清单逐项抄全，不只列运行时权限；用到后台音频时必须写上 abilities 的 "backgroundModes": ["audioPlayback"] 和 requestPermissions 的 ohos.permission.KEEP_BACKGROUND_RUNNING
- 收尾者落地 module.json5 之前，对照同一份清单核一遍
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 后台音频要的配置：abilities 的 backgroundModes 含 audioPlayback，requestPermissions 含 ohos.permission.KEEP_BACKGROUND_RUNNING：移交项里不能少的两项（出处：continuous-task.md，Stage模型）
来源：1 张卡，1 个应用
- case-1dee716aadc97af875f2（omni-notes-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
