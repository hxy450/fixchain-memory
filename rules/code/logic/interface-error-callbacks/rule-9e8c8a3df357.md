# 页面桥接失败时走应用接口的错误回调，不在桥里用裸资源键 toast

审的是：代码
触发（任一种）：
- 读到：源端拍照等操作的 errorCallback 只调应用接口的错误回调，由它 showToast 本地化提示；目标工程已有 toast(key) 先经 getStringByNameSync 解析的写法；写错的样子：页面桥的失败回调里直接 showToast('…_…', true) 传小写下划线的资源键字面量，绕过应用接口的错误回调；或在调了错误回调之外又 toast 一次
适用范围：页面层为拍照、录像等操作接失败回调时
做法：
- 失败时只调应用接口的错误回调（源 errorCallback 的唯一提示出口），不在桥里另行 toast
- 确需直接提示时，showToast 只传 getStringByNameSync(资源名) 解析后的文本，资源名与源一致
- 最小检查：grep showToast\('[a-z_]+' 找出裸键调用，并核对每个失败路径只产生一次提示
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringByNameSync(resName: string): string：按资源名取当前语言文案；资源名不存在时抛 9001004（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringByNameSync）
- 删除桥里两处裸键 toast，失败提示统一由应用接口错误回调经 sink 产生：修法，避免重复提示（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-385cf581f059f55e4e3b（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 4；取值 2 ← 诊断
