
import os
import shutil

inputDir = "/Users/jrsteven/Box Sync/GlueX/gluex_documents/gluex_papers/K+Sigma0_BeamAsym_2019/"
inputLatex = inputDir + "kpsig.tex"
papername = "2019ksigma"

outname = "papers/%s.yml" % papername
outfile = open(outname, 'w')

figDir = papername
print(figDir)
if not os.path.exists(figDir):
    os.mkdir(figDir)

numFigs = 0

with open(inputLatex) as fp:
    line = fp.readline()
    cnt = 1
    
    while line:
        #print("Line {}: {}".format(cnt, line.strip()))
        line = fp.readline()
        #print(type(line))
        cnt += 1
    
        # Find title and abstract in text
        foundTitle = False
        foundAbstract = False
        if 'title{' in line:
            foundTitle = True
            print("- name:", papername, file=outfile)
            removeStuff = ["~"]
            for stuff in removeStuff:
                line = line.replace(stuff," ")
            print("  title:", line[7:-2], file=outfile)
        if 'begin{abstract}' in line:
            abstract = ""
            
            # Loop until you find the end of the abstract
            while not foundAbstract:
                line = fp.readline()
                
                if 'end{abstract}' in line:
                    foundAbstract = True
                    break
                if line[0] == "%" or line[0] == "\\" or len(line) == 1:
                    continue
                else:
                    # strip out \n (new line) from abstract
                    removeStuff = ["\n", "~"]
                    for stuff in removeStuff:
                        line = line.replace(stuff," ")
                        
                    abstract += line
            
            print("  abstract:", abstract, file=outfile)
            print("  citation: ", file=outfile)
            print("  doi: ", file=outfile)
            print("  arXiv: ", file=outfile)
            print("  link: /papers/%s/paper.html\n" % papername, file=outfile)
    
    
        # Found figure in text
        if 'begin{figure}' in line:
            numFigs += 1
            print("- figure: %d" % numFigs, file=outfile)
            print("  papername:", papername, file=outfile)
            
            # Loop until you find end of figure
            foundFigureEnd = False
            while not foundFigureEnd:
                line = fp.readline()
                # print(line)
                
                if 'end{figure}' in line:
                    foundFigureEnd = True
                    break
                    
                if 'caption{' in line:
                    caption = "  caption: "
                    
                    line = line.replace(":",",")
                    removeStuff = ["\n", "~"]
                    for stuff in removeStuff:
                        line = line.replace(stuff," ")
                                       
                    # skip final closing parentheses
                    print("checking caption")
                    print(line)
                    print(line[len(line)-10:])
                    if '}' in line[len(line)-10:]:
                        print("found end of caption")
                        caption += line[9:-2]
                    else:
                        caption += line[9:]
                    #caption += line[9:]
                
                    foundCaptionEnd = False
                    while not foundCaptionEnd:
                        line = fp.readline()
                        
                        if 'end{' in line or 'label{' in line:
                            foundCaptionEnd = True
                            break
                        
                        # Need to strip out colons and new lines from captions
                        line = line.replace(":",",")
                        removeStuff = ["\n", "~"]
                        for stuff in removeStuff:
                            line = line.replace(stuff," ")
                        
                        # skip final closing parentheses
                        if '}' in line[len(line)-5:]:
                            caption += line[:-2]
                        else:
                            caption += line
                        
                    print(caption)
                    print(caption, file=outfile)
                    print("", file=outfile)
                    
                if 'includegraphics' in line:
                    #print(line)
                    extensions = [".pdf"]
                    
                    for ext in extensions:
                        if ext in line:
                            pathName = ""
                            extIndex = line.find(ext)
                            for i in range(1,100):
                                if line[extIndex-i] == "{":
                                    break
                                pathName = line[extIndex-i:extIndex]
                            
                            figName = "fig%d" % numFigs
                            pathName += ext
                            print(figName)
                            print(pathName)
                            shutil.copyfile(inputDir + "/" + pathName, figDir + "/" + figName + ext)
                            os.system("sips -s format png %s/%s.pdf --out %s/%s.png" % (figDir,figName,figDir,figName))

# move figure directory to proper location
if os.path.exists("../papers/%s" % figDir):
    shutil.rmtree("../papers/%s" % figDir)

shutil.move(figDir,"../papers/")

outfileMD = open("../papers/%s/paper.md" % figDir, 'w')
print("---", file=outfileMD)
print("layout: paper", file=outfileMD)
print("papername: %s" % papername, file=outfileMD)
print("---", file=outfileMD)

