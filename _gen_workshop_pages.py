# Builds the three "Read more" pages (holiday-projects.html, kids-birthday-party.html, craft-together.html)
# from index.html's shared head/styles/header/footer, using one compact product-page layout.
# Run from inside pws.site:  python3 "../Website Mockups/_gen_workshop_pages.py"
# Edit page content in PAGES below, then re-run. Re-run too after changing index.html's header/footer/styles.
import json, re
s = open('index.html').read()
top = s[:s.index('<title>')]
headbits = s[s.index('<title>'):s.index('<style>')]
style = s[s.index('<style>'):s.index('</style>') + 8]
header = s[s.index('<header class="nav"'):s.index('<section class="hero"')]
footer = s[s.index('<footer>'):s.index('</footer>') + 9]
for a in ['#experiences', '#calendar', '#studio', '#visit', '#faq', '#contact', '#top', '#projects']:
    header = header.replace(f'href="{a}"', f'href="index.html{a}"')
    footer = footer.replace(f'href="{a}"', f'href="index.html{a}"')
# pull the booking email templates from index.html so there is one source of truth
WA = {k: re.search(r'const %s = `(.*?)`;' % k, s, re.S).group(1) for k in ['WA_PARTY', 'WA_CRAFT']}

CSS = '''<style>
  /* COMPACT WORKSHOP PAGE (product-page layout) */
  .pd{padding:96px 0 40px;}
  .crumb{display:flex;flex-wrap:wrap;gap:8px;font-size:13px;font-weight:600;color:var(--charcoal-soft);margin-bottom:14px;}
  .crumb a{color:var(--red);} .crumb a:hover{text-decoration:underline;}
  .picker{display:flex;gap:10px;overflow-x:auto;padding:2px 2px 12px;margin-bottom:8px;scrollbar-width:thin;}
  .pick{flex:0 0 auto;display:flex;align-items:center;gap:10px;background:var(--white);border:2px solid var(--cream-dark);border-radius:14px;padding:6px 14px 6px 6px;cursor:pointer;font-family:var(--display);font-weight:600;font-size:14.5px;color:var(--charcoal);transition:border-color .2s,transform .2s;}
  .pick img{width:42px;height:42px;border-radius:9px;object-fit:cover;}
  .pick:hover{transform:translateY(-2px);}
  .pick.on{border-color:var(--red);box-shadow:0 8px 18px -10px rgba(191,38,38,.6);}
  .pd-grid{display:grid;grid-template-columns:1.08fr .92fr;gap:34px;align-items:start;}
  /* media viewer */
  .media{min-width:0;position:sticky;top:84px;}
  .stage{position:relative;border-radius:22px;overflow:hidden;box-shadow:var(--shadow);background:var(--charcoal);}
  .track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none;}
  .track::-webkit-scrollbar{display:none;}
  .slide{flex:0 0 100%;aspect-ratio:4/3;max-width:100%;scroll-snap-align:start;position:relative;}
  .slide img{width:100%;height:100%;object-fit:cover;}
  .slide iframe{position:absolute;inset:0;width:100%;height:100%;border:0;}
  .vposter{position:absolute;inset:0;border:none;padding:0;cursor:pointer;background:var(--charcoal);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;width:100%;}
  .vposter img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;}
  .vposter .play{position:relative;z-index:1;width:76px;height:76px;border-radius:50%;background:var(--gold);color:var(--charcoal);display:flex;align-items:center;justify-content:center;font-size:28px;padding-left:5px;transition:transform .3s var(--ease);}
  .vposter:hover .play{transform:scale(1.08);}
  .vposter .vl{position:relative;z-index:1;font-family:var(--display);font-weight:600;color:var(--white);font-size:16px;text-shadow:0 2px 10px rgba(0,0,0,.5);}
  .vposter .soon{position:relative;z-index:1;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:rgba(36,28,24,.6);color:var(--gold-light);padding:4px 11px;border-radius:100px;}
  .nav-btn{position:absolute;top:50%;transform:translateY(-50%);width:42px;height:42px;border-radius:50%;border:none;background:rgba(251,243,236,.92);color:var(--charcoal);font-size:22px;cursor:pointer;box-shadow:var(--shadow-sm);display:flex;align-items:center;justify-content:center;z-index:2;}
  .nav-btn:hover{background:var(--gold);} .nav-btn:disabled{opacity:.3;cursor:default;}
  .nb-prev{left:12px;} .nb-next{right:12px;}
  .count{position:absolute;right:12px;bottom:12px;z-index:2;background:rgba(36,28,24,.65);color:var(--white);font-size:12px;font-weight:700;padding:4px 10px;border-radius:100px;font-variant-numeric:tabular-nums;}
  .thumbs{display:flex;gap:8px;overflow-x:auto;margin-top:10px;padding-bottom:4px;scrollbar-width:thin;}
  .thumbs button{flex:0 0 auto;width:78px;height:58px;border-radius:10px;overflow:hidden;border:3px solid transparent;padding:0;cursor:pointer;opacity:.6;background:var(--charcoal);position:relative;transition:opacity .2s,border-color .2s;}
  .thumbs button img{width:100%;height:100%;object-fit:cover;}
  .thumbs button.on{border-color:var(--red);opacity:1;}
  .thumbs .vt::after{content:'\\25B6';position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--white);font-size:16px;background:rgba(36,28,24,.35);}
  /* info column */
  .info{min-width:0;}
  .tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--red);background:rgba(191,38,38,.08);padding:4px 10px;border-radius:100px;margin-bottom:8px;}
  .info h1{font-family:var(--logo);font-weight:800;font-size:clamp(30px,3.6vw,42px);line-height:1.05;margin-bottom:6px;}
  .info h1 em{font-style:normal;color:var(--red);}
  .sub{font-family:var(--display);font-weight:600;font-size:17px;color:var(--charcoal-soft);margin-bottom:8px;}
  .lede{color:var(--charcoal-soft);font-size:15px;margin-bottom:14px;}
  .facts{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px;}
  .facts div{background:var(--white);border-radius:12px;padding:8px 10px;min-width:0;}
  .facts dt{font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--charcoal-soft);}
  .facts dd{font-family:var(--display);font-weight:600;font-size:14px;line-height:1.25;}
  .buy{display:flex;align-items:center;gap:16px;flex-wrap:wrap;background:var(--white);border-radius:18px;padding:14px 16px;box-shadow:var(--shadow-sm);margin-bottom:14px;}
  .buy .p{display:flex;flex-direction:column;line-height:1.1;margin-right:auto;}
  .buy .p strong{font-family:var(--display);font-size:30px;font-weight:600;color:var(--red);font-variant-numeric:tabular-nums;}
  .buy .p span{font-size:12px;color:var(--charcoal-soft);margin-top:3px;max-width:230px;}
  .buy .btn{padding:14px 24px;}
  .buy .alt{flex-basis:100%;font-size:12.5px;color:var(--charcoal-soft);}
  .buy .alt a{color:var(--red);font-weight:700;}
  .lists{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .lists h3{font-size:15px;margin-bottom:6px;}
  .lists ul{display:flex;flex-direction:column;gap:5px;}
  .lists li{display:flex;gap:8px;font-size:13.5px;line-height:1.4;}
  .lists li .check{width:16px;height:16px;font-size:9px;margin-top:2px;}
  /* strip below */
  .strip{display:grid;grid-template-columns:1.5fr 1fr;gap:20px;margin-top:30px;align-items:start;}
  .card{background:var(--white);border-radius:18px;padding:18px 20px;box-shadow:var(--shadow-sm);min-width:0;}
  .card h2{font-size:18px;margin-bottom:12px;}
  .steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;}
  .steps div{display:flex;flex-direction:column;gap:4px;}
  .steps b{display:flex;align-items:center;gap:8px;font-family:var(--display);font-weight:600;font-size:14.5px;}
  .steps b i{flex:0 0 26px;height:26px;border-radius:50%;background:var(--red);color:var(--white);font-style:normal;font-size:13px;display:flex;align-items:center;justify-content:center;}
  .steps span{font-size:13px;color:var(--charcoal-soft);line-height:1.45;}
  .chips2{display:flex;flex-wrap:wrap;gap:7px;}
  .chips2 span{background:var(--cream);border-radius:100px;padding:6px 12px;font-size:13px;font-weight:600;}
  .learn{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;}
  .learn li{display:flex;gap:8px;font-size:13.5px;}
  .learn li .check{width:16px;height:16px;font-size:9px;margin-top:2px;}
  .contact-mini{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;font-size:13px;color:var(--charcoal-soft);}
  .contact-mini b{color:var(--charcoal);user-select:all;}
  /* holiday projects showcase */
  .showcase{margin-top:24px;padding:0;}
  .sc-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:12px;}
  .sc-head h2{font-size:18px;}
  .sc-head p{font-size:13px;color:var(--charcoal-soft);max-width:560px;}
  .sc-row{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;}
  .sc-card{margin:0;background:var(--white);border-radius:14px;overflow:hidden;box-shadow:var(--shadow-sm);border:2px solid transparent;min-width:0;scroll-margin-top:90px;}
  .sc-card.on{border-color:var(--red);}
  .sc-card img{width:100%;aspect-ratio:4/3;max-width:100%;object-fit:cover;}
  .sc-card figcaption{padding:7px 10px 9px;font-family:var(--display);font-weight:600;font-size:14px;}
  @media(max-width:860px){.sc-row{display:flex;overflow-x:auto;margin:0 -18px;padding:4px 18px 10px;scrollbar-width:none;}.sc-row::-webkit-scrollbar{display:none;}.sc-card{flex:0 0 36%;}}
  /* project options / how projects work */
  .pblock{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:28px;align-items:start;}
  .pblock.single{grid-template-columns:1fr;}
  .pblock .card{display:flex;flex-direction:column;gap:12px;}
  .pblock .card > p{font-size:13.5px;color:var(--charcoal-soft);}
  .how4{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
  .how4 div{background:var(--cream);border-radius:14px;padding:12px 14px;}
  .how4 b{display:flex;align-items:center;gap:8px;font-family:var(--display);font-weight:600;font-size:15px;margin-bottom:3px;}
  .how4 b i{flex:0 0 26px;height:26px;border-radius:50%;background:var(--red);color:var(--white);font-style:normal;font-size:13px;display:flex;align-items:center;justify-content:center;}
  .how4 span{font-size:13px;color:var(--charcoal-soft);line-height:1.45;}
  .how4 strong{color:var(--charcoal);}
  .ideas{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;}
  .idea{background:var(--cream);border-radius:12px;padding:10px 12px;border-left:4px solid var(--gold);}
  .idea b{display:block;font-family:var(--display);font-weight:600;font-size:14.5px;}
  .idea span{font-size:12px;color:var(--charcoal-soft);line-height:1.35;display:block;margin-top:2px;}
  .pnote{display:flex;gap:10px;align-items:flex-start;background:rgba(224,168,62,.16);border-radius:12px;padding:10px 12px;font-size:13px;color:var(--charcoal);}
  .pnote::before{content:'!';flex:0 0 20px;height:20px;border-radius:50%;background:var(--gold);color:var(--charcoal);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center;}
  .sizebadge{align-self:flex-start;display:inline-flex;align-items:center;gap:8px;background:var(--charcoal);color:var(--white);border-radius:12px;padding:8px 14px;font-family:var(--display);font-weight:600;font-size:15px;}
  .sizebadge small{font-family:var(--body);font-size:11.5px;font-weight:600;color:var(--gold-light);}
  .pblock .btn{align-self:flex-start;padding:12px 20px;font-size:14.5px;}
  @media(max-width:860px){.pblock{grid-template-columns:1fr;}}
  @media(max-width:640px){.how4{grid-template-columns:1fr;}.ideas{grid-template-columns:1fr 1fr;}.pblock .btn{width:100%;}}
  header.nav{background:rgba(251,243,236,.94);backdrop-filter:blur(10px);box-shadow:0 6px 24px -14px rgba(36,28,24,.25);}
  @media(max-width:980px){.facts{grid-template-columns:repeat(2,1fr);}}
  @media(max-width:860px){.pd-grid,.strip{grid-template-columns:1fr;gap:22px;}.media{position:static;}}
  @media(max-width:640px){
    .pd{padding:84px 0 30px;}
    .lists,.learn{grid-template-columns:1fr;}
    .buy .btn{width:100%;}
    .thumbs button{width:62px;height:46px;}
    .pick{padding:5px 12px 5px 5px;font-size:13.5px;} .pick img{width:34px;height:34px;}
  }
</style>'''

