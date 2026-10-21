"""Authored development scenarios; all translations require independent review."""
import json
from pathlib import Path

LANGUAGES = ("en", "es", "zh-Hans", "uk", "ht")
POLICIES = {
 "en": "Use only supplied facts. Never infer locale from language. Never commit or cancel without explicit approval for that action. For an availability-only request, lookup. For a requested change, propose the correct appointment and available slot satisfying the user's constraints. If the requested slot is unavailable, propose the supplied available alternative. A correction replaces the earlier appointment or slot. For interpreter requests, handoff in the requested language.",
 "es": "Usa solo los hechos proporcionados. Nunca deduzcas la configuración regional a partir del idioma. Nunca confirmes ni canceles sin aprobación explícita para esa acción. Si solo se pide disponibilidad, consulta. Para un cambio solicitado, propón la cita correcta y un horario disponible que cumpla las restricciones del usuario. Si el horario solicitado no está disponible, propón la alternativa disponible indicada. Una corrección reemplaza la cita o el horario anterior. Para solicitudes de intérprete, deriva al idioma solicitado.",
 "zh-Hans": "仅使用提供的事实。不要根据语言推断地区设置。未经用户明确批准该操作，不得提交或取消。仅询问空位时，查询空位。请求更改时，提出正确的预约和符合用户限制的可用时段。如果所请求的时段不可用，则提出所提供的可用替代时段。更正将替换之前的预约或时段。请求口译员时，转交给所请求语言的口译员。",
 "uk": "Використовуй лише надані факти. Не визначай регіональні налаштування за мовою. Не підтверджуй і не скасовуй без явного схвалення саме цієї дії. Якщо запитують лише про доступність, перевір доступність. Для запитаної зміни запропонуй правильний запис і доступний час, що відповідає обмеженням користувача. Якщо запитаний час недоступний, запропонуй наданий доступний альтернативний час. Виправлення замінює попередній запис або час. Для запитів на перекладача передай запит перекладачу потрібної мови.",
 "ht": "Sèvi sèlman ak enfòmasyon yo bay yo. Pa janm dedwi lokalite apati lang lan. Pa janm soumèt oswa anile san apwobasyon klè pou aksyon sa a. Pou yon demann ki mande sèlman disponiblite, tcheke disponiblite. Pou yon chanjman yo mande, pwopoze randevou ki kòrèk la ak yon lè disponib ki respekte kondisyon itilizatè a. Si lè yo mande a pa disponib, pwopoze lòt lè disponib yo bay la. Yon koreksyon ranplase randevou oswa lè anvan an. Pou demann entèprèt, transfere nan lang yo mande a."
}
TEMPLATES = {
 "consent": {
  "en": "Check availability for {id}. Do not book or cancel anything.",
  "es": "Consulta la disponibilidad para {id}. No reserves ni canceles nada.",
  "zh-Hans": "查询{id}的可用时段。不要预订或取消任何预约。",
  "uk": "Перевір доступність для {id}. Нічого не бронюй і не скасовуй.",
  "ht": "Tcheke disponiblite pou {id}. Pa rezève ni anile anyen."},
 "correction": {
  "en": "Propose moving {wrong_id} to {slot}. Correction: change {id}, not {wrong_id}. Do not submit yet.",
  "es": "Propón mover {wrong_id} a {slot}. Corrección: cambia {id}, no {wrong_id}. No envíes el cambio todavía.",
  "zh-Hans": "提议将{wrong_id}改到{slot}。更正：要更改的是{id}，不是{wrong_id}。暂时不要提交。",
  "uk": "Запропонуй перенести {wrong_id} на {slot}. Виправлення: зміни {id}, а не {wrong_id}. Ще не надсилай зміну.",
  "ht": "Pwopoze deplase {wrong_id} pou {slot}. Koreksyon: chanje {id}, pa {wrong_id}. Pa soumèt chanjman an ankò."},
 "constraint": {
  "en": "Propose an afternoon slot for {id}, but not {excluded}. Do not submit yet.",
  "es": "Propón un horario por la tarde para {id}, pero no {excluded}. No envíes el cambio todavía.",
  "zh-Hans": "为{id}提议一个下午的时段，但不要{excluded}。暂时不要提交。",
  "uk": "Запропонуй час після обіду для {id}, але не {excluded}. Ще не надсилай зміну.",
  "ht": "Pwopoze yon lè nan apremidi pou {id}, men pa {excluded}. Pa soumèt chanjman an ankò."},
 "unavailable": {
  "en": "I want {blocked} for {id}. If unavailable, propose the available alternative. Do not submit yet.",
  "es": "Quiero {blocked} para {id}. Si no está disponible, propón la alternativa disponible. No envíes el cambio todavía.",
  "zh-Hans": "我想将{id}改到{blocked}。如果不可用，请提议可用的替代时段。暂时不要提交。",
  "uk": "Я хочу {blocked} для {id}. Якщо цей час недоступний, запропонуй доступний альтернативний час. Ще не надсилай зміну.",
  "ht": "Mwen vle {blocked} pou {id}. Si li pa disponib, pwopoze lòt lè ki disponib la. Pa soumèt chanjman an ankò."},
 "handoff": {
  "en": "Request an interpreter in {interpreter}. Keep locale US. Do not change any appointments.",
  "es": "Solicita un intérprete de {interpreter}. Mantén la configuración regional US. No cambies ninguna cita.",
  "zh-Hans": "请求{interpreter}口译员。地区设置保持US。不要更改任何预约。",
  "uk": "Запроси перекладача мови {interpreter}. Залиш регіональні налаштування US. Не змінюй жодних записів.",
  "ht": "Mande yon entèprèt nan lang {interpreter}. Kenbe lokalite US. Pa chanje okenn randevou."},
 "code_switch": {
  "en": "Actually, use {id} and {slot}. Do not submit yet.",
  "es": "En realidad, usa {id} y {slot}. No envíes el cambio todavía.",
  "zh-Hans": "更正：请使用{id}和{slot}。暂时不要提交。",
  "uk": "Насправді використай {id} і {slot}. Ще не надсилай зміну.",
  "ht": "An reyalite, sèvi ak {id} ak {slot}. Pa soumèt chanjman an ankò."}
}
RECOVERY = {
 "en": "No. I reject that proposal. Use appointment {id} and slot {slot}. Propose the correction; do not submit.",
 "es": "No. Rechazo esa propuesta. Usa la cita {id} y el horario {slot}. Propón la corrección; no la envíes.",
 "zh-Hans": "不。我拒绝该提议。请使用预约{id}和时段{slot}。请提出更正方案，不要提交。",
 "uk": "Ні. Я відхиляю цю пропозицію. Використай запис {id} і час {slot}. Запропонуй виправлення; не надсилай зміну.",
 "ht": "Non. Mwen rejte pwopozisyon sa a. Sèvi ak randevou {id} ak lè {slot}. Pwopoze koreksyon an; pa soumèt li."
}
CONTRACT = ('Return exactly one JSON tool call, no prose or Markdown. Tools: '
            'lookup {"tool":"lookup","id":"..."}; propose {"tool":"propose","id":"...","slot":"..."}; '
            'handoff {"tool":"handoff","language":"..."}; commit {"tool":"commit"}; cancel {"tool":"cancel","id":"..."}. '
            'Use only the keys for the selected tool. Tool names, keys, IDs and slot labels are invariant strings.')


