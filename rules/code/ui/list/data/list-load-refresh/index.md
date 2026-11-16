# 列表页的加载入口和刷新状态

agent 会看到什么：源端 SwipeRefreshLayout 的 setOnRefreshListener / setRefreshing、列表进详情再返回；产物里 Refresh({ refreshing }) 和 .onRefreshing、aboutToAppear / onPageShow 里的加载调用，以及按 isLoading、errorMessage 分派的页面状态

## 规矩

- rule-34be9224d2ea｜Refresh.refreshing 绑定的状态会被事件置真时，onRefreshing 里先判断刷新是否已在运行｜读到：源端 SwipeRefreshLayout 同时有 setOnRefreshListener(…)（只响应用户下拉）和事件回调里的 setRefreshing(event.…)（只同步指示器）；写错：Refresh({ refreshing: $$状态 }) 的状态由运行态事件或菜单刷新置 true，同时 .onRefreshing(() => 刷新入口()) 无条件发起刷新
- rule-a5b52b7f72eb｜页面有 aboutToAppear 与 Refresh.onRefreshing 等多个加载入口时，调单例加载前加单飞｜写错：页面在 aboutToAppear 里调加载，又以 Refresh({ refreshing: true }) 为初值并在 .onRefreshing 里调加载（或 @Monitor 回调里再调），调用单例加载方法前没有在途标志或在途复用
- rule-3de446e454de｜列表页 push 去表单、保存后 back 回来时，加载放进 onPageShow，不只放 aboutToAppear｜读到：源端列表的新增、编辑都进独立的详情路由，返回后列表要显示变更（列表带下拉刷新 RefreshLayout）；写错：列表页只在 aboutToAppear() 里调加载，新增或编辑页保存后 router.back() 返回，列表没有任何重载
- rule-a9bb91122c50｜页面状态分派时已有内容优先于刷新错误，错误用提示条，加载用局部指示，不加全屏遮罩｜写错：页面里 `if (this.errorMessage.length > 0)` 优先、整块替换已有列表，或在 Refresh 外叠一层 `if (this.isLoading)` 的全屏遮罩，遮住其他分区
