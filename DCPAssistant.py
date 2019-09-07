from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image, ImageDraw
import os
import time
import psutil
import shutil
import subprocess as sp
from distutils.dir_util import copy_tree
from multiprocessing import Process,freeze_support
import math

def init_versions():
    global versions
    versions.clear()
    images.clear()
    photoImages.clear()
    imgpanels.clear()
    version_select_chkbtn_states.clear()
    vmarks.clear()
    try:
        versions = os.listdir(cwd + "/Working/DeepCreamPy")
        for v in versions:
            images.append(Image.open(cwd + "/Working/no_original.png"))
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
        start()
    else:
        for i in images:
            photoImages.append(ImageTk.PhotoImage(i))
        for p in photoImages:
            imgpanels.append(Label(window, image=p))
        for v in versions:
            version_select_chkbtn_states.append(IntVar())
            vmarks.append(Checkbutton(window, text=v, var=version_select_chkbtn_states[versions.index(v)])) # chk_state from config.txt
        for c in version_select_chkbtn_states:
            c.set(1)

def init_originals():
    originals_archive.clear()
    for of in originalfolders:
        try:
            originals_archive.extend(os.listdir(cwd + "/Archive/original/" + of + "/bar"))
        except:
            pass
        try:
            originals_archive.extend(os.listdir(cwd + "/Archive/original/" + of + "/mosaic"))
        except:
            pass
    if "Thumbs.db" in originals_archive:
        originals_archive.remove("Thumbs.db")
    originals_archive_mosaic.clear()
    try:
        inNames = os.listdir(cwd + "/Working/input")
        for of in originalfolders:
            originals_archive_mosaic.extend(os.listdir(cwd + "/Archive/original/" + of + "/mosaic"))
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    if "Thumbs.db" in originals_archive_mosaic:
        originals_archive_mosaic.remove("Thumbs.db")
    originals_working.clear()
    try:
        originals_working.extend(os.listdir(cwd + "/Working/original/bar"))
        originals_working.extend(os.listdir(cwd + "/Working/original/mosaic"))
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    if "Thumbs.db" in originals_working:
        originals_working.remove("Thumbs.db")
    originals_working_mosaic.clear()
    try:
        originals_working_mosaic.extend(os.listdir(cwd + "/Working/original/" + "/mosaic"))
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    if "Thumbs.db" in originals_working_mosaic:
        originals_working_mosaic.remove("Thumbs.db")

def init_directories():
    try:
        os.makedirs(cwd + "/Working/DeepCreamPy", 0o777, True)
        os.makedirs(cwd + "/Working/input", 0o777, True)
        os.makedirs(cwd + "/Working/current", 0o777, True)
        os.makedirs(cwd + "/Working/default_output", 0o777, True)
        os.makedirs(cwd + "/Working/original/bar", 0o777, True)
        os.makedirs(cwd + "/Working/original/mosaic", 0o777, True)
        os.makedirs(cwd + "/Archive/kept_pictures/" + dateS + "/bar", 0o777, True)
        os.makedirs(cwd + "/Archive/kept_pictures/" + dateS + "/mosaic", 0o777, True)
        os.makedirs(cwd + "/Archive/not_kept_pictures/" + dateS + "/bar", 0o777, True)
        os.makedirs(cwd + "/Archive/not_kept_pictures/" + dateS + "/mosaic", 0o777, True)
        os.makedirs(cwd + "/Archive/input/" + dateS + "/bar", 0o777, True)
        os.makedirs(cwd + "/Archive/input/" + dateS + "/mosaic", 0o777, True)
        os.makedirs(cwd + "/Archive/original/" + dateS + "/bar", 0o777, True)
        os.makedirs(cwd + "/Archive/original/" + dateS + "/mosaic", 0o777, True)
        os.makedirs(cwd + "/Archive/stats/" + dateS, 0o777, True)
        os.makedirs(cwd + "/Archive/not_selected/" + dateS + "/bar", 0o777, True)
        os.makedirs(cwd + "/Archive/not_selected/" + dateS + "/mosaic", 0o777, True)
        os.makedirs(cwd + "/Archive/manually_archived/" + dateS + "/bar", 0o777, True)
        os.makedirs(cwd + "/Archive/manually_archived/" + dateS + "/mosaic", 0o777, True)
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def decensorer(bar_or_mosaic, txtversions, cwd, originalfolders, dateS):
    mosaic_originals = []
    try:
        inNames = os.listdir(cwd + "/Working/input")
        for of in originalfolders:
            mosaic_originals.extend(os.listdir(cwd + "/Archive/original/" + of + "/mosaic"))
        mosaic_originals.extend(os.listdir(cwd + "/Working/original/" + "/mosaic"))
    except Exception as e:
        print(e)

    if len(inNames) == 0:
        print("ERROR: No pictures were found in input")
        print("Exiting")
        time.sleep(5)
        exit()

    if len(txtversions) == 0:
        print("ERROR: No versions of DeepCreamPy were found")
        print("Exiting")
        time.sleep(5)
        exit()
    try:
        for n in os.listdir(cwd + "/Working/input"):
            if not n.endswith(".png") and not n.endswith(".db"):
                print("Only png files can be decensored, please remove all non png files from the input folder")
                print("Exiting")
                time.sleep(5)
                exit()
    except Exception as e:
        print(e)
        exit()

    try:
        for n in mosaic_originals:
            if not n.endswith(".png") and not n.endswith(".db"):
                print("Only png files can be taken as originals, please remove all non png files from the original mosaic folders")
                print("Exiting")
                time.sleep(5)
                exit()
    except Exception as e:
        print(e)
        exit()

    #temp.py goes here if this doesn't work

    print("Moving pictures from input into 'Working/current' directory")
    # for all images in input
    for name in inNames: 
        try:
            # move them to current if they have no original
            if bar_or_mosaic == 1:
                if name not in mosaic_originals:
                    shutil.move(cwd + "/Working/input/" + name, cwd + "/Working/current")
            # move them to current if they have an original
            elif bar_or_mosaic == 2:
                if name in mosaic_originals:
                    shutil.move(cwd + "/Working/input/" + name, cwd + "/Working/current")
        except Exception as e:
            print(e)
            exit()

    print("Moved pictures to 'Working/current' successfully")

    try:
        current = os.listdir(cwd + "/Working/current")
    except Exception as e:
        print(e)
        exit()

    print("Copying input from current into the decensor_input folders")
    if len(current) > 0:
        for dcp in txtversions:
            input = cwd + "/Working/DeepCreamPy/" + dcp + "/decensor_input"
            original_input =  cwd + "/Working/DeepCreamPy/" + dcp + "/decensor_input_original"
            try:
                for c in current:
                        # os.symlink(cwd + "/Working/current/" + c, input)
                        shutil.copy(cwd + "/Working/current/" + c, input)
                if bar_or_mosaic == 2:
                    # look for the original in Working and copy to d_in_original
                    if name in (os.listdir(cwd + "/Working/original/mosaic")):
                        # os.symlink(cwd + "/Working/original/mosaic/" + name, original_input)
                        shutil.copy(cwd + "/Working/original/mosaic/" + name, original_input)
                    else:
                    # look for the original in Archive and copy to d_in_original
                        for of in originalfolders:
                            if name in os.listdir(cwd + "/Archive/original/" + of + "/mosaic"):
                                # os.symlink(cwd + "/Archive/original/" + of + "/mosaic/" + name, original_input)
                                shutil.copy(cwd + "/Archive/original/" + of + "/mosaic/" + name, original_input)
            except Exception as e:
                print(e)
                exit()
    else:
        print("No pictures to decensor were found")
        print("Exiting")
        exit()
    print("Copied images successfully")
            
    # temp.py ends here

    # decensor them parallel:

    for dcp in txtversions:
        try:
            os.chdir(cwd + "\Working\DeepCreamPy\\" + dcp)
            print("Starting " + dcp)
            if bar_or_mosaic == 1:
                sp.run("START /MIN decensor.exe", shell=True)
            elif bar_or_mosaic == 2:
                sp.run("START /B decensor_mosaic.bat", shell=True)
        except Exception as e:
            print(e)
            exit()
    
    os.chdir(cwd)
    # Wait until a decensor process has started
    while "decensor.exe" not in (p.name() for p in psutil.process_iter()):
        #time.sleep(1)
        pass
    t = time.perf_counter()
    print("Waiting for decensoring to finish")
    # Wait until all decensor process have finished
    while "decensor.exe" in (p.name() for p in psutil.process_iter()):
        tt = time.perf_counter()
        if tt - t > 60:
            print("Waiting for decensoring to finish")
            t = time.perf_counter()

    print("Removing inputs from DCPs")
    for dcp in txtversions:
        folder = cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_input"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        folder = cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_input_original"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    print("Finished")
    # exit()

