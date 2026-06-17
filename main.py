import os
import sys
import json
from pydantic import BaseModel
from google import genai
from google.genai import types


def ai_qebul_komitesi_mentoru():
    # 1. API AÇARININ AXTARILMASI VƏ TƏYİN EDİLMƏSİ
    api_key = os.environ.get("AIzaSyDYo387t77TFs5QHwaquTeNICBL_j0jXUU")

    # Əgər mühit dəyişəni tapılmasa, istifadəçidən birbaşa daxil etməsini istəyirik
    if not api_key:
        print("Məlumat: GEMINI_API_KEY mühit dəyişəni sistemdə tapılmadı.")
        api_key = input("Zəhmət olmasa Gemini API açarınızı bura yapışdırın: ").strip()

    if not api_key:
        print("Xəta: API açarı daxil edilmədiyi üçün proqram dayandırılır.")
        return

    # Klienti daxil edilən açarla başladırıq
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Klient yaradılarkən xəta: {e}")
        return

    print("\n=== GEMINI 2.5 FLASH İLƏ HOLİSTİK QƏBUL ANALİZİ ===\n")
    print("Özünüz, təhsiliniz, layihələriniz, nailiyyətləriniz və məhdudiyyətləriniz")
    print("barədə geniş məlumat yazın.")
    print("(Yazını bitirmək üçün yeni sətirdə Windows-da CTRL+Z, Mac/Linux-da CTRL+D sıxın və ya Enter-ə basın):\n")

    # Çoxsətirli mətn qəbulu
    user_story = sys.stdin.read()

    if not user_story.strip():
        print("Mətn daxil edilmədi. Proqram dayandırılır.")
        return

    print("\n[Süni İntellekt müraciəti analiz edir və insider qərarlarını formalaşdırır...]")

    # 2. STRUKTURLU ÇIXIŞ SXEMİ
    class Universitet(BaseModel):
        ad: str
        zona: str
        teqaub_imkani: str
        esas_sebeb: str

    class MentorAnalizi(BaseModel):
        muracietci_adi: str
        tehsil_seviyyesi: str
        akademik_indeks: float
        profil_indeksi: float
        resurs_kompensasiya_emsali: float
        yekun_ferdi_profil_gucu: float
        iti_bucaq_fokusu_tesviri: str
        universitetler: list[Universitet]
        strateji_tovsiye: str

    system_prompt = """
    Sən ABŞ-ın Ivy League və Böyük Britaniyanın Russell Group universitetlərinin beynəlxalq qəbul komitəsinin rəhbərisən. Qarşındakı müraciətçinin sərbəst yazdığı bioqrafiyanı, nailiyyətlərini və şəraitini "Holistik Baxış" (Holistic Review) fəlsəfəsi ilə təhlil etməlisən.

İstifadəçinin mətnini oxuyarkən aşağıdakı daxili məntiqlə hərəkət et:

1. TƏHSİL SƏVİYYƏSİNİN TƏYİNİ:
- Əgər müraciətçi məktəblidirsə, universitetə yeni hazırlaşırsa və ya heç bir bakalavr dərəcəsi yoxdursa, "tehsil_seviyyesi" sahəsini "Bachelor" təyin et.
- Əgər bakalavrdırsa, universiteti bitiribsə və ya korporativ iş təcrübəsi (məs. bank, şirkət, laboratoriya) varsa, "Master" təyin et.

2. ANALİTİK STATİSTİKANIN GENERASİYASI (100 ballıq şkala ilə):
- akademik_indeks: Qiymətlərə (GPA), imtahanlara (SAT/IELTS) və ən əsası qiymət dinamikasına bax. Əgər tələbə ilk illər zəif, son illər güclü oxuyubsa, intellektual yetkinləşmə bonusu ver. SAT yoxdursa, GPA və digər akademik uğurları süzgəcdən keçir.
- profil_indeksi: Fəaliyyətlərin sayına yox, dərinliyinə bax. 12 aydan çox davam edən layihələrə yüksək bal ver.
- resurs_kompensasiya_emsali: Bu ən kritik məqamdır. Əgər tələbə resursları kəskin məhdud olan bir mühitdən (məsələn, Azərbaycanın regionları, kənd məktəbi, internet qıtlığı olan yerlər) gəlirsə və buna rəğmən uğur qazanıbsa, bu balı maksimuma (90-100) yaxınlaşdır. Elit, bahalı özəl məktəb tələbələrinin standart uğurlarına isə kompensasiya balını aşağı (30-50) ver.
- yekun_ferdi_profil_gucu: Bu üç indeksin kontekstual çəkili ortalamasını çıxar.

3. İTİ BUCAQ FOKUSU (Spike):
- Azərbaycan bazarındakı "hər şeydən bir az edən" dağınıq profilləri tənqid et. Tələbənin bütün fəaliyyətlərini birləşdirən o tək "iti küncü" (məsələn, texnologiyanı sosial rifah üçün istifadə etmək, rəqəmsal humanitar elmlər və s.) tap və "iti_bucaq_fokusu_tesviri" sahəsində şərh et.

4. STRATEJİ UNİVERSİTET SEÇİMİ:
- Tələbənin profil gücünə uyğun olaraq real ABŞ və Britaniya universitetlərini 3 zonaya böl: "Sigorta" (mütləq qəbul), "Hedef" (tam uzlaşan və təqaüd şansı yüksək), "Arzu" (çətin, amma insider esselərlə möcüzə yaradıla biləcək Ivy League proqramları).
- Hər universitet üçün daxili maliyyə fondlarını (Need-Blind, Need-Based, Merit-Based) araşdırıb təqaüd növünü dəqiq yaz və qəbul komitəsi adından daxili qəbul sirrini ("esas_sebeb") izah et.

QAYDA: Cavabın yalnız təyin olunmuş Pydantic sxeminə uyğun təmiz JSON formatında olmalıdır. Mətnə heç bir əlavə giriş və ya çıxış sözləri əlavə etmə.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_story,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=MentorAnalizi,
                temperature=0.2,
            ),
        )

        data = json.loads(response.text)

        print("\n" + "=" * 50)
        print(f"MÜRACIƏTÇİ: {data.get('muracietci_adi', 'Naməlum').upper()}")
        print(f"TƏYİN OLUNAN TƏHSİL SƏVİYYƏSİ: {data.get('tehsil_seviyyesi', 'Bachelor/Master').upper()}")
        print("=" * 50)
        print(f"• Akademik İndeks: {data.get('akademik_indeks')} / 100")
        print(f"• Profil İndeksi: {data.get('profil_indeksi')} / 100")
        print(f"• Resurs Kompensasiya Əmsalı: {data.get('resurs_kompensasiya_emsali')} / 100")
        print(f"• YEKUN FƏRDİ PROFİL GÜCÜ: {data.get('yekun_ferdi_profil_gucu')} / 100")
        print(f"\n[İti Bucaq Fokusu]: {data.get('iti_bucaq_fokusu_tesviri')}\n")

        print("--- AI STRATEJİ UNIVERSITET VƏ TƏQAÜD MATRİSİ ---\n")
        for uni in data.get('universitetler', []):
            print(f"[{uni['zona'].upper()} ZONASI]")
            print(f"• Universitet: {uni['ad']}")
            print(f"  Təqaüd İmkanı: {uni['teqaub_imkani']}")
            print(f"  Qəbul Komitəsinin Rəyi: {uni['esas_sebeb']}\n")

        print("--- MENTORUN YEKUN STRATEJİ TÖVSİYƏSİ ---")
        print(data.get('strateji_tovsiye'))
        print("=" * 50)

    except Exception as e:
        print(f"\nGenerasiya zamanı xəta baş verdi: {e}")


if __name__ == "__main__":
    ai_qebul_komitesi_mentoru()
