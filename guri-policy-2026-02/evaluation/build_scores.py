"""scores.tsv -> scores.md 누적 순위표 생성. 사용: python3 build_scores.py "갱신시각 문구" """
import csv, sys, collections
rows = list(csv.DictReader(open('scores.tsv', encoding='utf-8'), delimiter='\t'))
K = ['근거', '효과', '실현', '창의', '측정', '어필']
for r in rows:
    r['total'] = sum(int(r[k]) for k in K)
    t = r['total']
    r['grade'] = 'A' if t >= 72 else 'B' if t >= 65 else 'C' if t >= 58 else 'D'
rows.sort(key=lambda r: (-r['total'], -int(r['효과']), r['id']))
stamp = sys.argv[1] if len(sys.argv) > 1 else ''
cnt = collections.Counter(r['grade'] for r in rows)
files = sorted({r['file'] for r in rows})
out = []
out.append('# 구리시 정책제안 아이디어 누적 순위표\n')
out.append(f'최종 갱신: {stamp} · 채점 완료 {len(rows)}건 (파일 {files[0]}~{files[-1]}) · A {cnt["A"]} / B {cnt["B"]} / C {cnt["C"]} / D {cnt["D"]}\n')
out.append('채점 기준은 [README.md](README.md), 회차별 판단 근거는 [log/](log/)에 있다. 원본 점수 데이터는 `scores.tsv`.\n')
out.append('## TOP 10\n')
out.append('| 순위 | ID | 아이디어 | 총점 | 핵심 이유 |\n|---|---|---|---|---|')
for i, r in enumerate(rows[:10], 1):
    out.append(f"| {i} | {r['id']} | {r['title']} | **{r['total']}** | {r['판단근거']} |")
out.append('\n## 전체 순위\n')
out.append('| 순위 | ID | 등급 | 총점 | 근거/20 | 효과/25 | 실현/20 | 창의/15 | 측정/10 | 어필/10 | 아이디어 | 원본 |\n|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, r in enumerate(rows, 1):
    out.append(f"| {i} | {r['id']} | {r['grade']} | {r['total']} | " + ' | '.join(r[k] for k in K) + f" | {r['title']} | [{r['file']}](../2026-11-13-{r['file']}.md) |")
open('scores.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(f"{r['id']} {r['total']} {r['grade']}" for r in rows[:15]))
