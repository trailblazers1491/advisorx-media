import re,sys,json
RES=r'\|{}@[]()<>*_~'
def li(text):
    out=[]
    for ch in text:
        out.append('\\'+ch if ch in RES else ch)
    t=''.join(out)
    # hashtags -> LinkedIn hashtag template
    t=re.sub(r'#(\w+)', r'{hashtag|\\#|\1}', t)
    return t
if __name__=="__main__":
    print(json.dumps(li(sys.stdin.read())))
