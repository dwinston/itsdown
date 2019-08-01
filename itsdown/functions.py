import re
from functools import partial


def fwsdash_24hr(soup, threshold_pct=0):
    """given bs node as input, decides whether the service is down and returns a useful message"""
    fw_report_text = soup.find("pre").get_text()
    total_fws = sum(int(n) for n in re.findall(f"\ntotal\s*:\s*(\d+)", fw_report_text))
    completed_fws = sum(
        int(n) for n in re.findall(f"\nCOMPLETED\s*:\s*(\d+)", fw_report_text)
    )
    if total_fws:
        pct_complete = 100 * completed_fws / total_fws
        if pct_complete <= threshold_pct:
            return f"{total_fws} submitted, but {completed_fws} completed (under {threshold_pct}% threshold)"
    return None


fwsdash_24hr_10 = partial(fwsdash_24hr, threshold_pct=10)
fwsdash_24hr_50 = partial(fwsdash_24hr, threshold_pct=50)
fwsdash_24hr_100 = partial(fwsdash_24hr, threshold_pct=100)

def test_page_content(soup):
    return(soup)


