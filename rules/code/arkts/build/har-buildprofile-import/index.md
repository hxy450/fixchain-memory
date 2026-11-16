# HAR 模块里的 BuildProfile 和跨模块导入

agent 会看到什么：读到或产物里 HAR 模块的 .ets 有 import { DEBUG } from 'BuildProfile'、if (DEBUG && …) 门控、跨模块的 import 路径，或宿主入口调用下沉到 HAR 的服务 initialize()

## 规矩

- rule-e4ca6f86bd91｜HAR 模块代码里有 from 'BuildProfile' 时删掉，构建模式改由宿主传参或读共享状态｜读到：迁入或下沉到 HAR 的源文件（或宿主 HAP 的同类文件）里有 import { DEBUG } from 'BuildProfile'，用 DEBUG 决定日志输出等构建模式行为；写错：HAR 模块的 .ets 里出现 import { DEBUG } from 'BuildProfile'（裸模块名），或用了没有来源的 DEBUG
- rule-5ab5fcca0e61｜HAR 页面照搬宿主的 DEBUG && 测试开关门控时，去掉 DEBUG，只按共享状态判断测试态｜读到：宿主 HAP 的页面里测试态门控写成 if (DEBUG && 测试开关)，DEBUG 来自 import { DEBUG } from 'BuildProfile'；写错：HAR 页面里出现 if (DEBUG && …) 门控，编译报 Cannot find name 'DEBUG'，或为此在 HAR 页面补了 import { DEBUG } from 'BuildProfile'
- rule-77bf4b3c6cbf｜带构建开关的服务下沉到 HAR 后，宿主每个入口调用初始化时都传宿主的 DEBUG｜读到：下沉前的服务自己 import { DEBUG } from 'BuildProfile' 决定行为，宿主的 UIAbility、FormExtensionAbility、WorkSchedulerExtensionAbility、BackupExtensionAbility 里都调用它的 initialize()；写错：宿主入口只把导入改成从 HAR 模块名导入，仍调用无参的 initialize()，没有传 DEBUG；或只改了主 UIAbility，漏了卡片、WorkScheduler、备份扩展
- rule-15c6a4792c3a｜跨模块用类时只从模块包名入口导入，不改成跨进别的模块 src/main/ets 的相对路径｜读到：代码里已有 import { … } from '<模块包名>'；静态检测报 orphan 并建议 `import ... from '<relative-path>'`；写错：跨模块的类被改成 from '../../../…/<另一模块>/src/main/ets/…' 这样的相对路径导入
