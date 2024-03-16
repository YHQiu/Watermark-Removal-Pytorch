from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import shutil
from remove_watermark import remove_watermark  # 确保从您的实际文件路径导入
import uuid
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from api import remove_watermark

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 仅用于示例，实际部署时应限制为真实的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/remove-watermark")
async def remove_watermark_api(
        image: UploadFile = File(...),
        mask: UploadFile = File(...),
        max_dim: int = Form(512),
        reg_noise: float = Form(0.03),
        input_depth: int = Form(32),
        lr: float = Form(0.01),
        show_step: int = Form(100),
        training_steps: int = Form(1000)
):
    image_path = f"temp/{uuid.uuid4()}.jpg"
    mask_path = f"temp/{uuid.uuid4()}.jpg"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    with open(mask_path, "wb") as buffer:
        shutil.copyfileobj(mask.file, buffer)

    # 调用remove_watermark函数
    output_path = remove_watermark(
        image_path, mask_path, max_dim, reg_noise, input_depth, lr, show_step, training_steps
    )

    # 清理临时文件
    # os.remove(image_path)
    # os.remove(mask_path)

    # 返回生成的图片
    return FileResponse(output_path)

# 主页路由，简单返回一个文本信息
@app.get("/")
async def main():
    return {"message": "Welcome to the watermark removal API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", reload=False)