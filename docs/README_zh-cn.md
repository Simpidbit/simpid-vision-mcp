[![English](https://img.shields.io/badge/Language-English-black?style=for-the-badge)](../README.md) [![简体中文](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-black?style=for-the-badge)](README_zh-cn.md)

# simpidbit-vision

`simpidbit-vision` 是一个 MCP Server，用于分析本地图片，并返回一段高信息密度的中文描述文本。它适合用于图像理解相关场景，例如检索、问答、归档、比对、界面分析和文档内容理解。

## 功能特点

- 暴露一个 MCP 工具：`analyse_image(image_fullpath: str) -> str`
- 输入本地图片的绝对路径
- 将图片发送给兼容 OpenAI 接口的多模态模型
- 返回高细节中文描述，而不是 JSON 结构化结果
- 适用于照片、截图、文档、海报、图表、商品图和插画等图像类型

## 项目结构

```text
.
├── server.py
├── requirements.txt
└── docs/
    └── README_zh-cn.md
```

## 环境要求

- Python 3.10+
- 可访问的、支持视觉能力的 OpenAI 兼容 API

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install openai python-dotenv simpidlog
```

## 环境变量

在项目根目录创建 `.env` 文件：

```env
BASE_URL=https://your-openai-compatible-endpoint/v1
API_KEY=your_api_key
MODEL_ID=your_vision_model
BASE_DIR=.
```

变量说明：

- `BASE_URL`：API 基础地址
- `API_KEY`：模型服务提供方的 API Key
- `MODEL_ID`：多模态模型名称
- `BASE_DIR`：`simpidlog` 使用的日志根目录

## 启动服务

```bash
python server.py
```

## MCP 工具

### `analyse_image`

输入：

- `image_fullpath`：本地图片文件的绝对路径

输出：

- 一段完整、细致的中文视觉描述文本

行为说明：

- 不接受相对路径
- 不接受不存在的文件
- 不接受非图片类型文件
- 会将图片编码为 base64 后发送给配置好的模型

## 示例

MCP 客户端中的调用示例：

```text
analyse_image("/absolute/path/to/image.png")
```

返回结果示例：

```text
画面是一张室内办公场景的照片，中央是一台打开的银色笔记本电脑，屏幕显示深色代码编辑器界面，左侧放着一只白色马克杯，背景中还能看到模糊的书架和暖色灯光...
```

## 说明

- 当前提示词专门针对“尽可能完整提取图像可见信息”进行了强化
- 当前实现固定返回中文描述
- 服务会通过 `simpidlog` 记录请求和结果

## 许可证

本项目基于 MIT License 开源，详见 `LICENSE`。
