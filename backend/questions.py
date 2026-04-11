"""
SBTI数据定义模块
根据规范直接定义数据结构，避免复杂的HTML解析
"""
from typing import List, Dict, Any

# 维度顺序
DIMENSION_ORDER = ['S1','S2','S3','E1','E2','E3','A1','A2','A3','Ac1','Ac2','Ac3','So1','So2','So3']

# 维度元数据
DIMENSION_META = {
  'S1': {'name': 'S1 自尊自信', 'model': '自我模型'},
  'S2': {'name': 'S2 自我清晰度', 'model': '自我模型'},
  'S3': {'name': 'S3 核心价值', 'model': '自我模型'},
  'E1': {'name': 'E1 依恋安全感', 'model': '情感模型'},
  'E2': {'name': 'E2 情感投入度', 'model': '情感模型'},
  'E3': {'name': 'E3 边界与依赖', 'model': '情感模型'},
  'A1': {'name': 'A1 世界观倾向', 'model': '态度模型'},
  'A2': {'name': 'A2 规则与灵活度', 'model': '态度模型'},
  'A3': {'name': 'A3 人生意义感', 'model': '态度模型'},
  'Ac1': {'name': 'Ac1 动机导向', 'model': '行动驱力模型'},
  'Ac2': {'name': 'Ac2 决策风格', 'model': '行动驱力模型'},
  'Ac3': {'name': 'Ac3 执行模式', 'model': '行动驱力模型'},
  'So1': {'name': 'So1 社交主动性', 'model': '社交模型'},
  'So2': {'name': 'So2 人际边界感', 'model': '社交模型'},
  'So3': {'name': 'So3 表达与真实度', 'model': '社交模型'}
}

