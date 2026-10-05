from pathlib import Path
import re, html

ROOT=Path(".")
BASE="https://jin-in-seoul.com"
slug="books-rule"
EN=f"{BASE}/short-stories/{slug}/en/"
KO=f"{BASE}/short-stories/{slug}/ko/"
HUB=f"{BASE}/short-stories/{slug}/"

raw=r'''I’m a book.

I should tell you right away that I’m a perfectly ordinary book. So there won’t be any mysterious wizard’s book or scary haunted book in this story. But don’t be disappointed just yet. My adventure is much more exciting and fun than anything those fancy books ever went through.

I was thrown out with the recycling this morning. Every Wednesday, the people in the apartment complex bring out paper, plastic, glass bottles, plastic bags, and all sorts of other things to be recycled.

My first owner, Doyoung, doesn’t read books anymore. He likes games on his smartphone better. I spent a long time stuck any old way on a bookshelf. Then Doyoung’s mother used their move as an excuse to throw me and a whole lot of other books into the recycling area.

If only she had sold us to a used bookstore or donated us to a library! Then I might have met some new friends. Instead, from Sunday morning on, I was tied up with other books, trembling with fear. For three whole days and nights.

You have no idea how desperately I wished Doyoung would untie the string and open me just once. But no such miracle happened. To tell you the truth, Doyoung had never even touched me. I was volume thirty-eight in a collection of children’s stories, and I wasn’t very lucky. Doyoung never touched anything after volumes one and two. Not that volumes one and two were much luckier. It wasn’t as if he had actually read them.

Buried under a mountain of paper, I could hardly breathe. At last I accepted my fate: I was going to be turned into recycled paper. I had come into the world as a wonderful storybook, but no one had ever enjoyed reading me or loved me. So I decided that being reborn as an even better book might not be such a bad thing. I placed my last hope in that.

Wednesday passed, and Thursday morning came. A truck with an enormous iron hand arrived to collect the recycling. The plastic was loaded first, and then it was the paper’s turn. The giant iron hand lifted huge sacks of paper onto the truck.

Finally, it was time for the sack I was in to be loaded. Just then, a cat darted out of nowhere. The man operating the giant hand flinched and stopped the machine. And that was how I fell onto a short privet bush.

The man saw me fall, but when the collection was finished, he pretended not to notice me and drove away from the recycling area. I suppose there was no reason to waste time picking up a worthless little book like me. My hope of being reborn as a new book shattered into pieces.

And then something frightening happened right before my eyes.

“Hey! Stop right there!”

A group of big kids shouted as they chased a smaller boy.

The little boy was panting hard when he came to a stop in front of the recycling area. It was a dead end. There was nowhere else to run.

“Hey, Jang Minsu! We told you not to come this way.”

The first boy snapped at him.

“This is our apartment complex. You’re not allowed to walk through here.”

The second boy flicked Minsu’s cap off his head.

Minsu bent down to pick it up.

And that was when his eyes met mine.

“Why aren’t you answering?”

The third boy raised his arm as if he was about to hit Minsu.

Minsu quickly dodged toward the privet bush and picked me up.

“Oh, yeah? You wanna fight?”

The first boy threw a punch at Minsu.

Minsu gripped me tightly with both hands and blocked the punch. The boy’s fist slammed into my hard cover, and his face twisted with pain.

Then the second boy charged at Minsu like an angry bull.

Once again, Minsu calmly blocked him with my hard cover.

When Minsu took a step toward the third boy, the boy didn’t dare attack. He flinched and backed away.

In the end, all three boys were so startled by Minsu’s counterattack that they turned and ran.

Minsu tucked me under his arm and marched home in triumph.

His house stood in an old neighborhood behind the recycling area that was scheduled for redevelopment. That must have been why Minsu walked through the apartment complex where Doyoung, my first owner, lived whenever he went to and from school. Otherwise, he would have had to take a detour of more than twenty minutes.

No one in Minsu’s family was home. From the outside, the house had looked very small and shabby, but inside it was bright and clean. Everything was neatly organized.

Minsu washed his hands and face, then sat down at the desk in his little room and started studying.

I secretly watched his face. He looked as happy as someone who had just had something wonderful happen to him.

Was he happy because he had taught those mean kids a lesson? Or had something exciting happened at school with his friends?

I wondered why Minsu looked so happy.

So I whispered in the tiniest voice.

‘Did something good happen?’

And Minsu answered me.

‘Yeah. I got a storybook. I’ve never owned a book before, except for my school textbooks. You have no idea how happy I am. Grandma says books are too expensive for us.’

Minsu put down the pencil in his right hand, stroked me once, and hugged me tightly to his chest.

For the first time in my life, someone held me in their arms.

I can’t even begin to tell you how full my heart felt, or how happy I was.

Minsu put me down and went back to his homework. About an hour later, he packed the textbooks and assignments he would need for school the next day into his backpack.

Minsu glanced at the clock on the wall, then picked me up.

He leaned against the wall and began reading me aloud.

I had never been so thrilled in my life.

*Robot Girl Miri*

Hello. My name is Miri. My name comes from *mireunae*, a native Korean word for the Milky Way. These days there are so many lights even in the middle of the night that it’s hard to see the stars, but if you’ve ever been out in the countryside, you may have seen stars flowing across the night sky like a river. Bright stars, shining as if someone had scattered bits of gold and silver paper across the sky. That is the Milky Way....

Minsu read for about thirty minutes, then looked at the clock again.

For a moment, he hesitated.

“Grrrrrrumble.”

Suddenly Minsu’s stomach sent out a hungry warning.

Apparently he couldn’t stand it any longer, because he carried me into the kitchen.

He took a cup of instant noodles from a drawer and boiled some water in the electric kettle. Thirty seconds later, the water was ready, and he carefully poured it into the cup.

I secretly worried that Minsu might put me on top of the noodles.

People use books as pot holders or to hold down cup-noodle lids all the time, you know.

Luckily, Minsu wasn’t that kind of kid.

Two minutes later, he peeled the lid all the way off and happily slurped down the noodles, blowing on them as he ate. He ate with such delight that even I started to feel hungry.

With his stomach nice and full, Minsu cleaned up the kitchen, went back to his little room, leaned against the wall, and started reading me again.

He giggled sometimes, looked sad at other times, and disappeared completely into the story.

After another thirty minutes or so, his head began to nod.

He had fought a whole battle with those mean kids earlier that day, so of course he was tired.

I became a book pillow so Minsu could sleep comfortably.

With his head resting on me, Minsu entered the world of dreams and began an exciting adventure.

“Wake up.”

Miri shook Minsu awake.

The moment her hand, cold as a lump of iron, touched his skin, Minsu jumped and opened his eyes.

“Are you...?”

“That’s right. I’m Miri.”

Minsu stared at her in surprise.

Miri’s arms and legs were made of steel.

“Hurry. We don’t have much time.”

Miri grabbed Minsu’s hand and started running.

Minsu had no idea what was going on, but he followed her and ran as hard as he could until he was out of breath.

Miri took him to a secret place on the outskirts of a city that had been reduced to ruins.

There, one by one, she told Minsu about the terrible things that were happening.

“The Decalcomania Organization is kidnapping children and turning them into artificial humans. I was lucky. They only replaced my arms and legs with steel. But countless children have had artificial-intelligence chips forced into their heads to make them obey the Decalcomania Organization.”

“What’s the Decalcomania Organization?”

“An evil force that rules the world. It stirs people up, brainwashes them, and controls them however it wants. No one can disobey its orders.”

“How could something like that happen?”

“Thirty years ago, people began handing annoying jobs over to robots one by one. At first it was things like cleaning and driving. Later, they started asking robots what they should choose and whose words they should believe. People stopped reading books, and even thinking for themselves began to feel like too much trouble. Eventually, politicians and scientists were able to control those people however they wanted.”

“A world just for them? What kind of world is that?”

“After 2078, no one heard babies crying anymore. People had even grown tired of living together. Families became rarer, and so did having children. Eventually robots took over even the roles that people once needed other people for. Human genes were stored in laboratories, so whenever a person was needed, one was simply made. That’s how I was born too. A month ago, they ordered me to be turned into an artificial human. But I ran away.”

“Then what are we supposed to do?”

“The first thing we have to do to bring down the Decalcomania Organization is....”

Just then, someone came into the house and called Minsu’s name.

“Minsu!”

Minsu woke from his exciting adventure with Miri.

He sprang to his feet and shouted, “Grandma!” as he ran to the front door.

The moment Grandma saw Minsu, she hugged him tightly.

“Sweetheart, you must be hungry.”

“No. I already had cup noodles. You must be even hungrier than me, Grandma.”

“All right, all right. Grandma will make dinner, so wait just a little while.”

Grandma changed into some comfortable clothes and went into the kitchen.

While she prepared dinner, Minsu proudly told her about the storybook he had brought home from the recycling area that day.

Grandma listened carefully.

“Then after dinner, will Minsu read the book to Grandma?”

Minsu nodded eagerly.

“Yes!”

Then he helped Grandma set the table.

He wiped the table with a clean dishcloth and neatly laid out the spoons and chopsticks.

Just then, a little black bug crawled between the dining chairs.

Minsu was so startled that he grabbed me from the table and was about to throw me at it.

But apparently he couldn’t bring himself to kill a bug with a book.

Instead, he pulled out a tissue, carefully picked up the bug, and gently let it go out the window.

After dinner, Minsu helped Grandma clear the table.

When Grandma finished washing the dishes and sat down in a chair, Minsu opened the storybook and began reading aloud.

Grandma’s face filled with a smile as she watched him read aloud clearly. He must have looked so cute and lovable to her.

When Minsu finished reading, Grandma said:

“Minsu, in this world, books rule!”

—The End—'''

