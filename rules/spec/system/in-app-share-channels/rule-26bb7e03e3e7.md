# 源端分享走应用内渠道面板时，核对表先列交互形态，再在目标工程找同形面板

审的是：规格
触发（任一种）：
- 读到：源端分享入口截图后调用自建分享工具的 shareImage(...)，传入渠道项列表，回调按 platformName 分发到 QQ 空间、动态、蓝牙等渠道；写错的样子：外部入口核对表把这项分享的既有目标定为系统分享封装（构造 systemShare.ShareController 再 show 系统面板），没列源端交互形态，也没检索应用内的“分享至”Sheet 组件
适用范围：规格或外部入口能力核对阶段，为源端分享入口选定目标工程里可复用的既有分享能力时
做法：
- 核对表先列源端交互形态：应用内面板还是系统面板、渠道列表、承载的是图片还是链接；再列目标候选，只有形态一致的现有组件才算“保留原动作”的既有目标
- 检索目标工程的应用内分享组件及其调用方：ShareTo*、Share*Sheet、Share*Dialog，bindSheet 与渠道项，以及微信/QQ 图片发送工具；范围覆盖公共组件目录和已有分享页面，不只看 utils 里的系统分享封装
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- systemShare.ShareController：the controller can present system share panel：系统分享封装弹的是系统面板，不是带自定义渠道的应用内面板，形态不同（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.systemShare.d.ts，systemShare.ShareController）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：应用内“分享至”半模态面板通常由它承载，检索时按它找调用方（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
针对本应用要查的：
- 目标工程里已有的应用内分享面板：目标工程公共组件目录和已有“分享”入口页面里 bindSheet 的调用、名为 ShareTo* / Share*Sheet / Share*Dialog 的组件；读出它提供的渠道项和调用的发送工具，判断形态是否与源端一致
来源：1 张卡，1 个应用
- case-d357aaaeb2b5bd0759b9（两步路）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 1、诊断
