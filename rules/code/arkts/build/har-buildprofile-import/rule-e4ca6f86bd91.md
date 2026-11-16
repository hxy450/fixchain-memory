# HAR 模块代码里有 from 'BuildProfile' 时删掉，构建模式改由宿主传参或读共享状态

审的是：代码
触发（任一种）：
- 读到：迁入或下沉到 HAR 的源文件（或宿主 HAP 的同类文件）里有 import { DEBUG } from 'BuildProfile'，用 DEBUG 决定日志输出等构建模式行为；写错的样子：HAR 模块的 .ets 里出现 import { DEBUG } from 'BuildProfile'（裸模块名），或用了没有来源的 DEBUG
适用范围：工程拆成宿主 HAP 加若干 HAR，把代码迁入 HAR 或在 HAR 里新增代码时
做法：
- 删掉 HAR 文件里的 import { DEBUG } from 'BuildProfile' 和据它求值的模块级常量
- 需要构建模式的服务把开关改成初始化参数（如 initialize(consoleEnabled: boolean)），由宿主入口或组合层传入；只用于测试态门控的改读共享状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 每个 HAR 模块有自己生成的 BuildProfile.ets；裸模块名 'BuildProfile' 只在宿主 HAP 里解析到宿主那份：HAR 里写 from 'BuildProfile' 拿不到宿主的构建模式；按 HAP 整体 assembleHap 可能照样通过，按模块的 ArkTS 检查报错（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-282d676ed02777809cac（记得日历）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
