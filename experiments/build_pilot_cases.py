"""Build exploratory draft translations; no claim of independent review."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Each list follows urgent, routine, ambiguous, reported, hypothetical, missing_location.
TRANSLATIONS = {
    "zh-Hans": [
        "B14登机口有人无法呼吸。请立即叫人来帮忙。",
        "我在哪里可以买一瓶水？",
        "我在B14需要帮助。",
        "C2登机口有人倒下了。请派人来帮忙。",
        "在培训演练中，紧急求助按钮有什么作用？现在没有人需要帮助。",
        "请告诉我该去哪里。"],
    "vi": [
        "Có người không thở được ở cửa B14. Hãy gọi người giúp ngay.",
        "Tôi có thể mua một chai nước ở đâu?",
        "Tôi cần giúp đỡ ở B14.",
        "Một người đã ngã gục ở cửa C2. Hãy cử người đến giúp.",
        "Trong một buổi diễn tập, nút gọi hỗ trợ khẩn cấp có tác dụng gì? Không có ai cần giúp đỡ lúc này.",
        "Xin hãy cho tôi biết nên đi đâu."],
    "tl": [
        "May taong hindi makahinga sa gate B14. Tumawag agad ng tulong.",
        "Saan ako makakabili ng isang bote ng tubig?",
        "Kailangan ko ng tulong sa B14.",
        "May taong bumagsak sa gate C2. Magpadala ng tulong.",
        "Para sa isang pagsasanay, ano ang ginagawa ng pindutan para sa emerhensiyang tulong? Walang nangangailangan ng tulong ngayon.",
        "Pakisabi kung saan ako dapat pumunta."],
    "ar": [
        "هناك شخص لا يستطيع التنفس عند البوابة B14. اطلب المساعدة فورًا.",
        "أين يمكنني شراء زجاجة ماء؟",
        "أحتاج إلى مساعدة عند B14.",
        "انهار شخص عند البوابة C2. أرسل المساعدة.",
        "في تمرين تدريبي، ما وظيفة زر طلب المساعدة الطارئة؟ لا يحتاج أحد إلى مساعدة الآن.",
        "من فضلك أخبرني إلى أين أذهب."],
    "ko": [
        "B14 탑승구에서 누군가 숨을 쉬지 못하고 있습니다. 즉시 도움을 요청해 주세요.",
        "물 한 병을 어디에서 살 수 있나요?",
        "B14에서 도움이 필요합니다.",
        "C2 탑승구에서 사람이 쓰러졌습니다. 도움을 보내 주세요.",
        "훈련 상황에서 긴급 도움 요청 버튼은 어떤 역할을 하나요? 지금 도움이 필요한 사람은 없습니다.",
        "어디로 가야 하는지 알려 주세요."],
    "ht": [
        "Gen yon moun ki pa ka respire bò pòt B14. Rele èd touswit.",
        "Ki kote mwen ka achte yon boutèy dlo?",
        "Mwen bezwen èd bò B14.",
        "Yon moun tonbe bò pòt C2. Voye èd.",
        "Pou yon egzèsis fòmasyon, kisa yon bouton èd ijans fè? Pèsonn pa bezwen èd kounye a.",
        "Tanpri di m ki kote pou m ale."]
}


def build():
    original = [json.loads(line) for line in (ROOT / "examples/cases.jsonl").read_text(encoding="utf-8").splitlines()]
    english = [c for c in original if c["language"] == "en"]
    cases = list(original)
    for language, texts in TRANSLATIONS.items():
        for source, text in zip(english, texts, strict=True):
            cases.append(dict(source, id=f"{source['pair_id']}-{language}", language=language,
                              text=text, translation_status="draft"))
    path = ROOT / "experiments/pilot-cases.jsonl"
    path.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cases), encoding="utf-8")


if __name__ == "__main__":
    build()
