# -*- coding: utf-8 -*-
"""构建 莲之空棉花娃娃收集进度 网页（index.html）"""
import os, json, shutil, re

GEN_SRC = os.path.join(os.environ.get('TEMP', '.'), 'hasu_out', 'gen_xlsx.py')
if not os.path.exists(GEN_SRC):
    GEN_SRC = r'C:\Users\liukai1\AppData\Local\Temp\hasu_out\gen_xlsx.py'
src = open(GEN_SRC, encoding='utf-8').read()
exec(src.split('# ============================ 生成 Excel')[0])  # 定义 R

ROOT = r'C:\Users\liukai1\WorkBuddy\2026-08-06-11-06-55'
OUT_DIR = os.path.join(ROOT, 'hasu_collection')
THUMB_SRC = os.path.join(ROOT, 'hasu_thumbs')
THUMB_DST = os.path.join(OUT_DIR, 'thumbs')
os.makedirs(THUMB_DST, exist_ok=True)

ROLE_INFO = [
    ('乙宗梢', '乙宗梢', '102期生', '已毕业（2025年3月）', 'スリーズブーケ'),
    ('夕雾缀理', '夕霧綴理', '102期生', '已毕业（2025年3月）', 'DOLLCHESTRA'),
    ('藤岛慈', '藤島慈', '102期生', '已毕业（2025年3月）', 'みらくらぱーく！'),
    ('日野下花帆', '日野下花帆', '103期生', '已毕业（2026年3月）', 'スリーズブーケ'),
    ('村野沙耶香', '村野さやか', '103期生', '已毕业（2026年3月）', 'DOLLCHESTRA'),
    ('大泽琉璃乃', '大沢瑠璃乃', '103期生', '已毕业（2026年3月）', 'みらくらぱーく！'),
    ('百生吟子', '百生吟子', '104期生', '现役', 'スリーズブーケ（105期起加入）'),
    ('徒町小铃', '徒町小鈴', '104期生', '现役', 'Edel Note（原）→ DOLLCHESTRA（105期起）'),
    ('安养寺姬芽', '安養寺姫芽', '104期生', '现役', 'Edel Note（原）→ みらくらぱーく！（105期起）'),
    ('桂城泉', '桂城泉', '104期生（105期转入）', '现役', 'Edel Note'),
    ('塞拉斯·柳田·莉莉恩菲尔特', 'セラス柳田リリエンフェルト', '105期生', '现役', 'Edel Note（106期起加入DOLLCHESTRA）'),
    ('锦上真花', '錦上マイカ', '106期生', '现役', '—'),
    ('令泽葵', '令沢葵', '106期生', '现役', '—'),
    ('紫轮澪音', '紫輪みおん', '106期生', '现役', '—'),
]

news_url_base = 'https://www.lovelive-anime.jp/hasunosora/news/detail.php?p='

# 日文角色名 → 中文名映射（统一角色标识）
JA2CN = {j: c for c, j, *_ in ROLE_INFO}
CN2JA = {c: j for c, j, *_ in ROLE_INFO}

def parse_chars(cs):
    """返回角色中文名列表；成套商品返回 None"""
    if '全' in cs or '未逐一' in cs or '各1款' in cs:
        return None
    names = [n.strip().replace('（暂译）', '') for n in cs.replace('／', '/').split('/') if n.strip()]
    return [JA2CN.get(n, n) for n in names] if names else None

def parse_sort_key(launch):
    """从发售/登场日期解析排序键（YYYY-MM-DD），无法解析则返回 9999-99-99"""
    if not launch:
        return '9999-99-99'
    m = re.search(r'(\d{4})年(\d{1,2})月', launch)
    if not m:
        return '9999-99-99'
    y, mo = int(m.group(1)), int(m.group(2))
    d = 1
    dm = re.search(r'(\d{1,2})日', launch)
    if dm:
        d = int(dm.group(1))
    return '%04d-%02d-%02d' % (y, mo, d)

def detect_version(name_ja, how):
    """判断商品版本：含限定字样 → 限定版，否则通常版"""
    hay = (name_ja or '') + (how or '')
    if '限定' in hay or 'オンライン限定' in hay:
        return '限定版'
    return '通常版'

def extract_style(name_zh, chars):
    """从商品名去掉角色名段，得到款式名（如 '趴趴毛绒玩偶"日野下花帆-加贺友禅联名纹样衣装"（S）' → '趴趴毛绒玩偶"加贺友禅联名纹样衣装"（S）'）"""
    if not chars:
        return name_zh
    for c in chars:
        pat = c + '-'
        if pat in name_zh:
            return name_zh.replace(pat, '', 1)
    return name_zh

def extract_style_ja(name_ja, chars):
    """日文款名：按日文角色名去段"""
    if not chars:
        return name_ja
    for c in chars:
        j = CN2JA.get(c)
        if j and (j + '-') in name_ja:
            return name_ja.replace(j + '-', '', 1)
    return name_ja