def decensor():
    global bar_or_mosaic
    global process
    global txtversions
    global cwd
    global originalfolders
    global dateS
    if __name__ == '__main__':
        if bar_or_mosaic == 2:
            for v in versions:
                b = open(cwd + "/Working/DeepCreamPy/" + v + "/decensor_mosaic.bat", "w")
                b.write("start /MIN \"decensor.exe\" \"decensor.exe\" --is_mosaic=True")
                b.close()
        process = Process(target=decensorer, args=(bar_or_mosaic, txtversions, cwd, originalfolders, dateS,))
        process.start()

def finish():
    global kept_ones_var
    global not_kept_ones_var
    global input_var
    global originals_var
    global stats_var
    global not_selected_var
    global manual_archive_var
    global sum_all

    if input_var.get() == 1:
        try:
            if bar_or_mosaic == 1:
                os.makedirs(cwd + "/Archive/input/" + dateS + "/bar", 0o777, True)
                copy_tree(cwd + "/Working/current", cwd + "/Archive/input/" + dateS + "/bar")
            elif bar_or_mosaic == 2:
                os.makedirs(cwd + "/Archive/input/" + dateS + "/mosaic", 0o777, True)
                copy_tree(cwd + "/Working/current", cwd + "/Archive/input/" + dateS + "/mosaic")
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)

    if not_selected_var.get() == 1:
        try:
            cur = os.listdir(cwd + "/Working/current")
            for im in not_selected_images:
                if bar_or_mosaic == 1:
                    shutil.copy(cwd + "/Working/current/" + im, cwd + "/Archive/not_selected/" + dateS + "/bar")
                elif bar_or_mosaic == 2:
                    shutil.copy(cwd + "/Working/current/" + im, cwd + "/Archive/not_selected/" + dateS + "/mosaic")
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)

    folder = cwd + "/Working/current"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    if stats_var.get() == 1:
        try:
            os.makedirs(cwd + "/Archive/stats/" + dateS, 0o777, True)
            stats_archive = "STATS:\nDate: " + dateS + "\n" + "Decensored: " + str(inlen) + "\nKept from version:\n"
            clcounter = 0
            for t in txtversions:
                stats_archive = stats_archive + t + ": " + str(len(chosen_list[clcounter])) + "\n"
                clcounter += 1
            stats_archive = stats_archive + "Kept from all versions: " + str(sum_all)
            stats_archive = stats_archive + "\nTime each version took (hrs:min:sec):\n"
            clcounter = 0
            for t in txtversions:
                stats_archive = stats_archive + t + ": " + timers[clcounter]['text'] + "\n"
                clcounter += 1
            
            newfile = time.strftime(cwd + "/Archive/stats/" + dateS + "/" + dateS + " %H-%M.txt")
            f = open(newfile, "x")
            f.write(stats_archive)
            f.close()
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)

    if manual_archive_var.get() == 1:
        for ma in range(0,len(manual_archive)):
            nr = txtversions[ma]
            temp = nr.index("y_")
            temp2 = nr.index("-")
            nr = nr[temp + 2:temp2]
            for img in manual_archive[ma]:
                if bar_or_mosaic == 1:
                    try:
                        shutil.copy(cwd + "/Working/DeepCreamPy/" + txtversions[ma] + "/decensor_output/" + img, cwd + "/Archive/manually_archived/" + dateS + "/bar")
                        os.rename(cwd + "/Archive/manually_archived/" + dateS + "/bar/" + img, cwd + "/Archive/manually_archived/" + dateS + "/bar/" + img.replace(".png", "-" + nr + ".png"))
                    except Exception as e:
                        print(e)
                        mb.showerror("ERROR", e)
                elif bar_or_mosaic == 2:
                    try:
                        shutil.copy(cwd + "/Working/DeepCreamPy/" + txtversions[ma] + "/decensor_output/" + img, cwd + "/Archive/manually_archived/" + dateS + "/mosaic")
                        os.rename(cwd + "/Archive/manually_archived/" + dateS + "/mosaic/" + img, cwd + "/Archive/manually_archived/" + dateS + "/mosaic/" + img.replace(".png", "-" + nr + ".png"))
                    except Exception as e:
                        print(e)
                        mb.showerror("ERROR", e)

    try:
        f = open(cwd + "/Working/config.txt")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
        f = open(cwd + "/Working/config.txt", "x")
        f.write("output_path=" + cwd + "/Working/default_output")
    path = f.readline()
    path = path[path.index("=")+1:]
    for cl in range(0, len(chosen_list)):
        nr = txtversions[cl]
        temp = nr.index("y_")
        temp2 = nr.index("-")
        nr = nr[temp + 2:temp2]
        for k in chosen_list[cl]:
            if kept_ones_var.get() == 1:
                if bar_or_mosaic == 1:
                    try:
                        shutil.copy(cwd + "/Working/DeepCreamPy/" + txtversions[cl] + "/decensor_output/" + k, cwd + "/Archive/kept_pictures/" + dateS + "/bar")
                        os.rename(cwd + "/Archive/kept_pictures/" + dateS + "/bar/" + k, cwd + "/Archive/kept_pictures/" + dateS + "/bar/" + k.replace(".png", "-" + nr + ".png"))
                    except Exception as e:
                        print(e)
                        mb.showerror("ERROR", e)
                elif bar_or_mosaic == 2:
                    try:
                        shutil.copy(cwd + "/Working/DeepCreamPy/" + txtversions[cl] + "/decensor_output/" + k, cwd + "/Archive/kept_pictures/" + dateS + "/mosaic")
                        os.rename(cwd + "/Archive/kept_pictures/" + dateS + "/mosaic/" + k, cwd + "/Archive/kept_pictures/" + dateS + "/mosaic/" + k.replace(".png", "-" + nr + ".png"))
                    except Exception as e:
                        print(e)
                        mb.showerror("ERROR", e)
            try:
                os.rename(cwd + "/Working/DeepCreamPy/" + txtversions[cl] + "/decensor_output/" + k, path + "/" + k.replace(".png", "-" + nr + ".png"))
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)

    if not_kept_ones_var.get() == 1:
        for cl in range(0, len(txtversions)):
            nr = txtversions[cl]
            temp = nr.index("y_")
            temp2 = nr.index("-")
            nr = nr[temp + 2:temp2]
            try:
                for k in os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[cl] + "/decensor_output"):
                    if k not in chosen_list[cl]:
                        if bar_or_mosaic == 1:
                            try:
                                os.rename(cwd + "/Working/DeepCreamPy/" + txtversions[cl] + "/decensor_output/" + k, cwd + "/Archive/not_kept_pictures/" + dateS + "/bar/" + k.replace(".png", "-" + nr + ".png"))
                            except Exception as e:
                                print(e)
                                mb.showerror("ERROR", e)
                        elif bar_or_mosaic == 2:
                            try:
                                os.rename(cwd + "/Working/DeepCreamPy/" + txtversions[cl] + "/decensor_output/" + k, cwd + "/Archive/not_kept_pictures/" + dateS + "/mosaic/" + k.replace(".png", "-" + nr + ".png"))
                            except Exception as e:
                                print(e)
                                mb.showerror("ERROR", e)
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)

    for dcp in versions:
        folder = cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_output"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    if originals_var.get() == 1:
        try:
            if bar_or_mosaic == 1:
                os.makedirs(cwd + "/Archive/original/" + dateS + "/bar", 0o777, True)
                copy_tree(cwd + "/Working/original/bar", cwd + "/Archive/original/" + dateS + "/bar")
            elif bar_or_mosaic == 2:
                os.makedirs(cwd + "/Archive/original/" + dateS + "/mosaic", 0o777, True)
                copy_tree(cwd + "/Working/original/mosaic", cwd + "/Archive/original/" + dateS + "/mosaic")
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
    if bar_or_mosaic == 1:
        folder = cwd + "/Working/original/bar"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    elif bar_or_mosaic == 2:
        folder = cwd + "/Working/original/mosaic"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    finish="Moved selected pictures in the output folder"
    mb.showinfo("Finished", finish)
    start()

