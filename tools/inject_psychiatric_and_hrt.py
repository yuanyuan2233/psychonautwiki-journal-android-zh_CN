#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全量精准注入精神类药物与 HRT 激素替代相关药物。
为每种药物配备权威药代动力学 (ADME: 半衰期 t1/2, 达峰时间 Tmax, 生物利用度 F, CYP450 酶谱)、
临床给药途径 (ROA: 起始量, 常规维持量, 强效量, 极量, 时程)、临床适应症、禁忌黑框警示、
原研商品名与全套拼音首字母检索索引。
"""

import os
import sys
import json
import re

try:
    from pypinyin import lazy_pinyin
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "pypinyin"], check=True)
    from pypinyin import lazy_pinyin

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBSTANCES_JSON_PATH = os.path.join(APP_DIR, "app", "src", "main", "assets", "Substances.json")
HELPER_KT_PATH = os.path.join(APP_DIR, "app", "src", "main", "java", "com", "isaakhanimann", "journal", "ui", "tabs", "search", "SubstanceLocalizationHelper.kt")

try:
    from tools.more_curated_drugs import ADDITIONAL_CURATED_DRUGS
except ImportError:
    try:
        from more_curated_drugs import ADDITIONAL_CURATED_DRUGS
    except ImportError:
        ADDITIONAL_CURATED_DRUGS = []


def generate_pinyin_tokens(chinese_text):
    if not chinese_text or not re.search(r'[\u4e00-\u9fa5]', chinese_text):
        return [], []
    tokens = lazy_pinyin(chinese_text)
    if not tokens:
        return [], []
    abbr = "".join([t[0] for t in tokens if t])
    full_clean = "".join(tokens)
    full_apostrophe = "'".join(tokens)
    return [full_apostrophe, full_clean], [abbr] if abbr else []

# 权威精选药物数据集：涵盖精神类（全抗抑郁、抗焦虑、抗精神病、情绪稳定剂、ADHD/促智、抗组胺抗胆碱、解痉肌松、脱瘾）及 HRT 全系
CURATED_DRUGS = [
    # ==========================================
    # 1. 抗抑郁药 (SSRI / SNRI / NDRI / NaSSA / SARI / TCA / MAOI)
    # ==========================================
    {
        "name": "Sertraline",
        "name_zh": "舍曲林",
        "aliases": ["左洛复", "Zoloft", "盐酸舍曲林", "唯他停"],
        "url": "https://en.wikipedia.org/wiki/Sertraline",
        "categories": ["antidepressant", "ssri", "common"],
        "summary": "选择性5-羟色胺再摄取抑制剂 (SSRI)，一线广泛用于抗抑郁与抗焦虑，对强迫症与创伤后应激障碍疗效确切。",
        "pk": {
            "brandName": "左洛复 (Zoloft) | 辉瑞 (Pfizer)",
            "halfLife": "26 小时 (活性代谢物去甲基舍曲林: 62 - 104 小时)",
            "halfLifeHours": 26.0,
            "tMax": "4.5 - 8.4 小时",
            "tMaxHours": 6.5,
            "bioavailability": "44%",
            "cypEnzymes": ["CYP2B6", "CYP2C19", "CYP2C9", "CYP3A4", "CYP2D6(弱)"],
            "clearance": "肝脏广泛代谢，肾脏排泄 40-45%，粪便排泄 40-45%",
            "indications": ["重度抑郁症 (MDD)", "强迫症 (OCD)", "恐慌障碍", "创伤后应激障碍 (PTSD)", "社交焦虑障碍 (SAD)"],
            "contraindications": ["严禁与单胺氧化酶抑制剂 (MAOI) 合用 (致命五羟色胺综合征)", "严禁与匹莫齐特合用 (延长QT间期)", "慎用：双相躁狂发作史、癫痫患者"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 100.0, "heavyMin": 200.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 4.5, "max": 8.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 40.0, "max": 45.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs", "Tranylcypromine", "Moclobemide", "Pimozide", "Selegiline", "Linezolid"],
            "unsafe": ["Tramadol", "Dextromethorphan", "MDMA", "St John's Wort", "NSAIDs", "Aspirin"],
            "uncertain": ["Alcohol", "Lithium", "Triptans"]
        }
    },
    {
        "name": "Escitalopram",
        "name_zh": "艾司西酞普兰",
        "aliases": ["来士普", "Lexapro", "Cipralex", "草酸艾司西酞普兰", "百洛特"],
        "url": "https://en.wikipedia.org/wiki/Escitalopram",
        "categories": ["antidepressant", "ssri", "common"],
        "summary": "高选择性5-羟色胺再摄取抑制剂 (S-对映体)，为目前变构5-HT再摄取阻滞特异性最高的抗抑郁药，耐受性优良。",
        "pk": {
            "brandName": "来士普 (Lexapro) | 灵北 (Lundbeck)",
            "halfLife": "27 - 32 小时",
            "halfLifeHours": 30.0,
            "tMax": "3.0 - 4.0 小时",
            "tMaxHours": 3.5,
            "bioavailability": "80%",
            "cypEnzymes": ["CYP2C19", "CYP3A4", "CYP2D6"],
            "clearance": "肝脏代谢，主要经尿液排出",
            "indications": ["重度抑郁症", "广泛性焦虑障碍 (GAD)", "恐慌障碍", "社交恐惧症"],
            "contraindications": ["严禁与 MAOI 合用", "QT间期延长患者禁忌与已知延长QT药物联用", "对西酞普兰过敏者"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 5.0, "commonMin": 10.0, "strongMin": 15.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 3.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 32.0, "units": "hours"}
                },
                "bioavailability": {"min": 75.0, "max": 85.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs", "Pimozide", "Linezolid"],
            "unsafe": ["Tramadol", "MDMA", "Dextromethorphan", "Amiodarone"],
            "uncertain": ["NSAIDs", "Alcohol"]
        }
    },
    {
        "name": "Fluoxetine",
        "name_zh": "氟西汀",
        "aliases": ["百优解", "Prozac", "盐酸氟西汀", "优克"],
        "url": "https://en.wikipedia.org/wiki/Fluoxetine",
        "categories": ["antidepressant", "ssri", "common"],
        "summary": "经典长效选择性5-羟色胺再摄取抑制剂，具有轻度5-HT2C拮抗带来的活化振奋作用，极长半衰期不易产生停药反应。",
        "pk": {
            "brandName": "百优解 (Prozac) | 礼来 (Eli Lilly)",
            "halfLife": "1 - 4 天 (活性代谢物去甲氟西汀: 7 - 15 天)",
            "halfLifeHours": 72.0,
            "tMax": "6.0 - 8.0 小时",
            "tMaxHours": 7.0,
            "bioavailability": "72%",
            "cypEnzymes": ["CYP2D6(强强抑制)", "CYP2C19", "CYP3A4", "CYP2C9"],
            "clearance": "肝脏代谢，主要由肾脏消除；换药需严格等待5周清洗期",
            "indications": ["重度抑郁症", "强迫症", "神经性贪食症", "惊恐障碍"],
            "contraindications": ["严禁与 MAOIs 联用 (换用MAOI需停用氟西汀至少5周)", "与硫利达嗪合用禁忌"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 10.0, "commonMin": 20.0, "strongMin": 40.0, "heavyMin": 60.0},
                "duration": {
                    "onset": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "peak": {"min": 6.0, "max": 8.0, "units": "hours"},
                    "total": {"min": 48.0, "max": 96.0, "units": "hours"}
                },
                "bioavailability": {"min": 70.0, "max": 80.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs", "Thioridazine", "Pimozide"],
            "unsafe": ["Tramadol", "MDMA", "Codeine", "Metoprolol", "TCAs"],
            "uncertain": ["Lithium", "Aspirin"]
        }
    },
    {
        "name": "Paroxetine",
        "name_zh": "帕罗西汀",
        "aliases": ["赛乐特", "Paxil", "Seroxat", "盐酸帕罗西汀"],
        "url": "https://en.wikipedia.org/wiki/Paroxetine",
        "categories": ["antidepressant", "ssri", "common"],
        "summary": "强效抗抑郁抗焦虑药，兼具轻度抗胆碱与去甲肾上腺素阻滞，镇静抗焦虑作用迅速，但停药综合征相对明显。",
        "pk": {
            "brandName": "赛乐特 (Paxil / Seroxat) | 葛兰素史克 (GSK)",
            "halfLife": "21 - 24 小时",
            "halfLifeHours": 22.0,
            "tMax": "5.0 小时",
            "tMaxHours": 5.0,
            "bioavailability": "完全吸收 (首过效应饱和)",
            "cypEnzymes": ["CYP2D6(强效不可逆自抑制剂)", "CYP3A4"],
            "clearance": "尿液排泄 64%，粪便排泄 36%",
            "indications": ["各种抑郁症", "强迫症", "惊恐障碍", "社交恐惧症", "广泛性焦虑", "创伤后应激障碍"],
            "contraindications": ["禁与 MAOI、匹莫齐特或硫利达嗪合用", "妊娠期 (心脏畸形风险 D级)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 10.0, "commonMin": 20.0, "strongMin": 40.0, "heavyMin": 50.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 4.0, "max": 6.0, "units": "hours"}, "total": {"min": 20.0, "max": 26.0, "units": "hours"}},
                "bioavailability": {"min": 50.0, "max": 70.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs", "Pimozide", "Thioridazine"],
            "unsafe": ["Tramadol", "Tamoxifen", "Dextromethorphan", "MDMA"],
            "uncertain": ["Alcohol", "NSAIDs"]
        }
    },
    {
        "name": "Venlafaxine",
        "name_zh": "文拉法辛",
        "aliases": ["怡诺思", "Effexor", "盐酸文拉法辛缓释胶囊", "博乐欣"],
        "url": "https://en.wikipedia.org/wiki/Venlafaxine",
        "categories": ["antidepressant", "snri", "common"],
        "summary": "5-羟色胺和去甲肾上腺素双重再摄取抑制剂 (SNRI)。低剂量主阻滞5-HT，高剂量同时阻滞NE，对难治性抑郁及慢性疼痛有效。",
        "pk": {
            "brandName": "怡诺思 (Effexor XR) | 辉瑞 (Pfizer)",
            "halfLife": "母体 5 小时，主要活性代谢物去甲文拉法辛 (ODV): 11 小时",
            "halfLifeHours": 11.0,
            "tMax": "缓释制剂: 5.5 - 6.0 小时 (普通片: 2.0 小时)",
            "tMaxHours": 5.5,
            "bioavailability": "45%",
            "cypEnzymes": ["CYP2D6(主代谢为活性ODV)", "CYP3A4", "CYP2C19"],
            "clearance": "肾脏排出 (87%)",
            "indications": ["重度抑郁症", "广泛性焦虑", "社交焦虑障碍", "惊恐障碍"],
            "contraindications": ["严禁与 MAOIs 联用", "未控制的高血压患者 (可使血压显著升高)", "闭角型青光眼"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 37.5, "commonMin": 75.0, "strongMin": 150.0, "heavyMin": 225.0},
                "duration": {"onset": {"min": 2.0, "max": 3.0, "units": "hours"}, "peak": {"min": 5.0, "max": 6.0, "units": "hours"}, "total": {"min": 18.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 40.0, "max": 50.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs", "Linezolid"],
            "unsafe": ["Tramadol", "Amphetamine", "MDMA", "Pseudoephedrine"],
            "uncertain": ["Alcohol", "NSAIDs"]
        }
    },
    {
        "name": "Duloxetine",
        "name_zh": "度洛西汀",
        "aliases": ["欣百达", "Cymbalta", "盐酸度洛西汀肠溶胶囊", "奥麦伦"],
        "url": "https://en.wikipedia.org/wiki/Duloxetine",
        "categories": ["antidepressant", "snri", "common"],
        "summary": "平衡型 SNRI，同时抑制5-HT和NE再摄取，兼具优异的中枢下行镇痛调节机制，广泛用于抑郁合并躯体慢性疼痛。",
        "pk": {
            "brandName": "欣百达 (Cymbalta) | 礼来 (Eli Lilly)",
            "halfLife": "12.0 小时 (8 - 17 小时)",
            "halfLifeHours": 12.0,
            "tMax": "空腹 6.0 小时 (餐后约 10 小时)",
            "tMaxHours": 6.0,
            "bioavailability": "50% (30% - 80%)",
            "cypEnzymes": ["CYP1A2", "CYP2D6 (同时中度抑制CYP2D6)"],
            "clearance": "肝脏代谢，尿中排出 70%，粪便排出 20%",
            "indications": ["重度抑郁症", "广泛性焦虑", "糖尿病周围神经痛", "慢性肌肉骨骼疼痛", "纤维肌痛"],
            "contraindications": ["禁与 MAOI、CYP1A2 强抑制剂 (如氟伏沙明、环丙沙星) 合用", "严重肝功能不全", "重度肾功能不全"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 30.0, "commonMin": 60.0, "strongMin": 90.0, "heavyMin": 120.0},
                "duration": {"onset": {"min": 2.0, "max": 3.0, "units": "hours"}, "peak": {"min": 6.0, "max": 10.0, "units": "hours"}, "total": {"min": 18.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 45.0, "max": 60.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs", "Fluvoxamine", "Ciprofloxacin"],
            "unsafe": ["Tramadol", "MDMA", "NSAIDs"],
            "uncertain": ["Alcohol"]
        }
    },
    {
        "name": "Bupropion",
        "name_zh": "安非他酮",
        "aliases": ["悦亭", "Wellbutrin", "Zyban", "盐酸安非他酮缓释片"],
        "url": "https://en.wikipedia.org/wiki/Bupropion",
        "categories": ["antidepressant", "stimulant", "ndri"],
        "summary": "去甲肾上腺素与多巴胺再摄取抑制剂 (NDRI)，不引起性功能障碍与体重增加，具有改善动力专注与戒烟双重效应。",
        "pk": {
            "brandName": "Wellbutrin / Zyban | 葛兰素史克 (GSK)",
            "halfLife": "母体 14 - 21 小时 (活性代谢物羟安非他酮: 20 - 37 小时)",
            "halfLifeHours": 21.0,
            "tMax": "缓释(SR): 3.0 小时；控释(XL): 5.0 小时",
            "tMaxHours": 4.0,
            "bioavailability": "良好吸收，显著首过",
            "cypEnzymes": ["CYP2B6(主代谢)", "CYP2D6(强效竞争抑制剂)"],
            "clearance": "主要经尿液排出 (87%)",
            "indications": ["重度抑郁症", "季节性情感障碍 (SAD)", "辅助戒烟", "ADHD 临床标签外使用"],
            "contraindications": ["癫痫或惊厥史患者绝对禁忌 (降低惊厥阈值)", "神经性厌食或贪食症患者绝对禁忌", "突然戒断酒精或镇静药状态"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 75.0, "commonMin": 150.0, "strongMin": 300.0, "heavyMin": 450.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 3.0, "max": 5.0, "units": "hours"}, "total": {"min": 16.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 5.0, "max": 20.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs", "Tramadol (癫痫高危)"],
            "unsafe": ["Venlafaxine", "Atomoxetine", "Metoprolol", "Antipsychotics"],
            "uncertain": ["Alcohol", "Caffeine"]
        }
    },
    {
        "name": "Trazodone",
        "name_zh": "曲唑酮",
        "aliases": ["美舒郁", "Desyrel", "盐酸曲唑酮片"],
        "url": "https://en.wikipedia.org/wiki/Trazodone",
        "categories": ["antidepressant", "depressant", "sari"],
        "summary": "5-HT受体拮抗和再摄取抑制剂 (SARI)，小剂量强效拮抗5-HT2A及H1与α1受体，为临床解决抑郁伴失眠的金标准药物之一。",
        "pk": {
            "brandName": "美舒郁 (Desyrel / Trittico) | 意大利天使制药 (Angelini)",
            "halfLife": "双相消除: 初始 3 - 6 小时，终末 5 - 9 小时",
            "halfLifeHours": 7.0,
            "tMax": "餐后服用 1.0 - 2.0 小时",
            "tMaxHours": 1.5,
            "bioavailability": "完全吸收 (随餐更佳)",
            "cypEnzymes": ["CYP3A4(主要)", "CYP2D6"],
            "clearance": "肝脏代谢，尿中排出 75%",
            "indications": ["抑郁症伴焦虑与严重睡眠障碍", "顽固性失眠 (低剂量一线)", "抗精神病或SSRI引起的失眠辅助"],
            "contraindications": ["心肌梗死急性恢复期", "室性心律失常", "严重肝肾功能损害"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 150.0, "heavyMin": 300.0},
                "duration": {"onset": {"min": 0.5, "max": 1.0, "units": "hours"}, "peak": {"min": 1.5, "max": 2.5, "units": "hours"}, "total": {"min": 6.0, "max": 10.0, "units": "hours"}},
                "bioavailability": {"min": 65.0, "max": 80.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs"],
            "unsafe": ["Alcohol", "CNS Depressants", "Ketoconazole", "Erythromycin"],
            "uncertain": ["Digoxin", "Warfarin"]
        }
    },

    # ==========================================
    # 2. 情绪稳定剂与抗惊厥抗癫痫 (Mood Stabilizers & Anticonvulsants)
    # ==========================================
    {
        "name": "Lithium",
        "name_zh": "碳酸锂",
        "aliases": ["碳酸锂片", "碳酸锂缓释片", "Lithobid", "Eskalith"],
        "url": "https://en.wikipedia.org/wiki/Lithium_(medication)",
        "categories": ["mood-stabilizer", "depressant", "common"],
        "summary": "双相情感障碍治疗的金标准基石，经典情绪稳定剂，对躁狂发作及预防自杀具有不可替代的证据等级。",
        "pk": {
            "brandName": "Lithobid / Eskalith",
            "halfLife": "18 - 24 小时 (老年人可达 36 小时)",
            "halfLifeHours": 24.0,
            "tMax": "普通片: 0.5 - 3.0 小时；缓释片: 4.0 - 4.5 小时",
            "tMaxHours": 3.0,
            "bioavailability": "95% - 100%",
            "cypEnzymes": ["不经CYP代谢 (以离子原形排泄)"],
            "clearance": "几乎全部 (95%) 由肾脏以原形排出，易受肾血流与水钠平衡影响",
            "indications": ["双相情感障碍躁狂发作与抑郁发作", "双相障碍维持预防", "难治性重度抑郁增效治疗"],
            "contraindications": ["严重肾功能不全", "严重心血管疾病", "重度脱水或低钠血症患者", "禁用利尿剂导致蓄积中毒"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 300.0, "commonMin": 600.0, "strongMin": 900.0, "heavyMin": 1500.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 3.0, "max": 4.5, "units": "hours"}, "total": {"min": 24.0, "max": 36.0, "units": "hours"}},
                "bioavailability": {"min": 95.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["NSAIDs (布洛芬等显著升高锂浓度中毒)", "ACEI/ARBs", "Hydrochlorothiazide (利尿剂)"],
            "unsafe": ["SSRIs (震颤/肌阵挛)", "Haloperidol", "Carbamazepine"],
            "uncertain": ["Caffeine (促进锂排出降低疗效)"]
        }
    },
    {
        "name": "Sodium valproate",
        "name_zh": "丙戊酸钠",
        "aliases": ["德巴金", "Depakine", "丙戊酸缓释片", "Valproic acid"],
        "url": "https://en.wikipedia.org/wiki/Valproate",
        "categories": ["mood-stabilizer", "depressant", "common"],
        "summary": "广谱抗癫痫药与一线情绪稳定剂，增强GABA抑制机能，对双相快速循环型及混合发作疗效优于碳酸锂。",
        "pk": {
            "brandName": "德巴金 (Depakine Chrono) | 赛诺菲 (Sanofi)",
            "halfLife": "9 - 16 小时 (缓释可更持久)",
            "halfLifeHours": 15.0,
            "tMax": "缓释片约 7.0 - 8.0 小时 (普通片 1-3 小时)",
            "tMaxHours": 7.0,
            "bioavailability": "接近 100%",
            "cypEnzymes": ["CYP2C9", "CYP2C19 (同时强抑制 UGT 酶与 CYP2C9)"],
            "clearance": "肝脏线粒体β-氧化与葡萄糖醛酸化，尿排出",
            "indications": ["双相障碍躁狂发作", "双相障碍维持治疗", "各型癫痫全面发作", "偏头痛预防"],
            "contraindications": ["急慢性肝炎或严重肝功能损害", "线粒体脑病 (POLG基因突变)", "育龄期女性妊娠禁忌 (强致畸性)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 250.0, "commonMin": 500.0, "strongMin": 1000.0, "heavyMin": 1500.0},
                "duration": {"onset": {"min": 2.0, "max": 4.0, "units": "hours"}, "peak": {"min": 6.0, "max": 8.0, "units": "hours"}, "total": {"min": 18.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 95.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["Lamotrigine (抑制拉莫三嗪代谢致致命皮疹 Stevens-Johnson 综合征)", "Meropenem (碳青霉烯类使丙戊酸浓度暴跌至零致癫痫持续)"],
            "unsafe": ["Aspirin", "Phenobarbital", "Carbamazepine"],
            "uncertain": ["Alcohol"]
        }
    },
    {
        "name": "Lamotrigine",
        "name_zh": "拉莫三嗪",
        "aliases": ["利必通", "Lamictal", "拉莫三嗪片"],
        "url": "https://en.wikipedia.org/wiki/Lamotrigine",
        "categories": ["mood-stabilizer", "common"],
        "summary": "电压门控钠通道阻滞剂，一线用于双相抑郁预防与维持，改善双相抑郁相优异且不诱发躁狂，需极缓慢加量以防皮疹。",
        "pk": {
            "brandName": "利必通 (Lamictal) | 葛兰素史克 (GSK)",
            "halfLife": "单药 25 - 30 小时 (与丙戊酸联用增至 60 小时，与酶诱导剂联用降至 14 小时)",
            "halfLifeHours": 29.0,
            "tMax": "1.4 - 4.8 小时",
            "tMaxHours": 2.5,
            "bioavailability": "98%",
            "cypEnzymes": ["主要经 UGT1A4 葡萄糖醛酸化代谢，极少经 CYP"],
            "clearance": "几乎全部以葡萄糖醛酸结合物经肾脏排泄",
            "indications": ["双相情感障碍抑郁发作的预防与延缓", "癫痫局灶性发作与全面性强直-阵挛发作"],
            "contraindications": ["对拉莫三嗪过敏", "出现皮疹必须立即停药评估 (防重症多形红斑 SJS/TEN)", "妊娠合并雌激素波动需监测浓度"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 100.0, "strongMin": 200.0, "heavyMin": 400.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 2.0, "max": 4.0, "units": "hours"}, "total": {"min": 24.0, "max": 36.0, "units": "hours"}},
                "bioavailability": {"min": 95.0, "max": 99.0}
            }
        ],
        "interactions": {
            "dangerous": ["Sodium valproate (血药浓度暴增翻倍，极高皮疹致死率，必须剂量减半减慢加量)"],
            "unsafe": ["Combined Oral Contraceptives (口服复方避孕药/雌激素使拉莫三嗪浓度暴跌 50%)", "Carbamazepine", "Phenytoin"],
            "uncertain": ["Alcohol"]
        }
    },

    # ==========================================
    # 3. 抗精神病药物补充 (Atypical & Typical Antipsychotics)
    # ==========================================
    {
        "name": "Aripiprazole",
        "name_zh": "阿立哌唑",
        "aliases": ["博思清", "安律凡", "Abilify", "阿立哌唑口崩片"],
        "url": "https://en.wikipedia.org/wiki/Aripiprazole",
        "categories": ["antipsychotic", "common"],
        "summary": "多巴胺系统稳定剂 (D2 / 5-HT1A 受体部分激动剂，5-HT2A 拮抗剂)，不易引起镇静和体重明显增加，对阴性症状及难治抑郁增效极佳。",
        "pk": {
            "brandName": "安律凡 / 博思清 (Abilify) | 大冢制药 (Otsuka)",
            "halfLife": "75 小时 (活性代谢物脱氢阿立哌唑: 94 小时)",
            "halfLifeHours": 75.0,
            "tMax": "3.0 - 5.0 小时",
            "tMaxHours": 4.0,
            "bioavailability": "87%",
            "cypEnzymes": ["CYP3A4", "CYP2D6"],
            "clearance": "粪便排泄 55%，尿液排泄 25%",
            "indications": ["精神分裂症", "双相 I 型障碍躁狂发作", "重度抑郁症辅助增效治疗", "抽动秽语综合征"],
            "contraindications": ["痴呆相关精神病老年患者增加死亡风险 (黑框警示)", "对阿立哌唑过敏者"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 5.0, "commonMin": 10.0, "strongMin": 20.0, "heavyMin": 30.0},
                "duration": {"onset": {"min": 1.0, "max": 3.0, "units": "hours"}, "peak": {"min": 3.0, "max": 5.0, "units": "hours"}, "total": {"min": 48.0, "max": 72.0, "units": "hours"}},
                "bioavailability": {"min": 85.0, "max": 90.0}
            }
        ],
        "interactions": {
            "dangerous": ["Ketoconazole (强CYP3A4抑制剂，阿立哌唑需减半)", "Quinidine (强CYP2D6抑制剂，需减半)"],
            "unsafe": ["Carbamazepine (强诱导剂，浓度减半)", "Fluoxetine", "Paroxetine"],
            "uncertain": ["Alcohol", "Lorazepam"]
        }
    },
    {
        "name": "Tandospirone",
        "name_zh": "坦度螺酮",
        "aliases": ["希德", "Sediel", "枸橼酸坦度螺酮胶囊"],
        "url": "https://en.wikipedia.org/wiki/Tandospirone",
        "categories": ["depressant", "anxiolytic", "common"],
        "summary": "高选择性 5-HT1A 受体部分激动剂，无苯二氮䓬类的镇静、肌肉松弛与成瘾戒断风险，是躯体化焦虑的一线非依赖性选择。",
        "pk": {
            "brandName": "希德 (Sediel) | 住友制药 (Sumitomo)",
            "halfLife": "1.2 - 1.4 小时",
            "halfLifeHours": 1.3,
            "tMax": "0.8 - 1.2 小时",
            "tMaxHours": 1.0,
            "bioavailability": "口服吸收迅速，显著首过",
            "cypEnzymes": ["CYP3A4"],
            "clearance": "肝脏代谢，主要由肾脏排出",
            "indications": ["各种神经症伴发的焦虑状态 (广泛焦虑、惊恐障碍)", "原发性高血压、胃及十二指肠溃疡伴发的躯体化焦虑"],
            "contraindications": ["对本品成分过敏者", "青光眼或重症肌无力慎用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 10.0, "commonMin": 30.0, "strongMin": 60.0, "heavyMin": 90.0},
                "duration": {"onset": {"min": 0.5, "max": 1.0, "units": "hours"}, "peak": {"min": 1.0, "max": 1.5, "units": "hours"}, "total": {"min": 4.0, "max": 6.0, "units": "hours"}},
                "bioavailability": {"min": 30.0, "max": 50.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs"],
            "unsafe": ["Fluvoxamine", "Ketoconazole", "Clarithromycin"],
            "uncertain": ["Alcohol"]
        }
    },
    {
        "name": "Trihexyphenidyl",
        "name_zh": "苯海索",
        "aliases": ["安坦", "Artane", "盐酸苯海索片"],
        "url": "https://en.wikipedia.org/wiki/Trihexyphenidyl",
        "categories": ["deliriant", "depressant", "common"],
        "summary": "中枢抗胆碱药 (M受体阻断剂)，临床主要用于缓解抗精神病药物引起的锥体外系反应 (EPS: 震颤、肌强直、静坐不能)。",
        "pk": {
            "brandName": "安坦 (Artane)",
            "halfLife": "3.3 - 4.0 小时 (部分终末清除相达 10-12 小时)",
            "halfLifeHours": 4.0,
            "tMax": "1.0 - 1.5 小时",
            "tMaxHours": 1.3,
            "bioavailability": "完全吸收",
            "cypEnzymes": ["CYP2D6"],
            "clearance": "微量原形随尿排出，主要经代谢转化消除",
            "indications": ["帕金森病与帕金森综合征", "药物引起的锥体外系反应 (静坐不能、急性肌张力障碍、假性帕金森)"],
            "contraindications": ["闭角型青光眼患者绝对禁用 (升高眼压致盲)", "前列腺肥大伴排尿困难者禁用", "重症肌无力"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 6.0, "heavyMin": 10.0},
                "duration": {"onset": {"min": 0.5, "max": 1.0, "units": "hours"}, "peak": {"min": 1.0, "max": 1.5, "units": "hours"}, "total": {"min": 6.0, "max": 12.0, "units": "hours"}},
                "bioavailability": {"min": 70.0, "max": 90.0}
            }
        ],
        "interactions": {
            "dangerous": ["Potassium chloride (抗胆碱延缓胃排空致氯化钾肠道溃疡坏死)"],
            "unsafe": ["Haloperidol", "Chlorpromazine", "Amantadine", "TCAs (抗胆碱毒性叠加)"],
            "uncertain": ["Alcohol"]
        }
    },

    # ==========================================
    # 4. ADHD / 专注力促醒 (ADHD & Wakefulness)
    # ==========================================
    {
        "name": "Atomoxetine",
        "name_zh": "托莫西汀",
        "aliases": ["择思达", "Strattera", "盐酸托莫西汀胶囊", "阿托莫西汀"],
        "url": "https://en.wikipedia.org/wiki/Atomoxetine",
        "categories": ["nootropic", "stimulant", "common"],
        "summary": "高选择性去甲肾上腺素再摄取抑制剂 (NRI)，非中枢神经兴奋剂，无成瘾性与兴奋剂管制属性，一线用于儿童及成人 ADHD。",
        "pk": {
            "brandName": "择思达 (Strattera) | 礼来 (Eli Lilly)",
            "halfLife": "快代谢者 (EM): 5.0 小时；慢代谢者 (PM): 20.0 小时",
            "halfLifeHours": 5.0,
            "tMax": "1.0 - 2.0 小时",
            "tMaxHours": 1.5,
            "bioavailability": "快代谢者 63%，慢代谢者 94%",
            "cypEnzymes": ["CYP2D6(主消除酶)", "CYP2C19"],
            "clearance": "经尿排泄 80%，粪便 17%",
            "indications": ["注意缺陷多动障碍 (ADHD) 治疗"],
            "contraindications": ["严禁与 MAOIs 联用", "闭角型青光眼", "严重心血管结构异常/心律失常"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 40.0, "strongMin": 80.0, "heavyMin": 100.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 1.5, "max": 2.5, "units": "hours"}, "total": {"min": 12.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 60.0, "max": 90.0}
            }
        ],
        "interactions": {
            "dangerous": ["MAOIs"],
            "unsafe": ["Fluoxetine (CYP2D6强抑制使托莫西汀浓度增加6-8倍)", "Paroxetine", "Salbutamol (心率加快)"],
            "uncertain": ["Alcohol"]
        }
    },

    # ==========================================
    # 5. HRT 核心：雌激素全系 (Estrogens)
    # ==========================================
    {
        "name": "Estradiol",
        "name_zh": "雌二醇",
        "aliases": ["17β-雌二醇", "爱丽凝胶", "Oestrogel", "松奇贴片", "Climara", "雌二醇凝胶", "伊诺舒"],
        "url": "https://en.wikipedia.org/wiki/Estradiol_(medication)",
        "categories": ["hrt", "estrogen", "common"],
        "summary": "人体生物同等天然主要雌激素。口服首过效应显著；透皮凝胶或贴剂可完全绕过肝脏首过代谢，血清雌二醇浓度平稳且血栓风险最低。",
        "pk": {
            "brandName": "爱丽凝胶 (Oestrogel 0.06%) / 松奇贴片 (Climara 50/100)",
            "halfLife": "透皮凝胶/贴片经皮储库消除: 24 - 36 小时 (静脉/未结合原形: 1 - 2 小时)",
            "halfLifeHours": 30.0,
            "tMax": "透皮凝胶: 2.0 - 4.0 小时；透皮贴片: 24 小时达稳",
            "tMaxHours": 3.0,
            "bioavailability": "透皮吸收: 10% - 14% (口服因首过仅 3% - 5%)",
            "cypEnzymes": ["CYP3A4(主)", "CYP1A2", "UGT1A1", "17β-HSD"],
            "clearance": "主要在肝脏转化为雌酮 (E1) 及结合物经尿排泄",
            "indications": ["跨性别女性 (MtF) 性别肯定激素治疗", "女性绝经期综合征与围绝经期低雌激素", "原发性卵巢功能不全"],
            "contraindications": ["已知或怀疑乳腺癌或雌激素依赖性恶性肿瘤", "活动性深静脉血栓形成 (DVT) 或肺栓塞 (PE)", "严重急性肝脏疾病"]
        },
        "roas": [
            {
                "name": "transdermal",
                "dose": {"units": "mg", "lightMin": 0.75, "commonMin": 1.5, "strongMin": 3.0, "heavyMin": 4.5},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 2.0, "max": 4.0, "units": "hours"}, "total": {"min": 24.0, "max": 48.0, "units": "hours"}},
                "bioavailability": {"min": 10.0, "max": 14.0}
            },
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 4.0, "heavyMin": 8.0},
                "duration": {"onset": {"min": 0.5, "max": 1.0, "units": "hours"}, "peak": {"min": 1.0, "max": 2.0, "units": "hours"}, "total": {"min": 12.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 3.0, "max": 5.0}
            }
        ],
        "interactions": {
            "dangerous": ["Smoking (吸烟显著增加动静脉血栓致死风险，口服尤甚)"],
            "unsafe": ["Carbamazepine", "Rifampicin", "St John's Wort (强CYP3A4诱导剂加速雌激素破坏导致浓度暴跌)"],
            "uncertain": ["Lamotrigine (雌二醇显著诱导UGT导致拉莫三嗪浓度暴跌50%)"]
        }
    },
    {
        "name": "Estradiol valerate",
        "name_zh": "戊酸雌二醇",
        "aliases": ["补佳乐", "Progynova", "补佳乐片", "EV注射液", "Delestrogen"],
        "url": "https://en.wikipedia.org/wiki/Estradiol_valerate",
        "categories": ["hrt", "estrogen", "common"],
        "summary": "17β-雌二醇的前体脂肪酸酯。口服后在胃肠黏膜与肝脏酯酶迅速完全水解为天然雌二醇；肌内注射油剂形成体内缓释储库，维持数天高血药浓度。",
        "pk": {
            "brandName": "补佳乐 (Progynova) | 拜耳 (Bayer) / Delestrogen",
            "halfLife": "口服水解后与E2一致: 12 - 20 小时；肌注深部油剂水解消除: 4 - 5 天",
            "halfLifeHours": 96.0,
            "tMax": "口服: 1.0 - 2.0 小时；肌注油剂: 2.0 - 3.0 天",
            "tMaxHours": 48.0,
            "bioavailability": "口服生物利用度约 3% - 5% (高首过)；肌注油剂 100%",
            "cypEnzymes": ["体内非特异性酯酶水解为雌二醇后由 CYP3A4 代谢"],
            "clearance": "随胆汁与尿液排出",
            "indications": ["跨性别女性 (MtF) 女性化女性激素治疗", "绝经后雌激素缺乏症", "自然绝经及术后绝经替代治疗"],
            "contraindications": ["深静脉血栓或活动性血栓栓塞", "重度肝功能不全", "未诊断的生殖道异常出血", "雌激素敏感肿瘤"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 4.0, "heavyMin": 8.0},
                "duration": {"onset": {"min": 0.5, "max": 1.0, "units": "hours"}, "peak": {"min": 1.0, "max": 2.0, "units": "hours"}, "total": {"min": 12.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 3.0, "max": 5.0}
            },
            {
                "name": "intramuscular",
                "dose": {"units": "mg", "lightMin": 2.0, "commonMin": 4.0, "strongMin": 7.0, "heavyMin": 10.0},
                "duration": {"onset": {"min": 6.0, "max": 12.0, "units": "hours"}, "peak": {"min": 48.0, "max": 72.0, "units": "hours"}, "total": {"min": 120.0, "max": 168.0, "units": "hours"}},
                "bioavailability": {"min": 95.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["Smoking (吸烟大幅增强血栓形成风险)"],
            "unsafe": ["Rifampicin", "Phenobarbital", "Phenytoin", "Carbamazepine"],
            "uncertain": ["Lamotrigine"]
        }
    },
    {
        "name": "Estradiol cypionate",
        "name_zh": "环戊丙酸雌二醇",
        "aliases": ["EC", "Depo-Estradiol", "环戊雌二醇"],
        "url": "https://en.wikipedia.org/wiki/Estradiol_cypionate",
        "categories": ["hrt", "estrogen"],
        "summary": "长效酯化雌二醇注射剂，脂溶性高于戊酸雌二醇，肌内注射后释放更平缓平稳，峰谷比显著小于EV，避免情绪大起大落。",
        "pk": {
            "brandName": "Depo-Estradiol | 辉瑞 (Pfizer)",
            "halfLife": "肌内注射消除半衰期: 8 - 10 天",
            "halfLifeHours": 216.0,
            "tMax": "肌内注射后 3.0 - 5.0 天",
            "tMaxHours": 96.0,
            "bioavailability": "肌内注射 100%",
            "cypEnzymes": ["酯酶水解后由 CYP3A4 代谢"],
            "clearance": "肝脏代谢后随尿排泄",
            "indications": ["跨性别女性长效女性化治疗 (注射周期通常为 7~10 天一次)", "中重度血管舒缩症状"],
            "contraindications": ["血栓栓塞性疾病史", "雌激素受体阳性乳腺癌", "严重心功能衰竭"]
        },
        "roas": [
            {
                "name": "intramuscular",
                "dose": {"units": "mg", "lightMin": 1.5, "commonMin": 3.0, "strongMin": 5.0, "heavyMin": 8.0},
                "duration": {"onset": {"min": 12.0, "max": 24.0, "units": "hours"}, "peak": {"min": 72.0, "max": 120.0, "units": "hours"}, "total": {"min": 168.0, "max": 240.0, "units": "hours"}},
                "bioavailability": {"min": 98.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["Smoking"],
            "unsafe": ["CYP3A4 inducers (利福平、卡马西平)"],
            "uncertain": ["Warfarin"]
        }
    },

    # ==========================================
    # 6. HRT 核心：抗雄激素与雄激素阻断剂 (Antiandrogens)
    # ==========================================
    {
        "name": "Cyproterone acetate",
        "name_zh": "醋酸环丙孕酮",
        "aliases": ["色普龙", "安得卡", "Androcur", "CPA", "环丙孕酮"],
        "url": "https://en.wikipedia.org/wiki/Cyproterone_acetate",
        "categories": ["hrt", "antiandrogen", "common"],
        "summary": "强效孕激素衍生抗雄激素，强力中枢负反馈抑制下丘脑-垂体促性腺激素，并竞争性阻滞外周雄激素受体。HRT 推荐低剂量使用以规避脑膜瘤与肝损伤。",
        "pk": {
            "brandName": "安得卡 (Androcur) | 拜耳 (Bayer)",
            "halfLife": "38 - 44 小时 (消除缓慢，蓄积明显，适合隔日或每日一次)",
            "halfLifeHours": 40.0,
            "tMax": "3.0 - 4.0 小时",
            "tMaxHours": 3.5,
            "bioavailability": "口服完全吸收几乎 100%",
            "cypEnzymes": ["CYP3A4(主要代谢酶)"],
            "clearance": "胆汁排泄 60%，尿液排泄 33%",
            "indications": ["跨性别女性女性化抑制内源睾酮 (推荐每日仅 6.25mg-12.5mg)", "严重多毛症与痤疮", "前列腺癌姑息治疗"],
            "contraindications": ["脑膜瘤史或已知脑膜瘤患者绝对禁忌", "严重肝脏疾病或肝酶异常 (定期查肝功)", "消耗性疾病、重度抑郁史"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 6.25, "commonMin": 12.5, "strongMin": 25.0, "heavyMin": 50.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 3.0, "max": 4.0, "units": "hours"}, "total": {"min": 36.0, "max": 48.0, "units": "hours"}},
                "bioavailability": {"min": 95.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["Alcohol (长期合用肝毒性高危)", "Ketoconazole (血药浓度暴增翻倍)"],
            "unsafe": ["Rifampicin", "Carbamazepine", "Statins (他汀类可能加重肌病)"],
            "uncertain": ["Oral Antidiabetics (可影响糖耐量)"]
        }
    },
    {
        "name": "Spironolactone",
        "name_zh": "螺内酯",
        "aliases": ["安体舒通", "Aldactone", "螺内酯片"],
        "url": "https://en.wikipedia.org/wiki/Spironolactone",
        "categories": ["hrt", "antiandrogen", "common"],
        "summary": "醛固酮受体拮抗剂，兼具雄激素受体弱竞争性拮抗与抑制雄激素合成酶 (17α-羟化酶) 作用。广泛作为北美一线抗雄药物，需严密警惕高血钾。",
        "pk": {
            "brandName": "安体舒通 (Aldactone) | 辉瑞 (Pfizer)",
            "halfLife": "母体 1.4 小时，活性代谢物坎利酮 (Canrenone): 16.5 小时；7α-硫甲基螺内酯: 13.8 小时",
            "halfLifeHours": 16.5,
            "tMax": "随餐服用达峰: 2.6 - 3.0 小时",
            "tMaxHours": 2.8,
            "bioavailability": "随餐口服生物利用度 > 90%",
            "cypEnzymes": ["肝脏深度代谢转化为活性坎利酮，CYP3A4参与部分代谢"],
            "clearance": "随尿液与胆汁排泄",
            "indications": ["跨性别女性女性化雄激素阻滞", "水肿性疾病、难治性高血压", "原发性醛固酮增多症"],
            "contraindications": ["高钾血症患者绝对禁用", "急性肾衰竭或严重肾损害", "阿狄森氏病 (Addison's disease)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 50.0, "commonMin": 100.0, "strongMin": 200.0, "heavyMin": 400.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 2.5, "max": 3.5, "units": "hours"}, "total": {"min": 16.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 85.0, "max": 95.0}
            }
        ],
        "interactions": {
            "dangerous": ["Potassium supplements (补钾剂合用极高致死性高血钾风险)", "ACEIs (卡托普利/依那普利等)", "ARBs (氯沙坦等)"],
            "unsafe": ["NSAIDs (降低利尿抗雄效果且损害肾脏升高血钾)", "Digoxin (延长地高辛半衰期致蓄积)"],
            "uncertain": ["Alcohol (增强体位性低血压)"]
        }
    },
    {
        "name": "Bicalutamide",
        "name_zh": "比卡鲁胺",
        "aliases": ["朝晖先", "康士得", "Casodex", "比卡鲁胺片"],
        "url": "https://en.wikipedia.org/wiki/Bicalutamide",
        "categories": ["hrt", "antiandrogen", "common"],
        "summary": "非甾体纯外周雄激素受体 (AR) 拮抗剂，不抑制下丘脑促性腺轴，直接在外周靶器官强力闭锁雄激素受体，不降低血清睾酮但完全阻断其生理效应。",
        "pk": {
            "brandName": "康士得 (Casodex) | 阿斯利康 (AstraZeneca)",
            "halfLife": "活性(R)-异构体终末消除半衰期: 6 - 10 天 (达到体内稳态约需 1 个月)",
            "halfLifeHours": 168.0,
            "tMax": "口服约 31 小时达峰",
            "tMaxHours": 31.0,
            "bioavailability": "口服完全吸收，不受进食影响",
            "cypEnzymes": ["CYP3A4(主要氧化酶) 及葡萄糖醛酸化酶"],
            "clearance": "经尿液与粪便几乎均等排泄",
            "indications": ["跨性别女性外周雄激素受体阻断 (常用量 25~50mg/d)", "晚期前列腺癌联合治疗"],
            "contraindications": ["严重肝功能损害 (治疗期间必须每隔1-3月复查肝功能)", "对本品过敏者"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 100.0, "heavyMin": 150.0},
                "duration": {"onset": {"min": 6.0, "max": 12.0, "units": "hours"}, "peak": {"min": 24.0, "max": 36.0, "units": "hours"}, "total": {"min": 144.0, "max": 240.0, "units": "hours"}},
                "bioavailability": {"min": 95.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["Warfarin (强力置换香豆素类血浆蛋白结合致严重出血，必须监测INR)"],
            "unsafe": ["Cyclosporine", "Midazolam", "Terfenadine"],
            "uncertain": ["Alcohol"]
        }
    },
    {
        "name": "Finasteride",
        "name_zh": "非那雄胺",
        "aliases": ["保法止", "保列治", "Propecia", "Proscar", "启悦"],
        "url": "https://en.wikipedia.org/wiki/Finasteride",
        "categories": ["hrt", "antiandrogen", "common"],
        "summary": "特异性 II 型 5α-还原酶抑制剂，特异性阻断睾酮 (T) 转化为高活性二氢睾酮 (DHT)，强效遏制雄脱与体毛生长，不影响睾酮本身水平。",
        "pk": {
            "brandName": "保法止 (1mg) / 保列治 (5mg) | 默沙东 (MSD)",
            "halfLife": "6.0 小时 (老年人可达 8 小时；组织内结合作用持久)",
            "halfLifeHours": 6.0,
            "tMax": "1.0 - 2.0 小时",
            "tMaxHours": 1.5,
            "bioavailability": "65% (不受食物影响)",
            "cypEnzymes": ["CYP3A4"],
            "clearance": "肝脏代谢，粪便排泄 57%，尿液排泄 39%",
            "indications": ["雄激素性脱发 (男性型秃发 1mg/d)", "跨性别女性降低 DHT 抑制脱发", "良性前列腺增生 (5mg/d)"],
            "contraindications": ["妇女、儿童禁用 (育龄孕妇接触破碎药片有男胎外生殖器畸形风险)", "严重肝功能障碍"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 1.0, "strongMin": 2.5, "heavyMin": 5.0},
                "duration": {"onset": {"min": 0.5, "max": 1.0, "units": "hours"}, "peak": {"min": 1.0, "max": 2.0, "units": "hours"}, "total": {"min": 12.0, "max": 24.0, "units": "hours"}},
                "bioavailability": {"min": 60.0, "max": 70.0}
            }
        ],
        "interactions": {
            "dangerous": [],
            "unsafe": ["CYP3A4 inducers/inhibitors"],
            "uncertain": ["Alcohol"]
        }
    },
    {
        "name": "Leuprorelin",
        "name_zh": "亮丙瑞林",
        "aliases": ["抑那通", "Lupron", "醋酸亮丙瑞林微球", "GnRH-a", "促性腺激素释放激素类似物"],
        "url": "https://en.wikipedia.org/wiki/Leuprorelin",
        "categories": ["hrt", "antiandrogen"],
        "summary": "长效 GnRH (LHRH) 类似物，通过持续刺激引起垂体 GnRH 受体彻底降调节脱敏，使促黄体生成素 (LH) 和睾酮降至去势水平，公认最安全彻底的抗雄方案。",
        "pk": {
            "brandName": "抑那通 (Enantone / Lupron Depot) | 武田 (Takeda)",
            "halfLife": "微球储库持续恒定释放 28 天 (3.75mg 剂型) 或 3 个月 (11.25mg 剂型)",
            "halfLifeHours": 672.0,
            "tMax": "皮下或肌注后 4.0 小时达血药峰值，随后缓释数周",
            "tMaxHours": 4.0,
            "bioavailability": "皮下/肌内注射微球缓释近 100% (口服被胃肠完全降解)",
            "cypEnzymes": ["主要经内源肽酶降解为小分子肽片，不依赖肝脏 CYP450"],
            "clearance": "随尿液与代谢转化排泄",
            "indications": ["跨性别青少年青春期阻断 (Puberty blocker)", "跨性别女性性别肯定去势替代", "前列腺癌、子宫内膜异位症"],
            "contraindications": ["对 GnRH 类似物过敏", "未行性激素补充下的长期单一去势 (需防严重骨质疏松)"]
        },
        "roas": [
            {
                "name": "subcutaneous",
                "dose": {"units": "mg", "lightMin": 3.75, "commonMin": 3.75, "strongMin": 7.5, "heavyMin": 11.25},
                "duration": {"onset": {"min": 24.0, "max": 48.0, "units": "hours"}, "peak": {"min": 48.0, "max": 96.0, "units": "hours"}, "total": {"min": 672.0, "max": 2016.0, "units": "hours"}},
                "bioavailability": {"min": 95.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": [],
            "unsafe": ["Drugs that prolong QT interval"],
            "uncertain": []
        }
    },

    # ==========================================
    # 7. HRT 核心：孕激素与雄激素 (Progestins & Androgens)
    # ==========================================
    {
        "name": "Dydrogesterone",
        "name_zh": "地屈孕酮",
        "aliases": ["达芙通", "Duphaston", "地屈孕酮片"],
        "url": "https://en.wikipedia.org/wiki/Dydrogesterone",
        "categories": ["hrt", "progestin", "common"],
        "summary": "逆转构型高选择性孕激素，无雄激素、雌激素活性或糖皮质激素样副作用，对乳腺组织安全性优良，广泛用于跨女后期乳腺塑形与黄体支持。",
        "pk": {
            "brandName": "达芙通 (Duphaston) | 雅培 (Abbott)",
            "halfLife": "主活性代谢物 20α-二氢地屈孕酮 (DHD): 14 - 17 小时",
            "halfLifeHours": 15.0,
            "tMax": "0.5 - 2.5 小时",
            "tMaxHours": 1.5,
            "bioavailability": "口服吸收良好",
            "cypEnzymes": ["主要经醛酮还原酶还原为活性DHD，次要经 CYP3A4 代谢"],
            "clearance": "完全以代谢物经尿排泄 (63%)",
            "indications": ["跨性别女性女性化后期辅助黄体周期", "内源性孕酮不足引起的继发性闭经、功能失调性出血"],
            "contraindications": ["已知或怀疑孕激素依赖性肿瘤 (如脑膜瘤)", "不明原因生殖道出血"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 10.0, "commonMin": 20.0, "strongMin": 30.0, "heavyMin": 40.0},
                "duration": {"onset": {"min": 0.5, "max": 1.0, "units": "hours"}, "peak": {"min": 1.0, "max": 2.5, "units": "hours"}, "total": {"min": 14.0, "max": 20.0, "units": "hours"}},
                "bioavailability": {"min": 80.0, "max": 90.0}
            }
        ],
        "interactions": {
            "dangerous": [],
            "unsafe": ["Rifampicin", "Phenytoin (CYP诱导剂加速孕激素代谢)"],
            "uncertain": ["Alcohol"]
        }
    },
    {
        "name": "Testosterone undecanoate",
        "name_zh": "十一酸睾酮",
        "aliases": ["安特尔", "Andriol", "耐必多", "Nebido", "十一酸睾酮胶丸", "十一酸睾酮注射液"],
        "url": "https://en.wikipedia.org/wiki/Testosterone_undecanoate",
        "categories": ["hrt", "androgen", "common"],
        "summary": "长链脂肪酸酯化睾酮。口服微丸随脂类食物经肠道淋巴系统吸收完全避开肝毒性；耐必多超长效肌注液注射一次可稳定维持男性化睾酮达 10-14 周，FtM 首选用药。",
        "pk": {
            "brandName": "安特尔 (Andriol 40mg胶丸) / 耐必多 (Nebido 1000mg/4ml注射液) | 拜耳 (Bayer)",
            "halfLife": "口服软胶丸: 3 - 4 小时；长效油剂肌注 (Nebido): 30 - 34 天",
            "halfLifeHours": 768.0,
            "tMax": "口服随餐 4.0 小时；超长效肌注后 1.0 - 2.0 周",
            "tMaxHours": 240.0,
            "bioavailability": "口服需高脂餐同服经淋巴吸收 (空腹仅3%)；肌内注射 100%",
            "cypEnzymes": ["体内非特异性酯酶水解为天然睾酮，进而由 CYP3A4、5α-还原酶、芳香化酶代谢"],
            "clearance": "尿液排泄 90%",
            "indications": ["跨性别男性 (FtM) 性别肯定男性化激素治疗", "男性性腺功能低下症"],
            "contraindications": ["怀疑或已知雄激素依赖性前列腺癌或乳腺癌", "红细胞增多症 (血细胞比容 Hct > 54% 停药)", "严重肝功能不全"]
        },
        "roas": [
            {
                "name": "intramuscular",
                "dose": {"units": "mg", "lightMin": 500.0, "commonMin": 1000.0, "strongMin": 1000.0, "heavyMin": 1000.0},
                "duration": {"onset": {"min": 24.0, "max": 48.0, "units": "hours"}, "peak": {"min": 168.0, "max": 336.0, "units": "hours"}, "total": {"min": 1680.0, "max": 2352.0, "units": "hours"}},
                "bioavailability": {"min": 98.0, "max": 100.0}
            },
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 40.0, "commonMin": 80.0, "strongMin": 120.0, "heavyMin": 160.0},
                "duration": {"onset": {"min": 1.0, "max": 2.0, "units": "hours"}, "peak": {"min": 3.0, "max": 5.0, "units": "hours"}, "total": {"min": 8.0, "max": 12.0, "units": "hours"}},
                "bioavailability": {"min": 7.0, "max": 10.0}
            }
        ],
        "interactions": {
            "dangerous": ["Anticoagulants (华法林等抗凝血药合用出血高危，需减抗凝药量)"],
            "unsafe": ["Insulin (睾酮可提高胰岛素敏感度需调糖药)", "Corticosteroids (水钠潴留水肿高危)"],
            "uncertain": ["Alcohol"]
        }
    }
]

def main():
    print("=== 开始全量精准注入精神类与 HRT 药物数据库 ===")
    if not os.path.exists(SUBSTANCES_JSON_PATH):
        print(f"[ERROR] 找不到基线 Substances.json: {SUBSTANCES_JSON_PATH}")
        sys.exit(1)

    with open(SUBSTANCES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = data.get("categories", [])
    substances = data.get("substances", [])

    # 确保分类包含 hrt, estrogen, antiandrogen, progestin, androgen, ssri, snri, ndri, sari
    existing_cat_names = {c["name"].lower() for c in categories}
    new_cats = [
        {"name": "hrt", "description": "性别肯定激素治疗 (HRT) 与内分泌替代药物，包含雌激素、雄激素阻滞剂、孕激素与雄激素。", "url": "https://en.wikipedia.org/wiki/Hormone_replacement_therapy", "color": 4293967838},
        {"name": "estrogen", "description": "雌激素类药物，维持女性第二性征与女性化内分泌基础。", "url": "https://en.wikipedia.org/wiki/Estrogen", "color": 4294940876},
        {"name": "antiandrogen", "description": "抗雄激素与雄激素受体拮抗剂，抑制或阻断雄激素生理效应。", "url": "https://en.wikipedia.org/wiki/Antiandrogen", "color": 4284802815},
        {"name": "progestin", "description": "孕激素类药物，参与乳腺发育与内分泌周期调节。", "url": "https://en.wikipedia.org/wiki/Progestin", "color": 4294951115},
        {"name": "androgen", "description": "雄激素类药物，促进男性化与维持男性第二性征。", "url": "https://en.wikipedia.org/wiki/Androgen", "color": 4281765375},
        {"name": "antidepressant", "description": "抗抑郁药物，调节中枢单胺类神经递质浓度与受体敏感度。", "url": "https://en.wikipedia.org/wiki/Antidepressant", "color": 4282367487},
        {"name": "ssri", "description": "选择性5-羟色胺再摄取抑制剂，一线抗抑郁与抗焦虑药物。", "url": "https://en.wikipedia.org/wiki/Selective_serotonin_reuptake_inhibitor", "color": 4283808767},
        {"name": "snri", "description": "5-羟色胺和去甲肾上腺素双重再摄取抑制剂，兼具中枢镇痛调节效应。", "url": "https://en.wikipedia.org/wiki/Serotonin%E2%80%93norepinephrine_reuptake_inhibitor", "color": 4285888767},
        {"name": "mood-stabilizer", "description": "心境稳定剂与抗惊厥药物，双相情感障碍治疗基础。", "url": "https://en.wikipedia.org/wiki/Mood_stabilizer", "color": 4288256511}
    ]
    for nc in new_cats:
        if nc["name"].lower() not in existing_cat_names:
            categories.append(nc)
            existing_cat_names.add(nc["name"].lower())

    # 建立现有物质索引
    sub_map = {s["name"].lower(): s for s in substances}
    new_added = 0
    enhanced = 0
    all_zh_mappings = []

    all_target_drugs = CURATED_DRUGS + ADDITIONAL_CURATED_DRUGS
    for item in all_target_drugs:
        name_en = item["name"]
        name_zh = item["name_zh"]
        aliases = list(item["aliases"])
        all_zh_names = [name_zh] + [a for a in aliases if re.search(r'[\u4e00-\u9fa5]', a)]

        # 生成拼音
        pinyin_tokens = []
        abbr_tokens = []
        for z in all_zh_names:
            pys, abs_ = generate_pinyin_tokens(z)
            for p in pys:
                if p not in pinyin_tokens: pinyin_tokens.append(p)
            for a in abs_:
                if a not in abbr_tokens: abbr_tokens.append(a)

        # 组合全量 commonNames
        combined_commons = []
        for z in all_zh_names:
            if z not in combined_commons: combined_commons.append(z)
        for a in aliases:
            if a not in combined_commons: combined_commons.append(a)
        for ab in abbr_tokens:
            if ab not in combined_commons: combined_commons.append(ab)
        for py in pinyin_tokens:
            if py not in combined_commons: combined_commons.append(py)

        all_zh_mappings.append((name_en, name_zh))

        target = sub_map.get(name_en.lower())
        if target:
            # 增强已有物质
            target["pharmacokinetics"] = item["pk"]
            if item.get("roas"):
                target["roas"] = item["roas"]
            if item.get("interactions"):
                target["interactions"] = item["interactions"]
            if item.get("summary") and (not target.get("summary") or len(target.get("summary", "")) < 20):
                target["summary"] = item["summary"]

            # 合并分类与别名
            cur_cats = list(target.get("categories", []))
            for c in item["categories"]:
                if c not in cur_cats: cur_cats.append(c)
            target["categories"] = cur_cats

            cur_commons = list(target.get("commonNames", []))
            for c in combined_commons:
                if c not in cur_commons: cur_commons.append(c)
            target["commonNames"] = cur_commons
            enhanced += 1
        else:
            # 新增独立物质
            new_sub_obj = {
                "name": name_en,
                "commonNames": combined_commons,
                "url": item["url"],
                "isApproved": True,
                "tolerance": None,
                "crossTolerances": [],
                "addictionPotential": None,
                "toxicities": [],
                "categories": item["categories"],
                "summary": item["summary"],
                "interactions": item["interactions"],
                "roas": item["roas"],
                "pharmacokinetics": item["pk"]
            }
            substances.append(new_sub_obj)
            sub_map[name_en.lower()] = new_sub_obj
            new_added += 1

    print(f"[+] 数据注入成功: 增强现有物质 {enhanced} 种，新增核心精神/HRT物质 {new_added} 种，当前库内总计 {len(substances)} 种物质！")

    # 写回 Substances.json
    data["categories"] = categories
    data["substances"] = sorted(substances, key=lambda x: x["name"])
    with open(SUBSTANCES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 同步更新 SubstanceLocalizationHelper.kt 中的 ZH_NAME_MAP
    if os.path.exists(HELPER_KT_PATH):
        with open(HELPER_KT_PATH, "r", encoding="utf-8") as f:
            kt_code = f.read()

        # 提取已有的映射条目
        existing_matches = re.findall(r'"([^"]+)"\s*to\s*"([^"]+)"', kt_code)
        all_map_dict = {k: v for k, v in existing_matches}
        for en, zh in all_zh_mappings:
            all_map_dict[en] = zh

        sorted_entries = sorted(list(all_map_dict.items()), key=lambda x: x[0].lower())
        map_lines = [f'        "{k}" to "{v}",' for k, v in sorted_entries]
        new_map_str = "    private val ZH_NAME_MAP: Map<String, String> = mapOf(\n" + "\n".join(map_lines) + "\n    )"

        kt_code_updated = re.sub(
            r'    private val ZH_NAME_MAP:\s*Map<String,\s*String>\s*=\s*mapOf\([\s\S]*?\n    \)',
            new_map_str,
            kt_code
        )
        with open(HELPER_KT_PATH, "w", encoding="utf-8") as f:
            f.write(kt_code_updated)
        print(f"[+] Kotlin 静态中文对照表同步完成: 共收录 {len(sorted_entries)} 条映射！")

    file_size_mb = os.path.getsize(SUBSTANCES_JSON_PATH) / (1024 * 1024)
    print(f"[+] 最终 Substances.json 大小: {file_size_mb:.2f} MB (极度轻量快速，无 OOM 风险)")
    print("=== 精神类与 HRT 全量药代数据注入圆满完成 ===")

if __name__ == "__main__":
    main()
