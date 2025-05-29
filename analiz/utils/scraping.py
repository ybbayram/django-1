import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_emails_and_phones_from_site(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    emails = []
    phones = []

    def extract_valid_emails(raw_list):
        cleaned = []
        for e in raw_list:
            e = e.strip()
            if not e or "@" not in e:
                continue
            match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", e)
            if match:
                cleaned.append(match.group())
        return list(set(cleaned))

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        def extract_visible_text():
            return driver.execute_script("""
                return Array.from(document.querySelectorAll('body *'))
                    .filter(el => el.offsetParent !== null &&
                                  getComputedStyle(el).visibility !== 'hidden' &&
                                  !['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName))
                    .map(el => el.innerText)
                    .join('\\n');
            """)

        visible_text = extract_visible_text()


        lines = visible_text.splitlines()
        filtered_lines = []
        for line in lines:
            if "fax" in line.lower():
                idx = line.lower().find("fax")
                filtered_lines.append(line[:idx].strip())
            else:
                filtered_lines.append(line)
        filtered_text = "\n".join(filtered_lines)

        emails += re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", visible_text)
        phones += re.findall(r"\+?\d[\d\s\-\(\)]{8,}\d", filtered_text)

        tel_links = driver.execute_script("""
            return Array.from(document.querySelectorAll('a[href^="tel:"]')).map(el => el.getAttribute("href"));
        """)
        phones += [
            re.sub(r"[^\d+]", "", tel.replace("tel:", ""))
            for tel in tel_links if tel and len(re.sub(r"[^\d]", "", tel)) >= 10
        ]

        mailto_data = driver.execute_script("""
            return Array.from(document.querySelectorAll('a[href^="mailto:"]')).map(el => ({
                href: el.getAttribute("href"),
                text: el.textContent.trim()
            }));
        """)
        for item in mailto_data:
            if item["href"]:
                clean_href = re.sub(r"^mailto:", "", item["href"]).split('?')[0].strip()
                emails.append(clean_href)
            if item["text"]:
                emails.append(item["text"].strip())

        hrefs = driver.execute_script("""
            return Array.from(document.querySelectorAll("a[href]")).map(a => a.getAttribute("href"));
        """)
        contact_links = [
            urljoin(url, h) for h in hrefs
            if h and any(k in h.lower() for k in ["contact", "iletisim", "iletisime-gec"])
        ]

        for contact_url in contact_links:
            try:
                driver.get(contact_url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                contact_text = extract_visible_text()

                emails += re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", contact_text)
                phones += re.findall(r"\+?\d[\d\s\-\(\)]{8,}\d", contact_text)

                mailto_data_extra = driver.execute_script("""
                    return Array.from(document.querySelectorAll('a[href^="mailto:"]')).map(el => ({
                        href: el.getAttribute("href"),
                        text: el.textContent.trim()
                    }));
                """)
                for item in mailto_data_extra:
                    if item["href"]:
                        clean_href = re.sub(r"^mailto:", "", item["href"]).split('?')[0].strip()
                        emails.append(clean_href)
                    if item["text"]:
                        emails.append(item["text"].strip())

                tel_links_extra = driver.execute_script("""
                    return Array.from(document.querySelectorAll('a[href^="tel:"]')).map(el => el.getAttribute("href"));
                """)
                phones += [
                    re.sub(r"[^\d+]", "", tel.replace("tel:", ""))
                    for tel in tel_links_extra if tel and len(re.sub(r"[^\d]", "", tel)) >= 10
                ]
            except Exception as e:
                continue

    finally:
        driver.quit()

    # Temizle
    emails = extract_valid_emails(emails)
    phones = list(set(phones))

    return emails, phones
