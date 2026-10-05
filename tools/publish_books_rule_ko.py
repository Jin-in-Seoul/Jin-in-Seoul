from pathlib import Path
import re, html

ROOT=Path(".")
BASE="https://jin-in-seoul.com"
slug="books-rule"
story_url=f"{BASE}/short-stories/{slug}/ko/"
hub_url=f"{BASE}/short-stories/{slug}/"

raw = r'''나는 책이야.

미리 말해 두지만 무척 평범한 책이야. 그러니까 이 동화 속에는 마법사의 신비한 책이나 귀신이 들린 무서운 책은 등장하지 않아. 그렇다고 벌써 실망할 필요는 없어. 내 모험담은 그런 대단한 책들보다 훨씬 더 멋지고 신나니까 말이야.

나는 오늘 아침 재활용 쓰레기로 버려졌어. 매주 수요일에는 아파트 주민들이 종이, 플라스틱, 유리병, 비닐 등을 가지고 나와 버리거든.

내 첫 번째 주인이었던 도영이는 더 이상 책을 읽지 않아. 스마트폰 게임을 더 좋아하거든. 나는 오랫동안 책꽂이에 아무렇게나 꽂혀 있었지. 그러자 도영이 엄마는 이사를 핑계로 나를 비롯해 많은 책들을 재활용 쓰레기장에 버렸어.

헌책방에 팔거나 도서관에 기증했다면 얼마나 좋았을까? 만약 그랬다면 새 친구들을 만날 수 있었을 테니 말이야. 나는 일요일 아침부터 다른 책들과 함께 노끈으로 묶인 채 두려움 속에서 떨어야 했어. 무려 사흘 밤낮이나 말이지.

도영이가 노끈을 풀고 나를 딱 한 번만이라도 펼쳐 주기를 얼마나 간절히 바랐는지 몰라. 하지만 그런 기적은 일어나지 않았어. 진실을 고백하자면 도영이는 이제까지 단 한 번도 나를 만진 적조차 없어. 어린이 창작 동화 전집에서 38번째였던 나는 별로 운이 좋지 않았어. 도영이는 1권과 2권 말고는 손도 대지 않았으니 말이야. 그렇다고 1권과 2권이 딱히 더 운이 좋다고 말할 수는 없어. 도영이가 그 책을 읽은 건 아니었으니까 말이야.

산처럼 쌓인 종이 더미 속에서 나는 숨조차 쉬기 힘들었어. 그리고 마침내 재활용 종이로 변해야 하는 나의 운명을 받아들였지. 이 세상에 멋진 동화책으로 나왔지만 아무도 나를 즐겁게 읽거나 사랑해 주지 않았어. 그러니 다시 태어나 더 멋진 책으로 부활하는 것도 나쁘지만은 않다고 생각했어. 나는 거기에 마지막 희망을 걸었지.

수요일이 가고 목요일 아침이 되었어. 무쇠로 만든 거대한 손을 가진 트럭이 재활용품을 수거하러 왔지. 맨 먼저 플라스틱이 트럭에 실리고 나자 다음은 종이 차례였어. 거대한 무쇠 손은 종이가 담긴 대형 포대들을 트럭에 실었지.

드디어 나를 담고 있는 포대가 차에 실릴 차례였어. 거대한 손을 운전하는 아저씨가 갑자기 튀어나온 고양이 때문에 움찔하며 기계를 멈췄지. 그 바람에 나는 키 작은 쥐똥나무 위로 떨어지고 말았어.

아저씨는 내가 떨어지는 걸 보았으면서도 수거가 끝나자 나를 못 본 척하고 재활용 쓰레기장을 떠났어. 나처럼 하찮은 책을 줍기 위해 시간 낭비할 필요는 없었겠지. 새 책으로 부활하겠다는 나의 희망은 산산이 부서졌어. 바로 그때 무서운 일이 눈앞에서 펼쳐졌지.

“야! 거기 서.”

덩치 큰 아이들이 조그만 아이를 쫓으며 소리쳤어. 조그만 아이는 숨이 차는지 헉헉거리며 재활용 쓰레기장 앞에 멈춰 섰지. 막다른 골목이어서 더 이상 도망갈 곳이 없었어.

“야, 장민수! 너 여기로 다니지 말라고 했잖아.”

첫 번째 아이가 성을 내며 말했어.

“여기는 우리 아파트야. 너는 이 길로 다니면 안 돼.”

두 번째 아이가 민수라는 아이의 모자를 손으로 툭 쳐서 벗겨 버렸어.

민수는 땅에 떨어진 모자를 주우려고 허리를 숙였어. 바로 그때 민수와 내 눈이 딱 마주쳤지.

“왜 대답이 없어?”

세 번째 아이가 민수에게 손찌검을 하려는지 팔을 들어 올렸어. 그러자 민수가 잽싸게 쥐똥나무 쪽으로 몸을 피하며 나를 집어 들었지.

“어쭈! 어디 한번 해보겠다는 거야?”

첫 번째 아이가 민수에게 주먹을 날렸어. 민수는 나를 두 손으로 꽉 움켜잡고 주먹을 막아 냈지. 첫 번째 아이는 주먹이 딱딱한 책 표지에 닿자 너무 아파서 울상이 되었어.

그러자 두 번째 아이가 성난 황소처럼 민수에게 달려들었지. 이번에도 민수는 달려드는 황소의 머리통을 단단한 책으로 침착하게 막아 냈어.

민수가 세 번째 아이에게 한 발짝 다가서자 감히 덤비지 못하고 움찔움찔 뒷걸음을 쳤어. 결국 세 아이 모두 민수의 반격에 놀라 줄행랑을 놓았지.

민수는 나를 옆구리에 끼고 의기양양하게 집으로 돌아갔어. 민수의 집은 재활용 쓰레기장 뒤편에 있는 재개발 예정지 안에 있었지. 그래서 민수는 나의 첫 번째 주인이었던 도영이가 살던 아파트를 가로질러 등하교를 했었나 봐. 그렇게 하지 않으면 20분도 넘게 돌아가야 하니까 말이지.

민수의 집에는 가족이 아무도 없었어. 밖에서 보았던 집은 무척 작고 초라했지만 집 안은 환하고 깨끗했지. 모든 게 잘 정돈되어 있었어.

민수는 손과 얼굴을 닦고 나서 작은방 책상에 앉아 공부를 시작했지. 나는 가만히 민수의 얼굴을 훔쳐보았는데 무슨 기분 좋은 일이 있는 사람처럼 행복해 보였어.

아까 못된 아이들을 혼내 줘서 기분이 좋은 걸까? 아니면 오늘 학교에서 친구들과 신나는 일이 있었던 걸까? 나는 민수가 왜 그렇게 행복한지 궁금했어. 그래서 아주 작은 목소리로 속삭였지.

‘무슨 기분 좋은 일이 있니?’

그러자 민수가 이렇게 대답했어.

‘응. 동화책이 생겼거든. 나는 이제껏 교과서 말고는 한 번도 책을 가져 본 적이 없어. 그래서 얼마나 기분이 좋은지 몰라. 할머니는 우리 집 형편에는 책이 너무 비싸다고 했어.’

민수는 오른손에 쥔 연필을 책상 위에 내려놓고, 나를 한 번 쓰다듬더니 품에 꼭 안았어. 나는 난생 처음 누군가의 품에 안겼지. 얼마나 가슴이 벅차오르며 행복했는지 말로는 다 표현할 수 없단다. 민수는 나를 내려놓고 다시 숙제에 열중했어. 그리고 한 시간쯤 지나자 민수는 내일 학교에 가져갈 교과서와 과제물을 책가방에 넣었지.

민수는 벽에 걸린 시계를 힐끔 쳐다보고 나서 나를 집어 들었어. 그리고 벽에 기대어 책을 소리 내어 읽기 시작했지. 얼마나 가슴이 떨리는 순간이었는지 몰라.

『로봇 소녀 미리』
안녕. 내 이름은 미리야. 미리는 미리내에서 따온 말인데 은하수의 순우리말이래. 요즘은 한밤중에도 불빛이 많아 별이 잘 보이지 않지만, 혹시 시골에 가본 적이 있다면 밤하늘에 강처럼 흐르는 별들을 보았을 거야. 마치 금색 은색 종이를 하늘에 뿌린 것처럼 밝게 빛나는 별들 말이지. 그게 바로 은하수야…….

민수는 30분쯤 책을 읽고 나더니 시계를 한 번 더 쳐다보았어. 그리고 잠시 망설이는 표정을 지었지.

“꼬르륵.”

갑자기 민수의 뱃속에서 배고프다는 신호가 왔어. 이제는 더 이상 참을 수 없었는지 나를 들고 주방으로 갔어. 민수는 서랍에서 컵라면을 꺼낸 다음 전기포트에 물을 끓였지. 30초 만에 물이 다 끓자 조심스럽게 컵라면에 뜨거운 물을 부었어.

나는 민수가 컵라면 위에 나를 올려둘까 봐 속으로 걱정을 했어. 보통 사람들은 책을 냄비 받침이나 컵라면 뚜껑으로 자주 이용하잖아. 하지만 민수는 다행히 그런 아이가 아니었어. 2분이 지나자 민수는 컵라면 뚜껑을 완전히 벗겨 낸 다음 후루룩후루룩 불어가며 맛있게 먹었지. 얼마나 잘 먹는지 나까지 배가 고프더라니까.

배가 빵빵하게 부른 민수는 주방을 정리한 다음, 작은방으로 돌아와 벽에 기대어 나를 읽었어. 키득거리며 웃기도 하고, 슬픈 표정을 짓기도 하며 책 속으로 빠져들었지. 민수는 그렇게 30분쯤 책을 읽더니 어느새 꾸벅꾸벅 졸기 시작했어. 오늘 못된 아이들과 한바탕 전쟁을 치렀으니 피곤할 만도 하잖아. 나는 민수가 편안하게 잘 수 있도록 책 베개가 되어 주었지. 나를 베고 꿈나라로 들어간 민수는 신나고 멋진 모험을 했어.

“어서 일어나.”

미리가 민수를 흔들어 깨웠다.

민수는 쇳덩이처럼 차가운 미리의 손이 살갗에 닿자 화들짝 놀라 잠에서 깼다.

“너는 혹시……?”

“맞아. 나는 미리야.”

민수는 미리의 모습을 보고 깜짝 놀랐다. 미리는 팔과 다리가 강철로 되어 있었다.

“어서 서둘러. 시간이 없어.”

미리는 민수의 손을 잡고 뛰기 시작했다. 민수는 영문도 모른 채 미리를 따라 숨이 차오를 때까지 힘껏 달렸다. 미리는 폐허처럼 변한 도시 외곽의 비밀 장소로 민수를 데려갔다. 그리고 지금 벌어지고 있는 끔찍한 사건들에 대해서 민수에게 하나씩 털어놓았다.

“데칼코마니 조직이 어린이들을 잡아서 인조인간으로 개조하고 있어. 나는 운이 좋아서 팔과 다리만 강철로 개조됐지. 하지만 데칼코마니 조직에게 복종하는 인공지능 칩을 머리에 강제로 삽입한 어린이들도 무수히 많아.”

“데칼코마니 조직은 뭔데?”

“이 세상을 지배하는 악의 세력이야. 사람들을 선동하고 세뇌하여 멋대로 조종하는 무서운 조직이야. 아무도 이들의 명령을 어길 수 없어.”

“어떻게 그런 일이 일어날 수 있지?”

“30년 전부터 사람들은 귀찮은 일을 하나씩 로봇에게 맡기기 시작했어. 처음에는 청소나 운전 같은 일이었지. 그러다 나중에는 무엇을 고를지, 누구 말을 믿을지까지 로봇에게 물었어. 사람들은 책도 읽지 않았고, 스스로 생각하는 일도 점점 귀찮아했지. 결국 정치가와 과학자들은 그런 사람들을 마음대로 움직일 수 있게 되었어.”

“그들만의 세상이라니? 그게 어떤 세상인데?”

“2078년 이후 갓난아이의 울음소리는 더 이상 들리지 않았어. 사람들은 서로 함께 살아가는 것조차 귀찮아했지. 가족을 이루는 일도, 아이를 낳는 일도 점점 사라졌어. 결국 사람에게 필요한 사람의 역할까지 로봇이 대신하게 되었어. 인간의 유전자는 실험실에 보관되어 있었기 때문에 사람이 필요하면 그때그때 만들어 냈지. 나도 그렇게 태어났어. 한 달 전에는 인조인간으로 개조하라는 명령을 받았고. 하지만 나는 도망쳤어.”

“그럼 우리는 어떻게 해야 해?”

“데칼코마니 조직을 무너뜨리기 위해서 가장 먼저 해야 할 일은…….”

그때 누군가 집 안으로 들어오며 민수의 이름을 불렀어.

“민수야.”

꿈속에서 미리와 신나는 모험을 하던 민수는 잠에서 깨어났어. 그리고 자리에서 벌떡 일어나 “할머니!” 하고 소리치며 현관으로 달려갔지.

할머니는 민수를 보자 품에 꼭 안아 주며 말했어.

“우리 강아지, 배고프지?”

“아니에요. 저 먼저 컵라면 먹었어요. 할머니가 더 배고프잖아요?”

“그래그래, 할머니가 저녁밥 차릴 테니 잠시만 기다리렴.”

할머니는 실내복으로 갈아입은 다음 주방으로 들어갔어. 할머니가 저녁밥을 준비하는 동안 민수는 오늘 재활용 쓰레기장에서 가져온 동화책을 자랑했지. 할머니는 민수의 이야기에 귀를 기울였어.

“그럼, 저녁밥 먹고 나서 민수가 할머니에게 책 읽어 줄래?”

민수는 고개를 힘차게 끄덕이며 “네!” 하고 대답했지. 그리고 나서 할머니를 도와 식탁을 차렸어. 식탁을 깨끗한 행주로 닦은 다음 숟가락과 젓가락을 가지런히 놓았지.

그런데 까만 벌레 한 마리가 식탁 의자 사이를 기어갔어. 민수는 너무 놀라서 식탁 위에 있던 나를 집어 벌레에게 던지려고 했지. 하지만 차마 책으로 벌레를 죽일 수 없었는지, 휴지 한 장을 뽑아 조심스럽게 벌레를 집었어. 그리고 창밖으로 살며시 내보내 주었지.

저녁밥을 다 먹은 민수는 할머니와 함께 식탁을 정리했어. 할머니가 설거지까지 마치고 의자에 앉자, 민수는 동화책을 펼쳐 소리 내어 읽기 시작했지. 또박또박 책을 읽는 민수의 모습이 귀엽고 사랑스러운지 할머니의 입가에 미소가 가득했어.

민수가 책 읽기를 마치자 할머니는 이렇게 말했어.

“민수야, 이 세상에서 책이 왕초란다.”

-끝-'''

