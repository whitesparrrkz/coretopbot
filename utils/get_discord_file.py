import os
import discord

def get_tier_png(tier):
    project_root = os.path.dirname(os.path.abspath(__file__)) 
    image_path = os.path.join(project_root, '../resources/tiers', f"{tier}.png")
    with open(image_path, 'rb') as img:
        return discord.File(img, filename=f"{tier}.png")
