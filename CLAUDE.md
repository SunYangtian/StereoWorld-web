# CLAUDE.md — project_page

团队项目宣传网页。纯静态：无构建、无依赖、无框架。双击 `index.html` 即可预览。

## 目录结构

```
project_page/
├── index.html            # 唯一页面：只有骨架 + SEO meta，内容全靠 JS 注入
├── css/style.css         # 全部样式。分 10 段，每段有 /* === N. NAME === */ 分隔注释
├── js/app.js             # 全部逻辑。IIFE，无导出，无依赖
├── data/projects.js       # ★ 内容数据（window.SITE_DATA）—— 日常只改这个文件
├── assets/
│   ├── favicon.svg
│   └── placeholder/*.svg # 占位素材，真素材进来后应逐步删除
└── README.md             # 面向使用者的替换/部署说明
```

## 核心约定

**内容与呈现严格分离。** 加项目、改文案、换图 → 只动 `data/projects.js`。
改版式、配色、动效 → 只动 `css/style.css`。加新的 section 类型 → 动 `js/app.js`。
不要把项目文案写进 `index.html`，那里只留骨架和无 JS 时的兜底文本。

**数据来源双通道。** `js/app.js` 的 `loadData()` 优先读 `window.SITE_DATA`（由
`data/projects.js` 挂上），失败才 `fetch('data/projects.json')`。用 JS 文件的理由是
`file://` 协议下 `fetch` 会被浏览器拦掉，而团队大概率会直接双击 HTML 预览。
如果以后换成 JSON，记得同时删掉 `index.html` 里那行 `<script src="data/projects.js">`。

**三种视图，全靠 query string 区分**，没有真实子页面（都是同一个 index.html）：

| URL | view | 内容 |
|---|---|---|
| `index.html` | `home` | 团队主张 + 每个栏目前 3 条预览 |
| `index.html?s=research` | `list` | 该栏目的全部条目 |
| `index.html?p=<id>` | `detail` | 完整项目/文章主页 |

`parseRoute()` 解析 URL → `render(data, route)` 分发到 `renderHomeSections` /
`renderList` / `renderDetail`。`history.pushState` + `popstate` 处理前进后退。
未知的 `?s=` 或 `?p=` 都回落到 home，不报错。
**`id` 一旦发出去就不要改**，改了等于换 URL。

栏目由 `data.nav[]` 定义，`key` 决定条目来源：`research` → `projects[]`，
`blog` → `posts[]`（见 `itemsOf()`）。加第三个栏目要同时改 `itemsOf()`。

项目切换器只在 detail 视图出现，且只列**同栏目**的条目 —— 跨栏目跳转走 header
主导航。列表页会 `switcher.hidden = true`。

## 中英双语（i18n）

**数据里任何面向读者的字段都可以写成 `{ zh: "中文", en: "English" }`**，也可以直接写
一个字符串 —— 那就两种语言共用（人名、会议名、数字、代码、URL 都适合这样）。
某个语言缺失会自动回落到另一个，不会渲染出空白或 `undefined`。

两个取值函数，**别绕过它们直接读数据字段**：

- `t(v)` —— 取内容字段。`t({zh,en})` 按当前语言返回；传字符串/数字原样返回；
  传不含 `zh`/`en` 键的对象（比如 `{src, poster}`）也原样返回，不会误伤结构化数据。
- `ui(key, ...args)` —— 取界面文案（按钮、提示、"查看全部 N 项"这类）。
  文案表在 `UI` 常量里，`zh` 和 `en` 两份必须同时加，漏了会回落到中文。
- `plain(v)` —— `t()` 之后再剥掉标题里的 `*` 强调标记，用于 meta、`aria-label`、
  切换器按钮这些纯文本场合。

**改动时最容易犯的三个错：**

1. **变量名 `t` 会遮蔽 i18n 函数。** 历史上 `renderHero` 用 `const t = el('figure')`、
   `table()` 用 `const t = el('table')`、`initLightbox` 用 `forEach((t) => ...)`，
   现在都改名了（`fig` / `table` / `tile`）。写新代码不要再用 `t` 当局部变量名。
