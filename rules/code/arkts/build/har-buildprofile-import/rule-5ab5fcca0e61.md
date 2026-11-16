# HAR 页面照搬宿主的 DEBUG && 测试开关门控时，去掉 DEBUG，只按共享状态判断测试态

审的是：代码
触发（任一种）：
- 读到：宿主 HAP 的页面里测试态门控写成 if (DEBUG && 测试开关)，DEBUG 来自 import { DEBUG } from 'BuildProfile'；写错的样子：HAR 页面里出现 if (DEBUG && …) 门控，编译报 Cannot find name 'DEBUG'，或为此在 HAR 页面补了 import { DEBUG } from 'BuildProfile'
适用范围：给 HAR 里的页面加 UI 测试门控，或修 HAR 页面里 Cannot find name 'DEBUG' 时
做法：
- 先判断门控是否该在 HAR 里；要留的，删掉 DEBUG 和它的导入，条件只读共享的测试态（放在公共模块里的状态对象，或 AppStorage.get<boolean>(key)）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static get<T>(propName: string): T | undefined：AppStorage 是应用级、与应用同生命周期的状态，HAP 和它依赖的 HAR 读的是同一份（出处：鸿蒙 SDK 的 ets/component/common_ts_ets_api.d.ts，AppStorage.get）
- static setOrCreate<T>(propName: string, newValue: T): void：宿主侧写入测试态的写法（出处：鸿蒙 SDK 的 ets/component/common_ts_ets_api.d.ts，AppStorage.setOrCreate）
- 删掉 BuildProfile 导入后测试态只依赖共享状态，HAR 页面门控照常生效：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-282d676ed02777809cac（记得日历）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
