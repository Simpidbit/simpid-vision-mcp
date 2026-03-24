[![English](https://img.shields.io/badge/Language-English-black?style=for-the-badge)](README.md) [![简体中文](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-black?style=for-the-badge)](docs/README_zh-cn.md)

# simpidbit-vision

`simpidbit-vision` is an MCP server that analyzes a local image and returns a dense Chinese description of everything visible in the image. It is designed for image understanding workflows such as retrieval, QA, archiving, comparison, UI inspection, and document interpretation.

## Features

- Exposes one MCP tool: `analyse_image(image_fullpath: str) -> str`
- Accepts a local absolute image path
- Sends the image to an OpenAI-compatible multimodal model
- Returns a high-detail Chinese description instead of structured JSON
- Works well for photos, screenshots, documents, posters, charts, product images, and illustrations

## Project Structure

```text
.
├── server.py
├── requirements.txt
└── docs/
    └── README_zh-cn.md
```

## Requirements

- Python 3.10+
- Access to an OpenAI-compatible API endpoint with vision support

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install openai python-dotenv simpidlog
```

## Environment Variables

Create a `.env` file in the project root:

```env
BASE_URL=https://your-openai-compatible-endpoint/v1
API_KEY=your_api_key
MODEL_ID=your_vision_model
BASE_DIR=.
```

Variable notes:

- `BASE_URL`: API base URL
- `API_KEY`: API key for the model provider
- `MODEL_ID`: multimodal model name
- `BASE_DIR`: log base directory used by `simpidlog`

## Run The Server

```bash
python server.py
```

## MCP Tool

### `analyse_image`

Input:

- `image_fullpath`: absolute path to a local image file

Output:

- A single Chinese paragraph with detailed visual description

Behavior:

- Rejects non-absolute paths
- Rejects missing files
- Rejects unsupported non-image files
- Encodes the image as base64 and sends it to the configured model

## Example

Example call from an MCP client:

```text
analyse_image("/absolute/path/to/image.png")
```

Example result:

```text
画面是一张室内办公场景的照片，中央是一台打开的银色笔记本电脑，屏幕显示深色代码编辑器界面，左侧放着一只白色马克杯，背景中还能看到模糊的书架和暖色灯光...
```

## Notes

- The prompt is intentionally optimized for exhaustive visual extraction
- The returned text is always Chinese in the current implementation
- The server logs requests and results through `simpidlog`

## License

This project is licensed under the MIT License. See `LICENSE` for details.
