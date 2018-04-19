"""
Utility functions to extract the HTML string from the common crawl entries
"""

def extract_html(cc_entry):
    """
    Takes:
    cc_entry [str]

    Returns:
    html [str]
    """
    return cc_entry.strip().split('\r\n\r\n',2)[-1]
