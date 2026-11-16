# strarray 作显示文本时，读出后对 '@string/' 前缀逐项 getStringByNameSync

审的是：代码
触发（任一种）：
- 读到：strarray.json 条目是 "@string/…"，或工程注释约定「strarray 内 @string/ 引用经 getStringByNameSync 解析」；写错的样子：共享的 strArray 助手直接 return resourceManager.getStringArrayValueSync(res)，没有处理 '@string/' 前缀，弹层显示原始资源名
适用范围：目标代码读 strarray 资源作弹层、列表等显示文本时
做法：
- 在共享的 strArray 助手里统一处理：arr.map(s => s.startsWith('@string/') ? resourceManager.getStringByNameSync(s.substring(8)) : s)
- 用之前先看工程里已有的解析约定；复用已有样板时把旁边的解析或映射分支一起带上，不只复制裸的 getStringArrayValueSync
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringByNameSync(resName: string): string：按资源名（不带 '@string/' 前缀）取当前语言的字符串（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringByNameSync）
- getStringArrayValueSync(resId: number): Array<string>：按资源 ID 读字符串数组（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringArrayValueSync）
- getStringArrayValueSync(resource: Resource): Array<string>，@deprecated since 20：传 Resource 对象的重载已废弃（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringArrayValueSync）
- strArray 里对 '@string/' 前缀逐项调 getStringByNameSync 后，引用型条目显示成实际文案：消费侧解析的修法，资源文件可保持原样（出处：卡里修好并验证过）
未核实：卡里上机结果出自 HarmonyOS 6.1.1(24)，本机声明是 API 23
来源：1 张卡，1 个应用
- case-a0ce76f2b62e29f7e625（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