paras = raw.split("\n\n")
body_parts=[]
for p in paras:
    if "\n" in p:
        lines=p.splitlines()
        body_parts.append("<p>"+ "<br>\n".join(html.escape(line) for line in lines) +"</p>")
    else:
        body_parts.append("<p>"+html.escape(p)+"</p>")
body="\n".join(body_parts)

ko_page=f'''---
---
<!doctype html>
<html lang="ko">
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
  <title>책이 왕초야 - Jin-in-Seoul</title>
  <meta name="description" content="책이 왕초야 — 버려진 동화책이 책을 처음 가져 보는 아이 민수를 만나며 다시 자신의 의미를 발견하는 Jin-in-Seoul의 어린이 단편동화.">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{story_url}">
  <link rel="alternate" hreflang="ko" href="{story_url}">
  <link rel="alternate" hreflang="x-default" href="{story_url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="책이 왕초야 - Jin-in-Seoul">
  <meta property="og:description" content="버려진 동화책이 책을 처음 가져 보는 아이 민수를 만나며 다시 자신의 의미를 발견하는 Jin-in-Seoul의 어린이 단편동화.">
  <meta property="og:url" content="{story_url}">
  <meta property="og:site_name" content="Jin-in-Seoul">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="책이 왕초야 - Jin-in-Seoul">
  <meta name="twitter:description" content="버려진 동화책이 책을 처음 가져 보는 아이 민수를 만나며 다시 자신의 의미를 발견하는 Jin-in-Seoul의 어린이 단편동화.">
  <script type="application/ld+json" data-seo="site">
{{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "name": "책이 왕초야",
  "alternateName": "Books Rule!",
  "url": "{story_url}",
  "inLanguage": "ko",
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
    <nav class="contents-nav" aria-label="목차"><a href="/short-stories/">목차</a></nav>

    <h1>책이 왕초야</h1>
    <article class="prose">
{body}
    </article>

    {{% include footer.html %}}
  </main>
</body>
</html>
'''

