# 源 Fragment 入参到目标页面和组件的传递

agent 会看到什么：读到 Fragment 的 newInstance / setArguments / getArguments、requireArguments、navArgs，或宿主调 setter 注入参数；产物里子组件的 @Param / @Event、@Builder 插槽传没传参，以及目标页取参的代码

## 规矩

- rule-0e268d9169ef｜源 Fragment 用 newInstance 参数按实例持有键时，目标组件要有对应入参并在插槽里传入｜读到：Fragment.newInstance(参数) 把键写进 Bundle（setArguments），加载时从 getArguments() 取出再按它请求数据；写错：目标组件没有对应入参、用本地默认值；@Builder 插槽已按 ForEach 当前项传参，却调用无参 Builder，参数被丢掉
- rule-bba65b1188d3｜宿主挂载带 @Param/@Event 的子组件时逐项传入真实数据源，不新增无参 Builder｜读到：源 Fragment 由宿主注入参数（如宿主调用 setter 传入当前城市、id、经纬度）；目标子组件声明了 `@Param`（默认 '' 或 0，组件据此进入错误态）和 `@Event` 回调，宿主里有待替换的 `FWD-REF` 占位；写错：替换 `FWD-REF` 时新增一个无参 `@Builder`，里面直接调用子组件、不传任何 `@Param` 和 `@Event`，宿主只调用这个 Builder
- rule-b729e94bfefe｜@Entry 页经 router 进入且有必填入参时，在 aboutToAppear 里 getParams 取参｜读到：源 Fragment 用 requireArguments().getString(键) / navArgs() 取参，导航图目的地声明了 <argument>；写错：目标页登记进 main_pages.json、加了 @Entry，入参却是默认 '' 的普通成员，没有 router.getParams() 或 NavPathStack 取参代码，aboutToAppear 里 if (this.参数) 才加载
