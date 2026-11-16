# SEND 分享入口在 standard Activity 上时，规格写明每次新建独立实例、只结束自己

审的是：规格
触发（任一种）：
- 读到：清单 Activity 上有 action SEND / SEND_MULTIPLE + category DEFAULT + mimeType 的 intent-filter，没写 launchMode（standard）；源码没有 onNewIntent，只在 onCreate 读 getIntent() 的 EXTRA_TEXT，处理完 finish()；写错的样子：规格写「EntryAbility onCreate/onNewWant 解析 want → 路由本页」「冷启动/热启动」，结束只写 setResult+finish 或 → terminateSelf，没写结束的是哪个实例
适用范围：规格提取时映射源端 SEND 类外部入口的实例形态、承接 Ability 和结束范围
做法：
- 规格写明实例形态：每次外部调用由框架新建实例，finish() 只结束这个实例并回到来源应用，原来运行中的应用不受影响
- 映射成独立的 UIAbility（launchType multiton，加载同一页面，经 loadContent 的 LocalStorage 把入参交给页面），结束时 terminateSelf 只结束这个实例；不写成入口 EntryAbility 的 onCreate/onNewWant 冷热启动承接加全局事件槽
- 验收条目写：分享后出现独立任务，导入或取消后原来的页面仍在前台
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- launchType：multiton 多实例，每次启动创建新实例；singleton 仅第一次启动创建；缺省为 singleton：唯一的入口 EntryAbility 默认 singleton，承接不了「每次新建」（出处：module-configuration-file.md，abilities标签 launchType）
- 独立 multiton Ability 承接分享后，分享出现独立任务，导入后分享任务结束、原列表回到前台：修复后的实例形态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4e3bf06f478ee642f9cb（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1；取值 2 ← 诊断