hub=f'''---
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
  <meta name="description" content="Books Rule! — a children’s short story by Jin-in-Seoul. Korean edition available now; additional language editions will follow.">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{hub_url}">
  <link rel="alternate" hreflang="ko" href="{story_url}">
  <link rel="alternate" hreflang="x-default" href="{story_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Books Rule! - Jin-in-Seoul">
  <meta property="og:description" content="A children’s short story by Jin-in-Seoul. Korean edition available now.">
  <meta property="og:url" content="{hub_url}">
  <meta property="og:site_name" content="Jin-in-Seoul">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Books Rule! - Jin-in-Seoul">
  <meta name="twitter:description" content="A children’s short story by Jin-in-Seoul. Korean edition available now.">
  <script type="application/ld+json" data-seo="site">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Books Rule!",
  "url": "{hub_url}",
  "inLanguage": "en"
}}
  </script>
  <link rel="stylesheet" href="../../assets/style.css?v=046">
</head>
<body>
  <main class="shell">

    {{% include header.html %}}
    <h1>Books Rule!</h1>
    <p class="deck">Choose a language.</p>
    <nav class="language-list" aria-label="Language selection">
      <a href="ko/" lang="ko">한국어</a>
    </nav>
    {{% include footer.html %}}
  </main>
</body>
</html>
'''

