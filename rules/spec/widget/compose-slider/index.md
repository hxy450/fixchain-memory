# Compose material3 Slider 的刻度和默认外观

agent 会看到什么：读到源端 material3 Slider(valueRange = …, steps = …) 或只用 SliderDefaults.colors 传了几种颜色；规格、快照或验收条目里的停靠点数、步长和外观不是按 steps 求值、库默认推出来的

## 规矩

- rule-6b991d7d614f｜Compose Slider 的 steps 在规格和验收条目里写成完整取值列表，取值数为 steps + 2｜读到：源端 material3 Slider(valueRange = a..b, steps = N)；写错：规格或验收条目写「steps=N（N+1 个离散停靠点）」，映射写 step = (b - a) / N，没有列出完整取值
- rule-a2f02329ce76｜提取 Compose Slider 时记录 steps 的求值结果，换算成目标步长，不把名为 step 的常量当步进｜读到：源端 Slider(valueRange = a..b, steps = (b / step).roundToInt() + 1) 这类由表达式算出的 steps，旁边有名为 step 的常量；写错：快照或规格写「Slider 0..3 步进 0.1」「steps 0.1」，映射写 Slider(min, max, step = 源常量)，没有写 steps 的求值结果和换算后的步长
- rule-36d62aa81b54｜源组件来自 material3 且只传部分颜色时，规格写明库默认外观和未传颜色的取值｜读到：源端 material3 Slider 只用 SliderDefaults.colors 传了 thumb / activeTrack / inactiveTrack 几种颜色，其余外观取库默认；写错：规格外观只记传入的几种颜色，映射直接写 ArkUI 内置样式（如 style: SliderStyle.OutSet），没写 thumb 形状、轨道高度、thumb 两侧留隙、刻度点和末端指示
