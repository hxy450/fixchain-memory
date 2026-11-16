# 页面有 aboutToAppear 与 Refresh.onRefreshing 等多个加载入口时，调单例加载前加单飞

审的是：代码
触发（任一种）：
- 写错的样子：页面在 aboutToAppear 里调加载，又以 Refresh({ refreshing: true }) 为初值并在 .onRefreshing 里调加载（或 @Monitor 回调里再调），调用单例加载方法前没有在途标志或在途复用
- 写错的样子：下拉刷新回调里先调一次强制加载、再在 .then( 里调一次加载，同一次刷新发出两组请求
适用范围：ArkUI 页面把多个生命周期或事件入口接到同一个单例加载方法上时
做法：
- 列出页面所有会调加载的入口：aboutToAppear、Refresh 的 refreshing 初值与 .onRefreshing、@Monitor 回调等
- 调单例加载方法前加单飞：用一个在途标志（或保存在途的 Promise），在途时直接返回或复用，不再发起；在 finally 里清掉标志
- 下拉刷新回调只调一次加载方法并带强制刷新参数，不串联两次加载
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- refreshing: boolean：RefreshOptions.refreshing：组件当前是否处于刷新中，支持 $$ 双向绑定；文档写默认值 false（出处：鸿蒙 SDK 的 ets/component/refresh.d.ts，RefreshOptions.refreshing；ts-container-refresh.md，RefreshOptions对象说明）
- onRefreshing(callback: () => void): RefreshAttribute：进入刷新状态时触发的回调（出处：鸿蒙 SDK 的 ets/component/refresh.d.ts，RefreshAttribute.onRefreshing）
- 页面加单飞、刷新回调只调一次加载后，冷启动只剩一组请求：改后的效果（出处：卡里修好并验证过）
未核实：refreshing 初值为 true 时 ArkUI 是否会触发 onRefreshing：声明和文档只写「进入刷新状态时触发」，卡里也没有直接确认，只推断最可能是它
来源：1 张卡，1 个应用
- case-fa7bbda457517260efc4（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断；做法第 3 步 ← 诊断；取值 3 ← 诊断
