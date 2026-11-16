# 自绘 View 的单位、尺寸分支和位图缩放

agent 会看到什么：读到自定义 View 在 onSizeChanged 的 px 尺寸上推导布局、Paint.setTextSize / measureText 按 px 算，尺寸函数按计数和 DisplayMetrics.density 分支返回 dp，BitmapFactory.decodeResource 加 createScaledBitmap 预缩放再 drawBitmap；规格里画布单位、vp 数值和位图缩放的写法

## 规矩

- rule-d284acb1685f｜自绘画布的规格只写一份单位契约，写明上下文构造和各量的单位｜读到：安卓自定义 View 在 onSizeChanged 的 int px 尺寸上推导布局，Paint.setTextSize / measureText 按 px 算字号和间距；写错：规格里画布单位的说法不止一处且互相矛盾（字体串写 px、坐标映射写 vp），或者没写 CanvasRenderingContext2D 用哪个构造、默认按什么单位
- rule-cfd942f9a49b｜源端尺寸带计数或密度分支时，规格写明所取分支、源函数和换算出的 vp 值｜读到：源端角标 / 红点的尺寸函数按计数分支和 DisplayMetrics.density 分支返回不同的 dp 值；写错：规格或规格补充只写一个 vp 数值（如「红点 N vp 直径」），没有源尺寸函数、所取的计数分支和密度分支、换算过程，或数值是参照入口大小估出来的
- rule-a0d4f63f084b｜源端位图是密度解码、预缩放再 1:1 绘制时，规格逐步写出解码、预缩放采样和绘制方式｜读到：自绘 View 里 BitmapFactory.decodeResource 解码只放在单一密度目录（如 res/drawable-ldpi）的位图，再 Bitmap.createScaledBitmap(raw, w, h, false) 预缩放，onDraw 里 drawBitmap(bmp, x, y, null) 原尺寸绘制；写错：规格写成「decodeImage + drawImage 指定 w/h」或「filter=false 等价为普通缩放」，没有密度解码这一步，也没写缩放的采样方式
- rule-8c2c4fe03768｜Paint→Canvas 映射行写明属性不能读回、font 的 px 是物理像素、drawImage 尺寸｜读到：安卓源码用 Paint 的 setter/getter 管理绘制状态（setTextSize、getTextAlign），字号按 scaledDensity 算，用 drawBitmap + Matrix 画位图；写错：规格的映射行只写“Paint 属性映射 Canvas 等价属性”，没写上下文属性不能当状态读回、font 串里 px 的含义、三参数 drawImage 的绘制尺寸
- rule-f10b5bbc6fda｜源端用 getIntrinsicWidth/Height 定格尺寸时，规格写成设备密度 px 契约并给换算式｜读到：自定义 View 用 Resources.getDrawable 取放在 drawable-mdpi…xxxhdpi 多个密度目录的位图，以 getIntrinsicWidth() / getIntrinsicHeight() 作格尺寸进 px 公式，再 setBounds 绘制；写错：规格映射行写「贴图资源固有 px」「解码尺寸」或「同 px 域」，没写明安卓固有尺寸已按设备密度缩放，也没给目标资源的来源目录 dpi 和换算式
