(function () {
  'use strict';
  var form = document.getElementById('search-form');
  var field = document.getElementById('search-query');
  var language = document.getElementById('search-language');
  var results = document.getElementById('search-results');
  var status = document.getElementById('search-status');
  var indexPromise;
  function normalize(s) { return String(s || '').normalize('NFKC').toLocaleLowerCase().replace(/\s+/g, ' ').trim(); }
  function loadIndex() {
    if (!indexPromise) indexPromise = fetch('/search-index.json', {cache:'no-cache'}).then(function(r){
      if(!r.ok) throw new Error('Index unavailable');
      return r.json();
    }).then(function(data) {
      if (!Array.isArray(data)) throw new Error('Invalid index');
      return data;
    });
    return indexPromise;
  }
  function matchPosition(text, query) {
    var original = String(text || '');
    var plain = normalize(original), needle = normalize(query);
    var direct = plain.indexOf(needle);
    if (direct >= 0) return direct;
    if (!/[가-힣ㄱ-ㅎㅏ-ㅣ]/.test(needle)) return -1;
    var compactNeedle = needle.replace(/\s+/g, '');
    var compact = '', positions = [];
    for (var i = 0; i < original.length; i++) {
      if (!/\s/.test(original[i])) {
        positions.push(i);
        compact += original[i];
      }
    }
    var offset = compact.normalize('NFKC').toLocaleLowerCase().indexOf(compactNeedle);
    return offset < 0 ? -1 : positions[offset];
  }
  function excerpt(text, query) {
    var position = matchPosition(text, query);
    if (position < 0) return text.slice(0, 220);
    var start = Math.max(0, position - 95);
    var end = Math.min(text.length, position + query.length + 125);
    return (start ? '…' : '') + text.slice(start, end).trim() + (end < text.length ? '…' : '');
  }
  function runSearch() {
    var q = field.value.trim(), lang = language.value;
    results.replaceChildren();
    if(!q) {status.textContent='Enter a word or phrase to search published works.';return;}
    status.textContent='Searching…';
    loadIndex().then(function(items) {
      var needle=normalize(q);
      var hits=items.filter(function(item) {
        if(lang !== 'all' && item.lang !== lang) return false;
        return matchPosition(item.title, q) >= 0 || matchPosition(item.text, q) >= 0;
      }).map(function(item) {
        var titleHit=matchPosition(item.title,q)>=0;
        var at=matchPosition(item.text,q);
        return {item:item, titleHit:titleHit, at:at, score:(titleHit?100000:0)+(at<0?0:Math.max(0,10000-at))};
      }).sort(function(a,b){return b.score-a.score;});
      status.textContent=hits.length+' result'+(hits.length===1?'':'s')+' found.';
      hits.forEach(function(hit) {
        var item=hit.item;
        var article=document.createElement('article');article.className='search-result';
        var h=document.createElement('h2'), link=document.createElement('a');
        link.href=item.url;link.textContent=item.title || item.url;h.appendChild(link);
        var meta=document.createElement('p');meta.className='search-result-meta';meta.textContent=item.lang.toUpperCase();
        var snippet=document.createElement('p');snippet.className='search-result-excerpt';
        snippet.textContent=excerpt(item.text,q);
        article.append(h,meta,snippet);results.appendChild(article);
      });
    }).catch(function() {
      status.textContent='Search index could not be loaded. Please try again later.';
    });
  }
  form.addEventListener('submit',function(e){e.preventDefault();runSearch();});
  language.addEventListener('change',function(){if(field.value.trim())runSearch();});
  var params=new URLSearchParams(location.search);
  if(params.has('q')) {field.value=params.get('q') || '';if(['en','fr','ja','ko'].includes(params.get('lang')))language.value=params.get('lang');runSearch();}
})();