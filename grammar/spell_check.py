import language_tool_python  

def check(name):  
    # using the tool  
    tool = language_tool_python.LanguageTool('en-US')  
    with open('%s.txt' %name) as f:
        lines = f.readlines()
    text = str(lines)
    # getting the matches  
    my_matches = tool.check(text)  
    
    # defining some variables  
    myMistakes = [] 
    startPositions = []  
    endPositions = []  
    
    # using the for-loop  
    for rules in my_matches:  
        if len(rules.replacements) > 0:  
            startPositions.append(rules.offset)  
            endPositions.append(rules.errorLength + rules.offset)  
            myMistakes.append(text[rules.offset : rules.errorLength + rules.offset])  
    count = len(myMistakes)
    print(myMistakes)
    print(count)
if __name__ == "__main__":
    name = "input"
    check(name)