def stats():
    global iterator_output_images
    global bar_or_mosaic
    global original_panel
    global inlen
    global sum_all
    

    keep_vars_flag = False # True if at least one keep_vars is 1

    # Save last selection
    for k in range(0, len(keep_vars)):
        if keep_vars[k].get() == 1:
            keep_vars_last[iterator_output_images-1][k] = True
        else:
            keep_vars_last[iterator_output_images-1][k] = False
        if manual_archive_vars[k].get() == 1:
            manual_archive_vars_last[iterator_output_images-1][k] = True
        else:
            manual_archive_vars_last[iterator_output_images-1][k] = False

    # Add all chosen images to the right lists
    for x in range(0,len(txtversions)):
        chosen_list[x].clear()
        manual_archive[x].clear()
    for k in range(0,inlen):
        for x in range(0,len(txtversions)):
            try:
                img = os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[x] + "/decensor_output")[k]
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
            if keep_vars_last[k][x]:
                keep_vars_flag = True
                chosen_list[x].append(img)
            if manual_archive_vars_last[k][x]:
                manual_archive[x].append(img)
        if not keep_vars_flag:
            try:
                not_selected_images.append(os.listdir(cwd + "/Working/current")[k])
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
        keep_vars_flag = False
    
    # Forget c_manual/c_all stuff
    c_manual.grid_forget()
    c_all.grid_forget()
    c_stats.grid_forget()
    
    for p in imgpanels:
        p.grid_forget()
    for kb in keep_boxes:
        kb.grid_forget()
    for mab in manual_archive_boxes:
        mab.grid_forget()
    # original_panel.grid(column = 2, row = 0) # TODO ? Warum ist das hier
    original_panel.grid_forget()
    original_lbl.grid_forget()
    image_count_lbl.grid_forget()

    window.grid_columnconfigure(0, weight=0)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=1)
    window.grid_columnconfigure(4, weight=1)
    window.grid_columnconfigure(5, weight=1)
    window.grid_columnconfigure(6, weight=0)
    window.grid_columnconfigure(7, weight=0)
    window.grid_columnconfigure(8, weight=0)

    # Display Archive-related stuff
    archive_column = 4
    archive_lbl.grid(column = archive_column, row = 0, sticky=W, columnspan=2)
    archive_warning_lbl.grid(column = archive_column, row = 1, sticky=W, columnspan=2)
    kept_ones_chkbtn.grid(column = archive_column, row = 2, sticky=W, columnspan=2)
    not_kept_ones_chkbtn.grid(column = archive_column, row = 3, sticky=W, columnspan=2)
    input_chkbtn.grid(column = archive_column, row = 4, sticky=W, columnspan=2)
    originals_chkbtn.grid(column = archive_column, row = 5, sticky=W, columnspan=2)
    stats_chkbtn.grid(column = archive_column, row = 6, sticky=W, columnspan=2)
    not_selected_chkbtn.grid(column = archive_column, row = 7, sticky=W, columnspan=2)
    manual_archive_chkbtn.grid(column = archive_column, row = 8, sticky=W, columnspan=2)

    stats_lbl.grid(column=0, row=0, sticky=W)
    decensored_lbl.grid(column=0, row=1, sticky=W)
    ccounter = 3

    # Display name of chosen versions
    for c in cversions:
        c.grid(column=0, row=ccounter, sticky=W)
        ccounter += 1
    ccounter -= len(cversions)
    clcounter = 0

    # Display number of chosen images per version 
    for cl in chosen_lbls:
        cl.configure(text = str(len(chosen_list[clcounter])))
        cl.grid(column=1, row=ccounter)
        ccounter += 1
        clcounter += 1
    cfromall_lbl.grid(column=0, row=ccounter, sticky=W)
    sum_all = 0
    for cl in chosen_list:
        sum_all += len(cl)
    cfromallnum_lbl.configure(text = str(sum_all))
    cfromallnum_lbl.grid(column=1, row=ccounter)
    ccounter -= len(cversions)

    # Display time each version took
    for t in timers:
        t.grid(column=2, row=ccounter)
        ccounter += 1

    finish_btn.grid(column=4, row=9, sticky=W)
    c_back_btn.grid(column=0, row=ccounter+1, sticky=W)
    decensorednum_lbl.configure(text = inlen)
    decensorednum_lbl.grid(column=1, row=1)
    chosen_text_lbl.grid(column=1, row=2, padx=10)
    time_text_lbl.grid(column=2, row=2)
    iterator_output_images += 1
    
