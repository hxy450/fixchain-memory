# 页面状态与数据流

读到 ViewModel、LiveData / StateFlow、remember、data class copy、Activity 实例字段和 static 字段，规格里写状态契约、状态接口表（@Local）、复位和数据流时

## 触发族

- [ViewModel 里请求前补齐和列表组装的步骤](viewmodel-assembly/index.md)（3 条）：读到 ViewModel 在发请求前 launch 按 ID 查本地库（Dao @Query）回填参数，或在 init 里组装列表（add(0, …) 插首项、去重），容器按持久化选中项 setCurrentItem；规格的数据流、跨 feature 契约、对接点和 AC 没写这一步，或声明「不认领」「仅消费选择对象」
- [ViewModel 的状态字段和格式化字段](viewmodel-state-fields/index.md)（2 条）：读到 ViewModel 用布尔状态切换覆盖层、数组常量当 Tab 文案，或用返回 LiveData<String> 的 getter 给文案模板 "${x}…" 插值；页面规格只是通用模板，状态契约只写原始数值字段
- [Activity 实例字段和 static 字段的作用域](activity-field-scope/index.md)（2 条）：读到源端状态分散在类 static 字段、Activity / 宿主 View 的实例字段和每局新建对象的字段里；规格的状态管理节并成一个「实例态」列表，服务层写成单例或「重置全局态」
- [remember 持有、由焦点等框架事件驱动的页面状态](remember-ui-state/index.md)（1 条）：读到源页面状态用 remember {}（不是 rememberSaveable）持有，其中 focused 等字段由 onFocusChanged 这类框架事件驱动；规格的复位方案只写「重新 new 状态对象」，把 TextInput.onFocus / onBlur 无条件映射到业务 focused
- [整体替换的列表和订阅队列（copy、StateFlow.update）](immutable-list-observation/index.md)（1 条）：读到源端用 data class copy 替换列表项、StateFlow.update { list + item } 生成新列表、宿主订阅队列；规格把「map + copy」「尾拼接」当照搬写法，没写 ArkUI 端行内字段变化靠什么被观察、队列消费方靠什么触发
- [每局重开的复位 AC](restart-reset-ac/index.md)（1 条）：源端 Java 类里带初始化器的 static 字段、宿主 View / Activity 的实例字段，和每局重开函数体里实际赋值的字段；规格里重开函数的复位 AC
- [状态接口表里与通用属性同名的成员](local-state-reserved-names/index.md)（1 条）：读到源端事件或模型字段叫 position、duration 之类（如播放进度事件的 position），要转成组件状态；规格的「@Local 变量」状态接口表直接沿用源字段名，写出 position / width / height / id / visibility / enabled / zIndex / opacity 这类与通用属性同名的成员
- [§状态管理里新拟的 AppStorageV2 / PersistenceV2 键名](appstorage-key-names/index.md)（1 条）：读到源端只有成员字段、回调或单例状态，没有现成的存储键，规格模板的 §状态管理 要求写出 AppStorageV2 / @Local 键名和类型；交回的规格里新拟的键带「.」或「-」写成「领域.字段」式命名空间，或只写了分组的逻辑名
