# Markdown 渲染和自写的行内标记解析

agent 会看到什么：读到源端用 react-markdown / remark-gfm 这类库渲染 Markdown、规格要求不成对的标记按字面输出；产物里自写的行内解析按 indexOf('**') / indexOf('*') 分支产出粗体、斜体 Span

## 规矩

- rule-6e68036cbe17｜自写行内标记解析时，长分隔符未闭合要整段写入字面缓冲，不落进短分隔符分支｜读到：源端用 ReactMarkdown + remarkGfm（react-markdown、remark-gfm）渲染 Markdown；规格要求子集外或不成对的标记按字面文本输出、内容不丢失；写错：自写的行内解析里 `**`（或 `~~`、```）分支只在 indexOf('**', i + 2) 命中时产出粗体，未命中时没有字面回退，直接落进后面共享首字符的 `*` 分支