def version_select():
    global bar_or_mosaic
    if bar_or_mosaic == 1:
        bar_lbl.grid(column=0, row=0, columnspan=2)
    elif bar_or_mosaic == 2:
        mosaic_lbl.grid(column=0, row=0, columnspan=2)
    counter = 1
    for vm in vmarks:
        vm.grid(column=0, row=counter, columnspan=2)
        counter += 1
    back.grid(column=0, row=counter, sticky=E)
    next_versions.grid(column=1, row=counter, sticky=W)

def resize(original_string):
    global width
    global height
    global original_img
    global images
    all_img_width = 0
    oldwidth = images[0].width
    oldheight = images[0].height
    for i in images:
        all_img_width += i.width
    all_img_width += images[0].width
    if all_img_width > width:
        newwidth = round(width/(len(txtversions)+1))
        newheight = round(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        for i in range(0,len(images)):
            images[i] = images[i].resize(newsize, Image.ANTIALIAS)
        original_img = original_img.resize(newsize, Image.ANTIALIAS)
    if images[0].height > height-180:
        newheight = height - 180
        newwidth = round(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        for i in range(0,len(images)):
            images[i] = images[i].resize(newsize, Image.ANTIALIAS)
        original_img = original_img.resize(newsize, Image.ANTIALIAS)
    portray(original_string)

def portray(original_string):
    global original_panel
    global original_img
    global original_photoimg
    original_photoimg = ImageTk.PhotoImage(original_img)
    original_panel = Label(window, image = original_photoimg)
    original_panel.grid(column=0, row=4, columnspan=3)

    for t in range(0,len(txtversions)):
        photoImages[t] = ImageTk.PhotoImage(images[t])
        imgpanels[t].configure(image = photoImages[t])
        imgpanels[t].grid(column=t+3 , row=4)

def c_man_both():
    global iterator_output_images
    global inlen
    global original_img
    global bar_or_mosaic
    global output_list

    # If we have one image left to decide for
    if iterator_output_images >= inlen-1:
        c_next.grid_forget()
        c_stats.grid(column=2, row=0, sticky=W)
    else:
        c_stats.grid_forget()
        c_next.grid(column=2, row=0, sticky=W)
    if iterator_output_images > 0:
        c_back_btn.grid(column=0, row=0, sticky=E)

    image_count_lbl.configure(text= "Image " + str(iterator_output_images + 1) + " of " + str(inlen))
    # Get all decensored images from output
    for t in range(0,len(txtversions)):
        try:
            #if bar_or_mosaic == 1:
            images[t] = Image.open(cwd + "/Working/DeepCreamPy/" + txtversions[t] + "/decensor_output/" + output_list[iterator_output_images])
            # elif bar_or_mosaic == 2:
        except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
        
    original_string = output_list[iterator_output_images]
    
    # Find original image in working
    if original_string in originals_working:
        try:
            if original_string in os.listdir(cwd + "/Working/original/bar"):
                original_img = Image.open(cwd + "/Working/original/bar/" + original_string)
            if original_string in os.listdir(cwd + "/Working/original/mosaic"):
                original_img = Image.open(cwd + "/Working/original/mosaic/" + original_string)
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
    # Or find original image in archive
    elif original_string in originals_archive:
        try:
            datis = os.listdir(cwd + "/Archive/original")
            for x in range(0, len(datis)):
                oslis = os.listdir(cwd + "/Archive/original/" + datis[x])
                for y in range(0,len(oslis)):
                    if original_string in os.listdir(cwd + "/Archive/original/" + datis[x] + "/"  + oslis[y]):
                        original_img = Image.open(cwd + "/Archive/original/" + datis[x] + "/" + oslis[y] + "/" + original_string)
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
    # Or no original could be found
    else:
        try:
            original_img = Image.open(cwd + "/Working/no_original.png")
        except Exception as e:
                print(e)
                mb.showerror("ERROR", e)

    resize(original_string)
    iterator_output_images += 1

def c_manual():
    global output_list
    global inlen

    # Initialize all checkboxes, the chosen_list and their labels
    for t in txtversions:
        chosen_list.append(list())
        keep_vars.append(IntVar())
        keep_boxes.append(Checkbutton(window, text="Keep", var=keep_vars[txtversions.index(t)]))
        manual_archive_vars.append(IntVar())
        manual_archive_boxes.append(Checkbutton(window, text="Archive manually", var=manual_archive_vars[txtversions.index(t)]))
        manual_archive.append(list())
        chosen_lbls.append(Label(window, text = ""))
    
    # Initialize memory for all keep_vars
    for l in range(0,inlen):
        keep_vars_last.append(list())
        manual_archive_vars_last.append(list())
        for t in range(0,len(txtversions)):
            keep_vars_last[l].append(False)
            manual_archive_vars_last[l].append(False)


    image_count_lbl.configure(text= "Image 1 of " + str(inlen))
    image_count_lbl.grid(column=1, row=0)
    # Put checkboxes on screen
    kbcounter = 3
    for kb in keep_boxes:
        kb.grid(column=kbcounter, row=2)
        kbcounter += 1
    mabcounter = 3
    for mab in manual_archive_boxes:
        mab.grid(column=mabcounter, row=3)
        mabcounter += 1
    
    # Forget old shit
    c_all.grid_forget()
    c_manual.grid_forget()

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=1)
    window.grid_columnconfigure(4, weight=1)
    window.grid_columnconfigure(5, weight=1)
    window.grid_columnconfigure(6, weight=1)
    window.grid_columnconfigure(7, weight=1)
    window.grid_columnconfigure(8, weight=1)

    original_lbl.grid(column=1, row=1)
    counter = 3
    for c in cversions:
        c.grid_forget()
        c.grid(column=counter, row=1)
        counter += 1

    # Get output lists
    try:
        output_list = os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[0] + "/decensor_output")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

    c_man_both()

