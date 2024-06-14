EDITOR = """
var codeBackgroundColor = "background-color: #414141;";
var fontFamily =
'font-family: "Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue", "pingfang sc", "microsoft yahei", sans-serif;';
if (document.getElementById("fields") === null) {
    // breaking changes in version 2.1.54
    var fields = document.getElementsByClassName("fields")[0].children;
    for (i = 0; i < 5; i++) {
        var shadowRoot = fields[i].children[0].children[2].children[0].children[0].shadowRoot;
        if (shadowRoot === null){
            continue;
        }
        if (i === 4) {
            // code
            shadowRoot.children[2].style = fontFamily + codeBackgroundColor;
        } else {
            shadowRoot.children[2].style = fontFamily;
        }
    }
} else {
    var fields = document.getElementById("fields").children;
    for (i = 0; i < 5; i++) {
        if (i === 4) {
            // code
            fields[i].children[1].shadowRoot.children[2].style =
            fontFamily + codeBackgroundColor;
        } else {
            fields[i].children[1].shadowRoot.children[2].style = fontFamily;
        }
    }
}

"""

FRONT = """
<div class="h1 red redleft">
  Question
  <span id="time"> </span>
</div>

<div class="h2 redleft wordwrap">{{Question}}</div>
"""

BACK = """
{{FrontSide}} {{#Tags}}
<head>
  <link rel="preload" href="_prism.css" as="style">
  <link rel="stylesheet" href="_prism.css">
</head>



<div class="h1 red redleft wordwrap">[Tags] {{Tags}}</div>
{{/Tags}} {{#Mindmap}}
<hr />
<div class="slide">
  <div class="h1 green greenleft">
    Mindmap
  </div>
  <div class="h2 greenleft">
    <svg id="mindmapgraph"></svg>
    <div id="mindmaptext" hidden>{{Mindmap}}</div>
  </div>
</div>
{{/Mindmap}} {{#Answer}}
<hr />
<div class="slide">
  <div class="h1 pink pinkleft">
    Answer
  </div>
  <div class="h2 pinkleft wordwrap">{{Answer}}</div>
</div>
{{/Answer}} {{#Detail}}
<hr />
<div class="slide">
  <div class="h1 purple purpleleft">
    Expand
  </div>
  <div class="h2 purpleleft wordwrap">{{hint:Detail}}</div>
</div>
{{/Detail}} 
{{#Code}}
<hr />
<div class="slide">
  <div class="h1 blue blueleft">
    Code
  </div>
  
  <pre class="language-js">
    <code >{{Code}}</code>
</pre>
</div>
{{/Code}}



<script>
const loadedResources = new Set();

const ResourceType = {
    js: 1,
    css: 2,
};

loadResource("_prism.js", "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js", ResourceType.js)
    .then(() => loadResource("_d3@6.js", "https://cdn.jsdelivr.net/npm/d3@6", ResourceType.js))
    .then(() => loadResource("_markmap-lib.js", "https://cdn.jsdelivr.net/npm/markmap-lib", ResourceType.js))
    .then(() => loadResource("_markmap-view.js", "https://cdn.jsdelivr.net/npm/markmap-view", ResourceType.js))
    .then(render)
    .catch(show);

function loadResource(path, altURL, resourceType) {
    if (loadedResources.has(altURL)) {
        return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
        const resource = resourceType === ResourceType.js ?
            Object.assign(document.createElement("script"), { src: altURL }) :
            Object.assign(document.createElement("link"), { rel: "stylesheet", type: "text/css", href: altURL });

        resource.onload = () => {
            loadedResources.add(altURL);
            resolve();
        };

        resource.onerror = reject;
        document.head.appendChild(resource);
    });
}


  function render() {
    mindmap("mindmaptext");
    show();
  }

  function show() {
    document.getElementById("mindmapgraph").style.visibility = "visible";
  }

  function mindmap(ID) {
    if (document.getElementById("mindmapgraph").children.length === 2) {
      // Already created graph, directly return
      return;
    }
    let text = escapeHTMLChars(document.getElementById(ID).innerHTML);
    const { Markmap, loadCSS, loadJS, Transformer } = window.markmap;
    var transformer = new Transformer();
    const { root, features } = transformer.transform(text);
    const { styles, scripts } = transformer.getUsedAssets(features);
    if (styles) loadCSS(styles);
    if (scripts) loadJS(scripts, { getMarkmap: () => window.markmap });
    Markmap.create("#mindmapgraph", null, root);
  }
  function escapeHTMLChars(str) {
    return str
      .replace(/<[\/]?pre[^>]*>/gi, "")
      .replace(/<br\s*[\/]?[^>]*>/gi, "\\n")
      .replace(/<br\s*[\/]?[^>]*>/gi, "\\n")
      .replace(/<[\/]?span[^>]*>/gi, "")
      .replace(/<ol[^>]*>/gi, "")
      .replace(/<\/ol[^>]*>/gi, "\\n")
      .replace(/<ul[^>]*>/gi, "")
      .replace(/<\/ul[^>]*>/gi, "\\n")
      .replace(/<div[^>]*>/gi, "")
      .replace(/<\/div[^>]*>/gi, "\\n")
      .replace(/<li[^>]*>/gi, "- ")
      .replace(/<\/li[^>]*>/gi, "\\n")
      .replace(/&nbsp;/gi, " ")
      .replace(/&tab;/gi, "	")
      .replace(/&gt;/gi, ">")
      .replace(/&lt;/gi, "<")
      .replace(/&amp;/gi, "&");
  }

    header = document.querySelector("#lang").classList.contains("language-py")
  if (document.querySelector("#lang").classList.contains("language-py") == true) {
    document.querySelector(".heading").innerHTML = '<div style="color: #ebcb8b;">Python</div>';
  } else if (document.querySelector("#lang").classList.contains("language-sh") == true) {
    document.querySelector(".heading").innerHTML = '<div style="color: #d08770">Bash</div>';
  } else if (document.querySelector("#lang").classList.contains("language-js") == true) {
    document.querySelector(".heading").innerHTML = '<div style="color: #bf616a">JavaScript</div>';
  } else {
    document.querySelector(".heading").innerHTML = '<div style="color: #bf616a">Please select a programming language in the language field!</div>';
  }
</script>
"""