2. **新增渲染分支忘了套 `t()`。** 任何 `esc(x)` / `rich(x)` 里的 `x` 只要来自数据，
   就必须是 `t(x)`。忘了的话中文模式下会显示成 `[object Object]`。
3. **界面文案硬编码中文。** 新加的按钮文字、空状态提示走 `ui()`，别直接写字符串。

语言状态存在 `localStorage['pp-lang']`，首次访问按 `navigator.language` 猜。
切语言的实现是 `initLang(rerender)`：改 `LANG` → 重画 header/页脚的静态文案和
`aria-label` → 调 `rerender()` 原地重渲染当前视图。**不改 URL、不跳回顶部**
（所以语言不体现在链接里，分享出去的链接会用对方自己的语言偏好打开）。

`document.documentElement.lang` 会跟着切成 `zh-CN` / `en`。
`index.html` 里那些静态 `aria-label` 和 skip-link 文字是无 JS 时的兜底值，
运行时由 `initLang()` 的 `paint()` 覆盖 —— 加新的静态文案记得往 `paint()` 里补一行。

## 数据契约（data/projects.js）

下面标 `L` 的字段可以写 `{zh, en}`（也可以写纯字符串两语共用）；
没标的是 URL、id、枚举值这类不该翻译的。

```js
window.SITE_DATA = {
  site: {
    team L, teamShort L, tagline L, logo,
    links: [{ label L, href, icon }],
    footer: { note L, credit L, contact },
  },
  home: { title L, intro L },                    // 首页 hero，title 支持 *星号* 强调
  nav: [{ key, label L, title L, intro L }],     // key 必须是 research | blog
  posts: [ ... ],                                // Blog 条目，结构同 projects
  projects: [{
    id, date, thumb, keywords: [L],
    title L, short L, subtitle L,
    venue L, badge L, venueNote L,               // venue 一般不用翻，写字符串即可
    authors: [{ name L, url, affil: [1,2], note L }],
    affiliations: [L],         // 数组下标+1 对应 authors[].affil 里的数字
    authorNotes L,
    links: [{ label L, href, icon }],
    teaser: { src, poster, alt L, caption L },
    highlights: [{ value L, label L }],
    abstract L,
    sections: [...],           // 有序，见下
    bibtex,                    // 代码，不分语言
    acknowledgements L,
  }]
}
```

除 `id` / `title` 外几乎所有字段都可省略，渲染函数都做了空值判断。
数组顺序 = 列表页和切换器里的顺序，想置顶就往前挪（没有 `featured` 字段了）。
`projects[]` 和 `posts[]` 的 `id` 不能重名 —— 两者共用 `?p=` 命名空间。

Blog 条目比项目少几个字段：用 `author`（单个人名）和 `readingTime` 代替
`authors[]` / `affiliations[]`，一般也不写 `venue` 和 `bibtex`。

表格的 `columns[]` 和 `rows[][]` 里**每个单元格**都能单独写 `{zh, en}`，
数字列直接写字符串就行 —— 见 `data/projects.js` 里 project-alpha 的表格。

### 标题强调

`title` 里用 `*星号*` 包住的词会被 `titleHTML()` 渲染成 `<em>`，显示为品牌色。
其余部分照常转义。一个标题里强调一处最好看，两处以上会花。
`short` 和各处 meta 会把星号剥掉，所以不用为切换器另写一份标题。

### section 类型

`js/app.js` 里的 `SECTION_RENDERERS` 是一张 `type -> 渲染函数` 的表。已支持：

| type | 必需字段 | 说明 |
|---|---|---|
| `text` | `body` | 纯文字段落 |
| `figure` | `src` | 图/视频 + caption，`video` 是它的别名 |
| `gallery` | `items[]` | 网格，点开进灯箱，`columns: 2\|3\|4` |
| `compare` | `before`, `after` | 拖动滑块前后对比 |
| `table` | `columns[]`, `rows[]` | `highlightRows: [3]` 高亮我们的方法（0-based） |
| `features` | `items[]` | 卖点卡片，`icon` 见下 |
| `steps` | `items[]` | 编号步骤，适合放安装/运行命令 |

