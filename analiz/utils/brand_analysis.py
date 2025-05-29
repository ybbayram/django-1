import re, difflib
import tldextract
from urllib.parse import urlparse
from django.conf import settings

from .serper import serper_google_search
from .scraping import extract_emails_and_phones_from_site
from .validators import is_valid_email, is_valid_phone
from ..models import BrandAnalysis


def get_similarity_score(url, brand_name):
    ext = tldextract.extract(url)
    domain = ext.domain.lower()
    brand = brand_name.lower()
    return difflib.SequenceMatcher(None, domain, brand).ratio()


def analyze_brand(brand_name, search_instance):
    try:
        emails = []
        phone_numbers = []

        # 1. Daha önce kayıtlı mı kontrol et
        existing = BrandAnalysis.objects.filter(brand_name__iexact=brand_name).order_by('-created_at').first()
        if existing:
            result = {
                "brand_name": existing.brand_name,
                "official_site": existing.official_site,
                "emails": existing.emails.split(", ") if existing.emails else [],
                "phone_numbers": existing.phone_numbers.split(", ") if existing.phone_numbers else [],
            }
            BrandAnalysis.objects.create(
                search=search_instance,
                brand_name=existing.brand_name,
                official_site=existing.official_site,
                emails=existing.emails,
                phone_numbers=existing.phone_numbers
            )
            return result

        # 2. Serper API ile sonuçları al
        query = f"{brand_name} help mail"
        results = serper_google_search(query)
        scored_sites = [
            (url.split('?')[0], get_similarity_score(url, brand_name), snippet)
            for (url, snippet) in results
        ]
        scored_sites.sort(key=lambda x: x[1], reverse=True)

        if not scored_sites:
            return {
                "brand_name": brand_name,
                "error": "Serper sonucu bulunamadı."
            }

        official_site = scored_sites[0][0]
        parsed = urlparse(official_site)
        official_site_cleaned = f"{parsed.scheme}://{parsed.netloc}"

        # Ana domaini ayıkla (örnek: example.com)
        ext = tldextract.extract(official_site)
        root_domain = f"{ext.domain}.{ext.suffix}"

        # Tüm aynı root domain'e sahip snippet'lerden veri çek
        for site, _, snippet in scored_sites:
            site_ext = tldextract.extract(site)
            site_root = f"{site_ext.domain}.{site_ext.suffix}"
            if site_root == root_domain:
                snippet_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", snippet)
                snippet_phones = re.findall(r"\+?\d[\d\s\-\(\)]{8,}\d", snippet)
                emails += snippet_emails
                phone_numbers += [
                    re.sub(r"[^\d+]", "", p) for p in snippet_phones if len(re.sub(r"[^\d]", "", p)) >= 10
                ]

        # Eğer hem e-posta hem telefon varsa Selenium'a gerek yok
        if emails and phone_numbers:
            cleaned_emails = list({e.strip() for e in emails if "@" in e})
            cleaned_phones = list(set(phone_numbers))

            result = {
                "brand_name": brand_name,
                "official_site": official_site_cleaned,
                "emails": cleaned_emails,
                "phone_numbers": cleaned_phones,
            }

            BrandAnalysis.objects.create(
                search=search_instance,
                brand_name=brand_name,
                official_site=official_site_cleaned,
                emails=", ".join(cleaned_emails),
                phone_numbers=", ".join(cleaned_phones),
            )

            return result

        # Eksik varsa: Selenium ile siteyi ziyaret et
        try:
            sel_emails, sel_phones = extract_emails_and_phones_from_site(official_site_cleaned)

            sel_emails_clean = [e for e in sel_emails if is_valid_email(e)]
            sel_phones_clean = [
                re.sub(r"[^\d+]", "", p) for p in sel_phones
                if is_valid_phone(re.sub(r"[^\d+]", "", p))
            ]

            combined_emails = list(set(emails + sel_emails_clean))
            combined_emails = [e.strip() for e in combined_emails if "@" in e]
            combined_phones = list(set(phone_numbers + sel_phones_clean))

            result = {
                "brand_name": brand_name,
                "official_site": official_site_cleaned,
                "emails": combined_emails,
                "phone_numbers": combined_phones,
            }

            BrandAnalysis.objects.create(
                search=search_instance,
                brand_name=brand_name,
                official_site=official_site_cleaned,
                emails=", ".join(combined_emails),
                phone_numbers=", ".join(combined_phones),
            )

            return result

        except Exception as selenium_err:
            return {
                "brand_name": brand_name,
                "error": f"Selenium hatası: {selenium_err}"
            }

    except Exception as e:
        return {
            "brand_name": brand_name,
            "error": str(e)
        }