(ROOT/f"short-stories/{slug}/ko").mkdir(parents=True,exist_ok=True)
(ROOT/f"short-stories/{slug}/ko/index.html").write_text(ko_page,encoding="utf-8")
(ROOT/f"short-stories/{slug}").mkdir(parents=True,exist_ok=True)
(ROOT/f"short-stories/{slug}/index.html").write_text(hub,encoding="utf-8")

# Short Stories index: append as last card.
p=ROOT/"short-stories/index.html"
s=p.read_text(encoding="utf-8")
if f'href="{slug}/ko/"' not in s:
    card=f'''
      <article class="work">
        <h3>
          <a class="work-link" href="{slug}/ko/">
            Books Rule!
          </a>
        </h3>
        <p>
          A discarded storybook finds a child who has never owned a book before, and discovers what it means to be read, loved, and needed.
        </p>
        <p>
          <a href="{slug}/ko/">한국어</a>
        </p>
      </article>
'''
    s=s.replace("\n    </section>\n\n    {% include footer.html %}",card+"\n    </section>\n\n    {% include footer.html %}")
p.write_text(s,encoding="utf-8")

# Human site map: append to Short Stories list.
p=ROOT/"site-map/index.html"
s=p.read_text(encoding="utf-8")
if f"/short-stories/{slug}/ko/" not in s:
    needle='''          <li>
            <span class="map-title">The Basics of Logic</span>'''
    pos=s.find(needle)
    if pos<0: raise RuntimeError("Short Stories anchor not found")
    end=s.find("          </li>",pos)
    end=s.find("\n",end)+1
    item=f'''          <li>
            <span class="map-title">Books Rule!</span>
            <span aria-hidden="true"> — </span>
            <span class="map-languages">
              <a href="/short-stories/{slug}/ko/">한국어</a>
            </span>
          </li>
'''
    s=s[:end]+item+s[end:]