def c_man_update():
    global iterator_output_images
    global original_panel

    original_panel.grid_forget()

    # Save last selection
    for k in range(0, len(keep_vars)):
        if keep_vars[k].get() == 1:
            keep_vars_last[iterator_output_images-1][k] = True
        else:
            keep_vars_last[iterator_output_images-1][k] = False
        if manual_archive_vars[k].get() == 1:
            manual_archive_vars_last[iterator_output_images-1][k] = True
        else:
            manual_archive_vars_last[iterator_output_images-1][k] = False

    # Reset all checkboxes
    for kv in range(0,len(keep_vars)):
        keep_vars[kv].set(keep_vars_last[iterator_output_images][kv])
        manual_archive_vars[kv].set(manual_archive_vars_last[iterator_output_images][kv])
    c_man_both()
    
def c_man_back():
    global iterator_output_images
    global original_panel
    global inlen

    # Forget Stats
    stats_lbl.grid_forget()
    decensored_lbl.grid_forget()
    cfromall_lbl.grid_forget()
    finish_btn.grid_forget()
    chosen_text_lbl.grid_forget()
    time_text_lbl.grid_forget()
    counter = 3
    for c in cversions:
        c.grid_forget()
        c.grid(column=counter, row=1)
        counter += 1
    cfromallnum_lbl.grid_forget()
    decensorednum_lbl.grid_forget()
    for t in timers:
        t.grid_forget()
    for cl in chosen_lbls:
        cl.grid_forget()

    # Forget Archive
    archive_lbl.grid_forget()
    archive_warning_lbl.grid_forget()
    kept_ones_chkbtn.grid_forget()
    not_kept_ones_chkbtn.grid_forget()
    input_chkbtn.grid_forget()
    originals_chkbtn.grid_forget()
    stats_chkbtn.grid_forget()
    not_selected_chkbtn.grid_forget()
    manual_archive_chkbtn.grid_forget()

    original_panel.grid_forget()

    kbcounter = 3
    for kb in keep_boxes:
        kb.grid(column=kbcounter, row=2)
        kbcounter += 1
    mabcounter = 3
    for mab in manual_archive_boxes:
        mab.grid(column=mabcounter, row=3)
        mabcounter += 1
    
    image_count_lbl.grid(column=1, row=0)
    original_lbl.grid(column=1, row=1)
    iterator_output_images -= 2

    # Save all boxes from last screen
    if iterator_output_images < (inlen-1):
        for k in range(0, len(keep_vars)):
            if keep_vars[k].get() == 1:
                keep_vars_last[iterator_output_images+1][k] = True
            else:
                keep_vars_last[iterator_output_images+1][k] = False
            if manual_archive_vars[k].get() == 1:
                manual_archive_vars_last[iterator_output_images+1][k] = True
            else:
                manual_archive_vars_last[iterator_output_images+1][k] = False

    for kv in range(0,len(keep_vars)):
        keep_vars[kv].set(keep_vars_last[iterator_output_images][kv])
        manual_archive_vars[kv].set(manual_archive_vars_last[iterator_output_images][kv])

    
    if iterator_output_images == 0:
        c_back_btn.grid_forget()

    c_man_both()

def c_all():
    global bar_or_mosaic

    for t in txtversions:
        chosen_list.append(list())
        chosen_lbls.append(Label(window, text = ""))
    for k in range(0, len(txtversions)):
        try:
            chosen_list[k].extend(os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[k] + "/decensor_output"))
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
    stats()

def choose_screen():
    for p in range(0,len(pbars)):
        pbars[p].grid_forget()
        pnums[p].grid_forget()
        timers[p].grid_forget()
    for t in cversions:
        t.grid_forget()
    progress_lbl.grid_forget()

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=0)
    window.grid_columnconfigure(4, weight=0)
    window.grid_columnconfigure(5, weight=0)
    window.grid_columnconfigure(6, weight=0)
    window.grid_columnconfigure(7, weight=0)
    window.grid_columnconfigure(8, weight=0)
    c_manual.grid(column=0, row=0)
    c_all.grid(column=0, row=1)

