# “不确定”“待补资源”“无等价”“延期”“契约未确认”这类占位只登记输入确实缺值的情况：登记前查源码、SDK 与写入时刻的目录，能实现的当场实现

ID：`lesson-a2f6a4ae9a72be740de6` · 版本：8

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-a2f6a4ae9a72be740de6.json` 改了 0 句，后面接了 10 条已核实的平台事实。原文、来源和证据卡见 [memory/process/task-handoff/lesson-a2f6a4ae9a72be740de6.lesson.md](../../../../memory/process/task-handoff/lesson-a2f6a4ae9a72be740de6.lesson.md)。

## 何时使用

页面转换阶段决定是否登记 forward-ref-uncertain、resource-pending-asset 等占位，以及收口或验收阶段把这些占位改成 deferred 时；接线阶段决定尚未接通的页面动作是实现还是给出不可用提示时；把源端效果登记为“无等价/保留近似”，或派发对已登记近似项的复审时；收尾闭环处理指向本组或“集成期”的占位、准备按降级形态关单时

## 适用情境

工程提供多种占位类型（不确定值、待补资源、延期），页面规格置信度为 medium 或同名资源看似存在；源码和规格其实已给出行为或所需图形。也包括接线者给尚未接通的页面动作统一写 fail-loud 兜底（如“契约未确认，暂不可用”），而源端这些动作已有实现、目标工程也已有承担它们的共享组件。也包括实现者认为目标框架缺少对应能力（混合模式、端点渐变平铺等）而写入“无等价、保留近似”登记，复审派工又预写“保留”；或页面转换与资源迁移并行，转换者在资源复制完成前列目录看到空目录，就登记“资源未就绪”并改用降级。也包括写者只按对称方法名检索就把平台能力判为“无对等 API”，把可在本地实现的变换、自有端点引擎或页内权限链挂成依赖未建工件，以及收尾者为避开债务闸把占位改挂“集成期”“死码域披露”或按降级现状关单。也包括写者以“目标没有对等能力”为由删去源端构建标志条件分支（工程源码内检索不到生成文件引用），或未查 Options 类型字段（如气泡整体底色）就用近似替代且未登记。也包括把源有动画、目标写成静态的已知永久降级登记为 resolve_by 后续切片的前向引用，或编排派工统一要求把动画、视觉保真类占位 retag 为外部视觉核验阶段，而本轮流水线不运行该阶段。

## 例外与边界

- 缺的确实是输入里没有的值，例如合成快照缺少尺寸、资源映射表里没有对应资产

## 原因

占位把能实现的工作挂成债务，后续阶段看到“已登记”就放过，直到验收门把 deferred 判成阻塞。来源两例：顶栏连续折叠在源码里写明，陷阱表也给了做法，转换者因页面置信度 medium 登记“不确定”；动画图标的资产存在，缺的是按状态选帧，转换者挂成“待补资源”。收口阶段两次改 resolve_by、标 deferred，都没有回看源码。另一应用中接线者读到源端把详情动作委托给共享详情弹窗、目标已有同名组件，仍把分享、附件、前序、添加后续、更多菜单统一改成“契约未确认”提示。“目标没有”常是没查 SDK；复审派工预写“保留”时后来者只会背书、不会复核。写入前看到的空目录也可能只是资源还在复制，沿用他人 pending 登记而不核触发条件，降级就一直保留到交付。改挂到不属于任何切片的延迟或“死码披露”后，债务闸放行，代码里的空桩、降级与 TODO 一直保留到交付。

## 做法

1. 登记前判断：缺的是输入里的值，还是实现工作？后者当场实现；确实做不到，在报告里写明缺哪一项（哪一帧、哪个值）。
2. 页面置信度 medium 不要求产出不确定标记；引用陷阱表条目时核对它给的修法与自己的实现一致。
3. 收口或验收阶段处理这类条目时先回看条目指向的源码与代码现状；能实现就实现，只有确需真机数据或依赖确在仓外（三方 SDK 或平台 API 缺失）时才改为 deferred。不把占位改挂到没有切片认领的“集成期”“死码域披露”或外部视觉核验阶段来消除债务闸，也不按降级现状翻为 resolved：源行为明确的视觉保真项交回有写权的实现步骤，只有确需渲染才能判定的项才交验证阶段，该阶段本轮不运行时在交付摘要列为未完成项。已转换并注册路由的死码页，要么撤销转换与注册，要么按源码兑现页内占位。
4. 写 fail-loud 或不可用提示前逐项核对：源端该动作是否已有实现、目标端是否已有等价组件或服务；两者都有就接线复用；只有平台凭据等真实外部缺口才给阻断提示，并在提示和交接中写明具体缺口。
5. 登记“无等价”前在本地 SDK 的 .d.ts（含 hms/ets/kits）按能力语义检索：对应枚举、属性名、属性集合读取（如 getXxxProperties）、设置模块的键与候选模块文件，不只猜对称的 getter 名。“不存在”只能来自按成员名检索为空，或读到声明体闭合处的完整枚举；固定字符窗口、head 或按行数截断的回执只证明看到了哪些成员，工程里找不到 getter 只说明工程未暴露，凭记忆的判断不算查证；检索结果与规格映射要求冲突时先按成员名定向复查。把检索词与结论写进登记；同工程已有可行写法时直接沿用。
6. 写“资源未就绪、暂用降级”或沿用他人 pending 登记前，在写入时刻重新列出目标资源目录，或执行登记里的可机读触发条件，确认确实缺失。列目录时覆盖 base 与各限定目录（如各密度的 media），并按源端调用点（设置图标的方法、布局 XML）核对实际资源名；资源只在限定目录时，按工程资源约定补 base 副本或确认其解析方式，不判为未迁移。
7. 派发复审或切片工单时只给已登记条目与证据，不预写“保留”，要求执行者对照 SDK 与同工程已有实现复核后再裁决。
8. 下结论前同时查对应 Options/Attribute 类型声明和构建生成目录（如 hvigor 生成的 BuildProfile）；规格或已批准决策明确写出的条件，不以“release 语义一致”等理由自行删掉一腿，确认无等价时登记决策缺口交审批。
9. 确实采用近似时，在占位登记或转换报告写明具体差异，供验收逐项核对，不只写在代码注释里。

## 已核实的平台事实

核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）；Android Gradle 插件 4.0.2、7.1.2、8.1.1、9.4.1（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄。

- 〔做法第 5 步〕本地 SDK 有两套声明：openharmony/ets（component、api、kits）和 hms/ets（api、kits）；@kit.* 只是转导出（出处：鸿蒙 SDK 的 ets/kits/@kit.ArkUI.d.ts，export；鸿蒙 SDK 的 hms/ets/kits/@kit.AccountKit.d.ts，export）
- 〔做法第 5 步〕混合模式：CommonMethod.blendMode(value: BlendMode, type?: BlendApplyType)（@since 12），默认 BlendMode.NONE（效果同 SRC_OVER），BlendApplyType 默认 FAST，OFFSCREEN 为离屏混合（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.blendMode、BlendMode、BlendApplyType）
  写法：全局可用，不用导入（通用属性与全局枚举）：.blendMode(BlendMode.SRC_IN, BlendApplyType.OFFSCREEN)
        全局 BlendMode：NONE=0、CLEAR=1、SRC=2、DST=3、SRC_OVER=4、DST_OVER=5、SRC_IN=6、DST_IN=7、SRC_OUT=8、DST_OUT=9、SRC_ATOP=10、DST_ATOP=11、XOR=12、PLUS=13、MODULATE=14、SCREEN=15、OVERLAY=16、DARKEN=17、LIGHTEN=18、COLOR_DODGE=19、COLOR_BURN=20、HARD_LIGHT=21、SOFT_LIGHT=22、DIFFERENCE=23、EXCLUSION=24、MULTIPLY=25、HUE=26、SATURATION=27、COLOR=28、LUMINOSITY=29
        BlendApplyType：FAST=0、OFFSCREEN=1；画布侧另有 drawing.BlendMode（数值不同）
- 〔做法第 5 步〕渐变平铺：linearGradient/sweepGradient/radialGradient 的选项有 repeating?: boolean（默认 false）；drawing.ShaderEffect.createLinearGradient(startPt, endPt, colors, mode: TileMode, …)，TileMode：CLAMP 0、REPEAT 1、MIRROR 2、DECAL 3（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions.repeating；ets/api/@ohos.graphics.drawing.d.ts，ShaderEffect.createLinearGradient、drawing.TileMode）
  写法：全局可用，不用导入：.linearGradient({ angle: 90, colors: [[Color.Red, 0], [Color.Blue, 1]], repeating: true })  // colors: Array<[ResourceColor, number]>
        import { drawing, common2D } from '@kit.ArkGraphics2D'
        drawing.ShaderEffect.createLinearGradient(startPt: common2D.Point, endPt: common2D.Point, colors: Array<number>, mode: drawing.TileMode, pos?: Array<number> | null, matrix?: drawing.Matrix | null): drawing.ShaderEffect
- 〔做法第 5 步〕属性集合式读取的例子：窗口亮度在 Window.getWindowProperties() 返回的 WindowProperties.brightness（没有 getWindowBrightness）；系统亮度在设置模块的键 settings.display.SCREEN_BRIGHTNESS_STATUS（0–255）（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowProperties、WindowProperties.brightness；ets/api/@ohos.settings.d.ts，display.SCREEN_BRIGHTNESS_STATUS）
  写法：import { window } from '@kit.ArkUI'; import { settings } from '@kit.BasicServicesKit'
        (await window.getLastWindow(ctx)).getWindowProperties().brightness
        settings.getValueSync(ctx, settings.display.SCREEN_BRIGHTNESS_STATUS, '0'): string  // ctx: Context
- 〔做法第 6 步〕资源匹配：先找与设备状态匹配的限定词目录，找不到或没有匹配目录才去 base；密度限定词不要求完全一致，先向上取最接近的、否则向下，所以只放在某个密度目录的资源在任何密度的设备上都能匹配到（出处：文档 resource-categories-and-access.md，资源匹配、限定词目录与设备状态的匹配规则）
- 〔做法第 6 步〕鸿蒙密度限定词：sdpi (0,120]、mdpi (120,160]、ldpi (160,240]、xldpi (240,320]、xxldpi (320,480]、xxxldpi (480,640]，与安卓 drawable-ldpi、hdpi 等同名不同义（出处：文档 resource-categories-and-access.md，限定词目录）
- 〔做法第 8 步〕CustomPopupOptions.popupColor 默认 TRANSPARENT 加 COMPONENT_ULTRA_THICK 模糊，backgroundBlurStyle 为 BlurStyle.NONE（= 7）时才不模糊；PopupOptions 也有 popupColor 与 backgroundBlurStyle（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomPopupOptions.popupColor、backgroundBlurStyle、PopupOptions.popupColor、BlurStyle.NONE）
  写法：全局可用，不用导入：.bindPopup(this.showPopup, { builder: this.popupBuilder, popupColor: Color.White, backgroundBlurStyle: BlurStyle.NONE, radius: 8 })  // CustomPopupOptions.builder: CustomBuilder 必填
        BlurStyle：Thin、Regular、Thick、BACKGROUND_THIN、BACKGROUND_REGULAR、BACKGROUND_THICK、BACKGROUND_ULTRA_THICK、NONE、COMPONENT_ULTRA_THIN、COMPONENT_THIN、COMPONENT_REGULAR、COMPONENT_THICK、COMPONENT_ULTRA_THICK
- 〔做法第 8 步〕hvigor 生成 <模块>/build/<product>/generated/profile/<target>/BuildProfile.ets，含 BUNDLE_NAME、VERSION_CODE、VERSION_NAME、BUILD_MODE_NAME、DEBUG 等，并合入 build-profile.json5 的 buildOption.arkOptions.buildProfileFields（出处：DevEco Studio 自带 hvigor-ohos-plugin 包内 src/tasks/build-profile-task.js（BuildProfileTask）及其路径常量（GENERATED、PROFILE、BUILD_PROFILE_FILE））
  写法：生成文件内容：每个字段一条 'export const DEBUG = true;' 这样的导出，另有 'export default class BuildProfile { static readonly DEBUG = DEBUG; … }'
        该目录由构建工具加入本模块的源码根目录（'sourceRoots'）
- 〔做法第 5 步〕窗口亮度的成对读写：Window.setWindowBrightness(brightness: number): Promise<void>（另有 AsyncCallback 重载），取值 [0.0, 1.0] 或 -1.0（恢复跟随系统），窗口在前台且获焦时生效、退到后台失效；WindowProperties.brightness 没设过时读到 -1.0。系统亮度键 settings.display.SCREEN_BRIGHTNESS_STATUS 三方应用只能读：settings.setValue、setValueSync 写入需要 ohos.permission.MANAGE_SETTINGS（USER_SECURITY 域为 MANAGE_SECURE_SETTINGS），都仅系统应用可用（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowBrightness；ets/api/@ohos.settings.d.ts，settings.setValue、settings.setValueSync；文档 arkts-apis-window-Window.md，setWindowBrightness；文档 arkts-apis-window-i.md，brightness；文档 js-apis-settings.md，settings.setValue）
  写法：import { window } from '@kit.ArkUI'
        await win.setWindowBrightness(0.8)  // win: window.Window；-1 恢复跟随系统
        win.getWindowProperties().brightness  // 没设过时为 -1
- 〔适用情境 / 做法第 8 步〕源端 BuildConfig 是 AGP 构建时由 GenerateBuildConfig 任务生成的类，工程源码目录里没有，字段有 DEBUG（取变体的 debuggable）、APPLICATION_ID（库模块为 LIBRARY_PACKAGE_NAME）、BUILD_TYPE、FLAVOR、VERSION_CODE、VERSION_NAME；是否生成看 buildFeatures.buildConfig，没写时取 gradle 属性 android.defaults.buildfeatures.buildconfig 的默认值：AGP 4.0.2、7.1.2 为 true，8.1.1 起为 false，9.x 已移除该属性（出处：Android Gradle 插件包内（com.android.tools.build:gradle 4.0.2、7.1.2、8.1.1、9.4.1）的 BooleanOption.BUILD_FEATURE_BUILDCONFIG、BuildFeatureValuesImpl、GenerateBuildConfig（字节码））
