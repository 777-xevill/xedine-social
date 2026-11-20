"""One-off: writes the 14 Xedine posts (content/posts/*.md) from the finished videos.
Re-run to regenerate. Hashtags are English only: the bot strips Bangla vowel signs from hashtags."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
POSTS = ROOT / "content" / "posts"
POSTS.mkdir(parents=True, exist_ok=True)
for old in POSTS.glob("*.md"):
    old.unlink()

BASE = ["Xedine", "RestaurantOwner", "RestaurantBangladesh"]
FOOT = "\n\nমেসেজ করুন বা xedine.org"

VIDEOS = [
    ("v01-money-leak", "দিনে ৫০ হাজার বিক্রি, মাসে ৪৫ হাজার টাকা গায়েব? | Xedine",
     "বিক্রি ভালো, তবু মাস শেষে লাভ কই?\n\nউদাহরণের হিসাব: মাত্র ৩% লিক হলে দিনে ৳১,৫০০, মাসে ৳৪৫,০০০ চুপচাপ গায়েব।\n\nআমি Xedine, আপনার রেস্টুরেন্টের AI ম্যানেজার। বিক্রি, স্টক আর বাজার মিলায়া দেখাই টাকা কোথায় যায়, প্রমাণসহ।",
     ["FoodCost", "ProfitLeak"]),
    ("v02-who-gave-discount", "৫টা ডিসকাউন্ট, মাসে ৳১৫,০০০, অনুমতি ছাড়া? | Xedine",
     "ক্যাশিয়ার ছাড় দিসে, আপনি জানেন না?\n\nউদাহরণের হিসাব: দিনে ৫টা ছাড় × ৳১০০ = ৳৫০০, মাসে ৳১৫,০০০।\n\nXedine-এ ছাড় দিতে লাগে আপনার সিক্রেট কোড, নাইলে ম্যানেজারের PIN। প্রতিটা ছাড়ের হিসাব থাকে।",
     ["RestaurantPOS", "CashControl"]),
    ("v03-missing-1kg", "২০ কেজি মুরগি কিনলেন, হিসাবে ১ কেজি নাই! | Xedine",
     "উদাহরণের হিসাব: ৫০টা বার্গার × ১২০ গ্রাম = ৬ কেজি হওয়ার কথা, গেসে ৭ কেজি। রোজ ১ কেজি, কেজি ৳৩০০ হলে মাসে ৳৯,০০০।\n\nXedine বিক্রি থেকেই স্টক হিসাব করে, রেসিপির চেয়ে বেশি গেলেই ধরে।",
     ["StockControl", "FoodCost"]),
    ("v04-bazar-guess", "কালকের বাজার আন্দাজে? মাসে ৳৩,২০০ নষ্ট | Xedine",
     "উদাহরণের হিসাব: দরকার ১০ কেজি টমেটো, আনলেন ১৫ কেজি। ৫ কেজি × ৳৮০ = ৳৪০০ নষ্ট। সপ্তাহে ২ বার হলে মাসে ৳৩,২০০।\n\nXedine বিক্রির আন্দাজ আর স্টক দেইখা কালকের বাজারের লিস্ট নিজেই বানায়। বাজার করার লোক Telegram-এ লিখলেই হিসাব।",
     ["Bazar", "FoodWaste"]),
    ("v05-extra-40g", "প্লেটে ১২০ গ্রামের জায়গায় ১৬০ গ্রাম! মাসে ৳৩৬,০০০ | Xedine",
     "উদাহরণের হিসাব: প্লেটে ৪০ গ্রাম বেশি × দিনে ১০০ প্লেট = ৪ কেজি চিকেন। কেজি ৳৩০০ হলে মাসে ৳৩৬,০০০।\n\nXedine প্রতিটা প্লেটের গ্রাম ধরে, লস টাকায় দেখায়, কী করবেন বলে দেয়।",
     ["FoodCost", "PortionControl"]),
    ("v06-offline-till", "নেট নাই, কাউন্টার বন্ধ? এক ঘণ্টায় ৳১২,০০০ আটকা | Xedine",
     "উদাহরণের হিসাব: ঘণ্টায় ৪০ অর্ডার × ৳৩০০ = ৳১২,০০০।\n\nXedine-এর টিল নেট ছাড়াও বিল করে, অর্ডার জমা থাকে, নেট আসলে সব নিজে নিজে মিলে।",
     ["RestaurantPOS", "OfflinePOS"]),
    ("v07-bestseller-profit", "যেটা বেশি চলে, সেটাই কি বেশি লাভ? | Xedine",
     "উদাহরণের হিসাব: বিরিয়ানি ৳২৫০ − ৳২০০ = ৳৫০ লাভ। বার্গার ৳২০০ − ৳১০০ = ৳১০০ লাভ। ১০০ প্লেটে ফারাক ৳৫,০০০।\n\nXedine প্রতিটা ডিশের আসল লাভ দেখায়, কোনটা চালাবেন বলে দেয়।",
     ["MenuProfit", "FoodCost"]),
    ("v08-rain-tomorrow", "কাল বৃষ্টি, আজকের মতো রান্না করলে ৳৩,২০০ ফেলবেন | Xedine",
     "উদাহরণের হিসাব: রোজ ১২০ প্লেট, বৃষ্টিতে হয়তো ৮০। ৪০ প্লেট × ৳৮০ = ৳৩,২০০ নষ্ট।\n\nXedine আবহাওয়া দেইখা কালকের বিক্রির আন্দাজ বদলায়, আগেই জানায় দেয়।",
     ["FoodWaste", "SalesForecast"]),
    ("v09-table-qr-menu", "মেনুর জন্য ৩ বার ডাক? দিনে ২০০ মিনিট নষ্ট | Xedine",
     "উদাহরণের হিসাব: ৫ মিনিট × ৪০ টেবিল = ২০০ মিনিট রোজ।\n\nটেবিলের QR স্ক্যান করলেই ফোনে পুরা মেনু, খাবারের তথ্য আর এলার্জি ফিল্টারসহ।",
     ["DigitalMenu", "TableQR"]),
    ("v10-silent-complaint", "কাস্টমার চুপচাপ চলে গেসে, বছরে ৳১৯,২০০ লস | Xedine",
     "উদাহরণের হিসাব: মাসে ৪ বার × ৳৪০০ = ৳১,৬০০, বছরে ৳১৯,২০০, একজন কাস্টমার।\n\nটেবিলের QR দিয়া কাস্টমার চুপিচুপি অভিযোগ পাঠায়, সোজা আপনার কাছে।",
     ["CustomerFeedback", "TableQR"]),
    ("v11-member-card", "যে কাস্টমার মাসে ৪ বার আসে, বছরে ৳২৪,০০০ | Xedine",
     "উদাহরণের হিসাব: ৪ বার × ৳৫০০ = ৳২,০০০ মাসে, বছরে ৳২৪,০০০।\n\nXedine মেম্বার কার্ড: পয়েন্ট আর ডিসকাউন্ট আপনার নিয়মে, কাউন্টারে এক স্ক্যানে।",
     ["CustomerLoyalty", "MemberCard"]),
    ("v12-ajke-labh-koto", "\"আজকে লাভ কত?\" বাংলায় জিগান | Xedine",
     "উদাহরণের হিসাব: বিক্রি ৳৪৮,০০০, খরচ ৳৩৫,০০০, লাভ ৳১৩,০০০।\n\nXedine-কে বাংলায় জিগান। উত্তর আপনার নিজের হিসাব থেকেই আসে, কোনো সংখ্যা বানায় না।",
     ["RestaurantAI", "AIManager"]),
    ("v13-five-notebooks", "৫টা খাতা, ১টা রেস্টুরেন্ট: মাসে ৩২ ঘণ্টা শুধু হিসাব | Xedine",
     "উদাহরণের হিসাব: মাসে ৪ দিন × ৮ ঘণ্টা = ৩২ ঘণ্টা।\n\nXedine-এ টিল, কিচেন, স্টক, বাজার আর লাভ সব এক জায়গায়, একটার সাথে আরেকটা জোড়া।",
     ["RestaurantManagement", "RestaurantAI"]),
    ("v14-see-it-first", "আগে দেখেন, তারপর কিনেন | Xedine",
     "উদাহরণের হিসাব: দিনে ৳১,০০০ লিক হলে মাসে ৳৩০,০০০, বছরে ৳৩,৬০,০০০।\n\nআমাদের মেসেজ করেন, আপনার রেস্টুরেন্টে Xedine কেমনে কাজ করে দেখায় দেই।",
     ["RestaurantSoftware", "RestaurantAI"]),
]

# Day 1 = 2026-11-21. Two a day: 12:00 and 21:00 (Asia/Dhaka), the order of the 7-day plan.
from datetime import date, timedelta
start = date(2026, 11, 20)  # today: the first posts go out as soon as the accounts are connected
for i, (slug, title, body, extra) in enumerate(VIDEOS):
    day = start + timedelta(days=i // 2)
    when = f"{day.isoformat()} {'12:00' if i % 2 == 0 else '21:00'}"
    tags = (BASE + extra)[:5]
    front = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"publish_at: {json.dumps(when)}",
        "platforms: [facebook, instagram, tiktok, youtube]",
        f"media: [xedine-{slug}.mp4]",
        "video_format: short",
        f"hashtags: [{', '.join(tags)}]",
        "---",
        "",
    ]
    name = f"{when.replace(' ', '-').replace(':', '')}-{slug}.md"
    (POSTS / name).write_text("\n".join(front) + body + FOOT + "\n", encoding="utf-8")
    print(name)
