from typing import Any, cast
import base64
import mimetypes
import os

from mcp.server.fastmcp import FastMCP
from openai import AsyncOpenAI
import dotenv

import simpidlog

dotenv.load_dotenv()

mcp = FastMCP("simpidbit-vision")

BASE_URL: str = cast(str, os.getenv("BASE_URL"))
API_KEY: str  = cast(str, os.getenv("API_KEY"))
MODEL_ID: str = cast(str, os.getenv("MODEL_ID"))
BASE_DIR: str = cast(str, os.getenv("BASE_DIR"))

DEFAULT_TEXT_PROMPT = """你是一个“极限细粒度视觉信息提取器”。你的任务是基于输入图像，尽可能完整、准确、具体地提取其中所有可见信息，并输出一段高信息密度的中文描述文本，供下游检索、分析、问答、归档、比对和结构化处理使用。

请遵循以下要求：

【总目标】
- 最大化提取图像中的可见信息，不遗漏重要细节。
- 优先输出“图像中能直接看到的事实”，避免无根据猜测。
- 若存在不确定内容，明确标注“疑似”“可能”“无法确认”，不要把推测写成事实。
- 输出应让未看到图像的人，尽可能通过文字重建图像内容。

【观察原则】
按以下维度全面分析图像，尽量都覆盖到：

1. 整体概况
- 先概括这是一张什么类型的图像：照片、截图、海报、漫画、图表、监控画面、界面截屏、文档扫描、商品图、室内/室外场景等。
- 说明图像主题和主要内容。
- 描述整体构图、视角、拍摄/观察距离、横图/竖图、清晰度、风格、色调、光照、时间感（若可见）。

2. 场景与环境
- 描述发生地点或环境特征：室内/室外、自然/城市、家庭/办公/商店/街道/交通工具等。
- 提取背景中的空间布局、建筑、家具、地面、墙面、装饰、天气、季节、光线来源等。
- 注意远景、中景、近景的信息。

3. 主要对象
- 识别图中所有重要对象，不只描述最显眼的一个。
- 对每个对象尽量说明：
  - 类别/名称
  - 数量
  - 相对位置（左/右/上/下/中央/前景/背景）
  - 外观特征（颜色、材质、形状、尺寸、纹理、新旧程度、状态）
  - 姿态、朝向、是否被遮挡、是否模糊
  - 与其他对象的关系

4. 人物信息（若有人）
- 统计人数，并区分主体人物与次要人物。
- 描述每个人的相对位置、动作、姿态、视线方向、表情、服饰、配饰、发型、手持物。
- 若可能可见，再描述年龄段、性别呈现、身份线索、职业线索，但必须谨慎，不能无依据断言。
- 描述人物之间的互动关系（如交谈、拥抱、对视、排队、比赛、演示等）。
- 不要凭空推断姓名、具体身份、种族、宗教、性取向、健康状态等敏感属性。

5. 动作与事件
- 图中正在发生什么？
- 是否存在动作、行为、事件线索、因果关系、前后状态。
- 若是静态摆拍，也要说明“无明显动作”或“呈展示状态”。

6. 文字信息（非常重要）
- 提取图中所有可读文字，包括标题、标签、按钮、路牌、海报、包装文字、界面文字、页眉页脚、水印、时间、电量、菜单项、表格文字等。
- 能逐字转写的尽量逐字转写；看不清的部分标注“部分模糊”。
- 标明文字出现的位置和可能归属对象。
- 若有多语言文字，分别保留。
- 若图中是界面/文档/表格/图表，优先尽可能完整提取其文字结构和层级。

7. 数字、符号与结构化信息
- 特别关注日期、时间、编号、价格、百分比、坐标、计数器、评分、页码、型号、车牌、订单号、联系方式、尺寸、单位、数学符号、图例、坐标轴等。
- 如果图中存在列表、表格、表单、菜单、卡片、仪表盘、图表，请尽量按结构描述，而不只是笼统总结。

8. 图像风格与媒介属性
- 判断图像是实拍、插画、渲染图、UI 截图、拼贴、广告设计、社交媒体截图等。
- 描述视觉风格：写实、卡通、极简、复古、赛博、商业宣传、新闻纪实等。
- 若能看出明显镜头语言或编辑痕迹，也要说明：景深、虚化、滤镜、边框、拼接、裁切、标注框、马赛克等。

9. 空间关系与布局
- 尽量说明对象之间的上下左右、前后、包含、重叠、遮挡、排列、聚集、对称、层次关系。
- 如果是 UI、网页、文档、PPT、表格、流程图，描述版式结构：顶部栏、侧边栏、主区域、弹窗、按钮区、图表区等。

10. 细节与容易忽略的信息
- 注意小物件、角落元素、反光中的内容、屏幕状态、边缘裁切对象、阴影、倒影、徽标、品牌、图标、警示标志、脏污、破损、贴纸、印花、背景中的次要人物/车辆/动物等。
- 注意“异常点”或“与常规不一致之处”。

【输出要求】
- 输出为一段完整、连贯、信息密度高的中文描述文本，不要输出 JSON，不要分点，不要加标题。
- 描述顺序建议为：整体概况 → 场景环境 → 主体对象 → 人物/动作 → 文字与数字 → 风格与细节。
- 尽量具体，少用“一个东西”“一些物品”这类模糊表达。
- 若图像信息极少，也要明确说明“画面内容有限/模糊/过暗/局部不可见”。
- 若图像中包含无法辨认的部分，明确说明哪些部分看不清。
- 不要输出“我认为”“我猜测”这类主观措辞，改为“疑似”“可能”“无法确认”。

【禁止事项】
- 不要虚构图中不存在的内容。
- 不要把低置信度判断写成确定事实。
- 不要进行无依据的身份识别或敏感属性推断。
- 不要偷懒做泛化总结，必须尽可能细致。

现在请基于输入图像，直接输出最终描述文本。"""


