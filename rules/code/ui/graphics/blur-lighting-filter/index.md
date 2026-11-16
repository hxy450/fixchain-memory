# 背景图的模糊变换和 LightingColorFilter 压暗

agent 会看到什么：读到源端加载背景图时做模糊变换（BlurTransformation），并 setColorFilter(new LightingColorFilter(mul, add)) 压暗；交回的背景 Image 没有 .blur，只用 Cover 加固定半透明遮罩近似

## 规矩

- rule-0411412b5a25｜源端模糊加 LightingColorFilter(mul, 0) 压暗时，用 blur 加黑色覆盖层按乘数换算｜读到：源码给头部背景图加模糊变换，并 setColorFilter(new LightingColorFilter(mul, add)) 压暗；写错：目标背景 Image 没有 .blur(...)，只用 ImageFit.Cover 加半透明遮罩近似，或没按 mul 的系数压暗
