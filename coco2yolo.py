
#############################################
# Script from @hwrenx and @ChriswooTalent   #
# Mail: hwrenx@gmail.com                    #
# ------------------------------------------#
# Usage:                                    #
#     Keep two scripts together with the    #
#     COCO data set and run this script.    #
#                                           #
#===========================================#
# Hopefully dir tree(finally):              #
#                                           #
# + HOMEDIR/                                #
# + - + annotations/                        #
#     + - + instances_train2017.json        #
#     |   + instances_val2017.json          #
#     + ImageSets/                          #
#     + - + labels/                         #
#     |   + - + train/                      #
#     |       + val/                        #
#     |       + train2017.txt               #
#     |       + val2017.txt                 #
#     + tarin2017/                          #
#     + test2017/                           #
#     + val2017/                            #
#     + coco.data                           #
#     + train.txt                           #
#     + test.txt                            #
#     + val.txt                             #
#                                           #
#############################################

import os
import subprocess
import sys
import shutil
from glob import glob

HOMEDIR      = os.path.dirname(os.path.realpath(__file__))
imgSet_dir   = "{}\\ImageSets".format(HOMEDIR)
labels_dir   = "{}\\labels".format(HOMEDIR)
anno_dir     = "{}\\annotations".format(HOMEDIR)
trainImg_dir = glob("{}\\train*".format(HOMEDIR))
testImg_dir  = glob("{}\\test*".format(HOMEDIR))
valImg_dir   = glob("{}\\val*".format(HOMEDIR))
train_anno   = glob("{}\\instances_train*.json".format(anno_dir))
val_anno     = glob("{}\\instances_val*.json".format(anno_dir))

def read_coco_data_json(anno_file):
    print "Read coco images data..."
    if not os.path.exists(anno_file):
        print "{} does not exist".format(anno_file)
    else:
        anno_name = os.path.splitext(anno_file)[0].split("_")[-1]
        out_dir = "{}\\{}".format(labels_dir, anno_name)
        imgset_file = "{}\\{}.txt".format(labels_dir, anno_name)
        print "Processing annotations:",os.path.splitext(anno_file)[0]
        cmd = "python {}\\split_annotation_foryolo.py --out-dir={} --imgset-file={} {}" \
                .format(HOMEDIR, out_dir, imgset_file, anno_file)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

def collect_coco_data():
    print "Copy coco images into single dir..."
    if not os.path.exists(imgSet_dir):
        os.makedirs(imgSet_dir)
    paths=[trainImg_dir, testImg_dir, valImg_dir]
    for ipath in paths:
        print ipath
        for root, dirs, files in os.walk(ipath[0]): 
            for tfile in files:
                shutil.copyfile(\
                    os.path.join(root, tfile),\
                    os.path.join(imgSet_dir,tfile))

def collect_coco_labels():
    print "Copy coco labels into single dir..."
    paths=glob("{}\\*".format(labels_dir))
    for ipath in paths:
        print ipath
        for root, dirs, files in os.walk(ipath):
            for tfile in files:
                shutil.copyfile(\
                    os.path.join(root, tfile),\
                    os.path.join(labels_dir,tfile))

def get_abs_path_txt(run_path, output_path, filename):
    print "Get abs path of each image...",run_path
    out_txt = output_path+"\\"+filename+".txt"
    fout = open(out_txt,'w')
    for root, dirs, files in os.walk(run_path):
        for tfile in files:
            if tfile.endswith(".jpg"):
                fout.write(root+"\\"+tfile+"\n")
    fout.close()

def make_coco_data():
    print "Writing coco.data..."
    coco_data=open(HOMEDIR+"\\"+"coco.data",'w')
    coco_data.write("\
classes= 80 \n\
train  = {}\\train.txt \n\
valid  = {}\\val.txt \n\
names  = cfg\\coco.names \n\
backup = backup \n\
eval=coco \
        ".format(HOMEDIR, HOMEDIR))

if __name__ == "__main__":
# Get txt-labels from json-annotations
    read_coco_data_json(val_anno[0])
    read_coco_data_json(train_anno[0])
# Move labels into single dir
    collect_coco_labels()
# Put all images and labels into single dir
    collect_coco_data()
# Get image path set
    get_abs_path_txt(valImg_dir[0],HOMEDIR,"val")
    get_abs_path_txt(testImg_dir[0],HOMEDIR,"test")
    get_abs_path_txt(trainImg_dir[0],HOMEDIR,"train")
# Make coco.data
    make_coco_data()
    print "Finished! please move the coco.data into darknet/cfg and make dir 'cfg/backup'"