CSS = """
  @font-face {
    font-family: "Cascadia Code";
    src: url("_CascadiaCode.ttf");
  }
  @font-face {
  font-family: "Josefin Sans";
  src: url("_JosefinSans-Regular.ttf");
}
  .card {
    font: 20px/30px ;
    background-color: white;
    text-align: left;
  }
  
  .h1 {
    font: 22px/22px ;
    padding: 0.3em 0em 0.3em 0.5em;
    font-family: "Josefin Sans","Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue",
      "pingfang sc", "microsoft yahei", sans-serif;
  }
  .h2 {
    font: 20px/30px ;
    padding: 0.3em 0em 0.3em 0.5em;
    font-family: "Josefin Sans","Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue",
      "pingfang sc", "microsoft yahei", sans-serif;
  }
  

.redleft {
  border-left: 3px solid #fd2b3b;
}
.blueleft {
  border-left: 3px solid #338eca;
}
.pinkleft {
  border-left: 3px solid #c11cad;
}
.greenleft {
  border-left: 3px solid #044c46;
}
.purpleleft {
  border-left: 3px solid #811d5e;
}

  .code {

    font-family: "Josefin Sans","Cascadia Code", "Consolas", Overpass, "GlowSansSC",
      "Helvetica Neue", "pingfang sc", "microsoft yahei", sans-serif;
  }
  
  .wordwrap {
    display: block;
    overflow-wrap: break-word;
  }

pre,
code {

  color: #fff;
  padding: 3px 5px;
  text-align: left;
  overflow-x: auto;
  white-space: pre-wrap !important;
  margin: 0 auto; 
}

.red {
  color: #fd2b3b;
}
.blue {
  color: #0c637f;
}
.green {
  color: #044c46;
}
.pink {
  color: #c11cad;
}
.purple {
  color: #594d9c;
}
  
  .redimg {
    background: url(_red-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .blueimg {
    background: url(_blue-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .pinkimg {
    background: url(_pink-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .greenimg {
    background: url(_green-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .purpleimg {
    background: url(_purple-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  
  .hint {
    color: #fff;
  }
  
  a {
    color: #7575ff;
  }
  img {
    max-width: 100%;
    vertical-align: middle;
  }
  .chrome img {
    max-width: 100%;
    vertical-align: middle;
  }
  ul,
  ol {
    margin-top: 0em;
  }
  ul li {
    margin-left: -0.9em;
  }
  i {
    padding: 0 3px 0 0;
  }
  u {
    text-decoration: none;
    background-color: #ffff75;
    border-bottom: 2px solid #ec6c4f;
  }
  hr {
    height: 1px;
    width: 100%;
    display: block;
    border: 0px solid #fff;
    margin: 5px 0px 10px 0px;
    background-color: #ccc;
  }
  
  #answer, #mindmapgraph {
      visibility: hidden;
  }

  #mindmapgraph{
    color: #fff;
    height: 50vh;
    width: 95vw;
  }
  
  .markmap-foreign {
    font: 16px/20px "Josefin Sans","Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue",
      "pingfang sc", "microsoft yahei", sans-serif;
  }

.fade-in {
  animation: fadein 0.5s;
}

@keyframes fadein {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

"""
