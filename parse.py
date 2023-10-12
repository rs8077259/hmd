a=open("CSS.md")
class Parse:
    
    heading_={
        '###### ':('<h6 id="%s">','</h6>'),
        '##### ':('<h5 id="%s">','</h5>'),
        '#### ':('<h4 id="%s">','</h4>'),
        '### ':('<h3 id="%s">','</h3>'),
        '## ':('<h2 id="%s">','</h2>'),
        '# ':('<h1 id="%s">','</h1>'),
    }
    heghlite=("<span class='heighlite'>","</span>")
    code_=("<pre><code class='language-%s'>","</code></pre>")
    
    ol=("<ol><li>","</li></ol>")
    ul=("<ul>","</ul>")
    li=("<li>","</li>")
    checkbox_1="<input type='checkbox' checked id='%s'>"
    
    label_=("<label for='%s'>","</label>")
    hrule="<hr>"
    block_=("<div id='%s'>","</div>")

    def has_heading(text:str)->bool:
        if text[0:1]=="#":
            return True
        return False
    def has_code(text:str)->bool:
        if text[:3]=="```":
            return True
        return False
    def to_heading(text:str)->str:
        for marker in Parse.heading_:
            if marker in text:
                return text.replace(marker,Parse.heading_[marker][0]%text.strip(marker).replace(' ','-') )+Parse.heading_[marker][1]
    def to_bold(text:str)->str:
        return (text.replace('**',Parse.bold[0],1)).replace('**',Parse.bold[1])
    def to_code_start(text:str)->str:
        return Parse.code_[0]%text[3:]
    def to_code_end(text:str)->str:
        return Parse.code_[0]
    def highlite(text:str)->str:
        h=("<mark>","</mark>")
        pos=0
        while '==' in text:
            text=text.replace("==",h[pos],1)
            pos=0 if pos else 1
        return text
    def cuttext(text):
        cuttext=("<s>","</s>")
        pos=0
        while '~~' in text:
            text=text.replace("~~",cuttext[pos],1)
            pos=0 if pos else 1
        return text
    def bold(text):
        bold=("<b>","</b>")
        pos=0
        while '**' in text:
            text=text.replace('**',bold[pos],1)
            pos=0 if pos else 1
        return text
    inlinetag={
        "**": lambda :Parse.bold,
        '~~':lambda: Parse.cuttext,
        '==':lambda: Parse.highlite,
        '![[':lambda:Parse.embed,
        '[[':lambda:Parse.link_page,
        '](':lambda:Parse.link_webpage

    }
    def link_page(text:str)->str:
        text=text.strip('[[').strip(']]')
        return "<a href='{{ url \"get_note\"+?note=%s }}'>%s</a>"%(text,text)
    def embed(text:str)->str:
        text=text.strip('![[').strip(']]')
        extention=text[text.find('.')+1:]
        if extention in ('mp4','mov','wmv','avi','avchd','swf','flv','f4v','mkv','webm'):
            return f"<video src='{{}}' controls muted>vide format not supported by browser</video>"
        elif extention in ('mp3','aac','aifc','wma','ogg'):
            return '<audio src="%s" controls>format not supported by browser</audio>'
        elif extention in ('jpeg','jpg','tiff','bmp','png','gif','psd','ai','raw','svg'):
            return '<img src="" alt="image">'
        else:
            return '<iframe src="{{ url \"get_note\"+?note=%s }}" width=100%s height="200px" frameborder="0"></iframe>'%(text,'%')
    def link_webpage(text:str)->str:
        text=text.strip('[').strip(')').split('](')
        return f'<a href="{text[1]}">{text[0]}</a>'
    def __init__(self,obj:'iterable') -> None:
        self.iterable=obj.__iter__()
        self.html=[]
    
    def to_html(self):
        # saving the "self.iterable.__nect__()" in  "Parse.to_html" to save memory
        Parse.to_html.text=self.iterable.__next__()
        if Parse.has_heading(self.to_html.text):
            self.html.append(Parse.to_heading(self.to_html.text))
        elif Parse.has_code(self.to_html.text):
            self.html.append(Parse.to_code_start(self.to_html.text))
            #appinding the code in list while we get ``
            text=self.iterable.__next__()
            while text[:3]!='```':
                text=text.replace("<","&lt")
                text=text.replace(">","&gt")
                self.html.append("\n")
                self.html.append(text)
                text=self.iterable.__next__()
            self.html.append(Parse.code_[1])
        elif Parse.to_html.text=="---":
            self.html.append('<hr>')
        elif '- [ ] ' in Parse.to_html.text:
            self.html.append(Parse.to_html.text.replace('- [ ] ','<br><input type="checkbox" >')+'</br>')
        elif '- [x] ' in Parse.to_html.text:
            self.html.append(Parse.to_html.text.replace('- [x] ','<br><input type="checkbox" checked>')+'</br>')
        else:
            for element in Parse.inlinetag:
                if element in Parse.to_html.text:
                    o.html.append(Parse.inlinetag[element]()(Parse.to_html.text))
                    break
            else:
                self.html.extend(['<br>',Parse.to_html.text])
        try:
            self.to_html()
        except StopIteration:
            pass
    def write_html(self,filename:str):
        filename=filename+'.html'
        file=open(filename,'w')
        file.write('''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="prism.css"><link rel="stylesheet" href="prism-odark.css"><link rel="stylesheet" href="md.css"><title>Document</title></head><body>'''
                   )
        file.writelines(self.html)
        file.write('''<script src="prism.js"></script></body></html>''')
        

g=a.read().splitlines()
o=Parse(g)
o.to_html()
o.write_html("first")


