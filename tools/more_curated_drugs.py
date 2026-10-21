#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
扩充精神类药物与 HRT 激素替代全系药物数据（包含临床 ADME 药代动力学、多途径剂量及相互作用）。
"""

ADDITIONAL_CURATED_DRUGS = [
    # ==========================================
    # 1. 经典及非典型抗精神病药 (Atypical & Typical Antipsychotics)
    # ==========================================
    {
        "name": "Quetiapine",
        "name_zh": "喹硫平",
        "aliases": ["思瑞康", "Seroquel", "富马酸喹硫平", "启维", "qpl", "qlp"],
        "url": "https://en.wikipedia.org/wiki/Quetiapine",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "非典型第二代抗精神病药，广谱拮抗 5-HT2A、D2、H1 及 α1 受体。低剂量强镇静催眠，中高剂量抗抑郁与抗精神分裂症。",
        "pk": {
            "brandName": "思瑞康 (Seroquel) | 阿斯利康 (AstraZeneca)",
            "halfLife": "约 6 - 7 小时 (活性代谢物去烷基喹硫平: 12 小时)",
            "halfLifeHours": 7.0,
            "tMax": "1.5 小时 (缓释片 XR 约 6 小时)",
            "tMaxHours": 1.5,
            "bioavailability": "约 9% (肝脏首过效应显著)",
            "cypEnzymes": ["CYP3A4", "CYP2D6(微弱)"],
            "clearance": "肝脏广泛代谢，尿排泄 73%，粪便 20%",
            "indications": ["精神分裂症", "双相情感障碍 (躁狂/抑郁发作及维持)", "重度抑郁症辅助增效", "常被超适应症用于难治性失眠 (需监测代谢指标)"],
            "contraindications": ["严禁与强效 CYP3A4 抑制剂合用 (如酮康唑、红霉素)", "严重心血管病、QT间期延长者禁用", "高度警惕嗜睡、体位性低血压、体重增加及血糖血脂代谢异常"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 100.0, "strongMin": 300.0, "heavyMin": 600.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.5, "max": 2.5, "units": "hours"},
                    "total": {"min": 8.0, "max": 14.0, "units": "hours"}
                },
                "bioavailability": {"min": 8.0, "max": 11.0}
            }
        ],
        "interactions": {
            "dangerous": ["酮康唑", "克拉霉素", "红霉素", "匹莫齐特"],
            "unsafe": ["酒精 (乙醇)", "苯二氮䓬类中枢抑制剂", "美沙酮", "氟哌啶醇"],
            "uncertain": ["苯妥英钠", "卡马西平"]
        }
    },
    {
        "name": "Olanzapine",
        "name_zh": "奥氮平",
        "aliases": ["再普乐", "Zyprexa", "奥氮平片", "欧兰宁"],
        "url": "https://en.wikipedia.org/wiki/Olanzapine",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "第二代非典型抗精神病药，对 5-HT2A、D2、M1-5、H1 及 α1 受体均有高亲和力。抗精神病与情绪稳定疗效确切，但代谢副作用突出。",
        "pk": {
            "brandName": "再普乐 (Zyprexa) | 礼来 (Eli Lilly)",
            "halfLife": "30 - 38 小时 (女性及非吸烟者半衰期显著延长)",
            "halfLifeHours": 33.0,
            "tMax": "5.0 - 8.0 小时",
            "tMaxHours": 6.0,
            "bioavailability": "约 85% (吸收完全，不受食物影响)",
            "cypEnzymes": ["CYP1A2", "CYP2D6", "UGT1A4"],
            "clearance": "肝脏直接葡萄糖醛酸结合与CYP1A2氧化，尿排泄 57%，粪便 30%",
            "indications": ["精神分裂症急性期及长期维持", "双相 I 型障碍躁狂或混合发作", "难治性抑郁症联用氟西汀 (OFC 方案)"],
            "contraindications": ["闭角型青光眼禁用", "高度警惕显著食欲增加、严重体重增加、胰岛素抵抗及 2 型糖尿病诱发", "吸烟显著诱导 CYP1A2 使血药浓度下降约 30-40%"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 2.5, "commonMin": 5.0, "strongMin": 10.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 5.0, "max": 7.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 80.0, "max": 90.0}
            }
        ],
        "interactions": {
            "dangerous": ["注射用苯二氮䓬类 (心肺骤停高危)"],
            "unsafe": ["氟伏沙明", "环丙沙星", "酒精 (乙醇)", "左旋多巴"],
            "uncertain": ["卡马西平", "丙戊酸钠 / 丙戊酸"]
        }
    },
    {
        "name": "Risperidone",
        "name_zh": "利培酮",
        "aliases": ["维思通", "Risperdal", "利培酮片", "索乐"],
        "url": "https://en.wikipedia.org/wiki/Risperidone",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "强效 5-HT2A / D2 受体拮抗剂，抗阳性症状作用强，低剂量锥体外系反应发生率低，但易引起高催乳素血症。",
        "pk": {
            "brandName": "维思通 (Risperdal) | 强生杨森 (Janssen)",
            "halfLife": "原型 3 小时 (活性代谢物帕利哌酮 21-24 小时，活性组分合计 24 小时)",
            "halfLifeHours": 24.0,
            "tMax": "1.0 小时 (活性代谢物 3.0 小时)",
            "tMaxHours": 1.0,
            "bioavailability": "70% (口服吸收迅速且完全)",
            "cypEnzymes": ["CYP2D6", "CYP3A4"],
            "clearance": "CYP2D6 代谢为 9-羟利培酮，尿排泄 70%，粪便 14%",
            "indications": ["精神分裂症急性发作及慢性维持", "双相情感障碍躁狂发作", "儿童及青少年孤独症易激惹症状"],
            "contraindications": ["高催乳素血症风险极高 (闭经、溢乳、性功能减退、男性乳腺发育)", "剂量 > 6mg/d 时锥体外系反应 (EPS) 显著增多", "老年痴呆相关精神病增加脑血管事件风险"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 4.0, "heavyMin": 6.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.0, "max": 3.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 65.0, "max": 75.0}
            }
        ],
        "interactions": {
            "dangerous": ["匹莫齐特", "左旋多巴 (疗效拮抗)"],
            "unsafe": ["氟西汀", "帕罗西汀", "酒精 (乙醇)", "氯氮平"],
            "uncertain": ["卡马西平"]
        }
    },
    {
        "name": "Clozapine",
        "name_zh": "氯氮平",
        "aliases": ["氯氮平片", "Clozaril", "Leponex"],
        "url": "https://en.wikipedia.org/wiki/Clozapine",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "难治性精神分裂症的“终极基石”。对 D1/D4 受体亲和力高于 D2，几乎不引起锥体外系反应，但血液毒性需终身严格监控。",
        "pk": {
            "brandName": "氯氮平 (Clozaril) | 诺华 (Novartis)",
            "halfLife": "12 - 14 小时",
            "halfLifeHours": 12.0,
            "tMax": "1.5 - 2.5 小时",
            "tMaxHours": 2.0,
            "bioavailability": "50 - 60%",
            "cypEnzymes": ["CYP1A2", "CYP2D6", "CYP3A4", "CYP2C19"],
            "clearance": "几乎全部由肝脏代谢，尿排泄 50%，粪便 30%",
            "indications": ["难治性精神分裂症 (至少两种抗精神病药足量足疗程无效)", "降低精神分裂症自杀倾向与严重攻击行为"],
            "contraindications": ["【黑框警告】致命性粒细胞缺乏症 (必须按规范每周/每月强制化验血常规)", "【黑框警告】心肌炎、心肌病", "【黑框警告】剂量依赖性癫痫发作", "【黑框警告】严重麻痹性肠梗阻/便秘致死"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 100.0, "strongMin": 300.0, "heavyMin": 600.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.5, "units": "hours"},
                    "peak": {"min": 1.5, "max": 3.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 50.0, "max": 60.0}
            }
        ],
        "interactions": {
            "dangerous": ["骨髓抑制剂 (骨髓抑制剂)", "卡马西平", "环丙沙星", "氟伏沙明 (血药浓度飙升数倍)"],
            "unsafe": ["苯二氮䓬类药物 (呼吸抑制)", "酒精 (乙醇)", "抗胆碱能药物"],
            "uncertain": ["吸烟 (吸烟显著降低血药浓度)"]
        }
    },
    {
        "name": "Paliperidone",
        "name_zh": "帕利哌酮",
        "aliases": ["芮达", "Invega", "棕榈酸帕利哌酮", "善思达", "善妥达"],
        "url": "https://en.wikipedia.org/wiki/Paliperidone",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "利培酮的主要活性代谢产物 (9-羟利培酮)，口服制剂采用 OROS 渗透泵技术实现 24 小时恒速释放，几乎不依赖肝脏 CYP450 代谢。",
        "pk": {
            "brandName": "芮达 (Invega) / 善思达 (Invega Sustenna) | 强生杨森",
            "halfLife": "口服 OROS 约 23 小时；长效注射剂 (棕榈酸酯) 25 - 49 天",
            "halfLifeHours": 23.0,
            "tMax": "口服 OROS 24 小时达到平稳平台期",
            "tMaxHours": 24.0,
            "bioavailability": "28%",
            "cypEnzymes": ["极少经 CYP 代谢 (<10% 由 CYP2D6/3A4 处理)"],
            "clearance": "59% 以原型经肾脏排泄，32% 为非活性代谢物",
            "indications": ["精神分裂症急性发作及预防复发", "分裂情感性障碍 (Schizoaffective disorder) 单药或辅助"],
            "contraindications": ["严重肾功能损害需调整剂量", "高催乳素血症", "QT 间期延长患者慎用", "口服 OROS 胶囊不可咀嚼或掰碎"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 3.0, "commonMin": 6.0, "strongMin": 9.0, "heavyMin": 12.0},
                "duration": {
                    "onset": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "peak": {"min": 20.0, "max": 24.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 25.0, "max": 30.0}
            }
        ],
        "interactions": {
            "dangerous": ["左旋多巴", "多巴胺受体激动剂"],
            "unsafe": ["延长 QT 间期药物", "酒精 (乙醇)"],
            "uncertain": ["卡马西平"]
        }
    },
    {
        "name": "Amisulpride",
        "name_zh": "氨磺必利",
        "aliases": ["索里昂", "Solian", "氨磺必利片"],
        "url": "https://en.wikipedia.org/wiki/Amisulpride",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "非典型抗精神病药，高选择性拮抗边缘系统 D2/D3 受体。低剂量优先阻断突触前自身受体促进多巴胺释放 (改善阴性症状)，高剂量阻断突触后受体 (改善阳性症状)。",
        "pk": {
            "brandName": "索里昂 (Solian) | 赛诺菲 (Sanofi)",
            "halfLife": "约 12 小时",
            "halfLifeHours": 12.0,
            "tMax": "双峰达峰: 1.0 小时与 3.0 - 4.0 小时",
            "tMaxHours": 3.0,
            "bioavailability": "约 48%",
            "cypEnzymes": ["基本不经 CYP450 代谢 (<4% 被微弱代谢)"],
            "clearance": "几乎完全以原型经肾脏随尿液排泄 (肾脏清除率约 330 mL/min)",
            "indications": ["精神分裂症阳性症状 (高剂量 400-800mg/d)", "精神分裂症以情感淡漠、退缩为主的阴性症状 (低剂量 50-300mg/d)"],
            "contraindications": ["嗜铬细胞瘤、催乳素依赖性肿瘤禁用", "严重肾功能损害 (CrCl < 10mL/min) 禁用", "剂量相关 QT 间期延长，禁与抗心律失常药合用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 50.0, "commonMin": 200.0, "strongMin": 400.0, "heavyMin": 800.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 45.0, "max": 50.0}
            }
        ],
        "interactions": {
            "dangerous": ["ⅠA 类及 Ⅲ 类抗心律失常药 (索他洛尔、胺碘酮等)", "左旋多巴", "静脉注射红霉素"],
            "unsafe": ["西酞普兰", "美沙酮", "氟哌啶醇"],
            "uncertain": ["酒精 (乙醇)", "中枢神经系统抑制剂"]
        }
    },
    {
        "name": "Ziprasidone",
        "name_zh": "齐拉西酮",
        "aliases": ["卓乐定", "Geodon", "Zeldox", "盐酸齐拉西酮"],
        "url": "https://en.wikipedia.org/wiki/Ziprasidone",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "非典型抗精神病药，兼具 5-HT1A 激动、5-HT/NE 再摄取阻滞作用。几乎不引起体重增加与代谢紊乱，但口服必须随不低于 500 大卡高脂肪餐服用。",
        "pk": {
            "brandName": "卓乐定 (Geodon) | 辉瑞 (Pfizer)",
            "halfLife": "6.6 小时",
            "halfLifeHours": 6.6,
            "tMax": "6.0 - 8.0 小时 (口服空腹吸收率骤降 50%)",
            "tMaxHours": 7.0,
            "bioavailability": "约 60% (饱腹下)；空腹仅 30%",
            "cypEnzymes": ["醛氧化酶 (约 66%)", "CYP3A4 (约 33%)"],
            "clearance": "肝脏代谢，主要经胆汁及尿液排出",
            "indications": ["精神分裂症急性发作及维持", "双相障碍伴发急性躁狂或混合发作"],
            "contraindications": ["近期心肌梗死、心衰失代偿期、显著 QT 间期延长禁用", "必须与高热量食物同服，否则生物利用度减半达不到有效血药浓度"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 20.0, "commonMin": 40.0, "strongMin": 80.0, "heavyMin": 160.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 6.0, "max": 8.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 18.0, "units": "hours"}
                },
                "bioavailability": {"min": 55.0, "max": 65.0}
            }
        ],
        "interactions": {
            "dangerous": ["延长 QT 间期药物 (奎尼丁、索他洛尔、多非利特、莫西沙星等)"],
            "unsafe": ["酮康唑", "卡马西平", "酒精 (乙醇)"],
            "uncertain": ["选择性5-羟色胺再摄取抑制剂 (SSRI)"]
        }
    },
    {
        "name": "Lurasidone",
        "name_zh": "鲁拉西酮",
        "aliases": ["荣迪思", "Latuda", "盐酸鲁拉西酮"],
        "url": "https://en.wikipedia.org/wiki/Lurasidone",
        "categories": ["antipsychotic", "atypical antipsychotic", "common"],
        "summary": "新型非典型抗精神病药，对 5-HT7 和 5-HT1A 受体有极高亲和力。对双相抑郁疗效卓著，体重与血脂代谢中性，口服需随至少 350 大卡餐服用。",
        "pk": {
            "brandName": "荣迪思 (Latuda) | 住友制药 (Sumitomo)",
            "halfLife": "18 小时 (长期用药稳态下)",
            "halfLifeHours": 18.0,
            "tMax": "1.0 - 3.0 小时",
            "tMaxHours": 2.0,
            "bioavailability": "9 - 19% (进食使吸收增加 2-3 倍)",
            "cypEnzymes": ["CYP3A4 (主要代谢酶)"],
            "clearance": "肝脏CYP3A4代谢，粪便排泄 80%，尿液 9%",
            "indications": ["精神分裂症 (成人及 13 岁以上青少年)", "双相 I 型障碍抑郁发作 (单药或联用锂盐/丙戊酸钠)"],
            "contraindications": ["严禁与强效 CYP3A4 抑制剂 (酮康唑等) 或强诱导剂 (利福平、卡马西平等) 合用", "常见恶心、嗜睡及静坐不能 (akathisia)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 20.0, "commonMin": 40.0, "strongMin": 80.0, "heavyMin": 120.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.0, "max": 3.0, "units": "hours"},
                    "total": {"min": 18.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 10.0, "max": 20.0}
            }
        ],
        "interactions": {
            "dangerous": ["酮康唑", "克拉霉素", "利福平", "贯叶连翘 (圣约翰草)"],
            "unsafe": ["地尔硫䓬", "氟康唑", "酒精 (乙醇)"],
            "uncertain": ["碳酸锂"]
        }
    },
    {
        "name": "Haloperidol",
        "name_zh": "氟哌啶醇",
        "aliases": ["安度利可", "Haldol", "氟哌啶片"],
        "url": "https://en.wikipedia.org/wiki/Haloperidol",
        "categories": ["antipsychotic", "typical antipsychotic", "common"],
        "summary": "经典第一代丁酰苯类高抗精神病药，超强阻断 D2 受体。对急性严重幻觉、妄想与冲动攻击控制迅速，但锥体外系反应风险高。",
        "pk": {
            "brandName": "安度利可 (Haldol) | 强生杨森 (Janssen)",
            "halfLife": "15 - 37 小时 (平均约 20 小时)",
            "halfLifeHours": 20.0,
            "tMax": "口服 2.0 - 6.0 小时；肌注 20 分钟",
            "tMaxHours": 3.0,
            "bioavailability": "60 - 70%",
            "cypEnzymes": ["CYP3A4", "CYP2D6", "羰基还原酶"],
            "clearance": "肝脏还原氧化，经胆汁与肾脏排泄",
            "indications": ["精神分裂症急性发作急救与控制", "抽动秽语综合征 (Tourette)", "急性谵妄激越状态镇静"],
            "contraindications": ["帕金森病、重度中枢神经抑制禁用", "极高风险引起急性肌张力障碍、静坐不能、迟发性运动障碍 (TD)", "恶性综合征 (NMS) 及 QT 间期延长危险"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 5.0, "heavyMin": 10.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 5.0, "units": "hours"},
                    "total": {"min": 18.0, "max": 30.0, "units": "hours"}
                },
                "bioavailability": {"min": 60.0, "max": 70.0}
            }
        ],
        "interactions": {
            "dangerous": ["静脉注射氟哌啶醇 + QT间期延长药物 (尖端扭转型室速风险)", "左旋多巴"],
            "unsafe": ["氟西汀", "帕罗西汀", "卡马西平", "酒精 (乙醇)"],
            "uncertain": ["碳酸锂 (高剂量脑病综合征风险)"]
        }
    },
    {
        "name": "Chlorpromazine",
        "name_zh": "氯丙嗪",
        "aliases": ["冬眠灵", "Thorazine", "盐酸氯丙嗪"],
        "url": "https://en.wikipedia.org/wiki/Chlorpromazine",
        "categories": ["antipsychotic", "typical antipsychotic", "common"],
        "summary": "历史上第一个现代抗精神病药 (吩噻嗪类)。镇静作用极强，抗 α 受体及抗胆碱作用显著，常用于急性精神兴奋与顽固性呃逆。",
        "pk": {
            "brandName": "冬眠灵 (Thorazine/Largactil) | 赛诺菲",
            "halfLife": "约 30 小时",
            "halfLifeHours": 30.0,
            "tMax": "1.0 - 4.0 小时",
            "tMaxHours": 2.0,
            "bioavailability": "约 20 - 30% (首过消除大)",
            "cypEnzymes": ["CYP2D6", "CYP1A2", "CYP3A4"],
            "clearance": "肝脏代谢超过 100 种代谢产物，肾脏排泄",
            "indications": ["精神分裂症狂躁激越", "人工冬眠合剂组成成分", "顽固性呃逆 (打嗝)"],
            "contraindications": ["严重心血管病、骨髓抑制禁用", "显著体位性低血压、过度镇静、嗜睡、光敏性皮炎"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 100.0, "heavyMin": 300.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 18.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 20.0, "max": 30.0}
            }
        ],
        "interactions": {
            "dangerous": ["肾上腺素 (翻转导致致命低血压)", "中枢神经系统抑制剂"],
            "unsafe": ["酒精 (乙醇)", "抗胆碱能药物", "巴比妥类药物"],
            "uncertain": ["普萘洛尔"]
        }
    },

    # ==========================================
    # 2. 抗抑郁药增补 (Fluvoxamine / Citalopram / Mirtazapine / Agomelatine / Vortioxetine / TCAs)
    # ==========================================
    {
        "name": "Mirtazapine",
        "name_zh": "米氮平",
        "aliases": ["瑞美隆", "Remeron", "米氮平片", "派迪升"],
        "url": "https://en.wikipedia.org/wiki/Mirtazapine",
        "categories": ["antidepressant", "nassa", "common"],
        "summary": "去甲肾上腺素能和特异性 5-羟色胺能抗抑郁药 (NaSSA)。强效拮抗 α2 突触前自受体及 5-HT2/3 受体与 H1 受体，抗抑郁兼具显著助眠与促食欲。",
        "pk": {
            "brandName": "瑞美隆 (Remeron) | 欧加农 (Organon)",
            "halfLife": "20 - 40 小时 (女性约 37 小时，男性约 26 小时)",
            "halfLifeHours": 30.0,
            "tMax": "约 2.0 小时",
            "tMaxHours": 2.0,
            "bioavailability": "约 50%",
            "cypEnzymes": ["CYP2D6", "CYP3A4", "CYP1A2"],
            "clearance": "肝脏代谢，75% 经尿液排出，15% 经粪便排出",
            "indications": ["重度抑郁症 (伴严重失眠、焦虑或食欲进食显著减退者尤佳)"],
            "contraindications": ["严禁与单胺氧化酶抑制剂 (MAOI) 合用", "反常镇静：低剂量 (7.5-15mg) 因 H1 亲和力占优镇静反而比高剂量 (30-45mg) 更强", "体重明显增加"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 7.5, "commonMin": 15.0, "strongMin": 30.0, "heavyMin": 45.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.5, "max": 2.5, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 45.0, "max": 55.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (反苯环丙胺、苯乙肼等)"],
            "unsafe": ["酒精 (乙醇)", "苯二氮䓬类中枢抑制剂", "曲马多", "酮康唑"],
            "uncertain": ["卡马西平", "西咪替丁"]
        }
    },
    {
        "name": "Fluvoxamine",
        "name_zh": "氟伏沙明",
        "aliases": ["兰释", "Luvox", "马来酸氟伏沙明", "氟伏草胺"],
        "url": "https://en.wikipedia.org/wiki/Fluvoxamine",
        "categories": ["antidepressant", "ssri", "common"],
        "summary": "选择性 5-HT 再摄取抑制剂 (SSRI)，兼具极强 σ-1 受体激动活性。对强迫症 (OCD) 疗效突出；为 CYP1A2 强效抑制剂。",
        "pk": {
            "brandName": "兰释 (Luvox) | 雅培 / 迈兰 (Mylan)",
            "halfLife": "15.6 小时 (单次给药) 至 17-22 小时 (稳态)",
            "halfLifeHours": 18.0,
            "tMax": "3.0 - 8.0 小时 (平均 5 小时)",
            "tMaxHours": 5.0,
            "bioavailability": "约 53%",
            "cypEnzymes": ["CYP1A2(强效抑制剂)", "CYP2C19(中效抑制剂)", "CYP2D6(代谢)"],
            "clearance": "肝脏氧化脱烃代谢，尿排泄 94%",
            "indications": ["强迫症 (OCD, FDA批准成人及儿童)", "重度抑郁症 (MDD)", "社交焦虑障碍"],
            "contraindications": ["严禁与替扎尼定、阿戈美拉汀、氯氮平合用 (强阻断 CYP1A2 引起致命毒性)", "严禁与 MAOI 合用 (五羟色胺综合征)", "不可与咖啡因过量同服"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 50.0, "commonMin": 100.0, "strongMin": 200.0, "heavyMin": 300.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 3.0, "max": 8.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 50.0, "max": 55.0}
            }
        ],
        "interactions": {
            "dangerous": ["替扎尼定", "阿戈美拉汀", "氯氮平", "单胺氧化酶抑制剂 (MAOI)", "雷美替胺"],
            "unsafe": ["茶碱", "华法林", "阿普唑仑", "奥氮平"],
            "uncertain": ["咖啡因 (半衰期大幅延长数倍)"]
        }
    },
    {
        "name": "Citalopram",
        "name_zh": "西酞普兰",
        "aliases": ["喜普妙", "Celexa", "氢溴酸西酞普兰"],
        "url": "https://en.wikipedia.org/wiki/Citalopram",
        "categories": ["antidepressant", "ssri", "common"],
        "summary": "经典 SSRI 外消旋体 (由左旋 S-体艾司西酞普兰与右旋 R-体组成)。每日上限 40mg (老年人 20mg)，需防范剂量依赖性 QT 延长。",
        "pk": {
            "brandName": "喜普妙 (Celexa/Cipramil) | 灵北 (Lundbeck)",
            "halfLife": "约 35 小时 (老年人及肝功能损害者达 50 小时)",
            "halfLifeHours": 35.0,
            "tMax": "2.0 - 4.0 小时",
            "tMaxHours": 3.0,
            "bioavailability": "约 80%",
            "cypEnzymes": ["CYP2C19", "CYP3A4", "CYP2D6"],
            "clearance": "肝脏代谢，尿排泄 85%，粪便 15%",
            "indications": ["重度抑郁症", "伴有或不伴广场恐怖的惊恐障碍"],
            "contraindications": ["先天性长 QT 综合征禁用，极量严禁超过 40mg/d (老年人 20mg/d)", "严禁与 MAOI 合用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 10.0, "commonMin": 20.0, "strongMin": 30.0, "heavyMin": 40.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 75.0, "max": 85.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI)", "匹莫齐特", "延长 QT 间期药物"],
            "unsafe": ["奥美拉唑 (CYP2C19抑制导致血药浓度升高)", "曲马多", "非甾体抗炎药 (NSAIDs)"],
            "uncertain": ["酒精 (乙醇)"]
        }
    },
    {
        "name": "Agomelatine",
        "name_zh": "阿戈美拉汀",
        "aliases": ["妥抒", "Valdoxan", "阿戈美拉汀片"],
        "url": "https://en.wikipedia.org/wiki/Agomelatine",
        "categories": ["antidepressant", "melatonergic", "common"],
        "summary": "褪黑素 MT1/MT2 受体激动剂与 5-HT2C 受体特异拮抗剂。调节昼夜节律改善睡眠架构，不引起性功能障碍或体重增加，但用药必须严密监测肝酶转氨酶。",
        "pk": {
            "brandName": "妥抒 (Valdoxan) | 施维雅 (Servier)",
            "halfLife": "1.0 - 2.0 小时 (超短消除)",
            "halfLifeHours": 1.5,
            "tMax": "0.75 - 1.5 小时",
            "tMaxHours": 1.0,
            "bioavailability": "< 5% (肝脏首过清除极高)",
            "cypEnzymes": ["CYP1A2 (90%)", "CYP2C9/2C19 (10%)"],
            "clearance": "肝脏羟基化及脱甲基化，尿排泄 80%",
            "indications": ["重度抑郁症伴生物节律/睡眠障碍"],
            "contraindications": ["肝功能损害或转氨酶超过正常上限 3 倍者严禁用药", "治疗前、第 6/12/24 周必须强制监测 ALT/AST 肝功能", "严禁与强效 CYP1A2 抑制剂合用 (如氟伏沙明、环丙沙星)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 25.0, "strongMin": 50.0, "heavyMin": 50.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 0.75, "max": 1.5, "units": "hours"},
                    "total": {"min": 6.0, "max": 10.0, "units": "hours"}
                },
                "bioavailability": {"min": 3.0, "max": 8.0}
            }
        ],
        "interactions": {
            "dangerous": ["氟伏沙明 (血药暴露暴增 60 倍)", "环丙沙星"],
            "unsafe": ["雌激素类药物 (升高阿戈美拉汀浓度)", "酒精 (乙醇)"],
            "uncertain": ["普萘洛尔"]
        }
    },
    {
        "name": "Vortioxetine",
        "name_zh": "伏硫西汀",
        "aliases": ["心达悦", "Brintellix", "Trintellix", "氢溴酸伏硫西汀"],
        "url": "https://en.wikipedia.org/wiki/Vortioxetine",
        "categories": ["antidepressant", "multimodal", "common"],
        "summary": "多模态抗抑郁药 (5-HT3/7/1D 拮抗，5-HT1B 部分激动，5-HT1A 全激动，SERT 再摄取阻滞)。显著改善抑郁症患者的认知受损与执行功能，胃肠道恶心常见。",
        "pk": {
            "brandName": "心达悦 (Brintellix/Trintellix) | 灵北 / 武田 (Takeda)",
            "halfLife": "约 66 小时",
            "halfLifeHours": 66.0,
            "tMax": "7.0 - 11.0 小时",
            "tMaxHours": 8.0,
            "bioavailability": "约 75%",
            "cypEnzymes": ["CYP2D6 (主要)", "CYP3A4", "CYP2C9"],
            "clearance": "经 CYP2D6 氧化后葡萄糖醛酸化，尿排泄 59%，粪便 26%",
            "indications": ["重度抑郁症 (MDD, 特别伴随认知迟钝与注意力涣散者)"],
            "contraindications": ["严禁与 MAOI 合用 (停药至少间隔 14 天/21 天)", "恶心发生率约 30% (建议饭后或睡前服以缓解)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 5.0, "commonMin": 10.0, "strongMin": 15.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "peak": {"min": 7.0, "max": 11.0, "units": "hours"},
                    "total": {"min": 48.0, "max": 72.0, "units": "hours"}
                },
                "bioavailability": {"min": 70.0, "max": 80.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI)", "利奈唑胺"],
            "unsafe": ["安非他酮 (CYP2D6强抑制使伏硫西汀暴露翻倍)", "氟西汀", "曲马多"],
            "uncertain": ["利福平 (降低浓度)"]
        }
    },
    {
        "name": "Amitriptyline",
        "name_zh": "阿米替林",
        "aliases": ["盐酸阿米替林", "Elavil", "阿米替林片"],
        "url": "https://en.wikipedia.org/wiki/Amitriptyline",
        "categories": ["antidepressant", "tca", "common"],
        "summary": "经典第一代三环类抗抑郁药 (TCA)。强效阻滞 5-HT 及 NE 再摄取，兼具强抗胆碱能、抗组胺与抗 α 作用。镇痛与偏头痛预防应用广泛，过量有心脏毒性。",
        "pk": {
            "brandName": "依拉维 (Elavil) | 默沙东 (MSD)",
            "halfLife": "10 - 28 小时 (活性代谢物去甲替林: 18 - 44 小时)",
            "halfLifeHours": 21.0,
            "tMax": "2.0 - 4.0 小时",
            "tMaxHours": 3.0,
            "bioavailability": "30 - 60% (首过消除明显)",
            "cypEnzymes": ["CYP2D6", "CYP2C19", "CYP3A4", "CYP1A2"],
            "clearance": "肝脏脱甲基转化为去甲替林，经尿液排泄",
            "indications": ["重度抑郁症", "神经病理性疼痛 (带状疱疹后神经痛、纤维肌痛)", "慢性紧张型头痛与偏头痛预防"],
            "contraindications": ["心肌梗死急性恢复期禁用", "青光眼、前列腺增生伴尿潴留禁用", "抗胆碱副作用显著 (口干、视力模糊、便秘、心动过速、认知迟钝)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 10.0, "commonMin": 25.0, "strongMin": 75.0, "heavyMin": 150.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 35.0, "max": 55.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI) (致死高热惊厥危象)", "西沙必利"],
            "unsafe": ["曲马多", "酒精 (乙醇)", "选择性5-羟色胺再摄取抑制剂 (SSRI) (Fluoxetine/Paroxetine 抑制 CYP2D6 致毒性蓄积)"],
            "uncertain": ["西咪替丁"]
        }
    },
    {
        "name": "Clomipramine",
        "name_zh": "氯米帕明",
        "aliases": ["安拿芬尼", "Anafranil", "盐酸氯米帕明"],
        "url": "https://en.wikipedia.org/wiki/Clomipramine",
        "categories": ["antidepressant", "tca", "common"],
        "summary": "三环类抗抑郁药，为三环类中 5-HT 再摄取抑制作用最强者。临床公认强迫症 (OCD) 药物治疗的经典基准金标准。",
        "pk": {
            "brandName": "安拿芬尼 (Anafranil) | 诺华 (Novartis)",
            "halfLife": "19 - 37 小时 (活性代谢产物去甲基氯米帕明: 54 - 77 小时)",
            "halfLifeHours": 32.0,
            "tMax": "2.0 - 6.0 小时",
            "tMaxHours": 4.0,
            "bioavailability": "约 50%",
            "cypEnzymes": ["CYP2D6", "CYP1A2", "CYP3A4", "CYP2C19"],
            "clearance": "肝脏代谢，主要由肾脏排泄",
            "indications": ["强迫性神经症 (OCD)", "难治性抑郁症", "猝倒症 (发作性睡病伴发)"],
            "contraindications": ["严禁与 MAOI 合用", "癫痫发作阈值显著降低 (剂量 > 250mg 惊厥风险升高)", "抗胆碱严重反应及心脏传导阻滞"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 150.0, "heavyMin": 250.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 6.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 48.0, "units": "hours"}
                },
                "bioavailability": {"min": 45.0, "max": 55.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI)", "利奈唑胺"],
            "unsafe": ["曲马多", "选择性5-羟色胺再摄取抑制剂 (SSRI)", "抗胆碱能药物", "酒精 (乙醇)"],
            "uncertain": ["吸烟 (烟草多环芳烃诱导CYP1A2)"]
        }
    },
    {
        "name": "Doxepin",
        "name_zh": "多塞平",
        "aliases": ["盐酸多塞平", "Sinequan", "Silenor", "普虑平"],
        "url": "https://en.wikipedia.org/wiki/Doxepin",
        "categories": ["antidepressant", "tca", "common"],
        "summary": "三环类抗抑郁药，超低剂量 (3-6mg) 表现出对组胺 H1 受体亚纳摩尔级的极端高选择性，为 FDA 批准的无成瘾性睡眠维持型催眠药。",
        "pk": {
            "brandName": "赛乐诺 (Silenor, 3/6mg 低剂量催眠) / Sinequan (高剂量抗抑郁)",
            "halfLife": "15 - 19 小时 (活性代谢物去甲基多塞平: 31 小时)",
            "halfLifeHours": 17.0,
            "tMax": "约 2.0 小时 (餐后推迟)",
            "tMaxHours": 2.0,
            "bioavailability": "约 30%",
            "cypEnzymes": ["CYP2D6", "CYP2C19"],
            "clearance": "肝脏代谢，尿排泄",
            "indications": ["睡眠维持困难型失眠 (超低剂量 3-6mg)", "抑郁症及焦虑状态伴睡眠障碍 (常规高剂量 50-150mg)"],
            "contraindications": ["未经治疗的闭角型青光眼或严重尿潴留禁用", "严禁与 MAOI 合用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 3.0, "commonMin": 6.0, "strongMin": 25.0, "heavyMin": 100.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.5, "max": 3.0, "units": "hours"},
                    "total": {"min": 8.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 25.0, "max": 35.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI)"],
            "unsafe": ["酒精 (乙醇)", "西咪替丁", "选择性5-羟色胺再摄取抑制剂 (SSRI)"],
            "uncertain": ["妥拉磺脲"]
        }
    },

    # ==========================================
    # 3. 苯二氮䓬与非苯催眠镇静药 (Benzos & Z-drugs)
    # ==========================================
    {
        "name": "Alprazolam",
        "name_zh": "阿普唑仑",
        "aliases": ["佳静安定", "Xanax", "三唑仑类似物", "甲基三唑安定"],
        "url": "https://en.wikipedia.org/wiki/Alprazolam",
        "categories": ["benzodiazepine", "anxiolytic", "common"],
        "summary": "强效中短效三唑苯二氮䓬类药物。快速缓解急性焦虑与惊恐发作，具有显著欣快与依赖耐受潜力，撤药综合征极为剧烈。",
        "pk": {
            "brandName": "佳静安定 (Xanax) | 辉瑞 (Pfizer)",
            "halfLife": "11.2 小时 (范围 6.3 - 26.9 小时)",
            "halfLifeHours": 11.2,
            "tMax": "1.0 - 2.0 小时",
            "tMaxHours": 1.5,
            "bioavailability": "80 - 90%",
            "cypEnzymes": ["CYP3A4 (主要代谢酶)"],
            "clearance": "肝脏 CYP3A4 羟基化为 4-羟基和 α-羟基阿普唑仑，经肾排出",
            "indications": ["广泛性焦虑障碍 (GAD)", "惊恐发作伴或不伴惊恐障碍 (Panic Disorder)", "抑郁相关的急性焦虑状态短期缓解"],
            "contraindications": ["严禁与强效 CYP3A4 抑制剂 (酮康唑、伊曲康唑) 合用", "急性闭角型青光眼禁用", "高度依赖成瘾风险，严禁突然停药 (可致反跳性重度焦虑、谵妄及癫痫大发作)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 0.25, "commonMin": 0.5, "strongMin": 1.0, "heavyMin": 2.0},
                "duration": {
                    "onset": {"min": 0.25, "max": 0.5, "units": "hours"},
                    "peak": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "total": {"min": 6.0, "max": 12.0, "units": "hours"}
                },
                "bioavailability": {"min": 80.0, "max": 90.0}
            }
        ],
        "interactions": {
            "dangerous": ["阿片类药物 (致命呼吸骤停)", "酮康唑", "伊曲康唑"],
            "unsafe": ["酒精 / 乙醇 (协同严重 CNS 抑制致昏迷)", "西柚汁 (葡萄柚汁)", "西咪替丁"],
            "uncertain": ["氟伏沙明"]
        }
    },
    {
        "name": "Clonazepam",
        "name_zh": "氯硝西泮",
        "aliases": ["利福全", "Klonopin", "Rivotril", "氯硝安定"],
        "url": "https://en.wikipedia.org/wiki/Clonazepam",
        "categories": ["benzodiazepine", "anxiolytic", "anticonvulsant", "common"],
        "summary": "高亲和力高效长效硝基苯二氮䓬类。抗焦虑、抗惊厥与肌松作用强，血药浓度稳定，广泛用于惊恐障碍、难治癫痫及 REM 睡眠行为障碍。",
        "pk": {
            "brandName": "利福全 (Rivotril/Klonopin) | 罗氏 (Roche)",
            "halfLife": "30 - 40 小时",
            "halfLifeHours": 35.0,
            "tMax": "1.0 - 4.0 小时",
            "tMaxHours": 2.5,
            "bioavailability": "约 90%",
            "cypEnzymes": ["CYP3A4", "NAT2 (乙酰化)"],
            "clearance": "肝脏还原为 7-氨基代谢物后经尿液排泄，极少原型排出",
            "indications": ["惊恐障碍", "失神发作、肌阵挛性癫痫发作", "不宁腿综合征 (RLS)", "快速眼动睡眠行为障碍 (RBD)"],
            "contraindications": ["重度肝功能不全禁用", "急性闭角型青光眼禁用", "长期用药耐受与躯体依赖，停药需数月缓慢阶梯递减"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 0.5, "commonMin": 1.0, "strongMin": 2.0, "heavyMin": 4.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.0, "max": 3.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 85.0, "max": 95.0}
            }
        ],
        "interactions": {
            "dangerous": ["阿片类药物", "酒精 / 乙醇 (协同强效中枢呼吸抑制)"],
            "unsafe": ["苯妥英钠", "苯巴比妥", "丙戊酸 / 丙戊酸钠 (可诱发失神发作持续状态)"],
            "uncertain": ["CYP3A4 抑制剂"]
        }
    },
    {
        "name": "Diazepam",
        "name_zh": "地西泮",
        "aliases": ["安定", "Valium", "安定片", "苯甲二氮䓬"],
        "url": "https://en.wikipedia.org/wiki/Diazepam",
        "categories": ["benzodiazepine", "anxiolytic", "anticonvulsant", "common"],
        "summary": "经典长效苯二氮䓬原型药。极高脂溶性起效迅速，活性代谢物半衰期可达 100-200 小时，急救止痉与酒精戒断治疗基石。",
        "pk": {
            "brandName": "安定 (Valium) | 罗氏 (Roche)",
            "halfLife": "原型 20 - 50 小时 (主要活性代谢物去甲地西泮: 36 - 200 小时)",
            "halfLifeHours": 48.0,
            "tMax": "0.5 - 2.0 小时 (脂溶性极高)",
            "tMaxHours": 1.0,
            "bioavailability": "约 98%",
            "cypEnzymes": ["CYP2C19", "CYP3A4"],
            "clearance": "肝脏代谢为去甲地西泮、替马西泮及奥沙西泮，肾脏排泄",
            "indications": ["焦虑症短期对症缓解", "癫痫持续状态急救 (静脉注射)", "骨骼肌痉挛缓解", "急性酒精戒断综合征预防震颤谵妄"],
            "contraindications": ["重症肌无力、严重呼吸抑制、睡眠呼吸暂停禁用", "多次给药活性代谢物在脂肪组织长达数天深度蓄积，老年人易嗜睡跌倒"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 2.5, "commonMin": 5.0, "strongMin": 10.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 0.25, "max": 0.75, "units": "hours"},
                    "peak": {"min": 0.5, "max": 2.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 95.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["阿片类药物", "中枢神经系统抑制剂"],
            "unsafe": ["奥美拉唑 (CYP2C19抑制延长清除)", "酒精 (乙醇)", "西咪替丁"],
            "uncertain": ["西柚汁 (葡萄柚汁)"]
        }
    },
    {
        "name": "Lorazepam",
        "name_zh": "劳拉西泮",
        "aliases": ["罗拉", "Ativan", "劳拉西泮片"],
        "url": "https://en.wikipedia.org/wiki/Lorazepam",
        "categories": ["benzodiazepine", "anxiolytic", "common"],
        "summary": "中短效羟基苯二氮䓬类。直接通过肝脏葡萄糖醛酸化代谢，完全不经过 CYP450 酶系统氧化，肝功能不全及老年患者的优先选择。",
        "pk": {
            "brandName": "罗拉 (Ativan) | 惠氏 / 辉瑞 (Pfizer)",
            "halfLife": "10 - 20 小时 (平均 14 小时，无活性蓄积产物)",
            "halfLifeHours": 14.0,
            "tMax": "1.5 - 2.5 小时",
            "tMaxHours": 2.0,
            "bioavailability": "约 90%",
            "cypEnzymes": ["不依赖 CYP450！通过 UGT2B7 / UGT2B15 葡萄糖醛酸化结合失活"],
            "clearance": "肝脏直接葡糖醛酸化为非活性物，88% 由尿液排出",
            "indications": ["焦虑障碍或抑郁症状伴随的焦虑短期治疗", "失眠症短期辅助", "癫痫持续状态急救一线 (静脉注射)", "精神科急性激越肌注控制"],
            "contraindications": ["重症肌无力、急性狭角型青光眼禁用", "相对地西泮不易在老年体内蓄积，但耐受与依赖性依然确切"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 0.5, "commonMin": 1.0, "strongMin": 2.0, "heavyMin": 4.0},
                "duration": {
                    "onset": {"min": 0.3, "max": 0.8, "units": "hours"},
                    "peak": {"min": 1.5, "max": 2.5, "units": "hours"},
                    "total": {"min": 8.0, "max": 16.0, "units": "hours"}
                },
                "bioavailability": {"min": 85.0, "max": 95.0}
            }
        ],
        "interactions": {
            "dangerous": ["阿片类药物 (致死性呼吸受损)"],
            "unsafe": ["丙戊酸 / 丙戊酸钠 (抑制葡糖醛酸结合使劳拉西泮浓度翻倍)", "酒精 (乙醇)", "丙磺舒"],
            "uncertain": ["复方口服避孕药"]
        }
    },
    {
        "name": "Oxazepam",
        "name_zh": "奥沙西泮",
        "aliases": ["去甲羟安定", "Serax", "舒宁"],
        "url": "https://en.wikipedia.org/wiki/Oxazepam",
        "categories": ["benzodiazepine", "anxiolytic", "common"],
        "summary": "短中效羟基苯二氮䓬类。地西泮的终极活性代谢物，同样无需 CYP450 氧化而直接与葡萄糖醛酸结合，吸收相对平缓无断崖峰值。",
        "pk": {
            "brandName": "舒宁 (Serax) | 惠氏",
            "halfLife": "4 - 15 小时 (平均 8.0 小时)",
            "halfLifeHours": 8.0,
            "tMax": "2.0 - 4.0 小时",
            "tMaxHours": 3.0,
            "bioavailability": "约 97%",
            "cypEnzymes": ["不依赖 CYP！肝脏 UGT 直接葡糖醛酸化结合"],
            "clearance": "尿液完全排泄结合物",
            "indications": ["轻中度焦虑、紧张与激动", "酒精戒断综合征伴震颤轻症", "肝功能受损患者的安心抗焦虑药"],
            "contraindications": ["重度呼吸衰竭、重症肌无力禁用", "起效缓慢达峰延迟，不适于突发急性惊恐发作抢救"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 10.0, "commonMin": 15.0, "strongMin": 30.0, "heavyMin": 60.0},
                "duration": {
                    "onset": {"min": 0.75, "max": 1.5, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 6.0, "max": 12.0, "units": "hours"}
                },
                "bioavailability": {"min": 90.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["阿片类药物"],
            "unsafe": ["酒精 (乙醇)", "中枢神经系统抑制剂"],
            "uncertain": ["苯妥英钠"]
        }
    },
    {
        "name": "Midazolam",
        "name_zh": "咪达唑仑",
        "aliases": ["多美康", "Versed", "Dormicum", "咪唑安定"],
        "url": "https://en.wikipedia.org/wiki/Midazolam",
        "categories": ["benzodiazepine", "sedative", "common"],
        "summary": "水溶性超短效咪唑并苯二氮䓬类。起效神速、顺行性遗忘作用极强、半衰期仅约 2 小时，为无痛内镜、手术麻醉诱导与 ICU 镇静核心首选用药。",
        "pk": {
            "brandName": "多美康 (Dormicum/Versed) | 罗氏 (Roche)",
            "halfLife": "1.5 - 2.5 小时 (超短消除)",
            "halfLifeHours": 2.0,
            "tMax": "口服 0.5 - 1.0 小时；肌注 15-30 分钟；静注即刻",
            "tMaxHours": 0.5,
            "bioavailability": "口服 36% (首过消除强)；肌注 > 90%",
            "cypEnzymes": ["CYP3A4", "CYP3A5"],
            "clearance": "肝脏迅速羟基化生成 1-羟基咪达唑仑后结合排泄，尿排出 60-80%",
            "indications": ["手术或诊断性操作前镇静、缓解恐惧与抗顺行遗忘", "全身麻醉诱导及维持", "难治性惊厥持续状态急救推注"],
            "contraindications": ["严禁在无通气抢救设备与心肺监护的非监护病区推注", "严禁与强效 CYP3A4 抑制剂合用", "重症肌无力禁用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 3.75, "commonMin": 7.5, "strongMin": 15.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 0.15, "max": 0.35, "units": "hours"},
                    "peak": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "total": {"min": 2.0, "max": 5.0, "units": "hours"}
                },
                "bioavailability": {"min": 30.0, "max": 45.0}
            }
        ],
        "interactions": {
            "dangerous": ["强效 CYP3A4 抑制剂 (Clarithromycin, Ketoconazole - 浓度提升5-10倍引起呼吸抑制)", "阿片类药物"],
            "unsafe": ["酒精 (乙醇)", "Protease inhibitors"],
            "uncertain": ["贯叶连翘 (圣约翰草)"]
        }
    },
    {
        "name": "Zolpidem",
        "name_zh": "唑吡坦",
        "aliases": ["思诺思", "Ambien", "Stilnox", "酒石酸唑吡坦"],
        "url": "https://en.wikipedia.org/wiki/Zolpidem",
        "categories": ["hypnotic", "z-drug", "common"],
        "summary": "吡啶类非苯二氮䓬催眠药 (Z-drug)。高选择性靶向结合 GABAA 受体 α1 亚基，专一发挥催眠镇静效应，抗焦虑与肌松作用弱，入睡困难一线首选。",
        "pk": {
            "brandName": "思诺思 (Stilnox/Ambien) | 赛诺菲 (Sanofi)",
            "halfLife": "2.4 小时 (女性及老年人清除偏慢，半衰期达 3-4 小时)",
            "halfLifeHours": 2.4,
            "tMax": "0.5 - 1.5 小时 (空腹最快 30 分钟达峰)",
            "tMaxHours": 0.8,
            "bioavailability": "约 70% (高脂肪餐推迟达峰并降低血峰)",
            "cypEnzymes": ["CYP3A4 (60%)", "CYP1A2", "CYP2C9"],
            "clearance": "肝脏氧化转化为无活性产物，尿排泄 56%，粪便 37%",
            "indications": ["入睡困难型严重失眠症短期治疗 (常规疗程不超过 2-4 周)"],
            "contraindications": ["【黑框警告】复杂睡眠行为 (包括异态睡眠梦游、睡中驾车、睡中烹饪进食，可致严重伤亡)", "必须在准备入睡前即刻上床服药", "重症肌无力、严重阻塞性睡眠呼吸暂停综合征 (OSA) 禁用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 5.0, "commonMin": 10.0, "strongMin": 10.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 0.25, "max": 0.5, "units": "hours"},
                    "peak": {"min": 0.5, "max": 1.5, "units": "hours"},
                    "total": {"min": 4.0, "max": 7.0, "units": "hours"}
                },
                "bioavailability": {"min": 65.0, "max": 75.0}
            }
        ],
        "interactions": {
            "dangerous": ["酒精 / 乙醇 (梦游致命行为发生率急剧上升)", "阿片类药物"],
            "unsafe": ["酮康唑", "利福平 (清除加速 70%)", "氟伏沙明"],
            "uncertain": ["选择性5-羟色胺再摄取抑制剂 (SSRI)"]
        }
    },
    {
        "name": "Zopiclone",
        "name_zh": "佐匹克隆",
        "aliases": ["忆梦返", "Imovane", "佐匹克隆片"],
        "url": "https://en.wikipedia.org/wiki/Zopiclone",
        "categories": ["hypnotic", "z-drug", "common"],
        "summary": "环吡咯酮类非苯二氮䓬催眠药。广谱作用于 GABAA 受体 α1、α2、α3 亚基，既缩短入睡时间又显著减少夜间觉醒次数，特征性副作用为次日口苦。",
        "pk": {
            "brandName": "忆梦返 (Imovane) | 赛诺菲 (Sanofi)",
            "halfLife": "约 5.0 小时 (老年人延长至 7-8 小时)",
            "halfLifeHours": 5.0,
            "tMax": "1.5 - 2.0 小时",
            "tMaxHours": 1.5,
            "bioavailability": "约 80%",
            "cypEnzymes": ["CYP3A4", "CYP2C8"],
            "clearance": "肝脏广泛脱甲基及氧化，部分经唾液腺排泄致口苦，尿排泄 80%",
            "indications": ["各种类型失眠症 (入睡困难、易醒及早醒)，特别是伴有中途频繁醒转者"],
            "contraindications": ["严重呼吸衰竭、重度睡眠呼吸暂停综合征禁用", "特征性金属味口苦 (发生率 > 10%)", "连续用药不建议超过 4 周"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 3.75, "commonMin": 7.5, "strongMin": 7.5, "heavyMin": 15.0},
                "duration": {
                    "onset": {"min": 0.3, "max": 0.6, "units": "hours"},
                    "peak": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "total": {"min": 6.0, "max": 8.0, "units": "hours"}
                },
                "bioavailability": {"min": 75.0, "max": 85.0}
            }
        ],
        "interactions": {
            "dangerous": ["酒精 / 乙醇 (严重协同神经抑制与谵妄)", "阿片类药物"],
            "unsafe": ["红霉素", "酮康唑", "卡马西平"],
            "uncertain": ["西咪替丁"]
        }
    },
    {
        "name": "Eszopiclone",
        "name_zh": "右佐匹克隆",
        "aliases": ["文飞", "Lunesta", "艾司佐匹克隆"],
        "url": "https://en.wikipedia.org/wiki/Eszopiclone",
        "categories": ["hypnotic", "z-drug", "common"],
        "summary": "佐匹克隆的右旋活性单一异构体。亲和力较左旋体高 50 倍，有效剂量减半，抗失眠同时保持完整睡眠架构，FDA 批准可用于长期慢性失眠管理。",
        "pk": {
            "brandName": "文飞 (Lunesta) | Sunovion / 大日本住友",
            "halfLife": "6.0 小时 (老年人延长至 9.0 小时)",
            "halfLifeHours": 6.0,
            "tMax": "1.0 小时 (进餐推迟达峰 1 小时)",
            "tMaxHours": 1.0,
            "bioavailability": "约 80%",
            "cypEnzymes": ["CYP3A4", "CYP2E1"],
            "clearance": "肝脏氧化水解，尿排泄为主",
            "indications": ["入睡困难及睡眠维持困难型慢性失眠症"],
            "contraindications": ["复杂睡眠行为 (梦游、梦驾) 风险警示", "避免高脂饮食后立即服药 (显著削弱峰浓度)", "次日口苦异味"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 3.0, "heavyMin": 3.0},
                "duration": {
                    "onset": {"min": 0.25, "max": 0.5, "units": "hours"},
                    "peak": {"min": 0.8, "max": 1.5, "units": "hours"},
                    "total": {"min": 6.0, "max": 8.5, "units": "hours"}
                },
                "bioavailability": {"min": 75.0, "max": 85.0}
            }
        ],
        "interactions": {
            "dangerous": ["酒精 (乙醇)", "阿片类药物"],
            "unsafe": ["酮康唑", "克拉霉素", "利福平"],
            "uncertain": ["西柚汁 (葡萄柚汁)"]
        }
    },
    {
        "name": "Zaleplon",
        "name_zh": "扎来普隆",
        "aliases": ["安钠芬", "Sonata", "扎来普隆胶囊"],
        "url": "https://en.wikipedia.org/wiki/Zaleplon",
        "categories": ["hypnotic", "z-drug", "common"],
        "summary": "吡唑并嘧啶类超短效催眠药。半衰期仅 1 小时，人体代谢极快，完全无次日宿醉迟钝感，适合半夜惊醒入睡困难补服 (只要剩余睡眠时间 > 4 小时)。",
        "pk": {
            "brandName": "安钠芬 (Sonata) | 辉瑞 (Pfizer)",
            "halfLife": "约 1.0 小时 (超短消除)",
            "halfLifeHours": 1.0,
            "tMax": "约 1.0 小时 (空腹)",
            "tMaxHours": 1.0,
            "bioavailability": "约 30% (高首过代谢)",
            "cypEnzymes": ["醛氧化酶 (主要)", "CYP3A4 (次要)"],
            "clearance": "主要经醛氧化酶代谢为 5-氧代扎来普隆，尿排泄 70%",
            "indications": ["入睡困难型失眠短期治疗", "夜间觉醒再次入睡困难 (需保证服后有 4 小时卧床时间)"],
            "contraindications": ["严重肝功能受损禁用", "高脂餐显著推迟达峰延后 2 小时", "复杂睡眠行为风险"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 5.0, "commonMin": 10.0, "strongMin": 10.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 0.2, "max": 0.4, "units": "hours"},
                    "peak": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "total": {"min": 3.0, "max": 5.0, "units": "hours"}
                },
                "bioavailability": {"min": 25.0, "max": 35.0}
            }
        ],
        "interactions": {
            "dangerous": ["酒精 (乙醇)"],
            "unsafe": ["西咪替丁 (抑制醛氧化酶使血药浓度剧增 85%)", "利福平"],
            "uncertain": ["中枢神经系统抑制剂"]
        }
    },
    {
        "name": "Buspirone",
        "name_zh": "丁螺环酮",
        "aliases": ["一舒", "BuSpar", "盐酸丁螺环酮"],
        "url": "https://en.wikipedia.org/wiki/Buspirone",
        "categories": ["anxiolytic", "common"],
        "summary": "氮杂双环葵烷二酮类 5-HT1A 受体部分激动剂。无镇静嗜睡、肌松松弛及成瘾滥用倾向，不产生戒断反应，但需要连续服用数周起效。",
        "pk": {
            "brandName": "一舒 (BuSpar) | 百时美施贵宝 (BMS)",
            "halfLife": "2.0 - 3.0 小时",
            "halfLifeHours": 2.5,
            "tMax": "0.7 - 1.5 小时",
            "tMaxHours": 1.0,
            "bioavailability": "约 4% (肝脏首过清除极高，餐后服用生物利用度提高)",
            "cypEnzymes": ["CYP3A4 (主要代谢酶)"],
            "clearance": "CYP3A4 代谢为 1-PP (1-嘧啶基哌嗪)，尿排泄 29-63%",
            "indications": ["广泛性焦虑障碍 (GAD) 的中长期管理", "抗抑郁治疗引起的性功能障碍对症缓解"],
            "contraindications": ["严禁与单胺氧化酶抑制剂 (MAOI) 合用 (高血压危象)", "起效缓慢 (通常需连续用药 2-4 周才达到最大抗焦虑效果，不可用于突发惊恐抢救)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 5.0, "commonMin": 15.0, "strongMin": 30.0, "heavyMin": 60.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.0, "max": 1.5, "units": "hours"},
                    "total": {"min": 6.0, "max": 10.0, "units": "hours"}
                },
                "bioavailability": {"min": 3.0, "max": 6.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI) (致命严重高血压反应)"],
            "unsafe": ["强效 CYP3A4 抑制剂 (Ketoconazole, Itraconazole, Erythromycin 显著升高浓度)", "西柚汁 (葡萄柚汁)"],
            "uncertain": ["氟哌啶醇", "曲唑酮"]
        }
    },

    # ==========================================
    # 4. 情绪稳定剂与神经调控药 (Mood Stabilizers & Anticonvulsants)
    # ==========================================
    {
        "name": "Carbamazepine",
        "name_zh": "卡马西平",
        "aliases": ["得理多", "Tegretol", "卡马西平片"],
        "url": "https://en.wikipedia.org/wiki/Carbamazepine",
        "categories": ["mood stabilizer", "anticonvulsant", "common"],
        "summary": "电压门控钠通道阻滞剂。双相障碍躁狂发作经典情绪稳定剂，三叉神经痛一线黄金用药；具有强大的自身酶诱导特性与重症药疹风险。",
        "pk": {
            "brandName": "得理多 (Tegretol) | 诺华 (Novartis)",
            "halfLife": "单剂 35 - 40 小时；连续服药自身酶诱导后缩短至 12 - 17 小时",
            "halfLifeHours": 15.0,
            "tMax": "4.0 - 8.0 小时 (缓释片约 12 小时)",
            "tMaxHours": 6.0,
            "bioavailability": "75 - 85%",
            "cypEnzymes": ["CYP3A4", "自身强效诱导剂 (诱导 CYP3A4, CYP1A2, CYP2C9, UGT)"],
            "clearance": "肝脏氧化生成活性产物 10,11-环氧化物，尿排泄 72%",
            "indications": ["双相情感障碍急性躁狂与混合发作", "原发性三叉神经痛及舌咽神经痛", "局灶性癫痫发作伴或不伴继发全面性发作"],
            "contraindications": ["房室传导阻滞、严重骨髓造血抑制禁用", "【严重药疹警告】HLA-B*1502 等位基因携带者 (汉族高发) 极易发生致死性 SJS/TEN，用药前必须强制基因筛查", "强酶诱导导致口服甾体避孕药/HRT 激素失效"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 100.0, "commonMin": 200.0, "strongMin": 600.0, "heavyMin": 1200.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 3.0, "units": "hours"},
                    "peak": {"min": 4.0, "max": 8.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 75.0, "max": 85.0}
            }
        ],
        "interactions": {
            "dangerous": ["氯氮平 (骨髓抑制协同致死)", "单胺氧化酶抑制剂 (MAOI)"],
            "unsafe": ["口服避孕药 / HRT (雌激素被加速清除失效)", "丙戊酸钠 / 丙戊酸", "红霉素", "氟西汀"],
            "uncertain": ["西柚汁 (葡萄柚汁)"]
        }
    },
    {
        "name": "Oxcarbazepine",
        "name_zh": "奥卡西平",
        "aliases": ["曲莱", "Trileptal", "奥卡西平片"],
        "url": "https://en.wikipedia.org/wiki/Oxcarbazepine",
        "categories": ["mood stabilizer", "anticonvulsant", "common"],
        "summary": "卡马西平的 10-酮基结构类似物前药。在体内直接还原为活性单羟基衍生物 (MHD)，自身酶诱导与过敏发生率远低于卡马西平，但易引起低钠血症。",
        "pk": {
            "brandName": "曲莱 (Trileptal) | 诺华 (Novartis)",
            "halfLife": "前药 2 小时 (活性代谢物 MHD: 8 - 10 小时)",
            "halfLifeHours": 9.0,
            "tMax": "活性代谢物 MHD 约 4.0 - 6.0 小时达峰",
            "tMaxHours": 5.0,
            "bioavailability": "全面吸收，生物利用度 > 95%",
            "cypEnzymes": ["胞质酮还原酶代谢；微弱诱导 CYP3A4，微弱抑制 CYP2C19"],
            "clearance": "MHD 经葡萄糖醛酸结合后随尿液排出 (95%)",
            "indications": ["双相障碍躁狂发作维持情绪稳定", "局灶性癫痫发作单药或添加治疗", "神经病理性疼痛辅助"],
            "contraindications": ["房室传导阻滞禁用", "低钠血症发生率较高 (需定期化验血电解质)", "与卡马西平存在 25-30% 交叉过敏"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 150.0, "commonMin": 300.0, "strongMin": 600.0, "heavyMin": 1200.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 4.0, "max": 6.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 90.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["大剂量联合口服避孕药 (降低避孕药有效性)"],
            "unsafe": ["酒精 (乙醇)", "苯妥英钠 (浓度升高)", "卡马西平"],
            "uncertain": ["丙戊酸钠 / 丙戊酸"]
        }
    },
    {
        "name": "Topiramate",
        "name_zh": "托吡酯",
        "aliases": ["妥泰", "Topamax", "托吡酯片"],
        "url": "https://en.wikipedia.org/wiki/Topiramate",
        "categories": ["anticonvulsant", "mood stabilizer", "common"],
        "summary": "磺胺取代单糖衍生物。具有阻断钠通道、增强 GABA、拮抗 AMPA/红藻氨酸受体及弱抑制碳酸酐酶多重机制。具有显著食欲抑制与减重特性，但可致认知迟钝。",
        "pk": {
            "brandName": "妥泰 (Topamax) | 强生杨森 (Janssen)",
            "halfLife": "约 21 小时 (线性药代动力学)",
            "halfLifeHours": 21.0,
            "tMax": "约 2.0 小时",
            "tMaxHours": 2.0,
            "bioavailability": "约 80%",
            "cypEnzymes": ["约 80% 不经代谢；部分经 CYP2C19 代谢"],
            "clearance": "以原型形式经肾小球滤过与肾小管排泄随尿排出 (约 70%)",
            "indications": ["偏头痛预防性发作减少", "癫痫发作单药或辅助", "情绪不稳定及暴食障碍/进食障碍辅助减重 (超适应症)"],
            "contraindications": ["妊娠期禁用 (致畸胎唇腭裂风险高)", "易诱发肾结石与代谢性酸中毒 (弱碳酸酐酶抑制，服药需大量饮水)", "特征性“话到嘴边说不出”、找词困难及思维迟钝 (Dopamax 效应)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 100.0, "heavyMin": 200.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 18.0, "max": 30.0, "units": "hours"}
                },
                "bioavailability": {"min": 75.0, "max": 85.0}
            }
        ],
        "interactions": {
            "dangerous": ["丙戊酸 / 丙戊酸钠 (协同诱发高氨血症性脑病与低温症)"],
            "unsafe": ["口服避孕药 (高剂量使炔雌醇暴露下降)", "碳酸酐酶抑制剂 (如乙酰唑胺，加剧肾结石风险)"],
            "uncertain": ["二甲双胍", "碳酸锂"]
        }
    },
    {
        "name": "Gabapentin",
        "name_zh": "加巴喷丁",
        "aliases": ["开思亭", "Neurontin", "加巴喷丁胶囊"],
        "url": "https://en.wikipedia.org/wiki/Gabapentin",
        "categories": ["anticonvulsant", "analgesic", "anxiolytic", "common"],
        "summary": "电压门控钙通道 α2δ 亚基配体。减少兴奋性神经递质释放，体内完全不代谢呈 100% 原型肾排泄。肠道吸收受 L-型氨基酸转运体饱和限制，剂量越大利用度反而递减。",
        "pk": {
            "brandName": "开思亭 (Neurontin) | 辉瑞 (Pfizer)",
            "halfLife": "5.0 - 7.0 小时 (肾功能减退时大幅延长)",
            "halfLifeHours": 6.0,
            "tMax": "2.0 - 3.0 小时",
            "tMaxHours": 2.5,
            "bioavailability": "饱和转运非线性：300mg 约 60%，400mg 约 47%，800mg 降至 34%",
            "cypEnzymes": ["完全不经肝脏 CYP450 代谢，不与血浆蛋白结合！"],
            "clearance": "100% 呈原型经肾脏随尿排泄",
            "indications": ["带状疱疹后神经痛 (PHN)", "成人及儿童部分性癫痫发作辅助", "广泛性焦虑及社交恐怖症 (超适应症)", "酒精依赖戒断辅助缓解"],
            "contraindications": ["严重肾功能减退患者必须按肌酐清除率严格减量", "突然停药可引发戒断症状反跳与癫痫发作", "常见头晕、嗜睡、共济失调与外周水肿"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 300.0, "commonMin": 600.0, "strongMin": 1200.0, "heavyMin": 2400.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 3.5, "units": "hours"},
                    "total": {"min": 6.0, "max": 10.0, "units": "hours"}
                },
                "bioavailability": {"min": 35.0, "max": 60.0}
            }
        ],
        "interactions": {
            "dangerous": ["阿片类药物 (严重协同中枢与呼吸抑制，FDA黑框警告)"],
            "unsafe": ["抗酸药物 (含铝镁抗酸药降低加巴喷丁吸收约 20%)", "酒精 (乙醇)"],
            "uncertain": ["吗啡 (增加加巴喷丁AUC)"]
        }
    },
    {
        "name": "Pregabalin",
        "name_zh": "普瑞巴林",
        "aliases": ["乐瑞卡", "Lyrica", "普瑞巴林胶囊"],
        "url": "https://en.wikipedia.org/wiki/Pregabalin",
        "categories": ["anticonvulsant", "analgesic", "anxiolytic", "common"],
        "summary": "新一代钙通道 α2δ 亚基特异配体。生物利用度 ≥90% 且呈理想线性吸收，疗效稳定预测性强。欧洲批准广泛性焦虑一线药物，但国内列管第二类精神药品防止滥用。",
        "pk": {
            "brandName": "乐瑞卡 (Lyrica) | 辉瑞 (Pfizer)",
            "halfLife": "约 6.3 小时",
            "halfLifeHours": 6.3,
            "tMax": "空腹 1.0 小时 (进食延迟达峰至 2.5 小时但不影响总量)",
            "tMaxHours": 1.0,
            "bioavailability": "≥ 90% (不受剂量饱和限制，线性吸收)",
            "cypEnzymes": ["体内基本不发生代谢，不抑制/诱导任何 CYP 酶"],
            "clearance": "约 98% 以原型经肾脏随尿排泄",
            "indications": ["广泛性焦虑障碍 (GAD, 欧洲一线推荐)", "神经病理性疼痛 (糖尿病外周神经痛、带状疱疹后神经痛)", "脊髓损伤后神经病理性疼痛", "纤维肌痛"],
            "contraindications": ["【第二类精神药品】具有躯体依赖与精神欣快潜力，需防范成瘾滥用", "心功能不全患者慎防充血性心衰加重与外周水肿", "头晕、嗜睡发生率高"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 50.0, "commonMin": 150.0, "strongMin": 300.0, "heavyMin": 600.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "total": {"min": 8.0, "max": 14.0, "units": "hours"}
                },
                "bioavailability": {"min": 90.0, "max": 95.0}
            }
        ],
        "interactions": {
            "dangerous": ["阿片类药物 (严重协同呼吸抑制与昏迷风险)"],
            "unsafe": ["劳拉西泮", "酒精 / 乙醇 (运动协调障碍与镇静大幅放大)", "噻唑烷二酮类降糖药 (加剧水肿)"],
            "uncertain": ["羟考酮"]
        }
    },

    # ==========================================
    # 5. 促智、注意缺陷多动障碍 (ADHD) 与觉醒促进药
    # ==========================================
    {
        "name": "Methylphenidate",
        "name_zh": "哌甲酯",
        "aliases": ["专注达", "利他林", "Concerta", "Ritalin", "盐酸哌甲酯"],
        "url": "https://en.wikipedia.org/wiki/Methylphenidate",
        "categories": ["stimulant", "adhd", "nootropic", "common"],
        "summary": "中枢神经去甲肾上腺素与多巴胺再摄取抑制剂 (NDRI)。前额叶认知控制与专注力提升的一线金标准，专注达采用渗透泵缓释技术维持 12 小时恒定疗效。",
        "pk": {
            "brandName": "专注达 (Concerta OROS 缓释) / 利他林 (Ritalin 速释) | 强生 / 诺华",
            "halfLife": "速释 2 - 3 小时；专注达 OROS 双峰释放平稳维持 12 小时",
            "halfLifeHours": 3.5,
            "tMax": "速释 1.5 - 2 小时；专注达 1 小时速释初峰、6-8 小时主峰",
            "tMaxHours": 2.0,
            "bioavailability": "约 30% (口服首过明显)",
            "cypEnzymes": ["主要经羧酸酯酶 CES1A1 脱酯化为非活性利他林酸 (不依赖 CYP450)"],
            "clearance": "90% 经尿液以利他林酸形式排泄",
            "indications": ["注意缺陷多动障碍 (ADHD)", "发作性睡病 (Narcolepsy)"],
            "contraindications": ["【第一类精神药品】青光眼、重症高血压、心律失常、甲亢禁用", "严禁与单胺氧化酶抑制剂 (MAOI) 合用 (高血压危象)", "慎用：明显焦虑、激越或抽动秽语综合征"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 5.0, "commonMin": 18.0, "strongMin": 36.0, "heavyMin": 54.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.5, "max": 6.0, "units": "hours"},
                    "total": {"min": 4.0, "max": 12.0, "units": "hours"}
                },
                "bioavailability": {"min": 25.0, "max": 35.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI)", "血管加压药 / 升压药"],
            "unsafe": ["酒精 / 乙醇 (破坏缓释机制导致剂量倾泻)", "华法林", "抗惊厥 / 抗癫痫药"],
            "uncertain": ["可乐定"]
        }
    },
    {
        "name": "Modafinil",
        "name_zh": "莫达非尼",
        "aliases": ["保清", "Provigil", "莫达芬尼", "不睡药"],
        "url": "https://en.wikipedia.org/wiki/Modafinil",
        "categories": ["stimulant", "wakefulness", "nootropic", "common"],
        "summary": "非安非他命类选择性促觉醒剂。微弱抑制多巴胺再摄取，活化下丘脑食欲素与下丘脑组胺系统，提供纯净促醒专注且无外周交感神经震颤心悸。",
        "pk": {
            "brandName": "保清 (Provigil) | Cephalon / Teva",
            "halfLife": "约 15 小时 (消除平稳)",
            "halfLifeHours": 15.0,
            "tMax": "2.0 - 4.0 小时",
            "tMaxHours": 2.5,
            "bioavailability": "高 (胃肠道吸收良好)",
            "cypEnzymes": ["CYP3A4/5(诱导剂)", "CYP2C19(抑制剂)", "CYP1A2(微弱诱导)"],
            "clearance": "肝脏代谢为莫达非尼酸及砜化物，肾脏排泄 80%",
            "indications": ["发作性睡病所致白天过度嗜睡 (EDS)", "阻塞性睡眠呼吸暂停低通气综合征辅助促醒", "轮班工作睡眠障碍 (SWSD)"],
            "contraindications": ["【重症剥脱性皮疹黑框警告】一旦出现皮疹立即永久停药 (防止 SJS/TEN 致死)", "强效诱导 CYP3A4，口服甾体避孕药及 HRT 激素水平显著下降导致避孕失效", "二尖瓣脱垂或左室肥厚心血管病史禁用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 50.0, "commonMin": 100.0, "strongMin": 200.0, "heavyMin": 400.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 10.0, "max": 16.0, "units": "hours"}
                },
                "bioavailability": {"min": 80.0, "max": 90.0}
            }
        ],
        "interactions": {
            "dangerous": ["甾体避孕药 / 雌激素 (诱导CYP3A4使避孕药/HRT失效)", "环孢素"],
            "unsafe": ["地西泮", "苯妥英钠", "华法林", "奥美拉唑"],
            "uncertain": ["酒精 (乙醇)"]
        }
    },
    {
        "name": "Armodafinil",
        "name_zh": "阿莫达非尼",
        "aliases": ["纽维吉", "Nuvigil", "左旋莫达非尼单一异构体"],
        "url": "https://en.wikipedia.org/wiki/Armodafinil",
        "categories": ["stimulant", "wakefulness", "nootropic", "common"],
        "summary": "莫达非尼的纯 R-对映异构体。比外消旋体具有更高的稳态血浆消除半衰期与更持久的午后促清醒平台期，药效平稳持久。",
        "pk": {
            "brandName": "纽维吉 (Nuvigil) | Teva",
            "halfLife": "约 15 小时",
            "halfLifeHours": 15.0,
            "tMax": "约 2.0 小时",
            "tMaxHours": 2.0,
            "bioavailability": "高",
            "cypEnzymes": ["CYP3A4(诱导剂)", "CYP2C19(中度抑制剂)"],
            "clearance": "肝脏水解氧化，尿排泄为主",
            "indications": ["发作性睡病与轮班工作障碍相关的白天过度嗜睡改善"],
            "contraindications": ["严重多形红斑与 Stevens-Johnson 综合征风险", "显著削弱口服避孕药及雌激素替代疗法血药水平"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 50.0, "commonMin": 150.0, "strongMin": 250.0, "heavyMin": 250.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.5, "max": 2.5, "units": "hours"},
                    "total": {"min": 12.0, "max": 18.0, "units": "hours"}
                },
                "bioavailability": {"min": 85.0, "max": 95.0}
            }
        ],
        "interactions": {
            "dangerous": ["激素类避孕药 / HRT (CYP3A4 诱导导致疗效失效)"],
            "unsafe": ["奥美拉唑", "地西泮", "华法林"],
            "uncertain": ["中枢神经系统兴奋剂"]
        }
    },
    {
        "name": "Clonidine",
        "name_zh": "可乐定",
        "aliases": ["开普乐", "Catapres", "盐酸可乐定", "可乐宁"],
        "url": "https://en.wikipedia.org/wiki/Clonidine",
        "categories": ["anxiolytic", "adhd", "antihypertensive", "common"],
        "summary": "中枢性 α2 肾上腺素受体激动剂。激活脑桥蓝斑核自身受体抑制交感神经冲动，用于难治性高血压、ADHD 二线改善冲动及阿片类药物戒断反应辅助控制。",
        "pk": {
            "brandName": "开普乐 (Catapres) / Kapvay (缓释 ADHD) | 勃林格殷格翰",
            "halfLife": "12 - 16 小时 (肾功能衰竭时可达 41 小时)",
            "halfLifeHours": 14.0,
            "tMax": "3.0 - 5.0 小时",
            "tMaxHours": 3.5,
            "bioavailability": "75 - 95%",
            "cypEnzymes": ["CYP2D6", "CYP1A2", "CYP3A4"],
            "clearance": "40-60% 呈原型经肾脏随尿排泄，其余肝脏代谢",
            "indications": ["儿童注意缺陷多动障碍 (ADHD) 伴多动冲动或抽动障碍", "高血压危象与难治性高血压", "阿片受体激动剂急骤戒断时自主神经亢进对症缓解"],
            "contraindications": ["严禁突然漏服或剧烈停药！否则可引发灾难性恶性高血压反跳危象与交感神经过度放电", "重度心动过缓与房室传导阻滞禁用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 0.05, "commonMin": 0.1, "strongMin": 0.2, "heavyMin": 0.4},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 8.0, "max": 16.0, "units": "hours"}
                },
                "bioavailability": {"min": 75.0, "max": 95.0}
            }
        ],
        "interactions": {
            "dangerous": ["β受体阻滞剂 (停药时加剧恶性高血压反跳)", "TCA (减弱降压效力)"],
            "unsafe": ["酒精 (乙醇)", "中枢神经系统抑制剂", "洋地黄类强心苷 (加重心动过缓)"],
            "uncertain": ["左旋多巴"]
        }
    },
    {
        "name": "Flupentixol and melitracen",
        "name_zh": "氟哌噻吨美利曲辛",
        "aliases": ["黛力新", "Deanxit", "氟哌噻吨美利曲辛片"],
        "url": "https://en.wikipedia.org/wiki/Flupentixol/melitracen",
        "categories": ["antidepressant", "anxiolytic", "common"],
        "summary": "小剂量噻吨类抗精神病药 (氟哌噻吨 0.5mg) 与小剂量三环抗抑郁药 (美利曲辛 10mg) 复方制剂。协同作用于突触前膜增强多巴胺/去甲肾上腺素传递，起效迅速，综合医院广泛用于轻中度焦虑抑郁伴躯体化障碍。",
        "pk": {
            "brandName": "黛力新 (Deanxit) | 丹麦灵北 (Lundbeck)",
            "halfLife": "氟哌噻吨约 35 小时；美利曲辛约 19 小时",
            "halfLifeHours": 27.0,
            "tMax": "氟哌噻吨 4.0 小时；美利曲辛 4.0 小时",
            "tMaxHours": 4.0,
            "bioavailability": "氟哌噻吨 40%；美利曲辛 50%",
            "cypEnzymes": ["CYP2D6 (主要代谢)", "CYP3A4"],
            "clearance": "肝脏代谢，经胆汁粪便与肾脏尿液排出",
            "indications": ["轻中度抑郁和焦虑状态", "胃肠道及心血管神经症等各种躯体化功能性自主神经紊乱", "神经衰弱"],
            "contraindications": ["严禁与非选择性单胺氧化酶抑制剂 (MAOI) 合用", "心肌梗死恢复早期、房室传导阻滞禁用", "不推荐长期无休止服用，防范迟发性运动障碍 (TD) 风险"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 2.0, "heavyMin": 4.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 3.0, "max": 5.0, "units": "hours"},
                    "total": {"min": 18.0, "max": 30.0, "units": "hours"}
                },
                "bioavailability": {"min": 40.0, "max": 50.0}
            }
        ],
        "interactions": {
            "dangerous": ["单胺氧化酶抑制剂 (MAOI)", "拟交感神经药物 (肾上腺素等增压反应加剧)"],
            "unsafe": ["酒精 (乙醇)", "中枢神经系统抑制剂", "抗胆碱能药物"],
            "uncertain": ["降血压药物"]
        }
    },

    # ==========================================
    # 6. 性别肯定激素替代治疗 (HRT 全系补充：雌激素、抗雄阻断剂、孕激素、雄激素)
    # ==========================================
    {
        "name": "Estradiol enanthate",
        "name_zh": "庚酸雌二醇",
        "aliases": ["EEn", "庚酸雌二醇注射液", "Perlutal", "Topasel"],
        "url": "https://en.wikipedia.org/wiki/Estradiol_enanthate",
        "categories": ["hrt", "estrogen", "hormone", "common"],
        "summary": "长链雌二醇脂肪酸前药酯。肌肉注射或皮下注射吸收极度平稳，消除半衰期长达 5.6 - 7.0 天，每 7-14 天注射一次即可维持平稳女性生理雌激素水平，是跨性别女性 (MtF) HRT 黄金推荐制剂。",
        "pk": {
            "brandName": "Perlutal / 跨性别社群自配医用级标准制剂 (EEn Depot)",
            "halfLife": "肌注或深层皮下注射约 5.6 - 7.0 天 (长效储存库效应)",
            "halfLifeHours": 144.0,
            "tMax": "注射后 3.0 - 4.5 天达到血浆峰浓度",
            "tMaxHours": 84.0,
            "bioavailability": "100% (完全规避口服肝脏首过清除与凝血级联刺激)",
            "cypEnzymes": ["体内酯酶裂解为游离雌二醇；经 CYP3A4、CYP1A2 代谢，UGT 葡糖醛酸化结合"],
            "clearance": "肝脏水解氧化，结合物经胆汁随粪便及肾脏尿液排出",
            "indications": ["跨性别女性 (MtF) 性别肯定激素替代治疗 (维持血清 E2 100-200 pg/mL)", "雌激素单药疗法 (Monotherapy, 靠平稳充足高水平雌激素强效负反馈抑制 LH/FSH 垂体分泌，无需服用抗雄药物即可完全压制睾酮水平)"],
            "contraindications": ["活动性静脉血栓栓塞症 (VTE)、肺栓塞禁用", "已知或疑似雌激素依赖性恶性肿瘤禁用", "严重活动性肝病禁用", "必须定期监测血清雌二醇 (E2) 谷值与总睾酮 (T) 浓度"]
        },
        "roas": [
            {
                "name": "intramuscular",
                "dose": {"units": "mg", "lightMin": 3.0, "commonMin": 5.0, "strongMin": 8.0, "heavyMin": 12.0},
                "duration": {
                    "onset": {"min": 12.0, "max": 24.0, "units": "hours"},
                    "peak": {"min": 72.0, "max": 108.0, "units": "hours"},
                    "total": {"min": 168.0, "max": 336.0, "units": "hours"}
                },
                "bioavailability": {"min": 98.0, "max": 100.0}
            },
            {
                "name": "subcutaneous",
                "dose": {"units": "mg", "lightMin": 3.0, "commonMin": 5.0, "strongMin": 7.0, "heavyMin": 10.0},
                "duration": {
                    "onset": {"min": 12.0, "max": 24.0, "units": "hours"},
                    "peak": {"min": 72.0, "max": 120.0, "units": "hours"},
                    "total": {"min": 168.0, "max": 336.0, "units": "hours"}
                },
                "bioavailability": {"min": 98.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["强促血栓形成药物"],
            "unsafe": ["CYP3A4 诱导剂 (Carbamazepine, Modafinil, St John's Wort 加快雌激素清除)", "吸烟 (烟草多环芳烃显著加快代谢)"],
            "uncertain": ["拉莫三嗪 (雌激素加速拉莫三嗪清除)"]
        }
    },
    {
        "name": "Estradiol hemihydrate",
        "name_zh": "半水合雌二醇",
        "aliases": ["爱斯妥", "Oestrogel", "诺坤复", "Estragel", "雌二醇凝胶", "雌二醇贴片"],
        "url": "https://en.wikipedia.org/wiki/Estradiol_hemihydrate",
        "categories": ["hrt", "estrogen", "hormone", "common"],
        "summary": "天然生物等同 17β-雌二醇微粒晶体制剂。经皮透皮吸收 (凝胶涂抹或贴片)，直接渗入毛细血管网进入大循环，完全避开肝脏首过代谢，血栓栓塞风险在所有给药方式中最低。",
        "pk": {
            "brandName": "爱斯妥 (Oestrogel) 凝胶 / 松奇贴片 / 诺坤复片剂 | 法国贝斯迪 (Besins)",
            "halfLife": "透皮给药因皮肤角质层储库效应达 36 小时；游离 E2 半衰期约 1-2 小时",
            "halfLifeHours": 36.0,
            "tMax": "经皮凝胶涂抹后 2.0 - 4.0 小时；贴片维持恒定释放",
            "tMaxHours": 3.0,
            "bioavailability": "经皮凝胶约 10% (吸收效率视皮肤角质层及部位而定，阴囊皮肤透皮吸收率为空前 5 倍以上)",
            "cypEnzymes": ["CYP3A4", "CYP1A2", "SULT1E1", "UGT1A1"],
            "clearance": "肝脏氧化为雌酮 (E1) 及雌三醇 (E3)，随尿液及粪便排泄",
            "indications": ["跨性别女性 (MtF) 性别肯定激素替代治疗", "绝经期综合征雌激素补充", "对于有高血栓风险、肝功能异常或吸烟者的最佳雌激素首选形式"],
            "contraindications": ["乳腺癌、雌激素依赖性肿瘤禁用", "凝胶严禁涂抹于乳房区域 (防范局部乳腺病变) 及面部；适宜涂抹于手臂、大腿内侧或阴囊部位"]
        },
        "roas": [
            {
                "name": "transdermal",
                "dose": {"units": "mg", "lightMin": 0.75, "commonMin": 1.5, "strongMin": 3.0, "heavyMin": 6.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 6.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 48.0, "units": "hours"}
                },
                "bioavailability": {"min": 8.0, "max": 15.0}
            },
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 1.0, "commonMin": 2.0, "strongMin": 4.0, "heavyMin": 8.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 3.0, "max": 5.0}
            }
        ],
        "interactions": {
            "dangerous": ["吸烟 (吸烟显著增加口服血栓风险，透皮相对较优)"],
            "unsafe": ["强效 CYP3A4 诱导剂 (利福平、圣约翰草等)", "拉莫三嗪"],
            "uncertain": ["甲状腺激素"]
        }
    },
    {
        "name": "Dutasteride",
        "name_zh": "度他雄胺",
        "aliases": ["安福达", "Avodart", "度他雄胺软胶囊"],
        "url": "https://en.wikipedia.org/wiki/Dutasteride",
        "categories": ["hrt", "antiandrogen", "common"],
        "summary": "双重 5α-还原酶抑制剂。全方位强效阻断 I 型与 II 型 5α-还原酶，降低血清二氢睾酮 (DHT) 浓度达 98% 以上 (远超非那雄胺的 70%)，在 HRT 抗雄辅助与雄激素性脱发治疗中疗效彻底。",
        "pk": {
            "brandName": "安福达 (Avodart) | 葛兰素史克 (GSK)",
            "halfLife": "约 3 - 5 周 (极长终末消除半衰期，高度蓄积)",
            "halfLifeHours": 720.0,
            "tMax": "2.0 - 3.0 小时",
            "tMaxHours": 2.5,
            "bioavailability": "约 60% (40-94%)",
            "cypEnzymes": ["CYP3A4", "CYP3A5"],
            "clearance": "肝脏广泛代谢，主要经粪便排泄 (约 40% 为代谢物，5% 原型)",
            "indications": ["良性前列腺增生 (BPH)", "雄激素性脱发 (AGA)", "跨性别女性 (MtF) HRT 辅助抑制二氢睾酮 DHT (消除痤疮、体毛与脱发)"],
            "contraindications": ["严禁育龄期女性接触漏液破损胶囊 (经皮吸收致男性胎儿外生殖器畸形)", "停药后体内清除长达 4-6 个月，期间严禁献血", "重度肝功能损害者慎用"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 0.5, "commonMin": 0.5, "strongMin": 0.5, "heavyMin": 1.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 3.0, "units": "hours"},
                    "total": {"min": 504.0, "max": 840.0, "units": "hours"}
                },
                "bioavailability": {"min": 55.0, "max": 65.0}
            }
        ],
        "interactions": {
            "dangerous": ["妊娠期 / 胎儿暴露禁忌"],
            "unsafe": ["CYP3A4 抑制剂 (Ketoconazole, Ciprofloxacin, Ritonavir 使度他雄胺清除更慢)"],
            "uncertain": ["华法林"]
        }
    },
    {
        "name": "Triptorelin",
        "name_zh": "曲普瑞林",
        "aliases": ["达菲林", "Diphereline", "Decapeptyl", "注射用醋酸曲普瑞林"],
        "url": "https://en.wikipedia.org/wiki/Triptorelin",
        "categories": ["hrt", "gnrh agonist", "antiandrogen", "common"],
        "summary": "促性腺激素释放激素类似物 (GnRH 激动剂)。持续刺激导致垂体 GnRH 受体完全减敏和下调，彻底阻断 LH 与 FSH 分泌，实现彻底的药物性去势 (睾酮降至去势水平)，是 MtF 的顶级中枢抗雄阻断剂。",
        "pk": {
            "brandName": "达菲林 (Diphereline) | 法国益普生 (Ipsen)",
            "halfLife": "微球缓释制剂缓慢恒释可持续 28 天 (1月型 3.75mg) 或 90 天 (3月型 11.25mg)；游离肽约 7.5 小时",
            "halfLifeHours": 672.0,
            "tMax": "注射后初次峰值在 1-3 小时，随后微球恒速溶解释放",
            "tMaxHours": 2.0,
            "bioavailability": "肌注缓释微球 100%",
            "cypEnzymes": ["不依赖肝脏 CYP 酶！主要由组织内肽酶降解水解为小肽段与氨基酸"],
            "clearance": "组织肽酶分解后经肾脏尿液排出",
            "indications": ["跨性别女性 (MtF) 及性别不一致青少年青春期阻断与彻底抗雄", "前列腺癌药物去势治疗", "子宫内膜异位症与中枢性性早熟"],
            "contraindications": ["初始给药第 1-2 周会出现短暂的促性腺激素与性激素反跳增高现象 (Flare 效应)，需警惕并可短期联用抗雄药预防", "长期去势且无雌激素/雄激素支持时增加严重骨质疏松风险"]
        },
        "roas": [
            {
                "name": "intramuscular",
                "dose": {"units": "mg", "lightMin": 3.75, "commonMin": 3.75, "strongMin": 11.25, "heavyMin": 11.25},
                "duration": {
                    "onset": {"min": 1.0, "max": 3.0, "units": "hours"},
                    "peak": {"min": 24.0, "max": 72.0, "units": "hours"},
                    "total": {"min": 672.0, "max": 2160.0, "units": "hours"}
                },
                "bioavailability": {"min": 98.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["无直接药理学相互作用"],
            "unsafe": ["延长 QT 间期药物 (雄激素去势可能轻度延长心电QT)"],
            "uncertain": ["升高催乳素水平药物"]
        }
    },
    {
        "name": "Goserelin",
        "name_zh": "戈舍瑞林",
        "aliases": ["诺雷得", "Zoladex", "醋酸戈舍瑞林植入剂"],
        "url": "https://en.wikipedia.org/wiki/Goserelin",
        "categories": ["hrt", "gnrh agonist", "antiandrogen", "common"],
        "summary": "合成 GnRH 十肽类似物缓释植入剂。通过特制专用针头皮下植入可生物降解的圆柱形微型骨架，恒速释放 1 个月 (3.6mg) 或 3 个月 (10.8mg)，中枢性完全压制性腺功能。",
        "pk": {
            "brandName": "诺雷得 (Zoladex) | 阿斯利康 (AstraZeneca)",
            "halfLife": "缓释骨架维持持续释放 28 天或 84 天；游离多肽半衰期约 4.2 小时",
            "halfLifeHours": 672.0,
            "tMax": "皮下植入后 12-15 天达到血浆药物浓度坪值",
            "tMaxHours": 300.0,
            "bioavailability": "皮下植入近 100%",
            "cypEnzymes": ["体内非特异性肽酶水解，不经肝脏微粒体酶代谢"],
            "clearance": "肾小球滤过随尿排泄为主",
            "indications": ["跨性别女性 (MtF) 性别肯定青春期阻断与药物去势", "前列腺癌、绝经前乳腺癌内分泌治疗"],
            "contraindications": ["初始用药短期 Flare 现象 (需严密监测)", "腹壁皮下植入时注意避免伤及腹壁下动脉与血肿形成"]
        },
        "roas": [
            {
                "name": "subcutaneous",
                "dose": {"units": "mg", "lightMin": 3.6, "commonMin": 3.6, "strongMin": 10.8, "heavyMin": 10.8},
                "duration": {
                    "onset": {"min": 24.0, "max": 48.0, "units": "hours"},
                    "peak": {"min": 288.0, "max": 360.0, "units": "hours"},
                    "total": {"min": 672.0, "max": 2016.0, "units": "hours"}
                },
                "bioavailability": {"min": 98.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["无直接相互作用冲突"],
            "unsafe": ["延长 QT 间期药物"],
            "uncertain": ["抗雄激素药物 (初始阶段联用对抗睾酮骤升)"]
        }
    },
    {
        "name": "Progesterone",
        "name_zh": "黄体酮",
        "aliases": ["天然黄体酮", "安琪坦", "Utrogestan", "琪宁", "微粒化黄体酮"],
        "url": "https://en.wikipedia.org/wiki/Progesterone_(medication)",
        "categories": ["hrt", "progestin", "hormone", "common"],
        "summary": "天然生物等同孕激素。在跨性别女性 (MtF) HRT 中可协同促进乳房 Tanner IV/V 期小叶腺泡成熟发育、改善性欲与情绪睡眠；代谢物为强效 GABAA 变构调节剂。",
        "pk": {
            "brandName": "安琪坦 (Utrogestan) / 琪宁 | 法国 Besins / 浙江海正",
            "halfLife": "口服约 16 - 18 小时；直肠/阴道给药约 13 小时",
            "halfLifeHours": 16.0,
            "tMax": "口服 1.5 - 3.0 小时 (进餐特别是富脂餐可使吸收率提升两倍以上)",
            "tMaxHours": 2.0,
            "bioavailability": "口服约 10% (首过代谢强)；直肠给药规避首过吸收率可达 30-50%",
            "cypEnzymes": ["CYP3A4", "CYP2C19", "5α/5β 还原酶"],
            "clearance": "肝脏还原转化为孕烷二醇及异孕烷醇酮 (Allopregnanolone)，经肾脏排泄",
            "indications": ["跨性别女性 HRT 促进第二性征成熟乳腺分化与情绪平衡", "绝经后激素替代治疗中拮抗雌激素对子宫内膜刺激保护作用", "严重失眠与焦虑情绪辅助缓解 (代谢物拟 GABA 镇静效应)"],
            "contraindications": ["活动性静脉血栓栓塞症 (VTE) 禁用", "重度肝功能不全禁用", "口服容易引起明显的头晕与深度嗜睡反应，强烈建议每晚睡前服用或采用直肠给药"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 100.0, "commonMin": 100.0, "strongMin": 200.0, "heavyMin": 400.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 1.5, "max": 3.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 8.0, "max": 12.0}
            },
            {
                "name": "rectal",
                "dose": {"units": "mg", "lightMin": 100.0, "commonMin": 100.0, "strongMin": 200.0, "heavyMin": 200.0},
                "duration": {
                    "onset": {"min": 0.5, "max": 1.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 16.0, "max": 28.0, "units": "hours"}
                },
                "bioavailability": {"min": 25.0, "max": 45.0}
            }
        ],
        "interactions": {
            "dangerous": ["活动性血栓栓塞性疾病"],
            "unsafe": ["CYP3A4 诱导剂 (加速代谢)", "酒精 (乙醇)", "镇静药物 (加重嗜睡)"],
            "uncertain": ["酮康唑 (减缓代谢提高浓度)"]
        }
    },
    {
        "name": "Medroxyprogesterone acetate",
        "name_zh": "醋酸甲羟孕酮",
        "aliases": ["安宫黄体酮", "Provera", "Depo-Provera", "甲羟孕酮片"],
        "url": "https://en.wikipedia.org/wiki/Medroxyprogesterone_acetate",
        "categories": ["hrt", "progestin", "hormone", "common"],
        "summary": "强效 17α-羟孕酮衍生物合成孕激素。抗促性腺激素效应强大，高剂量肌肉注射 (Depo-Provera 150mg) 可强效压制 LH/FSH 达到长效避孕或抗雄效果，但长期需关注骨密度与心血管风险。",
        "pk": {
            "brandName": "安宫黄体酮 (Provera) / 狄波-普维拉 (Depo-Provera) | 辉瑞 (Pfizer)",
            "halfLife": "口服约 12 - 17 小时；长效混悬肌注针剂达 40 - 50 天",
            "halfLifeHours": 15.0,
            "tMax": "口服 2.0 - 4.0 小时；长效肌注 1-3 周达峰",
            "tMaxHours": 3.0,
            "bioavailability": "口服全面吸收，生物利用度约 100%",
            "cypEnzymes": ["CYP3A4 (主要代谢酶)"],
            "clearance": "肝脏羟基化并结合，主要随尿液和粪便排泄",
            "indications": ["子宫内膜异位症与功能失调性子宫出血", "跨性别女性 HRT 辅助强化负反馈抗雄与乳腺发育", "长效注射避孕"],
            "contraindications": ["脑血管病、血栓栓塞病史禁用", "【黑框警告】长期使用 (> 2年) 可引起显著骨矿物质密度 (BMD) 流失，增加骨质疏松风险", "轻度雄激素样活性 (可能抵消部分抗脱发效应)"]
        },
        "roas": [
            {
                "name": "oral",
                "dose": {"units": "mg", "lightMin": 2.5, "commonMin": 5.0, "strongMin": 10.0, "heavyMin": 20.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 2.0, "max": 4.0, "units": "hours"},
                    "total": {"min": 12.0, "max": 24.0, "units": "hours"}
                },
                "bioavailability": {"min": 90.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["活动性深静脉血栓形成或肺栓塞"],
            "unsafe": ["强效 CYP3A4 诱导剂 (氨鲁米特、卡马西平、圣约翰草等)"],
            "uncertain": ["降血糖药物 (可能轻度损害葡萄糖耐量)"]
        }
    },
    {
        "name": "Testosterone",
        "name_zh": "睾酮",
        "aliases": ["天然睾酮", "AndroGel", "Testim", "睾酮凝胶", "睾丸酮"],
        "url": "https://en.wikipedia.org/wiki/Testosterone_(medication)",
        "categories": ["hrt", "androgen", "hormone", "common"],
        "summary": "天然内源性主要雄激素。跨性别男性 (FtM) 性别肯定激素替代治疗的核心支柱，诱导并维持男性第二性征 (变声低沉、胡须生长、肌肉增加、停经)，凝胶透皮给药血药水平平稳。",
        "pk": {
            "brandName": "昂特 (AndroGel) 凝胶 / Testim | 艾伯维 (AbbVie)",
            "halfLife": "透皮给药皮肤储库维持稳定；游离睾酮消除半衰期仅 10 - 100 分钟",
            "halfLifeHours": 24.0,
            "tMax": "连续每日涂抹凝胶后在第 2-3 天达到稳定生理血清稳态平台",
            "tMaxHours": 4.0,
            "bioavailability": "经皮凝胶吸收率约 9 - 14%",
            "cypEnzymes": ["5α-还原酶转化为强效双氢睾酮 (DHT)；芳香化酶 (CYP19A1) 芳构化为雌二醇；肝脏 CYP3A4 代谢"],
            "clearance": "肝脏氧化结合，90% 经肾脏尿液排出，6% 随粪便排出",
            "indications": ["跨性别男性 (FtM) 性别肯定激素替代治疗", "男性原发性或继发性性腺功能减退症"],
            "contraindications": ["已知或疑似前列腺癌、男性乳腺癌禁用", "红细胞增多症 (血细胞比容 HCT > 54% 时禁用，需定期监控血常规)", "凝胶涂抹后严禁与女性或儿童发生皮肤直接接触 (防范意外雄激素化暴露)"]
        },
        "roas": [
            {
                "name": "transdermal",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 75.0, "heavyMin": 100.0},
                "duration": {
                    "onset": {"min": 1.0, "max": 2.0, "units": "hours"},
                    "peak": {"min": 4.0, "max": 8.0, "units": "hours"},
                    "total": {"min": 24.0, "max": 36.0, "units": "hours"}
                },
                "bioavailability": {"min": 9.0, "max": 14.0}
            }
        ],
        "interactions": {
            "dangerous": ["儿童/孕妇二手接触禁忌"],
            "unsafe": ["口服抗凝血药 (华法林增效出血风险)", "胰岛素 (胰岛素敏感性改变)"],
            "uncertain": ["糖皮质激素 (加剧液体潴留水肿)"]
        }
    },
    {
        "name": "Testosterone enanthate",
        "name_zh": "庚酸睾酮",
        "aliases": ["Delatestryl", "庚酸睾丸素", "庚酸睾酮注射液"],
        "url": "https://en.wikipedia.org/wiki/Testosterone_enanthate",
        "categories": ["hrt", "androgen", "hormone", "common"],
        "summary": "中长链睾酮脂肪酸酯前药。油溶液深度肌肉注射或深层皮下注射，消除半衰期约 4.5 - 5 天，每 1-2 周注射一次，是全球跨性别男性 (FtM) 最常用的 HRT 经典雄激素注射剂之一。",
        "pk": {
            "brandName": "Delatestryl | Endo Pharmaceuticals",
            "halfLife": "肌注约 4.5 天 (范围 4 - 5 天)",
            "halfLifeHours": 108.0,
            "tMax": "注射后 24 - 48 小时达到血药浓度峰值",
            "tMaxHours": 36.0,
            "bioavailability": "100%",
            "cypEnzymes": ["体内非特异性酯酶水解为游离睾酮；随后经 5α-还原酶与 CYP19A1/CYP3A4 处理"],
            "clearance": "肝脏代谢，尿排泄 90%",
            "indications": ["跨性别男性 (FtM) 雄激素化性别肯定治疗", "男性促性腺激素不足性性腺功能低下"],
            "contraindications": ["红细胞增多症 (严重血栓栓塞风险，需定期监测血红蛋白/HCT)", "严重肝肾功能损害、严重心脏病禁用", "注意注射后初期数天血药浓度偏高、下一次注射前数天偏低的峰谷波动现象"]
        },
        "roas": [
            {
                "name": "intramuscular",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 100.0, "heavyMin": 200.0},
                "duration": {
                    "onset": {"min": 6.0, "max": 12.0, "units": "hours"},
                    "peak": {"min": 24.0, "max": 48.0, "units": "hours"},
                    "total": {"min": 168.0, "max": 336.0, "units": "hours"}
                },
                "bioavailability": {"min": 98.0, "max": 100.0}
            },
            {
                "name": "subcutaneous",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 75.0, "heavyMin": 100.0},
                "duration": {
                    "onset": {"min": 6.0, "max": 12.0, "units": "hours"},
                    "peak": {"min": 24.0, "max": 48.0, "units": "hours"},
                    "total": {"min": 168.0, "max": 336.0, "units": "hours"}
                },
                "bioavailability": {"min": 98.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["口服抗凝血药 (增强出血倾向)"],
            "unsafe": ["胰岛素及口服降血糖药物", "肾上腺皮质激素类药物"],
            "uncertain": ["环孢素"]
        }
    },
    {
        "name": "Testosterone cypionate",
        "name_zh": "环戊丙酸睾酮",
        "aliases": ["Depo-Testosterone", "环戊丙睾酮", "TCP"],
        "url": "https://en.wikipedia.org/wiki/Testosterone_cypionate",
        "categories": ["hrt", "androgen", "hormone", "common"],
        "summary": "脂溶性长效睾酮环戊丙酸酯。肌肉或皮下注射，半衰期约为 8 天，比庚酸睾酮略长，血药浓度曲线相对平稳，为北美 FtM 跨性别男性的首选注射剂型。",
        "pk": {
            "brandName": "Depo-Testosterone | 辉瑞 (Pfizer)",
            "halfLife": "约 8.0 天",
            "halfLifeHours": 192.0,
            "tMax": "注射后 48 - 72 小时",
            "tMaxHours": 60.0,
            "bioavailability": "100%",
            "cypEnzymes": ["血清与组织酯酶释放游离睾酮；肝脏酶氧化结合代谢"],
            "clearance": "肝脏代谢，主要由肾脏随尿排泄",
            "indications": ["跨性别男性 (FtM) 性别肯定雄激素替代治疗", "原发性睾丸衰竭或垂体功能低下之性腺功能减退"],
            "contraindications": ["红细胞压积 > 54% 禁用", "严重睡眠呼吸暂停综合征慎用 (雄激素可能加重 OSA)", "已知乳腺癌、前列腺癌禁用"]
        },
        "roas": [
            {
                "name": "intramuscular",
                "dose": {"units": "mg", "lightMin": 25.0, "commonMin": 50.0, "strongMin": 100.0, "heavyMin": 200.0},
                "duration": {
                    "onset": {"min": 6.0, "max": 12.0, "units": "hours"},
                    "peak": {"min": 36.0, "max": 72.0, "units": "hours"},
                    "total": {"min": 168.0, "max": 336.0, "units": "hours"}
                },
                "bioavailability": {"min": 98.0, "max": 100.0}
            }
        ],
        "interactions": {
            "dangerous": ["华法林等抗凝血药物"],
            "unsafe": ["胰岛素", "糖皮质激素类药物"],
            "uncertain": ["紫杉醇"]
        }
    }
]
