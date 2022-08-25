import language_tool_python  

def check(name):  
    # using the tool  
    tool = language_tool_python.LanguageTool('en-US')  
    with open('%s.txt' %name) as f:
        lines = f.readlines()
    f.close()
    text = str(lines)
    # getting the matches  
    my_matches = tool.check(text)  
    
    myMistakes = [] 
    
    for rules in my_matches:  
        if len(rules.replacements) > 0:  
            myMistakes.append(text[rules.offset : rules.errorLength + rules.offset])  
    count = len(myMistakes)
    print("List of spelling errors:",myMistakes)
    print("Count",count)
if __name__ == "__main__":
    name = "input" #tbi
    check(name)
