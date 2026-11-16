# 外部查看入口沿委托链迁每个分支，无 URI 时回落，不在注释里断言源端直接 return

审的是：代码
触发（任一种）：
- 读到：源端点击处理委托给工具方法，后者 uri 为空时用 MediaStore.Images 的 EXTERNAL_CONTENT_URI 打开图库，另有 RAW 分支；写错的样子：目标网关 `if (!uri) return`，注释写「无 uri 时不操作（源 … return）」，没有 startAbility 之外的回落入口
适用范围：迁移打开最近媒体、图库这类外部查看入口时
做法：
- 沿锚点追到委托链末端的真实实现，逐支迁移：有 URI、RAW、无 URI 回落图库；没读到源码前不在注释里断言「源直接 return」
- 没有 URI 或 startAbility 打开失败时，改为拉起 new photoAccessHelper.PhotoViewPicker().select()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- select(option?: PhotoSelectOptions): Promise<PhotoSelectResult>：PhotoViewPicker 拉起系统图库选择界面（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoViewPicker.select）
- 打开失败或没有 URI 时拉起 PhotoViewPicker：修复时用它作为无媒体时的回落入口（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-3d6568f13ae09eb5090d（opencamera-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断；取值 2 ← 诊断
