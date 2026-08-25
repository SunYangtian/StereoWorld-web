# Team Pages

团队主页 + 项目宣传页。纯静态，无构建步骤，无依赖。

**预览**：双击 `index.html`。
（或者起个服务器：`python -m http.server 8000` 然后开 http://localhost:8000）

## 页面结构

```
index.html               首页：团队主张 + 各栏目前 3 条
index.html?s=research    Research 列表：全部研究项目
index.html?s=blog        Blog 列表：全部文章
index.html?p=<id>        某个项目/文章的完整页面
```

header 里的 Research / Blog 进列表页，点列表里的卡片进详情页。
在详情页里，header 右侧的切换器可以直接切换同栏目的其他条目。

改内容只动 `data/projects.js` 一个文件。

---

## 中英双语怎么写

**任何给人看的字段都可以写成 `{ zh: "…", en: "…" }`：**

```js
title: { zh: "我们的方法", en: "Our Method" },
```

**不需要翻译的直接写字符串**，两种语言共用 —— 人名、会议名、数字、代码、URL：

```js
venue: "CVPR 2026",
bibtex: "@inproceedings{...}",
```

**只写一种也行**，另一种语言会自动用你写的那个，不会变空白：

```js
subtitle: { zh: "还没来得及翻译" },    // 英文模式下也显示中文
```

右上角那个「中 / EN」按钮切换语言，选择会记住。首次访问按浏览器语言自动判断。

> 加内容时建议先把中文写全，英文可以后补 —— 缺英文不会让页面出错。

---

## 加一个新研究项目

往 `data/projects.js` 的 `projects` 数组里加一个对象：

```js
{
  id: "my-new-project",              // URL 变成 index.html?p=my-new-project，定了别改
  title: {                           // *星号* 里的词会高亮成品牌色
    zh: "我的论文：一个*很酷的方法*",
    en: "My Paper: A *Cool Method* for Something",
  },
  short: "My Project",               // 列表卡片和切换器里的短名
  subtitle: {
    zh: "一句话说清这个方法做什么、好在哪。",
    en: "One line on what it does and why it is better.",
  },
  thumb: "assets/my-project/thumb.jpg",   // 列表卡片缩略图，16:10 最好

  // 会议信息：标题下方一行居中排版。没中会议就把这几行删掉，整块自动消失。
  venue: "CVPR 2026",                // 会议名不用翻译
  badge: { zh: "口头报告", en: "Oral Presentation" },   // 荣誉，可省略
  venueNote: "",                     // 副标注，如 "(ACM TOG)"，可省略
  date: "2026-06",

  authors: [
    { name: { zh: "张三", en: "San Zhang" }, url: "https://...", affil: [1], note: "*" },
    { name: { zh: "李四", en: "Si Li" },     url: "https://...", affil: [1, 2] },
  ],
  affiliations: [                    // affil 里的 1 对应第一个
    { zh: "某某实验室", en: "Some Lab" },
    { zh: "某某大学",   en: "Some University" },
  ],
  authorNotes: { zh: "* 同等贡献", en: "* Equal contribution" },

  links: [
    { label: { zh: "论文", en: "Paper" }, href: "https://...", icon: "paper" },
    { label: "arXiv",                     href: "https://...", icon: "arxiv" },
    { label: { zh: "代码", en: "Code" },  href: "https://...", icon: "code"  },
  ],

  teaser: { src: "assets/my-project/teaser.mp4",   // .mp4/.webm 自动识别成视频
            poster: "assets/my-project/teaser.jpg",
            caption: { zh: "这段视频在展示什么。", en: "What this clip shows." } },

  highlights: [                      // 顶部数字亮点，2~4 个最好看；不要就删掉
    { value: "12×",  label: { zh: "推理加速", en: "faster" } },
    { value: "+3.4", label: "PSNR" },
  ],

  abstract: { zh: "摘要正文……", en: "Abstract text…" },
  sections: [ /* 见下 */ ],
  bibtex: "@inproceedings{...}",     // 代码，不分语言
  acknowledgements: { zh: "致谢……", en: "Acknowledgements…" },
}
```

数组顺序 = 列表页顺序，想置顶就往前挪。素材放 `assets/my-project/` 下。

## 加一篇 Blog

往 `posts` 数组里加，结构一样但字段更少：

```js
{
  id: "post-my-note",                // 不能和 projects 里的 id 重名
  title: { zh: "标题", en: "Title" },
  short: { zh: "短标题", en: "Short title" },
  subtitle: { zh: "一句话导语。", en: "One-line lede." },
  date: "2026-08",
  readingTime: { zh: "8 分钟", en: "8 min read" },
  author: { zh: "张三", en: "San Zhang" },   // 博客用单个作者，不用 authors[]
  thumb: "assets/posts/my-note.jpg",
  abstract: { zh: "导语段落。", en: "Intro paragraph." },
  sections: [ /* 和项目一样 */ ],
}
```

## sections 能放什么

`sections` 是有序数组，页面按这个顺序渲染。`type` 决定长什么样。
下面为了看清结构用了简写，**每个文字字段都能写成 `{zh, en}`**：