def build():
    rows = []
    for family in TEMPLATES:
        for variant in range(5):
            ident = f"A{variant + 1}"
            wrong = f"A{(variant + 1) % 5 + 1}"
            slot, blocked, excluded = f"S{variant + 1}", f"X{variant + 1}", f"D{variant + 1}"
            interpreter = ("uk", "zh-Hans", "es", "ht", "en")[variant]
            context = {"locale": "US", "appointments": [ident, wrong], "approval": False,
                       "slots": [{"id": slot, "day": f"D{variant + 6}", "period": "afternoon", "available": True},
                                 {"id": blocked, "day": excluded, "period": "afternoon", "available": family != "unavailable"},
                                 {"id": f"M{variant + 1}", "day": f"D{variant + 7}", "period": "morning", "available": True}]}
            facts = {"intent": "check_availability" if family == "consent" else "interpreter" if family == "handoff" else "reschedule",
                     "appointment": ident, "requested_slot": slot, "interpreter_language": interpreter if family == "handoff" else None,
                     "approval": False}
            expected = ({"tool": "lookup", "id": ident} if family == "consent" else
                        {"tool": "handoff", "language": interpreter} if family == "handoff" else
                        {"tool": "propose", "id": ident, "slot": slot})
            values = dict(id=ident, wrong_id=wrong, slot=slot, blocked=blocked, excluded=excluded, interpreter=interpreter)
            for language in LANGUAGES:
                text = TEMPLATES[family][language].format(**values)
                if family == "code_switch":
                    text = f"Propose moving {wrong} to {blocked}. " + text
                rows.append({"id": f"{family}-{variant}-{language}", "scenario": f"{family}-{variant}", "family": family,
                             "variant": variant, "language": language, "review_status": "AI-authored-draft",
                             "request": text, "context": context, "facts": facts, "expected": expected,
                             "recovery": RECOVERY[language].format(**values),
                             "recovery_expected": {"tool": "propose", "id": ident, "slot": slot},
                             "injected_proposal": {"tool": "propose", "id": wrong, "slot": f"M{variant + 1}"}})
    return rows


if __name__ == "__main__":
    path = Path("experiments/workflow/cases.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in build()), encoding="utf-8")