def md_inline(t):
    t=html.escape(t)
    t=re.sub(r'\*([^*]+)\*', r'<em>\1</em>', t)
    return t

body="\n".join("<p>"+md_inline(p)+"</p>" for p in raw.split("\n\n"))

en_page=f'''---
---
<!doctype html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-72EG8XPTN7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-72EG8XPTN7');
</script>
  <meta charset="utf-8">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Books Rule! - Jin-in-Seoul</title>
  <meta name="description" content="Books Rule! — a children’s short story by Jin-in-Seoul about a discarded storybook that finds a child who has never owned a book before.">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{EN}">
  <link rel="alternate" hreflang="en" href="{EN}">
  <link rel="alternate" hreflang="ko" href="{KO}">
  <link rel="alternate" hreflang="x-default" href="{EN}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="Books Rule! - Jin-in-Seoul">
  <meta property="og:description" content="A discarded storybook finds a child who has never owned a book before, and discovers what it means to be read, loved, and needed.">
  <meta property="og:url" content="{EN}">
  <meta property="og:site_name" content="Jin-in-Seoul">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Books Rule! - Jin-in-Seoul">
  <meta name="twitter:description" content="A discarded storybook finds a child who has never owned a book before, and discovers what it means to be read, loved, and needed.">
  <script type="application/ld+json" data-seo="site">
{{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "name": "Books Rule!",
  "alternateName": "책이 왕초야",
  "url": "{EN}",
  "inLanguage": "en",
  "author": {{
    "@type": "Person",
    "name": "Jin-in-Seoul",
    "url": "{BASE}/"
  }}
}}
  </script>
  <link rel="stylesheet" href="../../../assets/style.css?v=046">
</head>
<body>
  <main class="shell">
    {{% include header.html %}}
    <nav class="contents-nav" aria-label="Contents"><a href="/short-stories/">Contents</a></nav>

    <h1>Books Rule!</h1>
    <article class="prose">
{body}
    </article>

    {{% include footer.html %}}
  </main>
</body>
</html>
'''
(ROOT/f"short-stories/{slug}/en").mkdir(parents=True,exist_ok=True)
(ROOT/f"short-stories/{slug}/en/index.html").write_text(en_page,encoding="utf-8")

