import sys
from html.parser import HTMLParser

class NexFiHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_ids = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == 'id':
                self.found_ids.add(value)

def verify_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parser = NexFiHTMLParser()
        parser.feed(content)
        
        required_ids = [
            'cli-toggle-btn',
            'cli-overlay',
            'cli-input-field',
            'budgetRingFill',
            'prompt-chips',
            'nav-pill',
            'ticker-content'
        ]
        
        failed = False
        for req_id in required_ids:
            if req_id in parser.found_ids:
                print(f"PASS: #{req_id} is present.")
            else:
                print(f"FAIL: #{req_id} is missing!")
                failed = True
                
        if failed:
            sys.exit(1)
        print("All HTML validations passed successfully!")
    except Exception as e:
        print(f"Error during validation: {e}")
        sys.exit(1)

if __name__ == '__main__':
    verify_html('/Users/sujal/finance-agent/index.html')