# 问题列表（根据规范）
QUESTIONS = [
  {
    'id': 'q1', 'dim': 'S1',
    'text': '我不仅是屌丝，我还是joker,我还是咸鱼，这辈子没谈过一场恋爱，胆怯又自卑，我的青春就是一场又一场的意淫，每一天幻想着我也能有一个女孩子和我一起压马路，一起逛街，一起玩，现实却是爆了父母金币，读了个烂学校，混日子之后找班上，没有理想，没有目标，没有能力的三无人员，每次看到你能在网上开屌丝的玩笑，我都想哭，我就是地底下的老鼠，透过下水井的缝隙，窥探地上的各种美好，每一次看到这种都是对我心灵的一次伤害，对我生存空间的一次压缩，求求哥们给我们这种小丑一点活路吧，我真的不想在白天把枕巾哭湿一大片',
    'options': [
      {'label': '我哭了。。', 'value': 1},
      {'label': '这是什么。。', 'value': 2},
      {'label': '这不是我！', 'value': 3}
    ]
  },
  {
    'id': 'q2', 'dim': 'S1',
    'text': '我不够好，周围的人都比我优秀',
    'options': [
      {'label': '确实', 'value': 1},
      {'label': '有时', 'value': 2},
      {'label': '不是', 'value': 3}
    ]
  },
  {
    'id': 'q3', 'dim': 'S2',
    'text': '我很清楚真正的自己是什么样的',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  },
  {
    'id': 'q4', 'dim': 'S2',
    'text': '我内心有真正追求的东西',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  },
  {
    'id': 'q5', 'dim': 'S3',
    'text': '我一定要不断往上爬、变得更厉害',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  },
  {
    'id': 'q6', 'dim': 'S3',
    'text': '外人的评价对我来说无所吊谓。',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  },
  {
    'id': 'q7', 'dim': 'E1',
    'text': '对象超过5小时没回消息，说自己窜稀了，你会怎么想？',
    'options': [
      {'label': '拉稀不可能5小时，也许ta隐瞒了我。', 'value': 1},
      {'label': '在信任和怀疑之间摇摆。', 'value': 2},
      {'label': '也许今天ta真的不太舒服。', 'value': 3}
    ]
  },
  {
    'id': 'q8', 'dim': 'E1',
    'text': '我在感情里经常担心被对方抛弃',
    'options': [
      {'label': '是的', 'value': 1},
      {'label': '偶尔', 'value': 2},
      {'label': '不是', 'value': 3}
    ]
  },
  {
    'id': 'q9', 'dim': 'E2',
    'text': '我对天发誓，我对待每一份感情都是认真的！',
    'options': [
      {'label': '并没有', 'value': 1},
      {'label': '也许？', 'value': 2},
      {'label': '是的！（问心无愧骄傲脸）', 'value': 3}
    ]
  },
  {
    'id': 'q10', 'dim': 'E2',
    'text': '你的恋爱对象是一个尊老爱幼，温柔敦厚，洁身自好，光明磊落，大义凛然，能言善辩，口才流利，观察入微，见多识广，博学多才，诲人不倦，和蔼可亲，平易近人，心地善良，慈眉善目，积极进取，意气风发，玉树临风，国色天香，倾国倾城，花容月貌的人，此时你会？',
    'options': [
      {'label': '就算ta再优秀我也不会陷入太深。', 'value': 1},
      {'label': '会介于A和C之间。', 'value': 2},
      {'label': '会非常珍惜ta，也许会变成恋爱脑。', 'value': 3}
    ]
  },
  {
    'id': 'q11', 'dim': 'E3',
    'text': '恋爱后，对象非常黏人，你作何感想？',
    'options': [
      {'label': '那很爽了', 'value': 1},
      {'label': '都行无所谓', 'value': 2},
      {'label': '我更喜欢保留独立空间', 'value': 3}
    ]
  },
  {
    'id': 'q12', 'dim': 'E3',
    'text': '我在任何关系里都很重视个人空间',
    'options': [
      {'label': '我更喜欢依赖与被依赖', 'value': 1},
      {'label': '看情况', 'value': 2},
      {'label': '是的！（斩钉截铁地说道）', 'value': 3}
    ]
  },
  {
    'id': 'q13', 'dim': 'A1',
    'text': '大多数人是善良的',
    'options': [
      {'label': '其实邪恶的人心比世界上的痔疮更多。', 'value': 1},
      {'label': '也许吧。', 'value': 2},
      {'label': '是的，我愿相信好人更多。', 'value': 3}
    ]
  },
  {
    'id': 'q14', 'dim': 'A1',
    'text': '你走在街上，一位萌萌的小女孩蹦蹦跳跳地朝你走来（正脸、侧脸看都萌，用vivo、苹果、华为、OPPO手机看都萌，实在是非常萌的那种），她递给你一根棒棒糖，此时你作何感想？',
    'options': [
      {'label': '呜呜她真好真可爱！居然给我棒棒糖！', 'value': 3},
      {'label': '一脸懵逼，作挠头状', 'value': 2},
      {'label': '这也许是一种新型诈骗？还是走开为好。', 'value': 1}
    ]
  },
  {
    'id': 'q15', 'dim': 'A2',
    'text': '快考试了，学校规定必须上晚自习，请假会扣分，但今晚你约了女/男神一起玩《绝地求生：刺激战场》（一款刺激的游戏），你怎么办？',
    'options': [
      {'label': '翘了！反正就一次！', 'value': 1},
      {'label': '干脆请个假吧。', 'value': 2},
      {'label': '都快考试了还去啥。', 'value': 3}
    ]
  },
  {
    'id': 'q16', 'dim': 'A2',
    'text': '我喜欢打破常规，不喜欢被束缚',
    'options': [
      {'label': '认同', 'value': 1},
      {'label': '保持中立', 'value': 2},
      {'label': '不认同', 'value': 3}
    ]
  },
  {
    'id': 'q17', 'dim': 'A3',
    'text': '我做事通常有目标。',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  },
  {
    'id': 'q18', 'dim': 'A3',
    'text': '突然某一天，我意识到人生哪有什么他妈的狗屁意义，人不过是和动物一样被各种欲望支配着，纯纯是被激素控制的东西，饿了就吃，困了就睡，一发情就想交配，我们简直和猪狗一样没什么区别。',
    'options': [
      {'label': '是这样的。', 'value': 1},
      {'label': '也许是，也许不是。', 'value': 2},
      {'label': '这简直是胡扯', 'value': 3}
    ]
  },
  {
    'id': 'q19', 'dim': 'Ac1',
    'text': '我做事主要为了取得成果和进步，而不是避免麻烦和风险。',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  },
  {
    'id': 'q20', 'dim': 'Ac1',
    'text': '你因便秘坐在马桶上（已长达30分钟），拉不出很难受。此时你更像',
    'options': [
      {'label': '再坐三十分钟看看，说不定就有了。', 'value': 1},
      {'label': '用力拍打自己的屁股并说："死屁股，快拉啊！"', 'value': 2},
      {'label': '使用开塞露，快点拉出来才好。', 'value': 3}
    ]
  },
  {
    'id': 'q21', 'dim': 'Ac2',
    'text': '我做决定比较果断，不喜欢犹豫',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  },
  {
    'id': 'q22', 'dim': 'Ac2',
    'text': '此题没有题目，请盲选',
    'options': [
      {'label': '反复思考后感觉应该选A？', 'value': 1},
      {'label': '啊，要不选B？', 'value': 2},
      {'label': '不会就选C？', 'value': 3}
    ]
  },
  {
    'id': 'q23', 'dim': 'Ac3',
    'text': '别人说你"执行力强"，你内心更接近哪句？',
    'options': [
      {'label': '我被逼到最后确实执行力超强。。。', 'value': 1},
      {'label': '啊，有时候吧。', 'value': 2},
      {'label': '是的，事情本来就该被推进', 'value': 3}
    ]
  },
  {
    'id': 'q24', 'dim': 'Ac3',
    'text': '我做事常常有计划，____',
    'options': [
      {'label': '然而计划不如变化快。', 'value': 1},
      {'label': '有时能完成，有时不能。', 'value': 2},
      {'label': '我讨厌被打破计划。', 'value': 3}
    ]
  },
  {
    'id': 'q25', 'dim': 'So1',
    'text': '你因玩《第五人格》（一款刺激的游戏）而结识许多网友，并被邀请线下见面，你的想法是？',
    'options': [
      {'label': '网上口嗨下就算了，真见面还是有点忐忑。', 'value': 1},
      {'label': '见网友也挺好，反正谁来聊我就聊两句。', 'value': 2},
      {'label': '我会打扮一番并热情聊天，万一呢，我是说万一呢？', 'value': 3}
    ]
  },
  {
    'id': 'q26', 'dim': 'So1',
    'text': '朋友带了ta的朋友一起来玩，你最可能的状态是',
    'options': [
      {'label': '对"朋友的朋友"天然有点距离感，怕影响二人关系', 'value': 1},
      {'label': '看对方，能玩就玩。', 'value': 2},
      {'label': '朋友的朋友应该也算我的朋友！要热情聊天', 'value': 3}
    ]
  },
  {
    'id': 'q27', 'dim': 'So2',
    'text': '我和人相处主打一个电子围栏，靠太近会自动报警。',
    'options': [
      {'label': '认同', 'value': 3},
      {'label': '中立', 'value': 2},
      {'label': '不认同', 'value': 1}
    ]
  },
  {
    'id': 'q28', 'dim': 'So2',
    'text': '我渴望和我信任的人关系密切，熟得像失散多年的亲戚。',
    'options': [
      {'label': '认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '不认同', 'value': 3}
    ]
  },
  {
    'id': 'q29', 'dim': 'So3',
    'text': '有时候你明明对一件事有不同的、负面的看法，但最后没说出来。多数情况下原因是：',
    'options': [
      {'label': '这种情况较少。', 'value': 1},
      {'label': '可能碍于情面或者关系。', 'value': 2},
      {'label': '不想让别人知道自己是个阴暗的人。', 'value': 3}
    ]
  },
  {
    'id': 'q30', 'dim': 'So3',
    'text': '我在不同人面前会表现出不一样的自己',
    'options': [
      {'label': '不认同', 'value': 1},
      {'label': '中立', 'value': 2},
      {'label': '认同', 'value': 3}
    ]
  }
]

# 特殊问题
SPECIAL_QUESTIONS = [
  {
    'id': 'drink_gate_q1',
    'special': True,
    'kind': 'drink_gate',
    'text': '您平时有什么爱好？',
    'options': [
      {'label': '吃喝拉撒', 'value': 1},
      {'label': '艺术爱好', 'value': 2},
      {'label': '饮酒', 'value': 3},
      {'label': '健身', 'value': 4}
    ]
  },
  {
    'id': 'drink_gate_q2',
    'special': True,
    'kind': 'drink_trigger',
    'text': '您对饮酒的态度是？',
    'options': [
      {'label': '小酌怡情，喝不了太多。', 'value': 1},
      {'label': '我习惯将白酒灌在保温杯，当白开水喝，酒精令我信服。', 'value': 2}
    ]
  }
]

# 26种常规SBTI类型
NORMAL_TYPES = [
  {'code': 'CTRL', 'pattern': 'HHH-HMH-MHH-HHH-MHM', 'cn': '拿捏者'},
  {'code': 'ATM-er', 'pattern': 'HHH-HHM-HHH-HMH-MHL', 'cn': '送钱者'},
  {'code': 'Dior-s', 'pattern': 'MHM-MMH-MHM-HMH-LHL', 'cn': '屌丝'},
  {'code': 'BOSS', 'pattern': 'HHH-HMH-MMH-HHH-LHL', 'cn': '领导者'},
  {'code': 'THAN-K', 'pattern': 'MHM-HMM-HHM-MMH-MHL', 'cn': '感恩者'},
  {'code': 'OH-NO', 'pattern': 'HHL-LMH-LHH-HHM-LHL', 'cn': '哦不人'},
  {'code': 'GOGO', 'pattern': 'HHM-HMH-MMH-HHH-MHM', 'cn': '行者'},
  {'code': 'SEXY', 'pattern': 'HMH-HHL-HMM-HMM-HLH', 'cn': '尤物'},
  {'code': 'LOVE-R', 'pattern': 'MLH-LHL-HLH-MLM-MLH', 'cn': '多情者'},
  {'code': 'MUM', 'pattern': 'MMH-MHL-HMM-LMM-HLL', 'cn': '妈妈'},
  {'code': 'FAKE', 'pattern': 'HLM-MML-MLM-MLM-HLH', 'cn': '伪人'},
  {'code': 'OJBK', 'pattern': 'MMH-MMM-HML-LMM-MML', 'cn': '无所谓人'},
  {'code': 'MALO', 'pattern': 'MLH-MHM-MLH-MLH-LMH', 'cn': '吗喽'},
  {'code': 'JOKE-R', 'pattern': 'LLH-LHL-LML-LLL-MLM', 'cn': '小丑'},
  {'code': 'WOC!', 'pattern': 'HHL-HMH-MMH-HHM-LHH', 'cn': '握草人'},
  {'code': 'THIN-K', 'pattern': 'HHL-HMH-MLH-MHM-LHH', 'cn': '思考者'},
  {'code': 'SHIT', 'pattern': 'HHL-HLH-LMM-HHM-LHH', 'cn': '愤世者'},
  {'code': 'ZZZZ', 'pattern': 'MHL-MLH-LML-MML-LHM', 'cn': '装死者'},
  {'code': 'POOR', 'pattern': 'HHL-MLH-LMH-HHH-LHL', 'cn': '贫困者'},
  {'code': 'MONK', 'pattern': 'HHL-LLH-LLM-MML-LHM', 'cn': '僧人'},
  {'code': 'IMSB', 'pattern': 'LLM-LMM-LLL-LLL-MLM', 'cn': '傻者'},
  {'code': 'SOLO', 'pattern': 'LML-LLH-LHL-LML-LHM', 'cn': '孤儿'},
  {'code': 'FUCK', 'pattern': 'MLL-LHL-LLM-MLL-HLH', 'cn': '草者'},
  {'code': 'DEAD', 'pattern': 'LLL-LLM-LML-LLL-LHM', 'cn': '死者'},
  {'code': 'IMFW', 'pattern': 'LLH-LHL-LML-LLL-MLL', 'cn': '废物'},
  {'code': 'HHHH', 'pattern': 'HHH-HHH-HHH-HHH-HHH', 'cn': '傻乐者'}
]

# TYPE_LIBRARY（简化的详细信息）
TYPE_LIBRARY = {
  'CTRL': {'code': 'CTRL', 'cn': '拿捏者', 'desc': '怎么样，被我拿捏了吧？'},
  'BOSS': {'code': 'BOSS', 'cn': '领导者', 'desc': '方向盘给我，我来开。'},
  'SHIT': {'code': 'SHIT', 'cn': '愤世者', 'desc': '这个世界，构石一坨。'},
  'DRUNK': {'code': 'DRUNK', 'cn': '酒鬼', 'desc': '烈酒烧喉，不得不醉。'},
  'HHHH': {'code': 'HHHH', 'cn': '傻乐者', 'desc': '哈哈哈哈哈哈。'}
}


def get_dimension_meta() -> Dict[str, Dict[str, str]]:
    """获取维度元数据"""
    return DIMENSION_META.copy()


def get_questions() -> List[Dict[str, Any]]:
    """获取30个常规问题"""
    return QUESTIONS.copy()


def get_special_questions() -> List[Dict[str, Any]]:
    """获取2个特殊问题"""
    return SPECIAL_QUESTIONS.copy()


def get_normal_types() -> List[Dict[str, str]]:
    """获取26种常规SBTI类型"""
    return NORMAL_TYPES.copy()


def get_type_library() -> Dict[str, Dict[str, str]]:
    """获取SBTI类型详细信息库"""
    return TYPE_LIBRARY.copy()


def get_dim_explanations() -> Dict[str, Dict[str, str]]:
    """获取各维度L/M/H等级解释（简化版）"""
    return {
      'S1': {'L': '低自尊', 'M': '中等自尊', 'H': '高自尊'},
      'E1': {'L': '低安全感', 'M': '中等安全感', 'H': '高安全感'},
      'A1': {'L': '悲观', 'M': '中立', 'H': '乐观'},
      'Ac1': {'L': '规避导向', 'M': '混合导向', 'H': '成就导向'},
      'So1': {'L': '被动', 'M': '中等', 'H': '主动'}
    }


def get_all_data() -> Dict[str, Any]:
    """获取所有数据"""
    return {
      'dimensionMeta': DIMENSION_META,
      'questions': QUESTIONS,
      'specialQuestions': SPECIAL_QUESTIONS,
      'normalTypes': NORMAL_TYPES,
      'typeLibrary': TYPE_LIBRARY,
      'dimExplanations': get_dim_explanations()
    }
