# android.util.Patterns 的平台正则

agent 会看到什么：读过的源码 import android.util.Patterns，用 matches(Patterns.WEB_URL.pattern()) 或 Patterns.EMAIL_ADDRESS 校验输入；交回的代码里自拟的「等价」RegExp 丢了分支或没有 ^…$ 全串锚定

## 规矩

- rule-86be3e96b1c7｜源端用 Patterns.WEB_URL 整串匹配时，目标逐段移植公开定义并 ^…$ 锚定｜读到：输入用 String.matches(Patterns.WEB_URL.pattern()) 或 Patterns.EMAIL_ADDRESS 这类平台正则常量校验；写错：目标写自拟的「等价」正则（如主机只收字母 TLD 或 localhost），丢了 IP_ADDRESS_STRING 分支，或没有 ^…$ 锚定
- rule-b584eb6fd6e9｜复用工程里已有的「等价」判定函数前，先用自身规格的正例和反例核对｜读到：自身规格契约写了正反例（如「普通句子假」、Patterns.WEB_URL 的 matches() 整串匹配），工程里别的页面已有注释为「等价」的同类判定函数；写错：直接 `import` 复用那个函数并把对应 AC 标为已满足，没用反例核对（那个函数的正则只锚 ^）
