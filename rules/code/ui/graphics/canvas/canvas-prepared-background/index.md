# 自绘 View 一次性准备的背景位图和颜色

agent 会看到什么：读到自定义 View 在构造、setup() 或 onSizeChanged 里一次性烘焙背景 Bitmap、从主题属性取色；产物里改成每帧重绘却没 clearRect、每帧读实时状态，或只在 aboutToAppear 取一次色

## 规矩

- rule-313f9e5008fe｜源端一次烘焙背景位图、目标改每帧矢量重绘时，render() 开头先 clearRect 整幅画布｜读到：自定义 View 构造里 `setBackgroundColor(…)`，`onDraw` 开头 `drawBitmap(background)` 画一张只烘焙一次的 `ARGB_8888` 透明背景位图（标题、说明等抗锯齿文字只栅格化一次），再叠动态层；写错：目标 `render()` 开头直接画背景层，标题、说明每帧 `fillText` 叠到上一帧上，没有 `clearRect`，也没有整幅填背景色
- rule-470b0237ba6d｜源端在 onSizeChanged 预渲染背景位图时，目标每帧重绘也要给条件元素的状态留快照｜读到：自定义 View 在 onSizeChanged 里生成背景 Bitmap，生成函数里 if (某状态字段) 才画某元素；onDraw 每帧只 canvas.drawBitmap(背景位图, …)；该字段之后还会被新开局一类流程改写；写错：目标 Canvas 每帧画背景层时直接读实时状态字段（if (状态字段) 每帧判断），没有在布局或尺寸变化入口留快照
- rule-e89c55afe10e｜构造期从主题属性取色的自绘 View，迁移时把取色写成可重入方法，主题变化时重取并重绘｜读到：自定义 View 在构造或 setup() 里用 obtainStyledAttributes / 主题属性取色，设给 Paint；写错：目标端只在 aboutToAppear 里 getColorSync 一次存成字符串（strokeColor 等），没有主题或配置变化时的重解析和重绘路径；其他组件以它为先例照抄
