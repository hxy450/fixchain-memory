# 构造期解码和预缩放的位图

agent 会看到什么：读到源端在 View 构造器或 onCreate 里同步 BitmapFactory.decodeResource、按屏宽算出的尺寸 Bitmap.createScaledBitmap 预缩放，再 drawBitmap 原尺寸绘制；产物里每帧 drawImage 缩放、没按密度解码、位图在几何计算前用模块级守护只装一次，或改成 async 启动加输入门控

## 规矩

- rule-3f450c33668b｜源端预缩放后原尺寸绘制时，目标按密度解码再 scaleSync，drawImage 不传 dw/dh｜读到：BitmapFactory.decodeResource 解码单一密度目录的位图，Bitmap.createScaledBitmap(raw, w, h, filter) 预缩放，drawBitmap(bmp, x, y, null) 原尺寸绘制；写错：原图解码一次后每帧 ctx.drawImage(img, x, y, w, h) 绘制期缩放，没有密度解码，也没指定最近邻
- rule-16cf879e396a｜预缩放尺寸依赖运行时几何时，放在几何计算之后、按源端时机每个视图实例重做，不用进程级守护｜读到：源端视图构造器里先算几何（由屏宽算出格径之类），再调用预缩放方法 createScaledBitmap(raw, 格径, 格径, …)；写错：位图装载放在几何计算之前，或用模块级的 `loaded` 布尔守护只做一次，后续页面复用旧尺寸的位图
- rule-c1c411b6e88a｜源端构造器里同步做完的初始化，目标在 aboutToAppear 按源顺序同步执行并用 Sync 接口｜读到：源端自定义 View 构造器或 Activity.onCreate 里同步完成取尺寸、初始化、BitmapFactory.decodeResource / createScaledBitmap，之后才接收输入；写错：目标改成 await source.createPixelMap()、await window.getLastWindow(...) 的 async 启动，并加 if (!this.booted) return 这类「初始化完成前忽略输入」的门控