共有的可选字段：`id`（锚点，也用于 TOC 链接）、`eyebrow`、`title`、`body`、`caption`
—— 除 `id` 外都可以写 `{zh, en}`。有 `title` 的 section 才会进吸顶 TOC。

**加新 type 的做法**：在 `SECTION_RENDERERS` 里加一个 `键(s) { return 节点 }`，
样式加到 `css/style.css` 的第 7 段 COMPONENTS。别在 `renderSection` 里写 if/else 分支。
未知 `type` 会 `console.warn` 并跳过，不会整页崩。
**新 renderer 里所有来自数据的字段记得套 `t()`**，界面文字用 `ui()`。

### 图标

`js/app.js` 顶部 `ICONS` 是内联 SVG 字典（无外部图标库）。现有 key：
`paper arxiv code github video demo hf data twitter link spark bolt check copy caret close slider zoom back arrow sun moon`。
`links[].icon` 和 `features.items[].icon` 引用这些 key，不认识的 key 回退到 `link`。
加图标就往 `ICONS` 里加一条，viewBox 统一 `0 0 24 24`。

### 媒体

`renderMedia()` 按扩展名判断：`.mp4/.webm/.mov/.m4v` → `<video>`（muted+loop+playsinline，
自动播放），其他 → `<img loading="lazy">`。所以数据里写 `src` 就行，不用声明是图是视频。
`prefers-reduced-motion` 下自动关掉 autoplay 并显示控制条。

## 样式系统（css/style.css）

所有设计决策都在第 1 段 TOKENS 的 `:root` 里。**换主题只需要改「品牌色」那几行**
（`--brand` `--brand-2` `--accent`），其余色值用 `color-mix()` 从它们推导。

**整体基调是克制**（师兄反馈过第一版"有点幼稚"）。当前的取舍，改动时请守住：

- **不用渐变填色**。全站只剩顶部阅读进度条一处用渐变，其余（标题强调、数字、
  图标、按钮、表格高亮）全是纯色。渐变字在学术页面上显轻浮。
- **不用彩色色块**。会议信息、TOC 当前项、表格高亮行都靠字重 + 极淡底色 +
  发丝线，不用品牌色胶囊。
- **不做 hover 上浮**。卡片、缩略图、按钮的 hover 只换边框色或透明度，
  不 `translateY`、不 `scale`、不加重阴影。
- **边框用 1px `border` 配 `--border`**，比大范围阴影干净。`--shadow-3/4` 现在只有
  切换器菜单和灯箱在用。
- BibTeX 是**浅底**代码块，不是深色终端风 —— 这是师兄第一条具体反馈。
- 字号用 `--step--2` … `--step-4` 的 `clamp()` 阶梯，不要写死 px。

深色模式：`@media (prefers-color-scheme: dark)` + `[data-theme="dark"]` 两处同样的
token 覆盖。**改了一处必须同步另一处** —— 这是当前最容易漏的地方。
（`:root:not([data-theme="light"])` 的写法是为了让手动选浅色能压过系统深色。）

hero 三层背景：`.hero__aurora`（一团静态淡色晕，不动画）/ `.hero__grid`（网格，
向下淡出）/ `.hero__noise`（内联 SVG 噪点）。都是 `z-index: -1/-2` +
`pointer-events: none`。home / list / detail 三种视图共用，由 `heroBackdrop()` 插入。

header 铺满整个视口宽度（`.header-inner` 不套 `.wrap`，自带 `padding-inline`），
正文仍受 `--page` 约束。

## JS 结构（js/app.js）

单个 IIFE，自上而下：helpers → ICONS → loadData → 渲染函数 →
SECTION_RENDERERS → 首页/列表渲染 → 交互 init* → 路由 → `render()` → `boot()`。

`render(data, route, opts)` 是唯一入口。`route` 由 `parseRoute()` 产出，形如
`{view: 'detail', item, navKey}`。它按 view 分发，然后统一重绑组件级交互。
所有内部跳转都走 `go(route)`，它等于 `render(..., {pushState: true})`。

