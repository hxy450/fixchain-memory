# 派工里按编号点名的迁移陷阱

agent 会看到什么：切片里有横向滚动的 Tab 行或标签条（PrimaryScrollableTabRow、horizontalScroll）、贴合内容的选中指示器（matchContentSize、fillMaxSize）；派工说明按编号列须遵守的迁移陷阱，却漏了对应的条目（P-22、P-20）

## 规矩

- rule-c52bab1a4076｜派工点名迁移陷阱时，涉及横向滚动行或覆盖式选中态的切片同时点名定高和百分比子层两条｜读到：切片里有横向滚动的 Tab 行或标签条（PrimaryScrollableTabRow、horizontalScroll），或贴合内容的选中指示器（matchContentSize、fillMaxSize）；写错：派工说明按编号列出须遵守的迁移陷阱，却没有点名“横向滚动容器须显式定高”（P-22）和“不用 100% 子层填父级、描边画在容器自身”（P-20）这两条
