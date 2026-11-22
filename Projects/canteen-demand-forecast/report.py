"""Build a portable HTML report from evaluated forecast results."""
from forecast import MODELS, mae


def write_report(result, path):
    rows = result["test"]
    selected = result["winner"]
    maximum = max(1, max(max(actual, models[selected]) for _, actual, models in rows))
    bars = []
    for day, actual, models in rows:
        forecast = models[selected]
        bars.append(f'<tr><th scope="row">{day:%d %b}</th><td>{actual}</td><td>{forecast}</td>'
                    f'<td class="plot"><i style="width:{100 * actual / maximum:.2f}%"></i>'
                    f'<i class="estimate" style="width:{100 * forecast / maximum:.2f}%"></i></td></tr>')
    scores = "".join(f'<tr><th scope="row">{model}</th><td>{mae(result["validation"], model):.2f}</td>'
                     f'<td>{mae(rows, model):.2f}</td></tr>' for model in MODELS)
    html = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Canteen demand | Forecast report</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f2e9;color:#182e29;font:16px/1.5 'Segoe UI',sans-serif}}
main{{max-width:860px;margin:auto;padding:36px clamp(18px,5vw,52px)}}h1,h2,p{{margin:0}}
h1,h2{{font-family:Georgia,serif;font-weight:500}}h1{{font-size:clamp(34px,7vw,62px);line-height:1.1}}
h2{{font-size:27px;margin:28px 0 8px}}.mast{{border-bottom:2px solid #213f38;padding-bottom:16px}}
.next{{background:#163f36;color:white;border-radius:8px;padding:18px 22px;margin:20px 0;display:flex;align-items:center;gap:22px;flex-wrap:wrap}}
strong{{font-size:38px;line-height:1.1}}table{{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}}
td,th{{border-bottom:1px solid #cdd3c8;padding:6px 4px;text-align:right}}th:first-child{{text-align:left}}
.plot{{width:52%;padding-left:12px}}i{{display:block;background:#206957;height:6px;border-radius:3px}}i.estimate{{background:#af5a28;margin-top:3px}}
small{{display:block;font-size:14px}}.legend{{font-size:14px;margin-bottom:8px}}.key{{display:inline-block;width:13px;height:7px;background:#206957;margin-right:3px}}
.key.second{{background:#af5a28;margin-left:12px}}thead th{{font-size:13px}}@media(max-width:500px){{.plot{{width:36%}}}}
</style><main><header class="mast"><h1>Canteen demand</h1>
<p>One-day-ahead meal forecast · {result["next_day"]:%d %B %Y}</p></header>
<section class="next"><strong>{result["forecast"]} meals</strong>
<span>{selected}<small>Selected by validation error</small></span></section>
<h2>Model comparison</h2><p>Average absolute error, in meals per day. Lower values are better.</p>
<table><thead><tr><th>Model</th><th>Validation</th><th>Test</th></tr></thead><tbody>{scores}</tbody></table>
<h2>Forecast vs. actual</h2><p class="legend"><b class="key"></b> Actual
<b class="key second"></b> Forecast · final {len(rows)} days</p>
<table><thead><tr><th>Date</th><th>Actual</th><th>Forecast</th><th>Daily comparison</th></tr></thead>
<tbody>{''.join(bars)}</tbody></table></main></html>"""
    path.write_text(html, encoding="utf-8")