导航链接都是真的 `<a href>`（Cmd/Ctrl+点击能开新标签、能右键复制链接），
同时 `preventDefault()` 走前端路由。加新的跳转入口时请保持这个双通道。

**重复绑定的坑**：`render()` 每次调用都会重新执行 `init*`。挂在 `document` /
`window` 上的监听必须用模块级 `bound` 标志位守住（现有 `lightboxBound`、
`switcherBound`），否则切几次项目就叠出几层监听。绑在新建 DOM 上的监听无所谓。

**转义**：`esc()` 用于所有从数据来的纯文本；`rich()` 是恒等函数，只用于我们
明确允许写 HTML 的字段（`body` / `caption` / `subtitle` / `step.body`）。
这是有意的口子，方便在文案里写 `<b>` `<code>` `<a>`。数据是我们自己写的，不是用户输入。

## 无障碍与性能底线

改动时不要破坏这些：`.skip-link`、切换器的 `aria-expanded` / `role="listbox"` /
`aria-current`、灯箱的 `role="dialog"` + Esc 关闭 + 焦点归还、对比滑块背后真实的
`<input type="range">`（键盘可操作）、表格的 `scope` 属性、
`prefers-reduced-motion` 分支、`:focus-visible` 样式、
`<html lang>` 跟随语言切换（屏幕阅读器靠它选发音）。

素材必须压缩后再进 `assets/`：图片过 TinyPNG，视频建议 H.264 mp4 且控制在几 MB 内，
teaser 视频给 `poster`。图片默认 `loading="lazy"`。

## 部署

任意静态托管。GitHub Pages：推到仓库 → Settings → Pages → 选分支根目录。
分享链接带上 `?p=<id>` 指向具体项目。

## 待办 / 已知取舍

- **全部内容都是占位素材**，`assets/placeholder/` 和 `data/projects.js` 里的
  team name、作者、链接都要替换。`site.links`、`footer.contact` 还是示例 URL。
- **没有在浏览器里视觉验证过。** 到目前为止的检查都是静态的（`node --check`、
  CSS 括号平衡、CSS 变量收支、class/id 交叉引用、路由分发和 i18n 回落的 headless
  单测）。视觉效果需要人工过目。
- **语言不进 URL。** 切语言只改 `localStorage` 和内存状态，分享出去的链接会按对方
  自己的语言偏好打开。如果以后需要「发中文链接给中文读者」，得加 `?lang=zh` 到
  `parseRoute()` / `urlFor` 里，并在 `updateMeta()` 补 `hreflang` 交替链接。
- 目前没有生成静态子页（`/research/xxx.html`）。若之后需要更好的 SEO 和 arXiv 引用
  友好度，可以写个脚本从 `SITE_DATA` 预渲染，`updateMeta()` 里已经按 view 分好了
  title/description/og:image/canonical，预渲染时可以直接复用。
  注意双语站预渲染要出两套页面（`/zh/...` 和 `/en/...`）才有 SEO 意义。
- Google Fonts 是外链。内网/离线环境要自托管字体，删 `index.html` 里那三行 link
  即可回落到系统字体栈。
- CSS 用了 `color-mix()`（Chrome 111+ / Safari 16.2+ / Firefox 113+）和 `:has()`。
  需要兼容更老的浏览器就得把这些换成静态色值。
- 栏目目前硬编码为 `research` / `blog` 两个 key（在 `itemsOf()` 里）。加第三个栏目
  要同时改数据的 `nav[]` 和这个函数。

## 参考

设计基调参考了这几个页面的做法（都不用彩色胶囊标 venue，都很克制）：
[Nerfies](https://nerfies.github.io/)、[DreamFusion](https://dreamfusion3d.github.io/)、
[3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)。
师兄还给过 [qwen.ai/research](https://qwen.ai/research) 和
[technology.robbyant.com](https://technology.robbyant.com/) 两个例子（都是 SPA，
抓不到源码，是照着"整宽 header + 栏目列表 + 克制排版"的描述做的）。
