# 源布局引用的 @drawable 位图资源

agent 会看到什么：读到源端 android:src、android:background、drawableStart、setImageResource 引用 @drawable/… 位图；产物里少了对应的 Image，换成名字不同的近似图标、SymbolGlyph($r('sys.symbol.…'))、Text('›') 字形或纯色，给替代图加 fillColor，或以 base/media 里没有为由判缺失

## 规矩

- rule-8aec841f44ae｜源布局的 src、drawableStart、装饰 ImageView 逐项对上目标同名 $r 引用，不按外观挑图｜读到：源布局里有 ImageView 的 android:src、TextView 的 android:drawableStart、只作装饰的 ImageView，引用的是 @drawable/…；写错：目标组件少了对应的 Image(...)（按钮前的图标、角上的装饰图、列表行图标没画，或行做成没绑图标的空列表），或用了名字不同、外观相近的通用图标 $r('app.media.…')
- rule-1a2eabd885ed｜源端用位图图标时，目标引用原名资源，不用近名图标、sys.symbol 或 Unicode 占位｜读到：规格的元素→资源表或源布局给出 @drawable/… 原图；写错：菜单里写的是 $r('app.media.…') 指向别的模块的同类近名图标（带 1 / 2 后缀等），而不是原名
- rule-482092df1a4f｜判 $r('app.media.…') 缺失前查遍各限定词目录，缺了登记，不用字形、纯色或近似图标顶替｜读到：源布局用 @drawable/… 引图（ImageView 的 android:src、TextView 的 android:drawableStart、容器的 android:background），图只在 drawable-xhdpi 这类密度目录里；写错：目标在该处写成 Text('›') 这类文字字形、只垫一个 .backgroundColor(...) 纯色，或换成名字不同的通用图标；理由是 base/media 里没有这张图
- rule-44d2b96abdd6｜目标位图颜色与源端不一致时，先查是不是用错了资源，不用 fillColor 给替代图着色｜读到：源端 ImageView 的 android:src 或背景用的位图本身带颜色；写错：目标的 Image($r('app.media.…')) 逐个加了 .fillColor('#…') 去模仿原图颜色
- rule-4bb43a65f70c｜公共组件的标题栏先复用现有导航组件；新建时返回入口用迁入的返回图标｜写错：公共组件里新写了一个 @Component 标题栏或导航条，而共享组件表把导航条这一行归到现有框架组件
- rule-b7efc4794e6e｜源端一个编码对多个资源、各处绑定不同字段时，目标按字段拆映射函数，每处按源端绑定选｜读到：源端枚举或映射为每个编码返回几个资源（如 Triple(背景图, 白色图标, 蓝色图标)），布局里不同位置绑定不同字段（data binding 的 viewModel 字段，选中与非选中取不同变体）；写错：目标只有一个映射函数，各处共用同一资源：背景图被当成小图标，或该用另一变体的地方用了同一个 $r('app.media.…')
- rule-0f5f360c99ab｜判定图标资源未迁移前，查 base 和各密度限定目录并按源端实际 drawable 名核对｜读到：源端 setImageResource(R.drawable.…) 或布局 XML 的 android:src 指向某个 drawable；写错：代码注释写「某资产未迁移」，回落到别的图标（$r('app.media.…') 换成普通态图标），判断依据只是看了 resources/base/media
