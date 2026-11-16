# string-array 条目引用 @string/ 时，strarray.json 不原样保留 '@string/…'

审的是：资源
触发（任一种）：
- 读到：res/values 里 <string-array> 的 <item>@string/…</item>（如 ListPreference 的 android:entries 数组）；写错的样子：strarray.json 的 value 原样是 "@string/…" 这种安卓语法，zh_CN 等语言目录也照样复制
适用范围：资源转换阶段把安卓 string-array 转成 strarray.json 时
做法：
- 逐项检查条目里的 @string/ 引用，按转换规则改写成 $string:name，或解析成各 locale 的实际文案写进对应语言目录的 strarray.json，不按「语言无关」原样复制
- 最小检查：用 resourceManager.getStringArrayValueSync 读回这些数组，确认首项不以 '@string/' 开头
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringArrayValueSync(resId: number): Array<string>：读回 strarray 的字符串数组，用来做最小检查（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringArrayValueSync）
- 原样保留时 getStringArrayValueSync 读出的就是 '@string/xxx' 字符串，界面显示原始资源名：不转换时的实际表现（出处：卡里修好并验证过）
未核实：strarray 值里写 $string:name 能否被 getStringArrayValueSync 在运行时解析，卡里和知识库都没核实
来源：1 张卡，1 个应用
- case-a0ce76f2b62e29f7e625（opencamera-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 2 ← 诊断
