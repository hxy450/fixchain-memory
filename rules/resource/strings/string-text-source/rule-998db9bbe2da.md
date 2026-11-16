# 框架默认的 ok、cancel 要落成目标资源，各语言值从 Android 框架对应语言目录取

审的是：资源
触发（任一种）：
- 读到：源端对话框按钮用框架默认的 @android:string/ok、@android:string/cancel（偏好 XML 没声明按钮文案）；写错的样子：base 和各语言 string.json 里没有框架 ok / cancel 对应的条目，只有应用自己的 ok、cancel、confirm
适用范围：资源迁移阶段为框架默认文案建目标字符串资源时
做法：
- 新增 android_ok、android_cancel 两个键：base 取框架 values/strings.xml 的 ok、cancel，每个语言目录取框架 values-<语言>/strings.xml 的同名值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- <string name="ok">OK</string>、<string name="cancel">Cancel</string>：框架默认语言的值（出处：Android SDK 平台资源 data/res/values/strings.xml，ok、cancel（按应用的 compileSdk 取对应平台））
- values-ko 里 ok = 확인、cancel = 취소：例：其他语言按同名键在对应 values-<语言> 里取（出处：Android SDK 平台资源 data/res/values-ko/strings.xml，ok、cancel（按应用的 compileSdk 取对应平台））
- 新增 android_ok / android_cancel：修好的资源（出处：卡里修好并验证过）
针对本应用要查的：
- 目标要支持的每种语言下框架的 ok、cancel：Android SDK 平台资源 data/res/values-<语言>/strings.xml，按 name="ok"、name="cancel" 找，平台按应用的 compileSdk 取；读出引号里的值写进目标对应语言目录的 string.json
来源：1 张卡，1 个应用
- case-4975883d1d11fd0cde40（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