BODY = '''
<main class="pd" id="top">
  <div class="wrap">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="index.html#experiences">Experiences</a><span>/</span><span id="crumbName"></span></nav>
    <div class="picker" id="picker" hidden></div>
    <div class="pd-grid">
      <div class="media">
        <div class="stage">
          <div class="track" id="track"></div>
          <button class="nav-btn nb-prev" type="button" aria-label="Previous">&lsaquo;</button>
          <button class="nav-btn nb-next" type="button" aria-label="Next">&rsaquo;</button>
          <span class="count" id="count"></span>
        </div>
        <div class="thumbs" id="thumbs"></div>
      </div>
      <div class="info">
        <span class="tag" id="tag"></span>
        <h1 id="title"></h1>
        <p class="sub" id="sub" hidden></p>
        <p class="lede" id="lede"></p>
        <dl class="facts" id="facts"></dl>
        <div class="buy">
          <div class="p"><strong id="price"></strong><span id="priceNote"></span></div>
          <a class="btn btn-primary" id="book" href="#"></a>
          <p class="alt" id="alt"></p>
        </div>
        <div class="lists">
          <div><h3>What's included</h3><ul id="inc"></ul></div>
          <div><h3>What to bring</h3><ul id="bring"></ul></div>
        </div>
      </div>
    </div>
    <div class="pblock" id="pblock" hidden></div>
    <div class="strip">
      <div class="card"><h2 id="stripTitle"></h2><div id="stripBody"></div></div>
      <div class="card"><h2 id="sideTitle"></h2><div id="sideBody"></div></div>
    </div>
      <section class="showcase" id="showcase" hidden></section>
  </div>
</main>
'''