# Hub: English + Korean, reciprocal hreflang, x-default English.
p=ROOT/f"short-stories/{slug}/index.html"; s=p.read_text(encoding="utf-8")
s=re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Books Rule! — a children’s short story by Jin-in-Seoul, available in English and Korean.">', s, count=1)
s=re.sub(r'(\s*<link rel="alternate" hreflang="(?:ko|x-default)"[^>]*>\n?)+',
         f'\n  <link rel="alternate" hreflang="en" href="{EN}">\n  <link rel="alternate" hreflang="ko" href="{KO}">\n  <link rel="alternate" hreflang="x-default" href="{EN}">\n', s)
s=s.replace('Korean edition available now; additional language editions will follow.','Available in English and Korean.')
s=s.replace('Korean edition available now.','Available in English and Korean.')
s=s.replace('<nav class="language-list" aria-label="Language selection">\n      <a href="ko/" lang="ko">한국어</a>',
            '<nav class="language-list" aria-label="Language selection">\n      <a href="en/" lang="en">English</a>\n      <a href="ko/" lang="ko">한국어</a>')
p.write_text(s,encoding="utf-8")

# KO page: add English reciprocal and x-default English.
p=ROOT/f"short-stories/{slug}/ko/index.html"; s=p.read_text(encoding="utf-8")
s=re.sub(r'(\s*<link rel="alternate" hreflang="(?:ko|x-default)"[^>]*>\n?)+',
         f'\n  <link rel="alternate" hreflang="en" href="{EN}">\n  <link rel="alternate" hreflang="ko" href="{KO}">\n  <link rel="alternate" hreflang="x-default" href="{EN}">\n', s)