def progress_update():
    global inlen
    global timer_start

    # Update every progessbar/-number
    for p in range(0,len(pbars)):
        try:
            new_value = min(inlen, len(os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[p] + "/decensor_output")))
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
        if pbars[p]['value'] < new_value:
            pbars[p]['value'] = new_value
            number = str(pbars[p]['value'])
            if number.endswith(".0"):
                number = number[:-2]
            pnums[p].configure(text = number + "/" + str(inlen))
        
        # Update timer
        if pbars[p]['value'] != inlen:
            tt = (round(time.perf_counter()) - timer_start)
            hours = max(int(math.ceil((tt+1)/60/60))-1,0)
            if hours < 10:
                hours_str = "0" + str(hours)
            else:
                hours_str = str(hours)
            minutes = max(int(math.ceil((tt+1)/60))-1,0)
            if minutes < 10:
                minutes_str = "0" + str(minutes)
            else:
                minutes_str = str(minutes)
            seconds = (tt)%60
            if seconds < 10:
                seconds_str = "0" + str(seconds)
            else:
                seconds_str = str(seconds)
            timers[p].configure(text=hours_str + ":" + minutes_str + ":" + seconds_str)

    pmax = 0
    for p in pbars:
        if p['value'] == inlen:
            pmax += 1

    if pmax != len(pbars):        
        window.after(100, progress_update)
    else:
        process.join()
        choose_screen()

def progress_check():
    global txtversions
    global inlen
    global timer_start
    
    pbarcounter = 0
    counter = 0
    timer_start = round(time.perf_counter())

    # Intitialise right amount of progressbars, progressnumbers and timecounters
    for t in txtversions:
        pbars.append(Progressbar(window, length= 200, mode= 'determinate', max = inlen))
        pnums.append(Label(window, text = "0/" + str(inlen)))
        timers.append(Label(window, text = "00:00"))
        pbarcounter += 1
        cversions.append(Label(window, text=t))
        cversions[pbarcounter-1].grid(column=0, row=pbarcounter, sticky=E, padx=10)

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=0)
    window.grid_columnconfigure(4, weight=0)
    window.grid_columnconfigure(5, weight=0)
    window.grid_columnconfigure(6, weight=0)
    window.grid_columnconfigure(7, weight=0)
    window.grid_columnconfigure(8, weight=0)

    progress_lbl.grid(column=1, row=0)
    if len(pbars) != 0:
        for p in range(0,len(pbars)):
            counter += 1
            pbars[p].grid(column=1, row=counter)
            pnums[p].grid(column=1, row=counter)
            timers[p].grid(column=2, row=counter, sticky=W, padx=10)

        progress_update()
    else:
        start()

def progress():
    global txtversions
    global inlen
    init_originals()
    no_versions_selected_flag = True # True if no versions were selected
    no_input_flag = False # True if no input images were found
    no_originals_flag = False # True if no mosaic originals were found in the Archive or Working directories
    temp_flag = False # True if at least one original image exists
    one_or_more_original_flag = False # True if at least one original image exists which matches names with an input image
    not_png_flag = False # True if not all images are pngs
    original_not_png_flag = False # True if not all original images are pngs
    try:
        if len(os.listdir(cwd + "/Working/input")) == 0:
            no_input_flag = True
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    
    if bar_or_mosaic == 2:
        try:
            if len(os.listdir(cwd + "/Working/original/mosaic")) == 0:
                for l in os.listdir(cwd + "/Archive/original/"):
                    if "mosaic" in os.listdir(cwd + "/Archive/original/" + l):
                        if (len(os.listdir(cwd + "/Archive/original/" + l + "/mosaic")) > 0):
                            temp_flag = True
                            break
                if not temp_flag:
                    no_originals_flag = True
            for n in os.listdir(cwd + "/Working/input"):
                if n in originals_archive_mosaic or n in originals_working_mosaic:
                    one_or_more_original_flag = True
                    break
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
    elif bar_or_mosaic == 1:
        one_or_more_original_flag = True

    for c in range(0, len(version_select_chkbtn_states)):
        if version_select_chkbtn_states[c].get() == 1:
            no_versions_selected_flag = False
            break

    try:
        for n in os.listdir(cwd + "/Working/input"):
            if not n.endswith(".png") and not n.endswith(".db"):
                not_png_flag = True
                break
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

    init_originals()

    for n in originals_archive:
        if not n.endswith(".png") and not n.endswith(".db"):
            original_not_png_flag = True
            break
    for n in originals_working:
        if not n.endswith(".png") and not n.endswith(".db"):
            original_not_png_flag = True
            break
    if not no_versions_selected_flag and not no_input_flag and not no_originals_flag and one_or_more_original_flag and not not_png_flag and not original_not_png_flag:
        for vm in vmarks:
            vm.grid_forget()
        bar_lbl.grid_forget()
        mosaic_lbl.grid_forget()
        back.grid_forget()
        next_versions.grid_forget()
        
        # for all images in input
        try:
            for name in os.listdir(cwd + "/Working/input"):
                if bar_or_mosaic == 1:
                    # count bar 1 up if they have no original
                    if name not in originals_archive_mosaic and name not in originals_working_mosaic:
                        inlen += 1
                elif bar_or_mosaic == 2:
                    # count mosaic 1 up if they have an original
                    if name in originals_archive_mosaic or name in originals_working_mosaic:
                        inlen += 1
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
        if len(txtversions) == 0:
            for c in range(0, len(version_select_chkbtn_states)):
                    if version_select_chkbtn_states[c].get() == 1:
                        txtversions.append(versions[c])
            decensor()
        progress_check()

    elif no_versions_selected_flag:
        mb.showerror("ERROR", "Please select at least one version!")
    elif no_input_flag:
        mb.showerror("ERROR", "Please input images to decensor!")
    elif not_png_flag:
        mb.showerror("ERROR", "Only png files can be decensored, please remove all non png files from the 'Working/input' directory")
    elif original_not_png_flag:
        mb.showerror("ERROR", "Only png files can be taken as originals, please remove all non-png files from the 'Working/original' and the 'Archive/original' directories, accessible through the 'Open original' and 'Open Archive' button respectively")
    elif no_originals_flag:
        mb.showerror("ERROR", "Please put original images in the 'Working/original' directory if you want to decensor mosaic images!")
    elif not one_or_more_original_flag:
        mb.showerror("ERROR", "Please put original images matching your input images in name in the 'Working/original' directory if you want to decensor mosaic images!")

