/* Static, local-only calculator: no cookies, storage or network requests. */
(function () {
  "use strict";
  const data = JSON.parse(document.getElementById("vps-data").textContent);
  const money = n => new Intl.NumberFormat("en-US", {style:"currency", currency:"USD"}).format(n);
  function render() {
    const os = document.getElementById("vps-os").value;
    const ram = Number(document.getElementById("vps-ram").value);
    const term = Number(document.getElementById("vps-term").value);
    const plans = data.plans.filter(p => p.os === os && p.ram_gb >= ram && p.term_months === term).sort((a,b) => a.monthly_usd-b.monthly_usd);
    const root = document.getElementById("vps-results"); root.replaceChildren();
    document.getElementById("vps-status").textContent = plans.length ? `${plans.length} verified offers | ${os} | at least ${ram} GB | ${term} months` : "No verified price for this selection. Try 24 months or a lower RAM requirement. We do not extrapolate promotional rates to other terms.";
    plans.forEach(p => {
      const card = document.createElement("article"); card.className = "vps-card";
      const heading = document.createElement("h3"); heading.textContent = `${p.provider} | ${p.name}`; card.append(heading);
      const rows = [ ["Base upfront subtotal", money(p.monthly_usd * term)], ["Effective monthly", money(p.monthly_usd)], ["Renewal / month", p.renewal_monthly_usd === null ? "Not displayed" : money(p.renewal_monthly_usd)], ["Renewal term subtotal", p.renewal_monthly_usd === null ? "Not displayed" : money(p.renewal_monthly_usd * term)], ["Memory / term", `${p.ram_gb} GB / ${term} months`], ["Setup fee", p.setup_usd === null ? "Not displayed; excluded" : money(p.setup_usd)] ];
      const list = document.createElement("dl"); rows.forEach(([label,value]) => {const dt=document.createElement("dt"), dd=document.createElement("dd");dt.textContent=label;dd.textContent=value;list.append(dt,dd);});card.append(list);
      const source = document.createElement("a"); source.href=p.source_url;source.textContent=`Pricing source | checked ${p.checked}`;card.append(source);root.append(card);
    });
  }
  ["vps-os","vps-ram","vps-term"].forEach(id => document.getElementById(id).addEventListener("change",render)); render();
})();
