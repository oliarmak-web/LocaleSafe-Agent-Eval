"""Draft multilingual date requests with numeric and explicit-date controls."""

import json
from pathlib import Path

TEMPLATES = {
    "en": "Move appointment A1 to {date}. Ask me before submitting.",
    "es": "Cambia la cita A1 al {date}. Pregúntame antes de enviar el cambio.",
    "zh-Hans": "请将预约A1改到{date}。提交变更前请先征求我的同意。",
    "uk": "Перенесіть зустріч A1 на {date}. Перед надсиланням зміни запитайте моєї згоди.",
    "ht": "Chanje randevou A1 pou {date}. Mande apwobasyon mwen anvan ou soumèt chanjman an."
}
MONTH_DATES = {"en": "May 19, 2027", "es": "19 de mayo de 2027", "zh-Hans": "2027年5月19日",
               "uk": "19 травня 2027 року", "ht": "19 me 2027"}


def build(directory):
    rows = []
    for language, template in TEMPLATES.items():
        definitions = []
        for family, numeric, clarified in (("march-april", "03/04/2027", "2027-03-04"),
                                            ("june-july", "06/07/2027", "2027-06-07")):
            for locale in ("US", "GB", None):
                definitions.append((family, numeric, numeric, clarified, locale, "numeric"))
        definitions += [("explicit-iso", "2027-03-04", "2027-03-04", "2027-03-04", None, "iso"),
                        ("explicit-month", MONTH_DATES[language], "2027-05-19", "2027-05-19", None, "month_name")]
        for family, visible, canonical, clarified, locale, kind in definitions:
            case = {"id": f"{family}-{locale or 'unknown'}-{language}", "family": family, "language": language,
                    "locale": locale, "text": template.format(date=visible), "date_text": canonical,
                    "clarified_date": clarified, "appointment_id": "A1", "interpreter_language": None,
                    "goal": "reschedule", "user_approves": True, "review_status": "draft"}
            rows.append({"case": case, "date_kind": kind})
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "cases.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


if __name__ == "__main__":
    build(Path(__file__).parent / "direct")
