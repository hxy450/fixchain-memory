# 源布局里的原生地图（MapView / AMapNaviView）

agent 会看到什么：读过的源码里 MapView / AMapNaviView 铺满全屏作底层，桥接分出 onResume / onPause / onDestroy 三个接口，或决策台账写三方地图不迁 SDK；交回的地图被改成固定高的地图卡、静态图冒充的假地图，页面被整页重写，或只在 onReady / onDisAppear 里创建和释放

## 规矩

- rule-912bd6c532a8｜目标地图或导航 SDK 不可用时，地图承载仍放全屏底层用占位面，不改成固定高的地图卡｜读到：源布局里 MapView / AMapNaviView 铺满全屏作底层，前景是覆盖层；或巡检发现写明「全屏底层」「缺少全屏地图承载」；写错：目标在覆盖层里插入一个固定高度（如 .height(180)）的圆角「地图卡」或「map-like」自绘面，代替全屏承载
- rule-7b8aef02c0ef｜功能切片给已转换页面接线时保留原布局骨架，只换数据绑定和事件，不删掉重写｜读到：已有目标页面是全屏 Stack 底层加按 ViewModel 布尔状态切换的两套前景覆盖层；源布局 XML 以铺满全屏的 MapView 等视图为底层；写错：切片先删页面再整页重写：全屏 Stack 底层没了，改成常驻标题栏加灰底的 Column 和单一居中卡片，源端两种状态下的可见节点缺失
- rule-775d1e2d6f6d｜地图 SDK、key 或配置缺失接不上时，显示真实的未配置状态，不用静态图冒充地图｜读到：决策台账写「三方地图不迁 SDK 二进制，用平台定位与可验证的地图承载」「定位失败不写伪坐标」；目标工程没有地图组件依赖、key 或 client_id 配置；写错：地图区在配置缺失时仍显示白底 Blank 加 marker Image 的假地图态，或写了伪坐标
- rule-764eaf0b9dd8｜Swiper/Tabs 预构建子页的原生地图不在 onReady 创建，隐藏时暂停、卸载才释放｜读到：页面除路由外还在宿主的 Swiper / Tabs 子页里被直接实例化（一次性预构建）；参考桥接把 MapView.onResume、MapView.onPause 和 MapView.onDestroy 分成激活、暂停、释放三个接口；写错：在 NavDestination 的 .onReady(…) 或 aboutToAppear 里创建原生地图；在 .onDisAppear(…) 里调完整释放（MapView.onDestroy），从不调用暂停/恢复
- rule-7743b67ac297｜地图服务层同时暴露初始化、暂停/恢复和完整释放，不以释放代替暂停｜读到：参考 SDK 桥接里激活 → MapView.onResume、暂停 → MapView.onPause、释放 → 注销创建回调并 MapView.onDestroy，是三个不同接口；写错：服务层只有初始化和完整释放两个方法，桥接层的激活/暂停（MapView.onResume / onPause）没有暴露给页面，页面消失时只能调释放
