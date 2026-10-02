/* Natal chart wheel for the natal-report skill — REPORT-SPEC.md §6 "The wheel".
   Data-driven: reads window.NATAL_WHEEL, which build.py injects from chart.json#wheel:
     { asc: <deg|null>, mc: <deg|null>,
       bodies: [{lon, g, t, w}],   lon = ecliptic longitude, g = glyph, t = degree label, w = 1 heavy
       aspects: [[i, j, 'cnj'|'hard'|'soft'], …] }
   asc === null (no birth time) draws the wheel with 0° Aries on the left and no angle axes.
   Colours come from the page's CSS custom properties, so the wheel follows the theme.
   NOTE spread() is order-preserving on purpose — see REPORT-SPEC.md, "The wheel". */
(function(){
  var cv=document.getElementById('wheel'); if(!cv) return;
  var D=window.NATAL_WHEEL; if(!D||!D.bodies||!D.bodies.length) return;
  var ctx=cv.getContext('2d'), VS='︎';
  var SIGNS=['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'].map(function(s){return s+VS});
  var hasAngles=(D.asc!==null&&D.asc!==undefined);
  var ASC=hasAngles?D.asc:0, MC=hasAngles?D.mc:null;
  var B=D.bodies, ASP=D.aspects||[];
  function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim()}
  function ang(l){return (180+(l-ASC))*Math.PI/180}
  function pt(cx,cy,r,l){var a=ang(l);return [cx+r*Math.cos(a), cy-r*Math.sin(a)]}

  // spread crowded glyphs apart in angle, order-preserving, each cluster
  // re-centred on the true mean so the pile-up stays where it really is
  function spread(lons,minSep){
    var n=lons.length; if(n<2) return lons.slice();
    var idx=lons.map(function(v,i){return i}).sort(function(a,b){return lons[a]-lons[b]});
    var gaps=idx.map(function(v,k){return (lons[idx[(k+1)%n]]-lons[idx[k]]+360)%360});
    var cut=0; for(var k=1;k<n;k++) if(gaps[k]>gaps[cut]) cut=k;
    var order=[]; for(k=0;k<n;k++) order.push(idx[(cut+1+k)%n]);
    var base=lons[order[0]];
    var t=order.map(function(i){return (lons[i]-base+360)%360});
    var p=t.slice();
    for(var pass=0;pass<80;pass++){
      for(k=1;k<n;k++) p[k]=Math.max(p[k], p[k-1]+minSep);
      for(k=n-2;k>=0;k--) p[k]=Math.min(p[k], p[k+1]-minSep);
      var changed=false, a=0;
      while(a<n){
        var b=a;
        while(b+1<n && p[b+1]-p[b] <= minSep+1e-7) b++;
        if(b>a){
          var cur=0,tru=0;
          for(var m=a;m<=b;m++){cur+=p[m];tru+=t[m]}
          var sh=(tru-cur)/(b-a+1);
          if(Math.abs(sh)>1e-7){for(m=a;m<=b;m++)p[m]+=sh; changed=true}
        }
        a=b+1;
      }
      if(!changed) break;
    }
    var out=new Array(n);
    order.forEach(function(i,k){out[i]=(base+p[k]%360+360)%360});
    return out;
  }

  function draw(){
    var rect=cv.getBoundingClientRect(), dpr=Math.max(1,Math.min(3,devicePixelRatio||1));
    var w=Math.max(240,rect.width||240), h=w;
    cv.width=w*dpr; cv.height=h*dpr; cv.style.height=w+'px';
    ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,w,h);
    // matte to the page ground so a PDF never gets a white box behind the wheel
    ctx.fillStyle=css('--ground')||'#fff'; ctx.fillRect(0,0,w,h);
    var cx=w/2, cy=h/2, R=w*0.40;
    var rOut=R, rSign=R*0.885, rIn=R*0.77, rGly=R*0.655, rLab=R*0.578, rWeb=R*0.455;
    var ink=css('--ink'), brass=css('--brass'), brassB=css('--brass-bright'), star=css('--star'),
        ring=css('--wheel-ring'), tick=css('--wheel-tick'), web=css('--wheel-web'), faint=css('--ink-faint');

    // ---- aspect web (drawn from TRUE longitudes) ----
    ASP.forEach(function(a){
      if(!B[a[0]]||!B[a[1]]) return;
      var p=pt(cx,cy,rWeb,B[a[0]].lon), q=pt(cx,cy,rWeb,B[a[1]].lon);
      if(a[2]==='hard'){ctx.strokeStyle=star;ctx.globalAlpha=.62;ctx.lineWidth=1.2;ctx.setLineDash([])}
      else if(a[2]==='cnj'){ctx.strokeStyle=brass;ctx.globalAlpha=.5;ctx.lineWidth=1.4;ctx.setLineDash([])}
      else {ctx.strokeStyle=star;ctx.globalAlpha=.34;ctx.lineWidth=1;ctx.setLineDash([2,4])}
      ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(q[0],q[1]);ctx.stroke();
      ctx.setLineDash([]);ctx.globalAlpha=1;
    });
    ctx.strokeStyle=web;ctx.lineWidth=1;
    ctx.beginPath();ctx.arc(cx,cy,rWeb,0,7);ctx.stroke();

    // ---- degree ticks ----
    for(var d0=0;d0<360;d0++){
      var isS=(d0%30===0), is10=(d0%10===0), is5=(d0%5===0);
      var len=isS?R*0.09:(is10?R*0.048:(is5?R*0.03:R*0.015));
      var p1=pt(cx,cy,rOut,d0), p2=pt(cx,cy,rOut-len,d0);
      ctx.strokeStyle=isS?ring:tick; ctx.lineWidth=isS?1.4:(is10?1:0.7);
      ctx.beginPath();ctx.moveTo(p1[0],p1[1]);ctx.lineTo(p2[0],p2[1]);ctx.stroke();
    }
    ctx.strokeStyle=ring;ctx.lineWidth=1.4;
    [rOut,rIn].forEach(function(r){ctx.beginPath();ctx.arc(cx,cy,r,0,7);ctx.stroke()});

    // ---- sign glyphs ----
    ctx.fillStyle=star;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.font='500 '+(R*0.10)+'px "Iowan Old Style",Palatino,Georgia,serif';
    for(var s=0;s<12;s++){var g=pt(cx,cy,rSign,s*30+15);ctx.fillText(SIGNS[s],g[0],g[1])}

    // ---- angle axes ----
    function axis(l,strong){
      var a=pt(cx,cy,rOut,l), b=pt(cx,cy,rOut,l+180);
      ctx.strokeStyle=strong?brass:faint; ctx.lineWidth=strong?1.8:1;
      if(!strong)ctx.setLineDash([3,4]);
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();ctx.setLineDash([]);
    }
    if(hasAngles){ axis(MC,false); axis(ASC,true); }

    // ---- bodies: true tick on ring, leader line, spread glyph, label ----
    var disp=spread(B.map(function(b){return b.lon}), 13);
    B.forEach(function(b,i){
      var tl=b.lon, dl=disp[i];
      var q1=pt(cx,cy,rIn,tl), q2=pt(cx,cy,rIn-R*0.035,tl);
      ctx.strokeStyle=b.w?brass:tick; ctx.lineWidth=b.w?1.4:1;
      ctx.beginPath();ctx.moveTo(q1[0],q1[1]);ctx.lineTo(q2[0],q2[1]);ctx.stroke();
      var g=pt(cx,cy,rGly,dl);
      if(Math.abs(((dl-tl+540)%360)-180)>0.6){
        ctx.strokeStyle=tick;ctx.lineWidth=0.8;ctx.globalAlpha=.75;
        ctx.beginPath();ctx.moveTo(q2[0],q2[1]);ctx.lineTo(g[0],g[1]);ctx.stroke();ctx.globalAlpha=1;
      }
      ctx.fillStyle=b.w?brassB:ink;
      ctx.font=(b.w?'600 ':'500 ')+(R*(b.w?0.105:0.09))+'px "Iowan Old Style",Palatino,Georgia,serif';
      ctx.fillText(b.g+VS,g[0],g[1]);
      var t=pt(cx,cy,rLab,dl);
      ctx.fillStyle=faint;ctx.font='500 '+(R*0.05)+'px ui-monospace,Menlo,monospace';
      ctx.fillText(b.t,t[0],t[1]);
    });

    // ---- angle labels ----
    if(hasAngles){
      ctx.font='600 '+(R*0.055)+'px ui-monospace,Menlo,monospace'; ctx.fillStyle=brass;
      function lab(l,txt){var p=pt(cx,cy,rOut+R*0.085,l);ctx.fillText(txt,p[0],p[1])}
      lab(ASC,'ASC'); lab(ASC+180,'DSC'); ctx.fillStyle=faint; lab(MC,'MC'); lab(MC+180,'IC');
    }
    ctx.fillStyle=brass;ctx.beginPath();ctx.arc(cx,cy,R*0.018,0,7);ctx.fill();
  }
  draw();
  addEventListener('resize',draw);
  try{matchMedia('(prefers-color-scheme:dark)').addEventListener('change',draw)}catch(e){}
  new MutationObserver(draw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
})();
