
import os
import shutil

# Notes:
## Still don't have citations or references in figure captions automated, so need to do that by hand
## Could find way to pull citation information from InspireHEP but haven't gotten there yet

# fill out input source file location and citation information for given paper
inputDir = "/Users/jrsteven/Box Sync/GlueX/gluex_documents/gluex_papers/gx4971-ALP-gx1/"
inputLatex = inputDir + "blah.tex"
papername = "2021alp"
papercitation = "  citation: Phys. Rev. D105, 052007 (2022)"
doi = "  doi: 10.1103/PhysRevD.105.052007"
arXiv = "  arXiv: 2109.13439"
hepdata = "  hepdata: 999999"

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
        line = line.replace("\gx","GlueX")
        line = line.replace("\gx{}","GlueX")
            
        # Find title and abstract in text
        foundTitle = False
        foundAbstract = False
        if 'title{' in line:
            foundTitle = True
            print("- name:", papername, file=outfile)
            removeStuff = ["\n", "~", "\\,", "\\\\", "\\boldmath"]
            for stuff in removeStuff:
                line = line.replace(stuff," ")
            print("  title:", line[7:-2], file=outfile)
        if 'begin{abstract}' in line:
            abstract = ""
            
            # Loop until you find the end of the abstract
            while not foundAbstract:
                line = fp.readline()
                if len(line) > 0 and '%' in line[0]: continue
                line = line.replace("\gx","GlueX")
                line = line.replace("\gx{}","GlueX")
                
                if 'end{abstract}' in line:
                    foundAbstract = True
                    break
                if line[0] == "%" or line[0] == "\\" or len(line) == 1:
                    continue
                else:
                    # strip out \n (new line) from abstract
                    removeStuff = ["\n", "~", "\\,", "\\boldmath", ":"]
                    for stuff in removeStuff:
                        line = line.replace(stuff," ")
                        
                    abstract += line
            
            abstract = abstract.replace("\\textsc{GlueX}","GlueX")
            abstract = abstract.replace("--","-")
            print("  abstract:", abstract, file=outfile)
            print(papercitation, file=outfile)
            print(doi, file=outfile)
            print(arXiv, file=outfile)
            print(hepdata, file=outfile)
            print("  link: /papers/%s/paper.html\n" % papername, file=outfile)
    
    
        # Found figure in text
        if 'begin{figure' in line:
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
                    
                if 'caption' in line:
                    line = line.replace(":",",")
                    line = line.replace("\%","%")
                    removeStuff = ["\\n", "~", "{\n"]
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
                        line = line.replace("\!"," ")
                                                
                        # skip final closing parentheses
                        if '}' in line[len(line)-5:]:
                            caption += line[:-2]
                        #elif '{' in line[0] or '[' in line[0]:
                        #    caption += line[1:]
                        else:
                            caption += line
                        
                    
                if 'includegraphics' in line:
                    #print(line)
                    extensions = [".pdf",".png",".jpg"]
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

            # print all subfigures
            print(figurelabels)
            for figurelabel,figurefile in zip(figurelabels,figurefiles): #subfigures:
                figurenumber = figurelabel.replace("fig","")
                print("- figure: %s" % figurenumber, file=outfile)
                print("  papername:", papername, file=outfile)
                print(papercitation, file=outfile)
                print(doi, file=outfile)
                
                removeStuff = ["\n", "~", "\\,", "]{", "(Color online)", "(color online)", "n{"]
                for stuff in removeStuff:
                    caption = caption.replace(stuff," ")
                caption = caption.replace("\gx{}","GlueX")
                caption = caption.replace("\GX{}","GlueX")
                caption = caption.replace("\gx","GlueX")
                caption = caption.replace("\textsc{GlueX}","GlueX")
                
                # remove labels from caption
                if 'label' in caption:
                    labelIndex = caption.find('label')
                    labelReplace = ""
                    for i in range(-1,100):
                        labelReplace += caption[labelIndex+i]
                        if caption[labelIndex+i] == "}":
                                break
                    caption = caption.replace(labelReplace,"")
                    
                # strip closing brace from caption
                if '}' in caption[len(caption)-10:]:
                    for i in range(1,10):
                        print(len(caption) - i)
                        if caption[len(caption)-i] == '}':
                            caption = caption[:len(caption)-i]
                            break
                    
                print(caption)
                print(caption, file=outfile)
                print("", file=outfile)
                
                if '.pdf' in figurefile:
                    shutil.copyfile(figurefile, figDir + "/" + figurelabel + ".pdf")
                    os.system("sips -s format png %s/%s.pdf --out %s/%s.png" % (figDir,figurelabel,figDir,figurelabel))
                if '.png' in figurefile:
                    shutil.copyfile(figurefile, figDir + "/" + figurelabel + ".png")
                    os.system("sips -s format pdf %s/%s.png --out %s/%s.pdf" % (figDir,figurelabel,figDir,figurelabel))
                if '.jpg' in figurefile:
                    shutil.copyfile(figurefile, figDir + "/" + figurelabel + ".jpg")
                    os.system("sips -s format png %s/%s.jpg --out %s/%s.png" % (figDir,figurelabel,figDir,figurelabel))
                    os.system("sips -s format pdf %s/%s.jpg --out %s/%s.pdf" % (figDir,figurelabel,figDir,figurelabel))
    
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

