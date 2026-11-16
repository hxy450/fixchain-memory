# 按朝向在代码里重排的 RelativeLayout 子控件

agent 会看到什么：读到源 Activity 按界面方向和系统朝向（getRotation、onConfigurationChanged）在代码里用 RelativeLayout.LayoutParams / setMargins 逐控件重排、按导航栏间隙加边距；产物里布局控制器产出的逐控件摆位和 margin 字段，以及按钮层固定百分比的 .position

## 规矩

- rule-54a14f832521｜布局控制器已产出逐控件摆位时，按钮层按摆位解算渲染，不用固定百分比 position｜读到：源 Activity 运行时按界面方向和系统朝向重排 RelativeLayout 子控件；目标布局状态里有控制器产出的逐控件摆位（边、沿边偏移、margin），注释写「按钮层消费」；写错：页面按钮层用固定百分比 .position({ x: 'NN%', y: 'NN%' }) 摆主控件列和面板，只取摆位状态里的按钮尺寸，不按逐控件摆位渲染
- rule-059298f9cea6｜源端按导航栏间隙给控件加边距时，布局控制器把三种朝向的间隙写进摆位 margin｜读到：源布局代码按导航栏间隙（竖屏、横屏、反向横屏三个值）逐控件 setMargins；规格验收项写首尾按钮用导航间隙占位、主控件按导航间隙内缩、对侧归零；写错：目标布局控制器只加了隐私指示一类的其他间隙，摆位的 `margin*` 字段里没有导航栏间隙，也没登记前向引用
