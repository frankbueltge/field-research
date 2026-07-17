import sys, json, numpy as np, pandas as pd
df = pd.read_parquet(sys.argv[1]).copy()
df["mean_score"] = df["scores"].apply(lambda a: float(np.mean(a)) if a is not None and len(a)>0 else np.nan)
def is_accept(d): return d.strip().lower().startswith("accept")
def is_reject(d): return d in ("Reject","Desk rejected")
df["y"] = df["decision"].apply(lambda d: 1 if is_accept(d) else (0 if is_reject(d) else -1))
sub = df.dropna(subset=["mean_score"])
sub = sub[sub["y"]>=0]
ms = sub["mean_score"].values; y = sub["y"].values
# Bin mean scores at 0.25 resolution across the observed range
lo, hi = np.floor(ms.min()*4)/4, np.ceil(ms.max()*4)/4
edges = np.arange(lo, hi+0.25, 0.25)
bins = []
for i in range(len(edges)-1):
    m = (ms>=edges[i]) & (ms<edges[i+1])
    a = int(y[m].sum()); n = int(m.sum()); r = n-a
    if n>0:
        bins.append({"lo":round(float(edges[i]),2),"hi":round(float(edges[i+1]),2),"accept":a,"reject":r})
# Client-side BA reconstruction from bins: threshold t predicts accept if bin center >= t
def ba_from_bins(bins, t):
    tp=fn=tn=fp=0
    for b in bins:
        c=(b["lo"]+b["hi"])/2
        if c>=t: tp+=b["accept"]; fp+=b["reject"]
        else: fn+=b["accept"]; tn+=b["reject"]
    tpr = tp/(tp+fn) if tp+fn else 0
    tnr = tn/(tn+fp) if tn+fp else 0
    return 0.5*(tpr+tnr)
# sweep bin edges as thresholds
cands = sorted(set([b["lo"] for b in bins]+[ (b["lo"]+b["hi"])/2 for b in bins]))
best=max((ba_from_bins(bins,t),t) for t in cands)
totA=sum(b["accept"] for b in bins); totR=sum(b["reject"] for b in bins)
print("bins:",len(bins),"totalA:",totA,"totalR:",totR,"total:",totA+totR,"accept_rate:",round(totA/(totA+totR),3))
print("best BA from bins:",round(best[0],4),"at t>=",round(best[1],2))
# also BA at a few round thresholds
for t in [5.0,5.5,5.69,5.75,6.0]:
    print(f"  BA at t>={t}: {ba_from_bins(bins,t):.4f}")
out={"source":{"dataset":"berenslab/iclr-dataset data/iclr24v2.parquet","sha256":"f486c7a0f58c71005ab8f86e6128038ca523a9efe7feb4ab353b37f789d47fb0","paper_url":"https://github.com/berenslab/iclr-dataset","described_in":"https://arxiv.org/abs/2404.08403"},
     "label_rule":"y=1 if decision startswith 'accept' (case-insensitive); y=0 if decision in {Reject, Desk rejected}; Withdrawn/Invite-to-Workshop excluded",
     "years":"2017-2024","n":totA+totR,"n_accept":totA,"n_reject":totR,"bin_width":0.25,"bins":bins,
     "reference":{"tool_ba":0.69,"tool_ba_ci":0.04,"tool_n":1000,"tool_years":"2017-2024",
                  "committee_ba":0.66,"committee_source":"Human (NeurIPS 2021) inter-committee consistency, arXiv:2306.03262; Table 1 of arXiv:2606.15497",
                  "constant_ba":0.50,"paper_baselines":{"random":0.50,"always_reject":0.50},
                  "our_n":totA+totR,"note":"tool_ba is arXiv:2606.15497 Table 1 Automated Reviewer row, 2017-2024 set (n=1000). committee_ba is that table's Human(NeurIPS) row. constant_ba matches the paper's own Random/Always-Reject baselines."}}
json.dump(out, open(sys.argv[2],"w"), indent=0)
print("wrote", sys.argv[2])