```js
// 纯文字
{ type: "text", id: "limitations",
  title: { zh: "局限", en: "Limitations" },
  body: { zh: "文字，可以写 <b>HTML</b>", en: "Text, <b>HTML</b> allowed" } }

// 图 / 视频
{ type: "figure", id: "method",
  eyebrow: { zh: "方法", en: "How it works" },
  title: { zh: "方法", en: "Method" },
  body: { zh: "方法说明段落", en: "Method paragraph" },
  src: "assets/x/pipeline.png",
  caption: { zh: "图 1：整体框架。", en: "Figure 1: architecture." } }

// 网格画廊，点开进灯箱
{ type: "gallery", id: "results", title: { zh: "更多结果", en: "More Results" },
  columns: 3,
  items: [ { src: "assets/x/a.jpg", caption: { zh: "案例 A", en: "Case A" } },
           { src: "assets/x/b.mp4", caption: { zh: "案例 B", en: "Case B" } } ] }

// 拖动滑块前后对比
{ type: "compare", id: "comparison", title: { zh: "对比", en: "Comparison" },
  before: { src: "assets/x/base.jpg", label: { zh: "基线", en: "Baseline" } },
  after:  { src: "assets/x/ours.jpg", label: { zh: "我们的", en: "Ours" } } }

// 数据表：每个单元格都能单独双语，数字列直接写字符串
{ type: "table", id: "quant", title: { zh: "定量结果", en: "Quantitative Results" },
  columns: [ { zh: "方法", en: "Method" }, "PSNR ↑", { zh: "耗时 ↓", en: "Time ↓" } ],
  rows: [ [ { zh: "基线", en: "Baseline" }, "24.1", "3.2" ],
          [ { zh: "我们的方法", en: "Ours" }, "29.7", "0.26" ] ],
  highlightRows: [1],              // 加粗第 2 行（从 0 数），一般是我们的方法
  footnote: { zh: "同一测试集、同一硬件。", en: "Same test set and hardware." } }

// 卖点卡片
{ type: "features", id: "highlights", title: { zh: "亮点", en: "What's New" },
  items: [ { title: { zh: "卖点一", en: "First point" },
             body: { zh: "一句话", en: "One line" }, icon: "spark" } ] }

// 编号步骤，适合放安装/运行命令
{ type: "steps", id: "usage", title: { zh: "快速开始", en: "Get Started" },
  items: [ { title: { zh: "安装", en: "Install" },
             body: "<code>pip install -e .</code>" } ] }   // 命令不用翻译
```

有 `title` 的 section 会自动出现在吸顶的章节导航里。
`id` 就是锚点，`index.html?p=my-project#results` 可以直接分享到某一节。

## 可用图标名

`links[].icon` 和 `features` 的 `icon` 从这里选：

`paper` `arxiv` `code` `github` `video` `demo` `hf` `data` `twitter` `link`
`spark` `bolt` `check`

写错了不会报错，会退回成通用链接图标。要加新图标见 `js/app.js` 顶部的 `ICONS`。

## 改团队信息和首页文案

`data/projects.js` 顶部三段（都支持 `{zh, en}`）：

- `site` — team name、logo、页脚链接和联系方式
- `home` — 首页那句大标题和简介（`*星号*` 同样能高亮）
- `nav` — 栏目名和列表页说明文字。目前支持 `research` 和 `blog` 两个 `key`

## 改界面文案

按钮、提示这类不属于内容的字（「查看项目」「阅读全文」「复制」等）在
`js/app.js` 顶部的 `UI` 常量里，`zh` 和 `en` 各一份，改那里即可。

## 换配色

`css/style.css` 最上面 `:root` 里这几行：

```css
--brand:  #5b4bdb;   /* 主色：链接、标题强调、进度条 */
--accent: #0fb5a6;   /* 副色：hero 环境光、复制成功态 */
```

其余颜色都是从这两个推导出来的，改完深浅两套主题一起变。

整体走克制路线：不用渐变填色、不用彩色标签、hover 不做位移动效。
加新样式时建议跟着这个基调，细节见 [CLAUDE.md](CLAUDE.md)。

## 素材建议

- 图片先过 [TinyPNG](https://tinypng.com/) 再放进来
- 视频用 H.264 mp4，控制在几 MB；teaser 视频记得给 `poster`
- teaser 用 16:9，列表缩略图用 16:10 左右比较整齐

## 部署

推到 GitHub → Settings → Pages → 选分支和根目录。或者丢到任意静态托管上。

分享时用 `https://your-site/?p=my-new-project` 直达具体项目。

注意：**语言不在 URL 里**，切语言只记在本地。所以分享出去的链接，对方会按他自己
浏览器的语言偏好打开。如果需要「发中文链接给中文读者」这种能力，跟我说，要改路由。

## 自带的东西

中英双语切换（记住选择，首次按浏览器语言判断）、深浅色切换（跟随系统，右上角可手动
切）、阅读进度条、章节吸顶导航、项目切换器、图片灯箱、前后对比滑块、BibTeX 一键复制、
键盘可达、`prefers-reduced-motion` 支持、打印样式、每个页面独立的 SEO/OG meta。