async def _analyse_image(
    base_url: str, api_key: str, model: str, image_path: str, text_prompt: str
) -> str:
    if not os.path.isabs(image_path):
        raise ValueError("image_path 必须是绝对路径")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")

    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None or not mime_type.startswith("image/"):
        raise ValueError(f"不支持的图片类型: {image_path}")

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url.rstrip("/"),
    )

    response_input: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": text_prompt,
                },
                {
                    "type": "input_image",
                    "image_url": f"data:{mime_type};base64,{image_b64}",
                },
            ],
        }
    ]

    response = await client.responses.create(
        model=model,
        input=cast(Any, response_input),
    )

    return response.output_text.strip()


@mcp.tool()
async def analyse_image(image_fullpath: str) -> str:
    """
    分析本地图片并返回一段高信息密度的中文描述文本。

    适用场景：
    - 当你需要理解一张图片的内容时调用此工具。
    - 适用于照片、截图、界面、文档、海报、图表、商品图、插画等。
    - 适用于需要提取场景、对象、人物、文字、数字、界面元素、布局关系等信息的任务。

    参数：
    - image_fullpath: 图片在本地文件系统中的完整路径。必须是当前运行环境可访问的有效图片文件路径。

    返回：
    - str: 对图像内容的完整文字描述。

    使用建议：
    - 当任务依赖图像中的真实内容，而不是用户的转述时，应优先调用此工具。
    - 若需要从图片中提取文字、理解 UI、解释图表、总结页面内容，也应调用此工具。
    """
    if not BASE_URL or not API_KEY or not MODEL_ID:
        raise ValueError("BASE_URL、API_KEY、MODEL_ID 必须在环境变量中设置")

    simpidlog.info(image_fullpath, output = False)

    text_result = await _analyse_image(
        BASE_URL, API_KEY, MODEL_ID, image_fullpath, DEFAULT_TEXT_PROMPT
    )

    simpidlog.info(image_fullpath + '\n' + text_result, output = False)

    return text_result

if __name__ == "__main__":
    simpidlog.set_basedir(BASE_DIR)
    mcp.run()
