# Compose 的 Slider

agent 会看到什么：读过的 Compose 源码里有 Slider（valueRange、steps、SliderDefaults.colors）；交回的代码里 ArkUI Slider 的 step 和 thumb、轨道、刻度的画法

## 规矩

- rule-d11b569440ac｜Slider 步长按源码写 (max - min) / (steps + 1)，规格口径冲突时不改成规格值｜读到：源端 Slider(valueRange = a..b, steps = N)；规格或验收条目写「N+1 个停靠点」；写错：目标 Slider({ step: max / steps }) 或直接用规格给的值，注释写「与 spec 口径差 1 个停靠点，留 verify」
- rule-e43fcaa54f3c｜源 material3 Slider 迁移时自绘 M3 轨道和竖条 thumb，顶层透明 Slider 负责交互｜读到：源端 material3 Slider，只用 SliderDefaults.colors 传部分颜色，thumb 和刻度取 M3 默认；写错：目标用 Slider({ style: SliderStyle.OutSet }) 内置圆形 thumb，没有竖条 thumb、thumb 两侧留隙和刻度点
