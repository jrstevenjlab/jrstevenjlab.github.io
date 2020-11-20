
import os
import shutil

# Notes:
## Still don't have citations or references in figure captions automated, so need to do that by hand
## Could find way to pull citation information from InspireHEP but haven't gotten there yet

# fill out input source file location and citation information for given paper
inputDir = "/Users/jrsteven/Box Sync/GlueX/gluex_documents/gluex_nim/GlueX_nim/"
inputLatex = inputDir + "blah.tex"
papername = "2020nim"
citation = "  citation: NIM A 987 (2021) 164807"
doi = "  doi: 10.1016/j.nima.2020.164807"
arXiv = "  arXiv: 2005.14272"

outname = "papers/%s.yml" % papername
outfile = open(outname, 'w')

figDir = papername
print(figDir)
if not os.path.exists(figDir):
    os.mkdir(figDir)

numFigs = 0

# loop over source file, create markdown for paper and write image files with proper naming convention
with open(inputLatex) as fp:
    line = fp.readline()
    
    while line:
        line = fp.readline()
        if len(line) > 0 and '%' in line[0]: continue
            
        # Find title and abstract in text
        foundTitle = False
        foundAbstract = False
        if 'title{' in line:
            foundTitle = True
            print("- name:", papername, file=outfile)
            removeStuff = ["\n", "~", "\\,", "\\\\"]
            for stuff in removeStuff:
                line = line.replace(stuff," ")
            print("  title:", line[7:-2], file=outfile)
        if 'begin{abstract}' in line:
            abstract = ""
            
            # Loop until you find the end of the abstract
            while not foundAbstract:
                line = fp.readline()
                if '%' in line[0]: continue
                
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
            print(citation, file=outfile)
            print(doi, file=outfile)
            print(arXiv, file=outfile)
            print("  link: /papers/%s/paper.html\n" % papername, file=outfile)
    
    
        # Found figure in text
        if 'begin{figure}' in line:
            numFigs += 1
            caption = "  caption: "
            
            # Loop until you find end of figure
            foundFigureEnd = False
            figurelabels = []
            figurefiles = []
            while not foundFigureEnd:
                line = fp.readline()
                if len(line) > 0 and '%' in line[0]: continue
                
                if 'end{figure}' in line:
                    foundFigureEnd = True
                    break
                    
                if 'caption{' in line:
                    line = line.replace(":",",")
                    line = line.replace("\%","%")
                    removeStuff = ["\\n", "~"]
                    for stuff in removeStuff:
                        line = line.replace(stuff," ")
                                       
                    # skip final closing parentheses
                    print("checking caption")
                    print(line)
                    print(line[len(line)-10:])
                    if '}' in line[len(line)-10:] and 'label' not in line:
                        print("found end of caption")
                        caption += line[9:-2]
                    else:
                        caption += line[9:]
                
                    foundCaptionEnd = False
                    while not foundCaptionEnd:
                        line = fp.readline()
                        if len(line) > 0 and '%' in line[0]: continue
                        print(line)
                               
                        if 'end{' in line or 'label{' in line:
                            foundCaptionEnd = True
                            foundFigureEnd = True
                            print("found end of caption")
                            break
                        
                        # Need to strip out colons and new lines from captions
                        line = line.replace(":",",")
                        line = line.replace("\%","%")
                        line = line.replace("\n"," ")
                        
                        # skip final closing parentheses
                        if '}' in line[len(line)-5:]:
                            caption += line[:-2]
                        else:
                            caption += line
                        
                    
                if 'includegraphics' in line:
                    #print(line)
                    extensions = [".pdf"]
                    if len(figurelabels) == 0:
                        figurelabels.append("fig%d" % numFigs)
                    else:
                        print("new subfigure")
                        figurelabels[0] = "fig%da" % numFigs
                        figurelabels.append("fig%d%c" % (numFigs, chr(ord('`')+len(figurelabels)+1)))
                    
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
                            figurefiles.append(inputDir + "/" + pathName)
                            
                            #shutil.copyfile(inputDir + "/" + pathName, figDir + "/" + figName + ext)
                            #os.system("sips -s format png %s/%s.pdf --out %s/%s.png" % (figDir,figName,figDir,figName))

            # print all subfigures
            print(figurelabels)
            for figurelabel,figurefile in zip(figurelabels,figurefiles): #subfigures:
                figurenumber = figurelabel.replace("fig","")
                print("- figure: %s" % figurenumber, file=outfile)
                print("  papername:", papername, file=outfile)
                
                removeStuff = ["\n", "~", "\\,"]
                for stuff in removeStuff:
                    caption = caption.replace(stuff," ")
                print(caption)
                print(caption, file=outfile)
                print("", file=outfile)
                
                shutil.copyfile(figurefile, figDir + "/" + figurelabel + ".pdf")
                os.system("sips -s format png %s/%s.pdf --out %s/%s.png" % (figDir,figurelabel,figDir,figurelabel))
    
    # anyting to be done with LaTeX file ends here
    print("finished parsing LaTeX file")
    
# move figure directory to proper location
if os.path.exists("../papers/%s" % figDir):
    shutil.rmtree("../papers/%s" % figDir)

shutil.move(figDir,"../papers/")

outfileMD = open("../papers/%s/paper.md" % figDir, 'w')
print("---", file=outfileMD)
print("layout: paper", file=outfileMD)
print("papername: %s" % papername, file=outfileMD)
print("---", file=outfileMD)