items = []
for i, it in enumerate(R, 1):
    img_key = it['img']
    img = 'thumbs/' + img_key + '.webp'
    launch = it['launch']
    chars = parse_chars(it['chars_zh'])
    items.append({
        'id': 'n%02d' % i,
        'series': it['series'],
        'nameJa': it['name_ja'],
        'nameZh': it['name_zh'],
        'chars': chars,
        'style': extract_style(it['name_zh'], chars),
        'styleJa': extract_style_ja(it['name_ja'], chars),
        'type': it['type'],
        'size': it['size'],
        'price': it['price'],
        'launch': launch,
        'sortKey': parse_sort_key(launch),
        'reserve': it['reserve'],
        'how': it['how'],
        'url': news_url_base + it['news'],
        'img': img,
        'version': detect_version(it['name_ja'], it['how']),
    })

# GiGO 官网未逐一公布角色，按用户确认补全
gigo_fix = {
    'vol.1': ['日野下花帆', '村野沙耶香', '大泽琉璃乃'],
    'vol.2': ['乙宗梢', '夕雾缀理', '藤岛慈'],
}
for it in items:
    if 'GiGO' in it['series']:
        for k, v in gigo_fix.items():
            if k in it['nameJa']:
                it['chars'] = v
                break

# BANDAI ぬいぐるみマスコット（"一生に夢が咲くように"衣装）全8種：按用户确认补全角色
for it in items:
    if '一生に夢が咲くように' in it['nameJa'] and 'マスコット' in it['nameJa']:
        it['chars'] = ['日野下花帆', '村野沙耶香', '大泽琉璃乃', '百生吟子', '徒町小铃', '安养寺姬芽', '塞拉斯·柳田·莉莉恩菲尔特', '桂城泉']

# 删除：肩挎小包（ショルダーポーチ "一生に夢が咲くように"衣装 全4種）
items = [it for it in items if 'ショルダーポーチ' not in it['nameJa']]

# 毛绒挂件（4楽曲ライブ衣装）全11種：按用户确认补全角色（8人，4ユニット现役成员）
for it in items:
    if 'マスコット' in it['nameJa'] and '一生に夢が咲くように' not in it['nameJa']:
        it['chars'] = ['日野下花帆', '村野沙耶香', '大泽琉璃乃', '百生吟子', '徒町小铃', '安养寺姬芽', '塞拉斯·柳田·莉莉恩菲尔特', '桂城泉']

# 删除：出行小包（おでかけポーチ 4楽曲ライブ衣装 全4種）
items = [it for it in items if 'おでかけポーチ' not in it['nameJa']]

# 删除：趴趴毛绒玩偶～Revival～（SUO限定・再登场）、Qurumaru圆滚滚毛绒玩偶（再登场）——均为再版条目
items = [it for it in items if 'Revival' not in it['nameJa'] and 'きゅるまる' not in it['nameJa']]

# 拆分 Unit Collection Vol.1/2：原记录 how 含"另有SUO限定表情Ver."，拆成 通常版 + 限定版 两条
extra = []
for it in items:
    if 'Unit Collection' in it['nameJa'] and '另有' in (it.get('how') or ''):
        it['how'] = '全国游戏中心景品机'
        it['version'] = '通常版'
        c = dict(it)
        c['id'] = it['id'] + '-lim'
        c['nameZh'] = it['nameZh'] + '（SUO限定表情Ver.）'
        c['nameJa'] = it['nameJa'] + '（SUO限定表情Ver.）'
        c['how'] = 'セガUFOキャッチャーオンライン限定'
        c['version'] = '限定版'
        extra.append(c)
items.extend(extra)
# 按发售/登场时间升序排
items.sort(key=lambda x: x['sortKey'])

roles = [{'cn': c, 'ja': j, 'period': p, 'status': s, 'unit': u} for c, j, p, s, u in ROLE_INFO]

data_json = json.dumps({'items': items, 'roles': roles}, ensure_ascii=False)

# 复制缩略图
copied = 0
for fn in os.listdir(THUMB_SRC):
    if fn.endswith('.webp'):
        shutil.copy2(os.path.join(THUMB_SRC, fn), os.path.join(THUMB_DST, fn))
        copied += 1

# 生成 index.html
tpl_path = os.path.join(OUT_DIR, 'template.html')
html = open(tpl_path, encoding='utf-8').read()
html = html.replace('__DATA__', data_json)
out_path = os.path.join(OUT_DIR, 'index.html')
open(out_path, 'w', encoding='utf-8').write(html)
# 保留 template.html 以便后续修改重建（构建产物为 index.html）

print('items:', len(items), '| roles:', len(roles), '| thumbs copied:', copied)
print('saved:', out_path)
