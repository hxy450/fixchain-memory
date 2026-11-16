# 页面 $r 引用的 element 资源键

agent 会看到什么：页面 .ets 里的 $r('app.float.…') / $r('app.color.…') / $r('app.string.…') 引用，和 resources/base/element/*.json 里追加的键；源布局同一容器写了几个方向的 padding / layout_margin 时常漏键

## 规矩

- rule-1488c67b70f5｜页面里的 $r 引用键都要在 element/*.json 有定义，按组件实际引用回对｜读到：源布局同一容器写了几个方向的内边距或外边距（android:paddingHorizontal、android:paddingTop、android:paddingBottom、layout_margin*），派工要求把 dp 值写成 $r 引用并只向共享 element/*_float.json 追加缺的键；写错：页面 .ets 里有 $r('app.float.…') / $r('app.color.…') / $r('app.string.…') 引用，resources/base/element/*.json 里却没有同名 name；追加的键清单是写组件前按源值预估的，漏了某个方向的值
- rule-9f4812a66331｜HAR 页面引用的资源名不在本模块或已声明依赖里时，复制或迁入本模块｜读到：HAR 里的页面用 `$r('app.string.X')` / `$r('app.media.X')` 或 `getStringByNameSync('X')` 引用资源；写错：名字只定义在壳 HAP（products 下）、AppScope 或目标 HAR 的 oh-package.json5 没声明依赖的 feature 的 `resources` 里，目标 HAR 自己没有
