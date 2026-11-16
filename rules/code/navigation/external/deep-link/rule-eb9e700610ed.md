# URLSearchParams.get 改成手写解析时，先把 + 换成空格再 URI 解码

审的是：代码
触发（任一种）：
- 读到：源端 new URLSearchParams(location.search).get(key) 读深链或路由 query 参数；写错的样子：目标手写 split('&') / split('=') 后只做 decodeURIComponent(value)，没有先 replace(/\+/g, ' ')；?title=A+B 得到 'A+B'
适用范围：把源端表单编码的 query 读取（URLSearchParams 等）翻成目标端手写取值函数时
做法：
- 取值写成 decodeURIComponent(raw.replace(/\+/g, ' '))：先把 '+' 换成空格，再做 URI 解码，按 application/x-www-form-urlencoded 语义
- 用三例核对结果和源端一致：?title=A+B → 'A B'；含 %20 的值 → 空格；非 ASCII 的百分号编码值 → 原字符
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- The plus sign "+" is converted into a space character：application/x-www-form-urlencoded 解码时 '+' 是空格（出处：java.net.URLDecoder（类说明，application/x-www-form-urlencoded 解码规则））
- replace(/\+/g, ' ') 后再 decodeURIComponent：修复后的取值写法，判别器复核通过（出处：卡里修好并验证过）
未核实：卡里的环境是 HarmonyOS 26.0.0，本机只有 API 23；decodeURIComponent 不转 '+' 是 ECMAScript 行为，本机来源里没有原文
来源：1 张卡，1 个应用
- case-9fe714b7ae5de2097fcf（Countdate）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 2 ← 诊断
