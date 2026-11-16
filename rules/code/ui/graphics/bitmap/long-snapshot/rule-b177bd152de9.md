# 源端按内容总高建 Bitmap 导出长图时，目标端超一屏内容分段快照再拼接，并校验高度

审的是：代码
触发（任一种）：
- 读到：安卓按子 View 累加的总高度 Bitmap.createBitmap(width, height) 后整体 draw(canvas) 导出，保存图高度随内容无上限；写错的样子：目标端只做一次 createFromBuilder 快照，builder 根组件只定宽、高度由内容撑开，注释或交付说明断言「不受可视区域、屏幕边界和裁剪限制」；没有分段，也没有校验返回 PixelMap 的高度
适用范围：需求要求任意长度内容完整导出为图片、目标端用 componentSnapshot 离屏快照时
做法：
- 不按「离屏渲染」推断不受尺寸限制：单次快照只用于不超过约一屏的内容
- 超出约一屏的内容按固定视口分段渲染（卡里每段 600vp），每段快照得到的 PixelMap 用 readPixels 读出、writePixels 写进按总高建的 PixelMap 里拼接
- 把返回 PixelMap 的像素高度和内容实测高度比较，不一致就走分段
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 截图不建议超过屏幕尺寸；目标长宽超过底层限制时截图返回失败，不同设备的底层限制不同：单次快照能承载的尺寸有上限，且随设备变（出处：js-apis-arkui-componentSnapshot.md，SnapshotOptions12+ 的 scale 说明）
- createFromBuilder(builder: CustomBuilder, delay?: number, checkImageStatus?: boolean, options?: componentSnapshot.SnapshotOptions): Promise<image.PixelMap>：UIContext.getComponentSnapshot() 得到的 ComponentSnapshot 上的离屏快照；componentSnapshot 模块里的同名函数从 API 18 起废弃（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，ComponentSnapshot.createFromBuilder）
- readPixels(area: PositionArea): Promise<void>；writePixels(area: PositionArea): Promise<void>：PixelMap 按区域读出、写入像素，用来把各段拼进一张图（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，PixelMap.readPixels、PixelMap.writePixels）
- createPixelMap(colors: ArrayBuffer, options: InitializationOptions): Promise<PixelMap>：按总宽高新建承载拼接结果的 PixelMap（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，image.createPixelMap）
- createFromComponent<T extends Object>(content: ComponentContent<T>, delay?: number, checkImageStatus?: boolean, options?: componentSnapshot.SnapshotOptions): Promise<image.PixelMap>：同族接口：ComponentSnapshot 对 ComponentContent 离屏快照，同受 SnapshotOptions 的尺寸限制（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，ComponentSnapshot.createFromComponent）
- get(id: string, options?: componentSnapshot.SnapshotOptions): Promise<image.PixelMap>：同族接口：ComponentSnapshot 对已上树组件按 id 截图（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，ComponentSnapshot.get）
- getSync(id: string, options?: componentSnapshot.SnapshotOptions): image.PixelMap：同族接口：ComponentSnapshot 同步截图（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，ComponentSnapshot.getSync）
未核实：卡里截断来自渲染表面像素上限还是离屏根布局约束没确认；分段拼接的最终版本没上机验证；文档说超限时截图返回失败，卡里看到的是保存结果不完整，两者是否同一机制没核实；卡里的行为出自 HarmonyOS 5.0.4(16)，本机按 API 23 声明核实
来源：1 张卡，1 个应用
- case-8f1c44fda18a688f1260（五星智投）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2、诊断
