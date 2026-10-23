---
title: 'Junk Removal Pricing Calculator (Load-Size Estimate From Your Own Costs)'
description: 'A free calculator for junk-removal jobs: enter your own labor, truck, disposal and overhead costs and your target margin to estimate a price by load size. All assumptions are editable.'
verified: '2026-10-12'
short: Pricing Calculator
---
# Junk Removal Pricing Calculator

**This is an estimate, not a market rate.** It works out a price from **your** costs and **your** target margin. The numbers already in the boxes are **placeholders only**, so replace every one with your own figures. We don't publish "typical" market prices because we haven't verified any.

<div class="calc" id="calc">
<p><label>Load size (fraction of a full truck) <select id="frac"><option value="0.125">1/8</option><option value="0.25">1/4</option><option value="0.5" selected>1/2</option><option value="0.75">3/4</option><option value="1">Full</option></select></label></p>
<p><label>Crew size (people) <input id="crew" type="number" min="1" step="1" value="2"></label></p>
<p><label>Hours on the job, including the drive and the dump run <input id="hours" type="number" min="0" step="0.25" value="2"></label></p>
<p><label>Labor cost per person per hour ($, including payroll costs) <input id="wage" type="number" min="0" step="0.5" value="25"></label></p>
<p><label>Truck cost per hour ($: fuel, insurance, payments, upkeep) <input id="truck" type="number" min="0" step="0.5" value="20"></label></p>
<p><label>Disposal fee for a FULL load at your facility ($) <input id="dumpfull" type="number" min="0" step="1" value="100"></label></p>
<p><label>Minimum disposal charge at your facility ($, 0 if none) <input id="dumpmin" type="number" min="0" step="1" value="0"></label></p>
<p><label>Item surcharges you pay ($ total: mattresses, tires, freon, etc.) <input id="items" type="number" min="0" step="1" value="0"></label></p>
<p><label>Overhead added to costs (%: ads, software, phone, insurance) <input id="ovh" type="number" min="0" max="200" step="1" value="15"></label></p>
<p><label>Target profit margin (% of price) <input id="margin" type="number" min="0" max="90" step="1" value="30"></label></p>
<p><label>Minimum job price you'll accept ($) <input id="minjob" type="number" min="0" step="1" value="0"></label></p>
</div>

<div class="calc-out" aria-live="polite"><p><strong>Estimated price: <span id="price">-</span></strong></p><p id="breakdown"></p></div>

<script>
(function(){
  var ids=["frac","crew","hours","wage","truck","dumpfull","dumpmin","items","ovh","margin","minjob"];
  function v(i){var x=parseFloat(document.getElementById(i).value);return isNaN(x)?0:x;}
  function f(n){return "$"+n.toFixed(2);}
  function run(){
    var labor=v("crew")*v("hours")*v("wage"), truck=v("hours")*v("truck");
    var dump=Math.max(v("frac")*v("dumpfull"), v("dumpmin"))+v("items");
    var cost=(labor+truck+dump)*(1+v("ovh")/100);
    var m=Math.min(v("margin"),90)/100, price=cost/(1-m), floor=v("minjob");
    var applied=price<floor; if(applied) price=floor;
    document.getElementById("price").textContent=f(price);
    document.getElementById("breakdown").textContent="Labor "+f(labor)+" + truck "+f(truck)+" + disposal "+f(dump)+
      " = "+f(labor+truck+dump)+"; with overhead "+f(cost)+"; price = cost / (1 - margin)"+(applied?" (raised to your minimum job price)":"")+".";
  }
  ids.forEach(function(i){document.getElementById(i).addEventListener("input",run);});
  run();
})();
</script>

## How the Math Works

1. **Labor** = crew × hours × cost per person-hour.
2. **Truck** = hours × truck cost per hour.
3. **Disposal** = load fraction × your full-load disposal fee, or your facility's minimum charge if that's higher, plus item surcharges.
4. **Cost with overhead** = (labor + truck + disposal) × (1 + overhead %).
5. **Price** = cost ÷ (1 − margin). A 30% margin isn't the same as a 30% markup: marking a $100 cost up by 30% gives $130, but a 30% margin needs about $142.86.

**Limits:** this assumes disposal scales with load size. Many facilities charge by weight, or have minimums that don't, so use your facility's real rate structure. Small loads still cost a whole truck trip, which is why the hours and the minimum job price matter. Prices for your area depend on local competition and costs, which we don't know.

Need real disposal costs? Start with our [city disposal costs](/for-haulers/dump-fees/) page (residential programs only) and your local facility's commercial rate.

**Affiliate disclosure:** HowToDumpIt is an independent information guide. This calculator contains no affiliate links.
