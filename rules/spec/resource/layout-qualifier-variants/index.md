# layout-* 限定符目录里的同名布局变体

agent 会看到什么：读到源 res 下 layout-sw600dp/、layout-land/、layout-w<N>dp/ 里有和主布局或 <include> 布局同名的 XML；页面 meta.json 的 layout_sources 和页面 spec 只列 base layout/ 下的文件，没写变体和断点语义

## 规矩

- rule-a4f8a6ffa6a3｜页面 layout_sources 的文件在 layout-* 下有同名变体时，meta 记下变体和断点语义｜读到：源 res 下有 layout-sw600dp/、layout-land/、layout-w<N>dp/ 等限定符目录，其中有和主布局或 <include> 布局同名的 XML；写错：页面 meta.json 的 layout_sources 只列 base layout/ 下的文件，没有同名变体，也没写断点语义；页面 spec 同样只列 base include