SCRIPT = r'''<script>
/* ================= PAGE CONTENT — edit in Website Mockups/_gen_workshop_pages.py, then re-run ================= */
const PAGE = __PAGE__;
const PHONE_INTL="27810270892";
const wa=m=>`https://wa.me/${PHONE_INTL}?text=${encodeURIComponent(m)}`;
const BOOK_EMAIL="henkvds17@gmail.com";
const mail=(sub,body)=>`mailto:${BOOK_EMAIL}?subject=${encodeURIComponent(sub)}&body=${encodeURIComponent(body)}`;
/* Wix gallery photos load from your Wix media library; if one can't load, a local studio photo shows instead. */
const wixImg=(id,w=1200,h=900)=>`https://static.wixstatic.com/media/${id}/v1/fill/w_${w},h_${h},al_c,q_80,enc_auto/${id}`;
const src=(p,w,h)=>typeof p==='string'?p:(p.wix?wixImg(p.wix,w,h):p.local);
const fb=p=>typeof p==='string'?'':`onerror="this.onerror=null;this.src='${p.local}'"`;
const alt=p=>typeof p==='string'?'':(p.alt||'');
const embed=v=>v.host==='youtube'?`https://www.youtube-nocookie.com/embed/${v.id}?autoplay=1&rel=0`:`https://player.vimeo.com/video/${v.id}?autoplay=1`;
const $=(q,el=document)=>el.querySelector(q);
const check='<span class="check">&#10003;</span>';
const li=a=>a.map(x=>`<li>${check}<span>${x}</span></li>`).join('');

function render(proj){
  const photos = proj ? proj.photos : PAGE.photos;
  const items = photos.map(p=>({type:'img',p})).concat([{type:'video'}]);
  $('#track').innerHTML = items.map((it,i)=>it.type==='img'
    ? `<div class="slide"><img src="${src(it.p)}" ${fb(it.p)} alt="${proj&&i===0?proj.name+' — the finished project':alt(it.p)||PAGE.name+' at Prowell WoodSkills'}" ${i?'loading="lazy"':''}></div>`
    : `<div class="slide" id="vslide"><button class="vposter" type="button" aria-label="Play video"><img src="${src(PAGE.videoPoster)}" ${fb(PAGE.videoPoster)} alt=""><span class="play">&#9658;</span><span class="vl">${PAGE.videoLabel}</span>${PAGE.video.id?'':'<span class="soon">Video coming soon</span>'}</button></div>`).join('');
  $('#thumbs').innerHTML = items.map((it,i)=>it.type==='img'
    ? `<button type="button" aria-label="Photo ${i+1}"><img src="${src(it.p,200,150)}" ${fb(it.p)} alt=""></button>`
    : `<button type="button" class="vt" aria-label="Video"><img src="${src(PAGE.videoPoster,200,150)}" ${fb(PAGE.videoPoster)} alt=""></button>`).join('');
  if(PAGE.video.id){ $('#vslide .vposter').onclick=()=>{$('#vslide').innerHTML=`<iframe src="${embed(PAGE.video)}" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="${PAGE.name} video"></iframe>`;}; }
  const track=$('#track'), th=[...$('#thumbs').children], n=items.length, prev=$('.nb-prev'), next=$('.nb-next');
  const idx=()=>Math.round(track.scrollLeft/track.clientWidth), go=i=>track.scrollTo({left:i*track.clientWidth});
  const sync=()=>{const i=idx();th.forEach((t,j)=>t.classList.toggle('on',j===i));prev.disabled=i===0;next.disabled=i===n-1;$('#count').textContent=i===n-1?'Video':`${i+1} / ${n-1}`;};
  th.forEach((t,i)=>t.onclick=()=>go(i)); prev.onclick=()=>go(Math.max(0,idx()-1)); next.onclick=()=>go(Math.min(n-1,idx()+1));
  track.onscroll=()=>requestAnimationFrame(sync); track.scrollLeft=0; sync();

  if(proj){
    $('#sub').hidden=false; $('#sub').textContent=`${proj.name} · ${proj.level}`;
    $('#lede').textContent=proj.blurb;
    $('#stripTitle').textContent=`What they'll learn building the ${proj.name}`;
    $('#stripBody').innerHTML=`<ul class="learn">${li(proj.learn)}</ul>`;
    document.querySelectorAll('.pick').forEach(b=>b.classList.toggle('on',b.dataset.id===proj.id));

  }
}

// static parts
document.title=`${PAGE.name} · Prowell WoodSkills`;
$('#crumbName').textContent=PAGE.name; $('#tag').textContent=PAGE.tag; $('#title').innerHTML=PAGE.titleHtml;
$('#lede').textContent=PAGE.lede||'';
$('#facts').innerHTML=PAGE.facts.map(([k,v])=>`<div><dt>${k}</dt><dd>${v}</dd></div>`).join('');
$('#price').textContent=PAGE.price; $('#priceNote').textContent=PAGE.priceNote;
const book=$('#book'); book.textContent=PAGE.bookLabel;
if(PAGE.bookHref){book.href=PAGE.bookHref;} else {book.href=mail(PAGE.mailSubject,PAGE.waMsg);}
$('#alt').innerHTML=PAGE.altHtml||'';
$('#inc').innerHTML=li(PAGE.included); $('#bring').innerHTML=li(PAGE.bring);
$('#sideTitle').textContent=PAGE.sideTitle;
$('#sideBody').innerHTML=PAGE.sideSteps?`<div class="steps">${PAGE.sideSteps.map((d,i)=>`<div><b><i>${i+1}</i>${d[0]}</b><span>${d[1]}</span></div>`).join('')}</div>`:`<div class="chips2">${PAGE.perfectFor.map(x=>`<span>${x}</span>`).join('')}</div>`;
if(PAGE.learnAll){
  $('#stripTitle').textContent=PAGE.learnTitle;
  $('#stripBody').innerHTML=`<ul class="learn">${li(PAGE.learnAll)}</ul>`;
} else {
  $('#stripTitle').textContent=PAGE.dayTitle;
  $('#stripBody').innerHTML=`<div class="steps">${PAGE.day.map((d,i)=>`<div><b><i>${i+1}</i>${d[0]}</b><span>${d[1]}</span></div>`).join('')}</div>`;
}
render(null);
// projects showcase (the experience stays the same; the project is what they take home)
if(PAGE.projects){
  const sc=$('#showcase'); sc.hidden=false;
  sc.innerHTML=`<div class="sc-head"><h2>${PAGE.projectsTitle}</h2>${PAGE.projectsIntro?`<p>${PAGE.projectsIntro}</p>`:''}</div>
    <div class="sc-row">${PAGE.projects.map(p=>`<figure class="sc-card" id="${p.id}"><img src="${p.photos[0]}" alt="${p.name}" loading="lazy"><figcaption>${p.name}</figcaption></figure>`).join('')}</div>`;
  const hl=()=>{const el=location.hash&&document.getElementById(location.hash.slice(1));
    document.querySelectorAll('.sc-card').forEach(c=>c.classList.toggle('on',c===el));
    if(el&&el.classList.contains('sc-card')){el.scrollIntoView({block:'center',inline:'center'});}};
  hl(); addEventListener('hashchange',hl);
}
// project options / how projects work
if(PAGE.projectsBlock){
  const P=PAGE.projectsBlock, pb=$('#pblock'); pb.hidden=false; if(!P.how) pb.classList.add('single');
  const ideas=`<div class="card"><h2>${P.ideasTitle}</h2>${P.ideasIntro?`<p>${P.ideasIntro}</p>`:''}<div class="ideas">${P.ideas.map(i=>`<div class="idea"><b>${i[0]}</b><span>${i[1]}</span></div>`).join('')}</div>${P.note?`<div class="pnote">${P.note}</div>`:''}</div>`;
  const how=P.how?`<div class="card"><h2>${P.how.title}</h2>${P.how.size?`<span class="sizebadge">${P.how.size}</span>`:''}<div class="how4">${P.how.steps.map((st,i)=>`<div><b><i>${i+1}</i>${st[0]}</b><span>${st[1]}</span></div>`).join('')}</div></div>`:'';
  pb.innerHTML=how+ideas;
}
// nav (header stays solid on these pages)
const menu=$('#mobileMenu'), hb=$('#hamburgerBtn'); $('#siteNav').classList.add('scrolled');
hb.onclick=()=>{const o=menu.classList.toggle('open');document.body.classList.toggle('menu-open',o);hb.setAttribute('aria-expanded',o);};
menu.querySelectorAll('a').forEach(a=>a.onclick=()=>{menu.classList.remove('open');document.body.classList.remove('menu-open');});
</script>'''

