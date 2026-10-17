# 控制门面的同步访问路径也要具备源端懒加载 getter 的回退来源

ID：`lesson-cd4a69e85ec59eabf5b9` · 版本：2 · 阶段：execute · 主题：[app/playback](index.md)

概要：门面同步路径也要有源懒加载 getter 的回退来源

信号：`seekTo`, `getPosition`, `getDuration`

## 何时使用

播放功能实现阶段，把源端控制器懒加载的当前媒体 getter 翻译为 seekTo、getPosition、getDuration 等同步路径时

## 适用情境

源 getter 在服务未运行时从偏好中保存的当前媒体 id 读库；目标服务实例只在起播后持有当前媒体，门面把 getter 做成异步方法、同步路径只读服务实例。

## 原因

同步路径只读服务实例时，冷启动未起服务前快退、定位都无效，规格中的“服务未运行”分支成为死代码。

## 做法

1. 为同步路径提供等价回退（如缓存页面已读出的偏好媒体并登记给控制器）；写完确认“服务未运行”分支的数据前提在冷启动时成立。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [不处理点击的全尺寸覆盖层显式设 Transparent 命中](../../ui/interaction/hit-testing/lesson-4a4f8d845a204ffa244b.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-8809177953953374a01e](../../../../store/cases/case-8809177953953374a01e/0f0a55473275f4a825fd345992d4bfd1b18db95262ea8d48b11572f0c0dfc81f.json) · 结论：rec-febe09b669, rec-e5d54a5792
  卡片版本：`0f0a55473275f4a825fd345992d4bfd1b18db95262ea8d48b11572f0c0dfc81f`