p.write_text(s,encoding="utf-8")

# Short Stories index: title points to EN and language links EN + KO.
p=ROOT/"short-stories/index.html"; s=p.read_text(encoding="utf-8")
s=s.replace(f'<a class="work-link" href="{slug}/ko/">\n            Books Rule!', f'<a class="work-link" href="{slug}/en/">\n            Books Rule!')
s=s.replace(f'<p>\n          <a href="{slug}/ko/">한국어</a>\n        </p>',
            f'<p>\n          <a href="{slug}/en/">English</a>\n          ·\n          <a href="{slug}/ko/">한국어</a>\n        </p>')
p.write_text(s,encoding="utf-8")

# Homepage: append Books Rule as final Short Stories item.
p=ROOT/"index.html"; s=p.read_text(encoding="utf-8")
if f'short-stories/{slug}/en/' not in s:
    marker='''      </div>

    </section>


    <section class="gray-note-section">'''
    card=f'''        <article class="work">
          <h3>
            <a class="work-link" href="short-stories/{slug}/en/">Books Rule!</a>
          </h3>
          <p>
            <a href="short-stories/{slug}/en/">English</a>
            ·
            <a href="short-stories/{slug}/ko/">한국어</a>
          </p>
        </article>

      </div>

    </section>


    <section class="gray-note-section">'''
    if marker not in s: raise RuntimeError("Homepage short stories marker not found")
    s=s.replace(marker,card,1)
p.write_text(s,encoding="utf-8")

# Human site map: EN + KO.
p=ROOT/"site-map/index.html"; s=p.read_text(encoding="utf-8")
old=f'''            <span class="map-languages">
              <a href="/short-stories/{slug}/ko/">한국어</a>
            </span>'''
new=f'''            <span class="map-languages">
              <a href="/short-stories/{slug}/en/">English</a> ·
              <a href="/short-stories/{slug}/ko/">한국어</a>
            </span>'''
if old not in s: raise RuntimeError("Site map Books Rule item not found")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")

# Publication Log: add English in same Oct 5 list.
p=ROOT/"publication-log/index.html"; s=p.read_text(encoding="utf-8")
needle='<li>Korean edition — <em>책이 왕초야</em> (<em>Books Rule!</em>) added</li>'
if '<li>English edition — <em>Books Rule!</em> added</li>' not in s:
    s=s.replace(needle, '<li>English edition — <em>Books Rule!</em> added</li>\n          '+needle,1)
p.write_text(s,encoding="utf-8")

# Sitemap: English URL.
p=ROOT/"sitemap.xml"; s=p.read_text(encoding="utf-8")
if f"<loc>{EN}</loc>" not in s:
    block=f'''  <url>
    <loc>{EN}</loc>
  </url>
'''
    s=s.replace("</urlset>",block+"</urlset>")
p.write_text(s,encoding="utf-8")

# Validate exact English text paragraphs (ignoring intended <em> inline markup).
out=(ROOT/f"short-stories/{slug}/en/index.html").read_text(encoding="utf-8")
article=re.search(r'<article class="prose">\n(.*?)\n    </article>',out,re.S).group(1)
decoded=[]
for m in re.finditer(r"<p>(.*?)</p>",article,re.S):
    t=re.sub(r'<em>(.*?)</em>', r'*\1*', m.group(1))
    decoded.append(html.unescape(t))
assert "\n\n".join(decoded)==raw, "English text/paragraphs changed"

# Structural checks
ko=(ROOT/f"short-stories/{slug}/ko/index.html").read_text(encoding="utf-8")
hub=(ROOT/f"short-stories/{slug}/index.html").read_text(encoding="utf-8")
home=(ROOT/"index.html").read_text(encoding="utf-8")
short=(ROOT/"short-stories/index.html").read_text(encoding="utf-8")
site=(ROOT/"site-map/index.html").read_text(encoding="utf-8")
sm=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
for page in (out,ko,hub):
    assert f'hreflang="en" href="{EN}"' in page
    assert f'hreflang="ko" href="{KO}"' in page
    assert f'hreflang="x-default" href="{EN}"' in page
assert f'short-stories/{slug}/en/' in home
assert f'href="{slug}/en/"' in short
assert f'/short-stories/{slug}/en/' in site
assert f'<loc>{EN}</loc>' in sm
print("Books Rule English + homepage publication validated; English text and paragraph boundaries are exact.")