def open_archive():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        os.startfile(cwd + "/Archive")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    
def open_input():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        os.startfile(cwd + "/Working/input")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    
def open_original():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        os.startfile(cwd + "/Working/original")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    
def open_dcp():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        os.startfile(cwd + "/Working/DeepCreamPy")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def tutorial():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        os.startfile(cwd + "/Working/How_To.txt")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def set_output():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    
    try:
        f = open(cwd + "/Working/config.txt")
        prev_path = f.read()
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    try:
        f = open(cwd + "/Working/config.txt", "w")
        path = "output_path=" + askdirectory(title='Please select a directory to save the output in')
        if path != "output_path=":
            f.write(path)
            f.close()
            output_lbl.grid(column=1, row=7)
        else:
            f.write(prev_path)
            f.close()
            no_output_lbl.grid(column=1, row=7)
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    
def open_output():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        f = open(cwd + "/Working/config.txt")
        path = f.readline()
        path = path[path.index("=")+1:]
        os.startfile(path)
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def both_dec():
    dcp_flag = False

    init_versions()

    if len(versions) == 0:
        dcp_flag = True

    if dcp_flag:
        mb.showerror("ERROR", "Please put at least one version of DeepCreamPy into the 'DeepCreamPy' folder,\naccessible through the 'Open DCP-versions' button")
    else:
        output_lbl.grid_forget()
        no_output_lbl.grid_forget()
        lbl.grid_forget()
        btn0.grid_forget()
        btn1.grid_forget()
        btn2.grid_forget()
        btn3.grid_forget()
        btn4.grid_forget()
        btn5.grid_forget()
        btn55.grid_forget()
        btn6.grid_forget()
        btn7.grid_forget()
        btn8.grid_forget()
        version_lbl.grid_forget()
        github_lbl.grid_forget()
        twitter_lbl.grid_forget()
    
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=0)
    window.grid_columnconfigure(4, weight=0)
    window.grid_columnconfigure(5, weight=0)
    window.grid_columnconfigure(6, weight=0)
    window.grid_columnconfigure(7, weight=0)
    window.grid_columnconfigure(8, weight=0)

def bar_dec():
    global bar_or_mosaic
    both_dec()
    bar_or_mosaic = 1
    version_select()

def mosaic_dec():
    global bar_or_mosaic
    both_dec()
    bar_or_mosaic = 2
    version_select()

