# 深链验收条目写隐式 Want 的拉起法，不用 aa start -b/-a 显式拉起

审的是：规格
触发（任一种）：
- 读到：验收条目以清单深链为来源，要求外部 URL 打开对应页面；写错的样子：验收条目或验收步骤里深链用例写成 aa start -b <bundleName> -a <abilityName> -U <url> 显式拉起
适用范围：外部深链功能的验收条目和验收步骤
做法：
- 验收步骤写成隐式拉起：aa start -A ohos.want.action.viewData -U <url>，不带 -b、-a；或从外部应用点击链接
- 条目里写明：带 -b/-a 显式拉起不经 skills 匹配，不能当作深链通过的依据
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- aa start [-d <deviceId>] [-U <URI>] [-t <type>] [-A <action>] [-e <entity>] …：隐式启动的命令形式；参数都不填会启动失败（出处：aa-tool.md，启动命令（start））
- 10103101：Failed to find a matching application for implicit launch.：隐式拉起找不到匹配的应用时的错误码，多半是 skills 没声明或没匹配上（出处：aa-tool.md，启动命令（start）错误码）
- 显式拉起（-b/-a）不经 skills 匹配，缺 skills 声明也能打开页面：显式拉起的通过不说明深链可用（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-6bc0c044e9bb2281aa01（Cofi）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
