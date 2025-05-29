import re

def is_valid_email(email):
    email = email.lower()

    if (
        re.search(r"\d{5,}", email)  # Çok fazla rakam spam olabilir
        or len(email) < 6
        or len(email) > 64
        or "yourname" in email
        or "domain" in email
    ):
        return False

    valid_tlds = [
        # Genel üst düzey alanlar (gTLD)
        ".com", ".org", ".net", ".info", ".biz", ".name", ".pro", ".tel", ".asia",
        ".coop", ".int", ".jobs", ".mobi", ".museum", ".travel", ".cat", ".aero",

        # Popüler yeni nesil alanlar
        ".online", ".site", ".tech", ".store", ".xyz", ".website", ".space", ".app",
        ".dev", ".page", ".cloud", ".fun", ".life", ".live", ".today", ".world",
        ".shop", ".company", ".digital", ".media", ".systems", ".group", ".agency",
        ".support", ".solutions", ".network", ".tools", ".services", ".finance",
        ".capital", ".global", ".business", ".center", ".email", ".expert", ".guru",
        ".institute", ".academy", ".training", ".ventures", ".works", ".software",

        # Ülke kodlu alanlar (ccTLD)
        ".us", ".uk", ".de", ".fr", ".it", ".es", ".nl", ".ru", ".ch", ".se", ".no",
        ".fi", ".be", ".pl", ".at", ".cz", ".gr", ".pt", ".dk", ".tr", ".ir", ".ua",
        ".ca", ".au", ".in", ".cn", ".jp", ".kr", ".co.kr", ".br", ".ar", ".mx", ".cl",
        ".id", ".my", ".ph", ".hk", ".sg", ".tw", ".sa", ".ae", ".il", ".nz",

        # Diğer yaygın alanlar
        ".io", ".ai", ".me", ".tv", ".cc", ".ly", ".to", ".fm", ".am", ".gl", ".la"
    ]

    return any(email.endswith(tld) for tld in valid_tlds)


def clean_phone_number(phone):
    if not phone:
        return None
    return re.sub(r"[^\d+]", "", phone)


def is_valid_phone(phone):
    phone = phone.strip()

    if not re.match(r"^\+?\d{10,15}$", phone):
        return False

    if phone.startswith("1") or phone.startswith("2"):
        return False

    if len(set(phone.replace("+", ""))) == 1:
        return False

    if not phone.startswith("+") and len(phone) < 11:
        return False

    return True