def configs():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        os.startfile(cwd + "/Working/config.txt")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def start():
    global iterator_output_images
    global original_panel
    global cwd
    global inlen
    global bar_or_mosaic

    original_panel.grid_forget()
    stats_lbl.grid_forget()
    decensored_lbl.grid_forget()
    cfromall_lbl.grid_forget()
    finish_btn.grid_forget()
    for c in cversions:
        c.grid_forget()
    cfromallnum_lbl.grid_forget()
    decensorednum_lbl.grid_forget()
    c_manual.grid_forget()
    c_all.grid_forget()
    progress_lbl.grid_forget()
    for cl in chosen_lbls:
        cl.grid_forget()
    for vm in vmarks:
        vm.grid_forget()
    back.grid_forget()
    next_versions.grid_forget()
    bar_lbl.grid_forget()
    mosaic_lbl.grid_forget()
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    archive_lbl.grid_forget()
    archive_warning_lbl.grid_forget()
    kept_ones_chkbtn.grid_forget()
    not_kept_ones_chkbtn.grid_forget()
    input_chkbtn.grid_forget()
    originals_chkbtn.grid_forget()
    stats_chkbtn.grid_forget()
    not_selected_chkbtn.grid_forget()
    c_back_btn.grid_forget()
    manual_archive_chkbtn.grid_forget()
    for t in timers:
        t.grid_forget()
    for p in pbars:
        p.grid_forget()
    for p in pnums:
        p.grid_forget()
    for t in cversions:
        t.grid_forget()
    chosen_text_lbl.grid_forget()
    time_text_lbl.grid_forget()

    pbars.clear()
    cversions.clear()
    txtversions.clear()
    pnums.clear()
    chosen_list.clear()
    keep_boxes.clear()
    keep_vars.clear()
    keep_vars_last.clear()
    chosen_lbls.clear()
    chosen_list.clear()
    not_selected_images.clear()
    manual_archive.clear()
    manual_archive_boxes.clear()
    manual_archive_vars.clear()
    manual_archive_vars_last.clear()
    timers.clear()

    iterator_output_images = 0
    bar_or_mosaic = 0
    inlen = 0

    init_directories()
    init_versions()

    # Move images from current to input
    folder = cwd + "/Working/current"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                shutil.move(file_path, cwd + "/Working/input")
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    # Delete leftovers from DCPs
    for dcp in versions:
        folder = cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_input"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        folder = cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_input_original"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        
        # Delete leftovers from output and move them to error_output
        try:
            if len(os.listdir(cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_output")) > 0:
                os.makedirs(cwd + "/Working/error_output/" + dcp, 0o777, True)
                copy_tree(cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_output", cwd + "/Working/error_output/" + dcp)
        except Exception as e:
            print(e)

        folder = cwd + "/Working/DeepCreamPy/"+ dcp + "/decensor_output"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=0)
    window.grid_columnconfigure(4, weight=0)
    window.grid_columnconfigure(5, weight=0)
    window.grid_columnconfigure(6, weight=0)
    window.grid_columnconfigure(7, weight=0)
    window.grid_columnconfigure(8, weight=0)

    lbl.grid(column=0, row=0)
    btn0.grid(column=0, row=2)
    btn1.grid(column=0, row=3)
    btn2.grid(column=0, row=4)
    btn3.grid(column=0, row=5)
    btn4.grid(column=0, row=6)
    btn5.grid(column=0, row=7)
    btn55.grid(column=0, row=8)
    btn6.grid(column=0, row=9)
    btn7.grid(column=0, row=10)
    btn8.grid(column=0, row=11)
    version_lbl.grid(column=0, row=12)
    github_lbl.grid(column=0, row=13)
    twitter_lbl.grid(column=0, row=14)

if __name__ == '__main__':
    freeze_support()

    cwd = os.getcwd()
    window = Tk()
    window.title("DCPAssistant")
    window.update_idletasks()
    window.state('zoomed')
    height = window.winfo_screenheight()
    width = window.winfo_screenwidth()
    window.geometry(str(width) + 'x' + str(height))
    dateS =  time.strftime("20%y-%m-%d")
    
    init_directories()
    
    originalfolders = os.listdir(cwd + "/Archive/original")
    originals_archive = []
    originals_archive_mosaic = []
    originals_working = []
    originals_working_mosaic = []
    try:
        f = open(cwd + "/Working/config.txt", "x")
        f.write("output_path=" + cwd + "/Working/default_output")
        f.close()
    except:
        pass
    try:
        f = open(cwd + "/Working/How_To.txt", "x")
        f.write("""How To use DCPAss:\n
1. Click 'Open DCP-versions' and put an untouched copy of every version of DeepCreamPy you want to use in there
2. Click 'Set output' and select the output you want your selected images saved in later
3. Click 'Open input' and put all images (bar AND mosaic, the program will sort them out for you) you want to decensor in after you marked the area that should be decensored
4. If you want to decensor mosaic images, click 'Open original' and put the original images in the mosaic folder
4.5 [optional] Since you will be able to compare all images later it is recommended that you put the originals for the bar images into the bar folder but not neccesary
5. Click the 'Start bar decensor' or 'Start mosaic decensor' button
6. Select the versions you want to decensor with
7. Wait
8. If you want to save all decensored pictures, you want to 'Choose all'
9. If you want to compare the versions decensorings and the original you want to 'Choose manually'
9.5 For every image you want to have in your selected output folder, check the 'Keep' box
10. Archive the stuff you want to have saved seperately from your output, otherwise it will get deleted
\tI recommend archiving the input and the originals. 
\tThe originals in the archive can be used by the program for future decensorings, so you need not re-add them if you want to decensor an image a second time
11. Profit""")
        f.close()
    except:
        pass
    img = Image.new('RGB', (200, 200), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((5,90), "No original image could be found!", fill=(0,0,0))
    img.save(cwd + "/Working/no_original.png")

    # start
    lbl = Label(window, text="DCPAss", font=("Arial Bold", 50))
    btn0 = Button(window, text="Open Archive", command=open_archive)
    btn1 = Button(window, text="Open input", command=open_input)
    btn2 = Button(window, text="Open original", command=open_original)
    btn3 = Button(window, text="Open DCP-versions", command=open_dcp)
    btn4 = Button(window, text="How To Use", command=tutorial)
    btn5 = Button(window, text="Set output", command=set_output)
    btn55 =Button(window, text="Open output", command=open_output)
    btn6 = Button(window, text="Start bar decensor", command=bar_dec)
    btn7 = Button(window, text="Start mosaic decensor", command=mosaic_dec)
    btn8 = Button(window, text="configs", command=configs)

    # set output
    output_lbl = Label(window, text="New output folder was set successfully!")
    no_output_lbl = Label(window, text="No new output folder was set!")

    # version_select
    bar_or_mosaic = 0
    bar_lbl = Label(window, text="Choose versions for BAR decensoring", font=("Arial Bold", 14))
    mosaic_lbl = Label(window, text="Choose versions for MOSAIC decensoring", font=("Arial Bold", 14))
    back = Button(window, text="Back", command=start)
    next_versions = Button(window, text="Next", command=progress)
    
    version_select_chkbtn_states = [] # checkstates for buttons in version select
    vmarks = [] # checkbuttons in version select
 
    # progress
    pbars = [] # Progressbars
    pnums = [] # Progressbarnumbers
    timer_start = 0
    timers= [] # How long did each one take
    all_timer = 0 # How long did all take

    # progress_update
    progress_lbl = Label(window, text="PROGRESS", font=("Arial Bold", 20))

    # chosen
    c_manual = Button(window, text="Choose manually", command=c_manual)
    original_lbl = Label(window, text="original")
    c_next = Button(window, text="Next", command=c_man_update)
    c_stats = Button(window, text="Stats", command=stats)
    c_all = Button(window, text="Choose all", command=c_all)
    iterator_output_images = 0
    versions = [] # All versions that exist inside DeepCreamPy directory
    images = []
    photoImages = []
    imgpanels = []
    original_img = Image.open(cwd + "/Working/no_original.png")
    original_photoimg = ImageTk.PhotoImage(original_img)
    original_panel = Label(window, image = original_photoimg)
    chosen_list = []
    keep_boxes = []
    keep_vars = []
    keep_vars_last = []
    output_list = []
    # output_mosaic = []
    image_count_lbl = Label(window, text="Image 0 of 0")
    not_selected_images = []
    c_back_btn = Button(window, text="Back", command=c_man_back)
    manual_archive = []
    manual_archive_boxes = []
    manual_archive_vars = []
    manual_archive_vars_last = []


    # stats
    stats_lbl = Label(window, text="STATS", font=("Arial Bold", 20))
    decensored_lbl = Label(window, text="Decensored images:")
    cfromall_lbl = Label(window, text="All versions:")
    chosen_text_lbl = Label(window, text="Chosen")
    time_text_lbl = Label(window, text="Time")
    finish_btn = Button(window, text="Finish", command=finish)
    decensorednum_lbl = Label(window, text="")
    cfromallnum_lbl = Label(window, text="")
    chosen_lbls = []
    sum_all = 0

    # Archive
    archive_lbl = Label(window, text="ARCHIVE", font=("Arial Bold", 20))
    archive_warning_lbl = Label(window, text="Everything unchecked will delete the used/produced pictures\nfrom the last session from DCPAss Working directories!", font=("Arial Bold", 15))
    kept_ones_var = IntVar()
    not_kept_ones_var = IntVar()
    input_var = IntVar()
    originals_var = IntVar()
    stats_var = IntVar()
    not_selected_var = IntVar()
    manual_archive_var = IntVar()
    manual_archive_var.set(1)
    kept_ones_chkbtn = Checkbutton(window, text="Images you already keep", var=kept_ones_var)
    not_kept_ones_chkbtn = Checkbutton(window, text="Images you don't want to keep", var=not_kept_ones_var)
    input_chkbtn = Checkbutton(window, text="Input images", var=input_var)
    originals_chkbtn = Checkbutton(window, text="Original images", var=originals_var)
    stats_chkbtn = Checkbutton(window, text="Stats", var=stats_var)
    not_selected_chkbtn = Checkbutton(window, text="Input images where no decensored version was selected\n(for later use in another version)", var=not_selected_var)
    manual_archive_chkbtn = Checkbutton(window, text="All images where the 'Archive manually' checkbox was ticked", var=manual_archive_var)

    inlen = 0 # Length of input
    cversions = [] # Labels of all chosen versions
    txtversions = [] # Names of all chosen versions

    process = Process(target=decensorer, args=(0,))

    version_lbl = Label(window, text="Version: beta 1.1.0(PrettyBackwards)")
    github_lbl = Label(window, text="GitHub: https://github.com/DCPAssistant/DCPAssistant")
    twitter_lbl = Label(window, text="Twitter: https://twitter.com/DCPAssistant")

    init_originals()
    start()
    window.mainloop()