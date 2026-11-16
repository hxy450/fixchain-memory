# Ionic 的 IonHeader / IonToolbar 顶部工具栏

agent 会看到什么：读到源页面 IonHeader > IonToolbar 里的 IonTitle（Ionic mode: "ios" 下居中）、IonButtons slot="end" 的图标按钮、有没有 IonBackButton；产物里 NavDestination 的 .title / .menus 自定义槽、hideTitleBar(true) 加页内头部、头部 Row 里标题的 layoutWeight 和居中

## 规矩

- rule-8d274ae312e3｜源工具栏无返回键、标题居中或带右侧动作时，用 hideTitleBar(true) 加页内头部｜读到：源页面 IonHeader > IonToolbar 里没有 IonBackButton，IonTitle 在 Ionic mode: "ios" 下居中，IonButtons slot="end" 放一组图标 IonButton；写错：目标端用 NavDestination 的 .title(this.builder) 和 .menus(this.builder) 自定义槽拼整条工具栏，保留了源端没有的系统返回键，标题左对齐；运行时标题栏塌缩，标题和动作按钮不可见
- rule-e31b7dc146f6｜复用已有头部写法前核对源端标题对齐，Ionic iOS 的 IonTitle 全宽居中｜读到：源 IonToolbar 里 IonTitle 加 slot="end" 的按钮（Ionic iOS 模式）；写错：目标头部 Row 里标题只有 .layoutWeight(1)，没有居中，end 按钮挤占了居中空间
