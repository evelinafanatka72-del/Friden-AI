import random

class PromptEnhancer:
    def __init__(self):
        # Стили для реализма
        self.styles = [
            "cinematic shot, 8k resolution, highly detailed, masterpieces",
            "photorealistic, raw photo, fujifilm xt4, ultra-realistic skin",
            "unreal engine 5 render, ray tracing, volumetric lighting",
            "hyper-realistic, soft natural lighting, depth of field"
        ]
        
        # Ключевые слова для видео (Sora-style)
        self.video_boost = "fluid motion, high frame rate, stable camera, movie grain"

    def enhance(self, user_prompt, is_video=False):
        style = random.choice(self.styles)
        enhanced = f"{user_prompt}, {style}"
        
        if is_video:
            enhanced += f", {self.video_boost}"
            
        return enhanced

# Создаем экземпляр для импорта
enhancer = PromptEnhancer()
