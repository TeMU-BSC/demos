#!/usr/bin/env python
import csv, os

def writeOut(termdic,termcodes,fileout,type):
    w = open(fileout,"w")
    if type ==1:
        wr = csv.writer(w,dialect='excel',delimiter="\t")
        for term, code in zip(termdic,termcodes):
            score = code[0][1]
            codigo = code[0][0]
            if code[0][0]=="NIL":
                wr.writerow([term,"NIL",score])
            else:   
                wr.writerow([term,', '.join(codigo),score])
    else:
        wr = csv.writer(w,dialect='excel',delimiter="\t")
        wr.writerow(["parameter", "value"])
        for x in termdic:
            wr.writerow([x, termdic[x]])
    w.close()

def saveAnn(annpath, outpath, termcodes):
    annotation_content = list()
    #Load annotation, and save with new field.
    for linea,code in zip(csv.reader(open(annpath),dialect='excel',delimiter="\t"),termcodes):
        # Prepare code depending on the result (NIL, one term or list of terms)
        if isinstance(code[0][0],list):
            if len(code[0][0])==1:
                elemento = str(code[0][0][0])
            else:
                elemento = str("+".join(code[0][0]))
        else:
            elemento = str(code[0][0])

        linea += [elemento]
        annotation_content.append(linea)
    # Save to file
    w = open(outpath,"w")
    wr = csv.writer(w,dialect='excel',delimiter="\t")
    for x in annotation_content:
            wr.writerow(x)
    w.close()

def prepare_output_path(out_path, filename, is_single):
    if out_path[-1] != os.path.sep:
        out_path = out_path+os.path.sep
    # If folder don't exist, create it 
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    # Specify this to work with option -t ="1"
    if is_single:
        file_name = "output_norm"
    else:
        file_name = filename
    return out_path, file_name