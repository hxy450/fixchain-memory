# 被搬页面归到哪个模块

agent 会看到什么：读到被搬的页面 import 了某业务模块的 ViewModel 或 Service，入口却是另一模块列表页的条目跳转；产物里页面按 import 移进那个模块，同一业务对象的列表、新增、详情页和 Model、Service、ViewModel 分在两个模块

## 规矩

- rule-d14bfba397f3｜搬页面时按入口调用方和业务定去向，不按它 import 了哪个模块的 ViewModel｜读到：被搬的页面 import 了某个业务模块的 ViewModel 或 Service，但它的入口是另一模块里列表页的条目跳转；写错：页面按「import 了哪个模块的 ViewModel」被移进那个模块，同一业务对象的列表、新增页和详情、编辑页及 Model、Service、ViewModel 分在两个模块
