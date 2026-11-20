"""One-off: writes the 12 English image posts (content/posts/*-img-*.md) and their JPEGs from
E:\\Editing\\projects\\2026-11-20-xedine-english-images\\out. Only touches the img files, never the video posts.
Two a day, 09:00 and 17:00 Asia/Dhaka, 21-26 Nov 2026 (the videos keep 12:00 and 21:00).
Facebook, Instagram and TikTok (photo post via Buffer). YouTube has no image-post API."""
import json
from datetime import date, timedelta
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
SRC = Path(r"E:\Editing\projects\2026-11-20-xedine-english-images\out")
POSTS, MEDIA = ROOT / "content" / "posts", ROOT / "content" / "media"
for old in POSTS.glob("*-img-*.md"):
    old.unlink()

BASE = ["Xedine", "RestaurantOwner", "RestaurantBangladesh"]
FOOT = "\n\nMessage us or visit xedine.org"
EX = "Example figures, for illustration."

IMAGES = [
    ("01-where-is-the-profit", "Sales are good. So where is the profit? | Xedine",
     "Busy tables, full bills, and still nothing left at the end of the month?\n\nXedine is your restaurant's AI manager. It matches sales, stock and bazar, and shows where the money goes, with proof.",
     ["ProfitLeak", "RestaurantAI"], "A worried restaurant owner at his desk"),
    ("02-quiet-leak", "A 3% leak is quiet | Xedine",
     f"{EX} On ৳50,000 of daily sales, a 3% leak is ৳1,500 a day and ৳45,000 a month.\n\nXedine finds where it goes, shows the proof and tells you what to do next.",
     ["ProfitLeak", "FoodCost"], "A busy restaurant dining room at night"),
    ("03-who-gave-discount", "Who gave this discount? | Xedine",
     f"{EX}\n\nIn Xedine a discount needs your secret code or a manager's PIN. Every discount keeps a name, a time and a reason.",
     ["RestaurantPOS", "CashControl"], "A restaurant manager checking a bill at the counter"),
    ("04-missing-stock", "1 kg of chicken went missing | Xedine",
     f"{EX} Bought 20 kg, the dishes sold used 17.5 kg, so 2.5 kg should be left. Only 1.5 kg is.\n\nXedine works out the stock from your sales and recipes, so nobody has to count the shelf.",
     ["StockControl", "FoodCost"], "A cook taking chicken from the cold room"),
    ("05-extra-grams", "Every extra gram is a loss | Xedine",
     "40 g over the recipe on every plate adds up fast.\n\nXedine compares each dish with its recipe and shows the loss in taka, dish by dish.",
     ["FoodCost", "PortionControl"], "A chef weighing a plate of chicken on a scale"),
    ("06-bazar-list", "Stop guessing the bazar | Xedine",
     f"{EX}\n\nXedine reads your sales, the weather and the days ahead, then writes tomorrow's bazar list with the quantities. Your buyer just types the bazar in Telegram.",
     ["Bazar", "FoodWaste"], "A cook checking a list on his phone next to fresh vegetables"),
    ("07-rain-tomorrow", "Rain tomorrow? Cook less. | Xedine",
     "Rain keeps guests at home. Cooking for a normal day means food in the bin.\n\nXedine checks the weather for each branch and adjusts tomorrow's forecast by itself.",
     ["FoodWaste", "SalesForecast"], "Heavy rain outside a restaurant window"),
    ("08-waste", "Food in the bin is money in the bin | Xedine",
     "Log waste in one tap. Xedine shows which item, which day and why, so you can stop it next week.",
     ["FoodWaste", "FoodCost"], "A cook throwing tomatoes into a bin"),
    ("09-table-qr", "One QR. Every table. | Xedine",
     "Guests scan the table QR to see the menu, join your member card, review you on Google or send a private complaint.\n\nNo app to install.",
     ["TableQR", "DigitalMenu"], "A guest scanning a QR menu at a restaurant table"),
    ("10-silent-complaint", "Most unhappy guests never tell you | Xedine",
     "They just don't come back.\n\nWith Xedine every table has a private complaint box, so the guest tells you first, not Google.",
     ["CustomerFeedback", "TableQR"], "A guest walking away from a restaurant table"),
    ("11-one-screen", "Five notebooks. One phone. | Xedine",
     "Sales, stock, bazar, staff and customers in one place, in English and Bangla.\n\nThe till keeps working when the internet goes down.",
     ["RestaurantManagement", "RestaurantAI"], "A restaurant owner smiling at his phone"),
    ("12-see-it-first", "See where your money really goes | Xedine",
     "Xedine: AI profit intelligence and restaurant OS.\n\nMessage us and we will show you how it works on your own restaurant.",
     ["RestaurantSoftware", "RestaurantAI"], "Two restaurant owners looking at a phone together"),
]

start = date(2026, 11, 21)
for i, (slug, title, body, extra, alt) in enumerate(IMAGES):
    jpg = f"xedine-img-{slug}.jpg"
    Image.open(SRC / f"xedine-{slug}.png").convert("RGB").save(MEDIA / jpg, quality=92, optimize=True)
    day = start + timedelta(days=i // 2)
    when = f"{day.isoformat()} {'09:00' if i % 2 == 0 else '17:00'}"
    front = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"publish_at: {json.dumps(when)}",
        "platforms: [facebook, instagram, tiktok]",
        f"media: [{jpg}]",
        f"alt: {json.dumps(alt)}",
        f"hashtags: [{', '.join((BASE + extra)[:5])}]",
        "---",
        "",
    ]
    name = f"{when.replace(' ', '-').replace(':', '')}-img-{slug}.md"
    (POSTS / name).write_text("\n".join(front) + body + FOOT + "\n", encoding="utf-8")
    print(name)