p.write_text(s,encoding="utf-8")

# Publication log: prepend Oct 5 section.
p=ROOT/"publication-log/index.html"
s=p.read_text(encoding="utf-8")
if "October 5, 2026" not in s:
    marker='''    <div class="publication-log">'''
    section='''    <div class="publication-log">
      <section>
        <h2>October 5, 2026</h2>
        <h3>Short Stories</h3>
        <ul>
          <li>Korean edition — <em>책이 왕초야</em> (<em>Books Rule!</em>) added</li>
        </ul>
      </section>
'''
    s=s.replace(marker,section,1)
p.write_text(s,encoding="utf-8")

# Sitemap: add hub and KO page before closing urlset.
p=ROOT/"sitemap.xml"
s=p.read_text(encoding="utf-8")
for u in (hub_url,story_url):
    if f"<loc>{u}</loc>" not in s:
        block=f'''  <url>
    <loc>{u}</loc>
  </url>
'''
        s=s.replace("</urlset>",block+"</urlset>")
p.write_text(s,encoding="utf-8")

# Validate body against raw source exactly after HTML unescape / br restoration.
out=(ROOT/f"short-stories/{slug}/ko/index.html").read_text(encoding="utf-8")
article=re.search(r'<article class="prose">\n(.*?)\n    </article>',out,re.S).group(1)
decoded=[]
for m in re.finditer(r"<p>(.*?)</p>",article,re.S):
    t=html.unescape(re.sub(r"<br>\n?", "\n", m.group(1)))
    decoded.append(t)
reconstructed="\n\n".join(decoded)
assert reconstructed==raw, "Korean text/paragraphs changed"

# Validate SEO and navigation.
assert out.count('rel="canonical"')==1
assert 'hreflang="ko"' in out and 'hreflang="x-default"' in out
assert 'alternateName": "Books Rule!"' in out
assert f'<loc>{story_url}</loc>' in (ROOT/"sitemap.xml").read_text(encoding="utf-8")
assert f'<loc>{hub_url}</loc>' in (ROOT/"sitemap.xml").read_text(encoding="utf-8")
assert f'href="{slug}/ko/"' in (ROOT/"short-stories/index.html").read_text(encoding="utf-8")
print("Books Rule! Korean publication validated; source text and paragraph boundaries are exact.")