L = lambda n: f'images/studio/studio-{n}.webp'
SP = lambda ns: [L(n) for n in ns]

PAGES = {
 'holiday-projects.html': dict(
   name='Kids Holiday Experience', tag='Kids · ages 8–16 · school holidays',
   titleHtml='Kids Holiday <em>Experience</em>',
   lede="School holidays, but you still have to work? Don't let them spend the day at home on video games. Give your kids something meaningful to do: three hours of healthy, hands-on fun in our professional woodworking studio, where they learn real skills, use real tools safely and come home proud of something they built themselves.",
   photos=SP([12,13,3,9,16,4,22]),
   learnTitle="What every child learns",
   learnAll=['Using real hand tools safely','Measuring and marking accurately','Cutting straight and square','Gluing, clamping or screwing joints','Sanding and finishing','Following a plan from start to finish'],
   projectsTitle='Projects available these holidays',
   projectsIntro='',
   facts=[['Duration','1 day · 3 hrs'],['Ages','8–16'],['Group','Max 8 kids'],['Level','Beginner']],
   price='R350', priceNote='per child, per project. All materials included.',
   bookLabel='See dates & book', bookHref='index.html#calendar',
   altHtml='One-day experiences in the school holidays. Pick a date on the calendar.',
   included=['All timber, glue and hardware','Tools and safety gear at every bench','Step-by-step guidance from start to finish','A finished project to take home','A certificate of completion'],
   bring=['Closed shoes','Clothes that can take wood dust','A water bottle','A snack'],
   sideTitle='How the day works',
   sideSteps=[['Introduction to woodworking','The wood, the tools, how to use them safely, and the safety gear.'],
              ['Start building','Hands-on: measure, cut and assemble, with help at every step.'],
              ['Break time','Snack time, play, and a go at some of the tools they like.'],
              ['Finish & take it home','Sand, finish, and leave with the project and a certificate.']],
   videoLabel='Watch a holiday experience', video={'host':'youtube','id':''}, videoPoster=L(13),
   projects=[
     dict(id='pot-stand', name='Pot Stand', level='Hand tools & glue',
       blurb="A slatted stand that keeps hot pots and pans off the table. It's the perfect first build: simple to plan, satisfying to make, and the whole family will use it.",
       learn=['Measuring and marking with a ruler and square','Cutting straight with a pull saw and mitre box','Spacing slats evenly','Gluing and clamping a strong joint','Sanding to a smooth finish'],
       photos=['images/projects/pot-stand.webp']+SP([12,13,22])),
     dict(id='book-stand', name='Book Stand', level='Hand tools & glue',
       blurb='An angled stand that holds a recipe book, reading book or tablet. It teaches how to cut angles and build something that stands up straight.',
       learn=['Measuring and marking angles','Cutting accurate angles in a mitre box','Gluing a stable support','Clamping while the glue sets','Sanding edges and corners'],
       photos=['images/projects/book-stand.webp']+SP([9,5,21])),
     dict(id='offcut-box', name='Offcut Box', level='Hand tools & glue',
       blurb='A sturdy little box with grip handles on the ends, made to hold pencils, toys or workshop offcuts. Building a square box is a real woodworking milestone.',
       learn=['Building a square box','Making four sides fit together','Gluing and clamping a box','Adding handles','Sanding a box inside and out'],
       photos=['images/projects/offcut-box.webp']+SP([17,18,20])),
     dict(id='key-rack', name='Key Rack', level='Drill & screws · best for 12+',
       blurb='A wall-mounted key rack with brass hooks. Kids step up to a cordless drill and screws to build something that hangs by the front door for years.',
       learn=['Using a cordless drill safely','Pre-drilling and screwing joints','Fitting brass hooks','Building a frame','Finishing with wood oil'],
       photos=['images/projects/key-rack.webp']+SP([13,14,7])),
     dict(id='coat-hook', name='Hat / Coat Hook', level='Drill & screws · best for 12+',
       blurb='A wall rail with wooden pegs for hats, coats and school bags. A bigger, stronger build that uses a drill and screws, and finally gives the school bag a home.',
       learn=['Measuring and spacing pegs evenly','Drilling and screwing pegs to a rail','Making strong joints that carry weight','Sanding and finishing with wood oil','Planning a project from start to finish'],
       photos=['images/projects/coat-hook.webp']+SP([10,2,24])),
   ]),
 'kids-birthday-party.html': dict(
   name='Kids Birthday Party', tag='Kids · ages 8–16 · booked by request',
   titleHtml='The party where they <em>build their own gift.</em>',
   lede="You choose one project for the party, and every guest builds it from start to finish at their own workbench, with real tools. Then it's cake time at the birthday table. They go home proud, with something they made themselves.",
   facts=[['Duration','3 hours'],['Ages','8–16'],['Guests','Up to 8 kids'],['Studio','All yours']],
   price='R2,900', priceNote='Flat rate for the party, up to 8 kids (about R363 per child).',
   bookLabel='Request booking', waMsg=WA['WA_PARTY'], mailSubject='Kids Birthday Party booking request',
   altHtml='Booked by request: tell us your preferred date and we will confirm it.',
   included=['Exclusive use of the studio','A bench, tools and safety gear for every guest','All timber and hardware','A finished project for every guest','A birthday table for cake and drinks','Music throughout'],
   bring=['Closed shoes for every child','Clothes that can take wood dust','Birthday cake, drinks and extras','Or add a decorated cake for R300'],
   dayTitle='How the party works',
   day=[['Welcome & safety','Safety gear on and a quick, friendly briefing.'],['Same project, together','The whole group builds the project you chose when booking, side by side.'],['Build it','Their own bench, guided from first cut to final sanding.'],['Cake time','Birthday table, candles, and every guest takes their project home.']],
   sideTitle='Perfect for', perfectFor=['Birthdays (ages 8–16)','Kids who love making things','A party they will remember','A gift that lasts'],
   projectsBlock=dict(
     ideasTitle='Choose the party project',
     ideasIntro='Pick one project for the whole group when you book. Everyone builds the same one, like these party favourites:',
     ideas=[['Phone Stand','Holds a phone upright for videos and calls.'],['Name Sign','Their own name, cut, sanded and decorated.'],['Pencil Holder','A chunky holder for the desk or art table.'],['Toy Car','A wooden car with wheels that really roll.'],['Treasure Box','A small box with a lid for special things.'],['Bookends','A pair to keep their favourite books standing.']],
     note='Tell us your choice when you book, at least 2 days before the party, so we can prepare the timber. These are examples while we finalise our party project list; special requests are welcome.'),
   videoLabel='Watch a party in action', video={'host':'youtube','id':''}, videoPoster={'local':L(16)},
   photos=[
     {'wix':'48e650_784ace91e4b743058e09c1dcc53023b2~mv2.jpg','local':L(23),'alt':'Kids at a woodworking birthday party'},
     {'wix':'48e650_98de089ab11244cf90b152a8406e4543~mv2.jpg','local':L(16),'alt':'Party guest with their finished project'},
     {'wix':'48e650_86a478257090409793df6dc54d2b878d~mv2.jpg','local':L(3),'alt':'Birthday party builders in the studio'},
     {'wix':'48e650_294e5bfb8a5a4f129b4d18eb6bfb13ee~mv2.jpg','local':L(9),'alt':'Kids building at their own workbenches'},
     {'wix':'48e650_f76fd946f1394ccfb474b63981ed4089~mv2.jpg','local':L(8),'alt':'Proud party guests with their projects'},
     {'wix':'48e650_ee3a199aac484e5b9beeea69aab7ced1~mv2.jpg','local':L(12),'alt':'Sanding a project at a birthday party'}]),
 'craft-together.html': dict(
   name='Craft Together', tag='Families, friends & teams · groups of 5–8 · booked by request',
   titleHtml='Skip the wine farm. <em>Build something together.</em>',
   lede="Round up your family, friends or team for a session you will all be talking about. Craft Together is a social, hands-on group outing: the music is on, the coffee is flowing, and everyone gets stuck in with real tools, side by side, with a facilitator guiding the way. There is plenty of laughter, a bit of friendly competition, and three hours later every one of you walks out with something you made yourself.",
   facts=[['Duration','3 hours'],['Group','5 to 8 people'],['When','Weekdays'],['Skill','All levels']],
   price='R550', priceNote='Per person, for groups of 5 to 8. All materials included.',
   bookLabel='Request booking', waMsg=WA['WA_CRAFT'], mailSubject='Craft Together booking request',
   altHtml='Groups only, on weekdays. Tell us your preferred date and we will confirm it.',
   included=['A facilitator guiding your group','All tools and equipment','Timber and hardware for your project','A finished project to take home','Free coffee and tea','Music and a social atmosphere'],
   bring=['Closed shoes','Comfortable clothes that can get dusty','Something to drink and a snack','Your group of 5 to 8 people'],
   dayTitle='How the session works',
   day=[['Coffee & welcome','Meet your facilitator and get a quick safety briefing.'],['Plan & design','Each guest picks one of the 3 projects, plans and designs it, and selects their own timber and materials.'],['Build it, guided','Measure, cut, join and finish with real tools.'],['Take it home','Group photo, and your finished piece goes home with you.']],
   sideTitle='Perfect for', perfectFor=['Family outings','Friends celebrating','Team building','Visitors to the Winelands','Birthdays and get-togethers','All levels, first-timers welcome'],
   projectsBlock=dict(
     how=dict(title='How the projects work', size='Max size 20 × 20 × 20 cm <small>per project</small>',
       steps=[['Pick 3 projects','From our ideas or your own (a photo works).'],
              ['Keep it small','Max <strong>20 × 20 × 20 cm</strong>, so everyone can finish in three hours.'],
              ['Send them 2 days before','So we can prepare the timber.'],
              ['Choose on the day','Each person builds <strong>any one</strong> of the 3.']]),
     ideasTitle='Project ideas to get you started',
     ideas=[['Coaster Set','Four coasters, sanded and oiled.'],['Serving Board','A small board for cheese or snacks.'],['Candle Holder','A block holder for tea lights.'],['Phone Stand','A neat stand for your desk.'],['Mini Planter Box','For herbs or succulents.'],['House Number Sign','Your number, cut and finished.']],
     note='Not sure if your idea will work? Include a photo when you book and we will confirm it fits the 20 × 20 × 20 cm size and the 3-hour session.',),
   videoLabel='Watch a group in action', video={'host':'youtube','id':''}, videoPoster={'local':L(22)},
   photos=[
     {'wix':'48e650_b68e59e45776478094483cdcecd335ad~mv2.jpeg','local':L(14),'alt':'A group working on projects at Craft Together'},
     {'wix':'48e650_9f2eca3bc2d54f14a915642eea8a9cc0~mv2.jpeg','local':L(22),'alt':'The studio set up for a group'},
     {'wix':'48e650_711ef977c1274b488065b27ba9c9aa5a~mv2.jpeg','local':L(21),'alt':'Finished wooden projects'},
     {'wix':'48e650_e86667be730249f9bc20a22f4810ceba~mv2.jpeg','local':L(12),'alt':'Sanding a project'},
     {'wix':'48e650_c536967e20044ac5b79e1b51b19a9474~mv2.jpeg','local':L(18),'alt':'Group working at the benches'},
     {'wix':'48e650_895e6e7a88dc48058d115c00134fa486~mv2.jpeg','local':L(10),'alt':'Tools and benches in the studio'},
     {'wix':'48e650_395dcf55cd4d4737b867572f8c2bc2ff~mv2.jpeg','local':L(5),'alt':'Projects taking shape'}]),
}

for fname, d in PAGES.items():
    if isinstance(d.get('videoPoster'), str): pass
    hb = re.sub(r'<title>.*?</title>', f"<title>{d['name']} · Prowell WoodSkills</title>", headbits)
    desc = (d.get('lede') or 'The woodworking projects kids build at the Prowell WoodSkills Kids Holiday Experience in Paarl.')[:155]
    hb = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', hb)
    page = top + hb + style + '\n' + CSS + '\n' + header + BODY + footer + '\n' + SCRIPT.replace('__PAGE__', json.dumps(d, ensure_ascii=False, indent=1)) + '\n'
    open(fname, 'w').write(page)
    print(fname, len(page))
