from tkinter import Tk, W, E, IntVar
from tkinter.ttk import Label, Checkbutton, Progressbar, Button
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

# Checks for DCP versions and initializes image arrays
def init_versions():
    global versions
    global oldversions
    versions = [0]
    
    try:
        versions = os.listdir(cwd + "/Working/DeepCreamPy")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
        start()
    if versions != oldversions:
        images.clear()
        photoImages.clear()
        imgpanels.clear()
        version_select_chkbtn_states.clear()
        try:
            for v in versions:
                images.append(Image.open(cwd + "/Working/no_original.png"))
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
        for v in vmarks:
            v.grid_forget()
        vmarks.clear()
        for i in images:
            photoImages.append(ImageTk.PhotoImage(i))
        for p in photoImages:
            imgpanels.append(Label(window, image=p))
        while len(version_select_chkbtn_states) < len(versions):
            version_select_chkbtn_states.append(IntVar())
        for v in versions:
            vmarks.append(Checkbutton(window, text=v, var=version_select_chkbtn_states[versions.index(v)])) # chk_state from config.txt
        oldversions = versions

# Searches originals in every original folder
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
    try:
        for of in originalfolders:
            originals_archive_mosaic.extend(os.listdir(cwd + "/Archive/original/" + of + "/mosaic"))
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    originals_working.clear()
    try:
        originals_working.extend(os.listdir(cwd + "/Working/original/bar"))
        originals_working.extend(os.listdir(cwd + "/Working/original/mosaic"))
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
    originals_working_mosaic.clear()
    try:
        originals_working_mosaic.extend(os.listdir(cwd + "/Working/original/" + "/mosaic"))
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

    # Remove all non png files from lists
    for name in originals_archive:
        if not name.endswith(".png"):
            originals_archive.remove(name)
    for name in originals_archive_mosaic:
        if not name.endswith(".png"):
            originals_archive_mosaic.remove(name)
    for name in originals_working:
        if not name.endswith(".png"):
            originals_working.remove(name)
    for name in originals_working_mosaic:
        if not name.endswith(".png"):
            originals_working_mosaic.remove(name)

def init_input_images():
    global bar_input_length
    global bar_original_length
    global mosaic_input_length
    global mosaic_original_length

    inputs = os.listdir(cwd + "/Working/input")
    originals_bar = os.listdir(cwd + "/Working/original/bar")
    mosaic_input_images.clear()
    bar_input_images.clear()

    for img in inputs:
        if img.endswith(".png"):
            if img in originals_working_mosaic or img in originals_archive_mosaic:
                mosaic_input_images.append(img)
            else:
                bar_input_images.append(img)
    
    bar_input_length = len(bar_input_images)
    bar_original_length = len(originals_bar)
    mosaic_input_length = len(mosaic_input_images)
    mosaic_original_length = mosaic_input_length

# Makes all directories
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

# Moves images around and starts DCP
def decensorer(bar_or_mosaic, txtversions, cwd, originalfolders, dateS, mosaic_input_images, bar_input_images, originals_archive_mosaic, originals_working_mosaic):
    mosaic_originals = []
    mosaic_originals.extend(originals_archive_mosaic)
    mosaic_originals.extend(originals_working_mosaic)

    if bar_or_mosaic == 1:
        inNames = bar_input_images
    elif bar_or_mosaic == 2:
        inNames = mosaic_input_images
    
    print("Moving pictures from input into 'Working/current' directory")
    # for all images in input
    for name in inNames: 
        try:
            shutil.move(cwd + "/Working/input/" + name, cwd + "/Working/current")
        except Exception as e:
            print(e)
            exit()

    print("Moved pictures to 'Working/current' successfully")

    print("Copying input from current into the decensor_input folders")
    for dcp in txtversions:
        input = cwd + "/Working/DeepCreamPy/" + dcp + "/decensor_input"
        original_input =  cwd + "/Working/DeepCreamPy/" + dcp + "/decensor_input_original"
        try:
            for c in inNames:
                shutil.copy(cwd + "/Working/current/" + c, input)
                if bar_or_mosaic == 2:
                    # look for the original in Working and copy to d_in_original
                    if c in originals_working_mosaic:
                        shutil.copy(cwd + "/Working/original/mosaic/" + c, original_input)
                    else:
                    # look for the original in Archive and copy to d_in_original
                        for of in originalfolders:
                            if c in os.listdir(cwd + "/Archive/original/" + of + "/mosaic"):
                                shutil.copy(cwd + "/Archive/original/" + of + "/mosaic/" + c, original_input)
        except Exception as e:
            print(e)
            exit()
    print("Copied images successfully")
            
    # decensor them parallel:

    for dcp in txtversions:
        try:
            os.chdir(cwd + "\\Working\\DeepCreamPy\\" + dcp)
            print("Starting " + dcp)
            if bar_or_mosaic == 1:
                sp.run("START /MIN decensor.exe", shell=True)
            elif bar_or_mosaic == 2:
                sp.run('START /MIN "decensor.exe" "decensor.exe" --is_mosaic=True', shell=True)
        except Exception as e:
            print(e)
            exit()
    
    # os.chdir(cwd)
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

# Starts a new process for the multiple DCPs
def decensor():
    global bar_or_mosaic
    global process
    global txtversions
    global cwd
    global originalfolders
    global dateS
    if __name__ == '__main__':
        process = Process(target=decensorer, args=(bar_or_mosaic, txtversions, cwd, originalfolders, dateS, mosaic_input_images, bar_input_images, originals_archive_mosaic, originals_working_mosaic,))
        process.start()

# 7 Save all selected images
def finish():
    global kept_ones_var
    global not_kept_ones_var
    global input_var
    global originals_var
    global stats_var
    global not_selected_var
    global manual_archive_var
    global sum_all
    global output_list
    global back_id
    global manual

    if manual:
        window.unbind('<Left>', back_id)

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
        path = f.readline()
        path = path[path.index("=")+1:]
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
        path = cwd + "/Working/default_output"
    
    os.makedirs(path, 0o777, True)
    for cl in range(0, len(chosen_list)):
        nr = txtversions[cl]
        temp = nr.index("y_")
        temp2 = nr.index("-")
        nr = nr[temp + 2:temp2]
        for k in chosen_list[cl]:
            if kept_ones_var.get() == 1:
                if k in output_list[cl]:
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
            if k in output_list[cl]:
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
    finish="Moved selected pictures in the output folder\nDefault: " + cwd + "\\Working\\default_output"
    mb.showinfo("Finished", finish)
    start()

# 6 Show stats and archive options
def stats(_event=None):
    global iterator_output_images
    global bar_or_mosaic
    global original_panel
    global inlen
    global sum_all
    global manual
    global next_id

    if manual:
        c_back_btn.configure(state='active')
        window.unbind('<Right>', next_id)
        for i in range(6):
            window.unbind(str(i+1), set_keep_id_list[i])
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

        if inlen != 0:
            # Add all chosen images to the right lists
            for x in range(0,len(txtversions)):
                chosen_list[x].clear()
                manual_archive[x].clear()
            
            for o in range(0, len(output_list)):
                for x in range(0, len(output_list[o])):
                    try:
                        img = output_list[o][x]
                    except Exception as e:
                        print(e)
                        mb.showerror("ERROR", e)
                    if keep_vars_last[x][o]:
                        keep_vars_flag = True
                        chosen_list[o].append(img)
                    if manual_archive_vars_last[x][o]:
                        manual_archive[o].append(img)
            for k in range(0,inlen):
                for x in range(0,len(txtversions)):
                    if keep_vars_last[k][x]:
                        keep_vars_flag = True
                if not keep_vars_flag:
                    try:
                        not_selected_images.append(os.listdir(cwd + "/Working/current")[k])
                    except Exception as e:
                        print(e)
                        mb.showerror("ERROR", e)
                keep_vars_flag = False
    
    
    # Forget c_all stuff
    children = window.winfo_children()
    for item in children:
        item.grid_forget()

    window.grid_columnconfigure(0, weight=0)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=1)
    window.grid_columnconfigure(4, weight=1)
    window.grid_columnconfigure(5, weight=1)
    window.grid_columnconfigure(6, weight=0)
    window.grid_columnconfigure(7, weight=0)
    window.grid_columnconfigure(8, weight=0)

    window.grid_columnconfigure(0, minsize=0)
    window.grid_columnconfigure(1, minsize=0)
    window.grid_columnconfigure(2, minsize=0)
    for i in range(0,len(txtversions)):
        window.grid_columnconfigure(i+3, minsize=0)

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

    stats_lbl.grid(column=0, row=0, padx = 15, sticky=W)
    decensored_lbl.grid(column=0, row=1, padx = 15, sticky=W)
    ccounter = 3

    # Display name of chosen versions
    for c in cversions:
        c.grid(column=0, row=ccounter, padx = 15, sticky=W)
        ccounter += 1
    ccounter -= len(cversions)
    clcounter = 0

    # Display number of chosen images per version 
    for cl in chosen_lbls:
        cl.configure(text = str(len(chosen_list[clcounter])))
        cl.grid(column=1, row=ccounter)
        ccounter += 1
        clcounter += 1
    cfromall_lbl.grid(column=0, row=ccounter, padx = 15, sticky=W)
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
    if inlen != 0 and manual:
        c_back_btn.grid(column=0, row=ccounter+1, padx = 15, sticky=W)
    else:
        c_back_btn.grid_forget()
    decensorednum_lbl.configure(text = inlen)
    decensorednum_lbl.grid(column=1, row=1)
    chosen_text_lbl.grid(column=1, row=2, padx=10)
    time_text_lbl.grid(column=2, row=2)
    iterator_output_images += 1

def set_keep(event):
    global iterator_output_images
    num = int(event.keysym) - 1
    if num < len(keep_vars):
        if keep_vars[num].get() == 1:
            keep_vars[num].set(0)
        else:
            keep_vars[num].set(1)

# 5.5 Go back to previous images
def c_man_back(_event=None):
    global iterator_output_images
    global original_panel
    global inlen
    global width 

    lentxt=len(txtversions)+1
    window.grid_columnconfigure(0, weight=0, minsize=(round(width/lentxt)/3))
    window.grid_columnconfigure(1, weight=0, minsize=(round(width/lentxt)/3))
    window.grid_columnconfigure(2, weight=0, minsize=(round(width/lentxt)/3))
    for i in range(0,len(txtversions)):
        window.grid_columnconfigure(i+3, weight=0, minsize=round(width/lentxt))

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
        c.grid(column=counter, row=0)
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
        kb.grid(column=kbcounter, row=1, sticky=W, padx=round(width/lentxt)/3)
        kbcounter += 1
    mabcounter = 3
    for mab in manual_archive_boxes:
        mab.grid(column=mabcounter, row=1, sticky=E, padx=round(width/lentxt)/3.5)
        mabcounter += 1
    
    c_back_btn.grid(column=0, row=0, sticky=E)
    image_count_lbl.grid(column=1, row=0)
    original_lbl.grid(column=0, row=1, columnspan=3)
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

    c_man_both()

# 5.4 Save user selections and reset all checkboxes
def c_man_update(_event=None):
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

# 5.3 Put images on screen
def portray():
    global original_panel
    global original_img
    global original_photoimg
    original_photoimg = ImageTk.PhotoImage(original_img)
    original_panel = Label(window, image = original_photoimg)
    original_panel.grid(column=0, row=2, columnspan=3)

    for t in range(0,len(txtversions)):
        photoImages[t] = ImageTk.PhotoImage(images[t])
        imgpanels[t].configure(image = photoImages[t])
        imgpanels[t].grid(column=t+3 , row=2)

# 5.2 Resize images to fit on screen
def resize():
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
        newwidth = round(width/(len(txtversions)+1))-5
        newheight = round(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        for i in range(0,len(images)):
            images[i] = images[i].resize(newsize, Image.ANTIALIAS)
        original_img = original_img.resize(newsize, Image.ANTIALIAS)
    if images[0].height > height-120:
        newheight = height - 120
        newwidth = round(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        for i in range(0,len(images)):
            images[i] = images[i].resize(newsize, Image.ANTIALIAS)
        original_img = original_img.resize(newsize, Image.ANTIALIAS)
    portray()

# 5.1 Load images into memory
def c_man_both():
    global bar_or_mosaic
    global iterator_output_images
    global inlen
    global original_img
    global bar_or_mosaic
    global output_list
    global back_id
    global next_id

    # If we have one image left to decide for
    if iterator_output_images >= inlen-1:
        c_next.grid_forget()
        c_stats.grid(column=2, row=0, sticky=W)
        next_id = window.bind('<Right>', stats)
    else:
        c_stats.grid_forget()
        c_next.grid(column=2, row=0, sticky=W)
        next_id = window.bind('<Right>', c_man_update)
    if iterator_output_images > 0:
        c_back_btn.configure(state='active')
        back_id = window.bind('<Left>', c_man_back)
    else:
        window.unbind('<Left>', back_id)
        c_back_btn.configure(state='disabled')
    
    

    set_keep_id_list.clear()
    set_keep_id_list.append(window.bind('1', set_keep))
    set_keep_id_list.append(window.bind('2', set_keep))
    set_keep_id_list.append(window.bind('3', set_keep))
    set_keep_id_list.append(window.bind('4', set_keep))
    set_keep_id_list.append(window.bind('5', set_keep))
    set_keep_id_list.append(window.bind('6', set_keep))
    set_keep_id_list.append(window.bind('7', set_keep))
    set_keep_id_list.append(window.bind('8', set_keep))
    set_keep_id_list.append(window.bind('9', set_keep))

    image_count_lbl.configure(text= "Image " + str(iterator_output_images + 1) + " of " + str(inlen))

    olen = 0
    opos = 0
    for liste in output_list:
        if olen < len(liste):
            olen = len(liste)
            opos = output_list.index(liste)
    original_string = output_list[opos][iterator_output_images]

    # Get all decensored images from output
    for t in range(0,len(txtversions)):
        if original_string in output_list[t]:
            try:
                images[t] = Image.open(cwd + "/Working/DeepCreamPy/" + txtversions[t] + "/decensor_output/" + original_string)
            except Exception as e:
                    print(e)
                    mb.showerror("ERROR", e)
        else:
            try:
                images[t] = Image.open(cwd + "/Working/no_original.png")
            except Exception as e:
                    print(e)
                    mb.showerror("ERROR", e)
    
    
    
    # Find original image in working
    if original_string in originals_working:
        try:
            if bar_or_mosaic == 1:
                original_img = Image.open(cwd + "/Working/original/bar/" + original_string)
            if bar_or_mosaic == 2:
                original_img = Image.open(cwd + "/Working/original/mosaic/" + original_string)
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
    # Or find original image in archive
    elif original_string in originals_archive:
        try:
            datis = os.listdir(cwd + "/Archive/original")
            for x in range(0, len(datis)):
                if bar_or_mosaic == 1 and original_string in os.listdir(cwd + "/Archive/original/" + datis[x] + "/bar"):
                    original_img = Image.open(cwd + "/Archive/original/" + datis[x] + "/bar/" + original_string)
                if bar_or_mosaic == 2 and original_string in os.listdir(cwd + "/Archive/original/" + datis[x] + "/mosaic"):
                    original_img = Image.open(cwd + "/Archive/original/" + datis[x] + "/mosaic/" + original_string)
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

    resize()
    iterator_output_images += 1

# 5.0 User chose manual selection of images. Loads manual selection screen
def c_manual():
    global output_list
    global inlen
    global manual
    global width

    manual = True

    # Forget old shit
    children = window.winfo_children()
    for item in children:
        item.grid_forget()

    if inlen != 0:
        # Initialize all checkboxes, the chosen_list and their labels
        for t in txtversions:
            chosen_list.append(list())
            keep_vars.append(IntVar())
            keep_boxes.append(Checkbutton(window, text="Keep", var=keep_vars[txtversions.index(t)]))
            manual_archive_vars.append(IntVar())
            manual_archive_boxes.append(Checkbutton(window, text="Archive", var=manual_archive_vars[txtversions.index(t)]))
            manual_archive.append(list())
            chosen_lbls.append(Label(window, text = ""))
        
        # Initialize memory for all keep_vars
        for l in range(0,inlen):
            keep_vars_last.append(list())
            manual_archive_vars_last.append(list())
            for t in range(0,len(txtversions)):
                keep_vars_last[l].append(False)
                manual_archive_vars_last[l].append(False)

        c_back_btn.grid(column=0, row=0, sticky=E)
        image_count_lbl.configure(text= "Image 1 of " + str(inlen))
        image_count_lbl.grid(column=1, row=0)

        lentxt=len(txtversions)+1
        window.grid_columnconfigure(0, weight=0, minsize=(round(width/lentxt)/3))
        window.grid_columnconfigure(1, weight=0, minsize=(round(width/lentxt)/3))
        window.grid_columnconfigure(2, weight=0, minsize=(round(width/lentxt)/3))
        for i in range(0,len(txtversions)):
            window.grid_columnconfigure(i+3, weight=0, minsize=round(width/lentxt))

        # Put checkboxes on screen
        kbcounter = 3
        for kb in keep_boxes:
            kb.grid(column=kbcounter, row=1, sticky=W, padx=(round(width/lentxt)/3))
            kbcounter += 1
        mabcounter = 3
        for mab in manual_archive_boxes:
            mab.grid(column=mabcounter, row=1, sticky=E, padx=(round(width/lentxt)/3.5))
            mabcounter += 1

        
        original_lbl.grid(column=1, row=1)
        counter = 3
        for c in cversions:
            c.grid_forget()
            c.grid(column=counter, row=0)
            counter += 1

        output_list.clear()
        # Get output lists
        for t in range(0,len(txtversions)):
            output_list.append(list())
            try:
                output_list[t].extend(os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[t] + "/decensor_output"))
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
                for o in output_list[t]:
                    if not o.endswith(".png"):
                        output_list.remove(o)

        c_man_both()
    else:
        stats()

# 5.0 User chose all images, jumps immediately to 6
def c_all():
    global bar_or_mosaic
    global inlen
    global manual
    global output_list

    manual = False
    for t in txtversions:
        chosen_list.append(list())
        chosen_lbls.append(Label(window, text = ""))
    if inlen == 0:
        stats()
    else:
        output_list.clear()
        for k in range(0, len(txtversions)):
            output_list.append(list())
            chosen_list[k].clear()
            try:
                chosen_list[k].extend(os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[k] + "/decensor_output"))
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
            for x in chosen_list[k]:
                if not x.endswith(".png"):
                    chosen_list[k].remove(x)
            # Get output lists
            try:
                output_list[k].extend(os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[k] + "/decensor_output"))
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
                for o in output_list[k]:
                    if not o.endswith(".png"):
                        output_list.remove(o)
        stats()

# 4 Load screen for choosing images manually or choosing all images
def choose_screen():
    global bar_or_mosaic
    global inlen
    global width
    for p in range(0,len(pbars)):
        pbars[p].grid_forget()
        pnums[p].grid_forget()
        timers[p].grid_forget()
    for t in cversions:
        t.grid_forget()
    progress_lbl.grid_forget()

    window.grid_columnconfigure(0, weight=0, minsize=round(width/2))
    window.grid_columnconfigure(1, weight=0, minsize=round(width/2))
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=0)
    window.grid_columnconfigure(4, weight=0)
    window.grid_columnconfigure(5, weight=0)
    window.grid_columnconfigure(6, weight=0)
    window.grid_columnconfigure(7, weight=0)
    window.grid_columnconfigure(8, weight=0)

    choose_lbl.grid(column=0, row=0, columnspan=2)
    c_manual.grid(column=1, row=1, sticky=W)
    c_all.grid(column=0, row=1, sticky=E)
    input_lbl.grid(column=0, row=2, sticky=E, padx = 20)
    decensored_lbl.grid(column=0, row=3, columnspan=2)
    if bar_or_mosaic == 1:
        bar_input_length_lbl.grid(column=1, row=2, sticky=W, padx=20)
    elif bar_or_mosaic == 2:
        mosaic_input_length_lbl.grid(column=1, row=2, sticky=W, padx=20)

    counter = 4
    for c in cversions:
        decensored_per_version_lbls.append(Label(window, text=""))
        c.grid_forget()
        c.grid(column=0, row=counter, sticky=E, padx = 20)
        counter += 1
    counter = 4
    out = []
    inlen = 0
    for t in txtversions:
        try:
            out = os.listdir(cwd + "/Working/DeepCreamPy/" + t + "/decensor_output")
        except Exception as e:
            print(e)
            mb.showerror("ERROR", e)
        for o in out:
            if not o.endswith(".png"):
                out.remove(o)
        decensored_per_version_lbls[txtversions.index(t)].configure(text=str(len(out)))
        decensored_per_version_lbls[txtversions.index(t)].grid(column=1, row=counter, sticky=W, padx=20)
        counter += 1
        if inlen < len(out):
            inlen = len(out)

# 3.2 Updating progress screen
def progress_update():
    global inlen
    global timer_start

    # Wait until all decensor process have finished
    if "decensor.exe" in (p.name() for p in psutil.process_iter()):
        # Update every progessbar/-number
        for p in range(0,len(pbars)):
            try:
                out = os.listdir(cwd + "/Working/DeepCreamPy/" + txtversions[p] + "/decensor_output")
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
            for o in out:
                if not o.endswith(".png"):
                    out.remove(o)
            outlen = len(out)
            new_value = min(inlen, outlen)
            
            if pbars[p]['value'] < new_value:
                pbars[p]['value'] = new_value
                number = str(pbars[p]['value'])
                if number.endswith(".0"):
                    number = number[:-2]
                pnums[p].configure(text = number + "/" + str(inlen))
            
            # Update timer
            if pbars[p]['value'] != inlen:
                tt = (round(time.perf_counter()) - timer_start) # tt = time elapsed since start in seconds 
                # hours = max(int(math.ceil((tt+1)/60/60))-1,0)
                hours = math.floor(tt/60/60)%60
                if hours < 10:
                    hours_str = "0" + str(hours)
                else:
                    hours_str = str(hours)
                #minutes = max(int(math.ceil((tt+1)/60))-1,0)
                minutes = math.floor(tt/60)%60
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

        window.after(500, progress_update)
    else:
        process.join()
        choose_screen()

def progress_idle():
    if "decensor.exe" not in (p.name() for p in psutil.process_iter()):
        window.after(100, progress_idle)
    else:
        progress_update()

# 3.1 Loading progress screen
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
        timers.append(Label(window, text = "00:00:00"))
        pbarcounter += 1
        txt = "DCP v" + t[t.index("y_")+2:t.index("-")]
        cversions.append(Label(window, text=txt))
        cversions[pbarcounter-1].grid(column=0, row=pbarcounter, sticky=E, padx=10)

    window.grid_columnconfigure(0, weight=1, minsize=0)
    window.grid_columnconfigure(1, weight=0, minsize=0)
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
    for p in range(0,len(pbars)):
        counter += 1
        pbars[p].grid(column=1, row=counter)
        pnums[p].grid(column=1, row=counter)
        timers[p].grid(column=2, row=counter, sticky=W, padx=10)

    progress_idle()

# 3.0 Set inlen(number of input images)
def progress():
    global txtversions
    global inlen
    
    if bar_or_mosaic == 1:
            inlen = bar_input_length
    elif bar_or_mosaic == 2:
            inlen = mosaic_input_length

    txtversions.clear()
    for c in range(0, len(version_select_chkbtn_states)):
            if version_select_chkbtn_states[c].get() == 1:
                txtversions.append(versions[c])
    decensor()
    progress_check()

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
            output_lbl.grid(column=0, row=1, sticky=W, padx=15)
        else:
            f.write(prev_path)
            f.close()
            no_output_lbl.grid(column=0, row=1, sticky=W, padx=15)
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

# 1.1
def both_dec():
    children = window.winfo_children()
    for item in children:
        item.grid_forget()

    window.grid_columnconfigure(0, weight=0)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=0)
    window.grid_columnconfigure(4, weight=0)
    progress()

# 1.0 Clicked Bar decensor
def bar_dec():
    global bar_or_mosaic
    bar_or_mosaic = 1

# 1.0 Clicked Mosaic decensor
def mosaic_dec():
    global bar_or_mosaic
    bar_or_mosaic = 2

def configs():
    output_lbl.grid_forget()
    no_output_lbl.grid_forget()
    try:
        os.startfile(cwd + "/Working/config.txt")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

# 0 Start menu
def start():
    global iterator_output_images
    global original_panel
    global cwd
    global inlen
    global bar_or_mosaic
    global width

    children = window.winfo_children()
    for item in children:
        item.grid_forget()

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
    decensored_per_version_lbls.clear()
    set_keep_id_list.clear()

    iterator_output_images = 0
    bar_or_mosaic = 0
    inlen = 0

    init_directories()

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
        
    window.grid_columnconfigure(0, weight=2, minsize=round(width/4))
    window.grid_columnconfigure(1, weight=1, minsize=round(width/5))
    window.grid_columnconfigure(2, weight=0)
    window.grid_columnconfigure(3, weight=0)
    window.grid_columnconfigure(4, weight=0)
    window.grid_columnconfigure(5, weight=15)

    lbl.grid(column=0, row=0, columnspan=2, sticky=W, padx=15)
    empty2_lbl.grid(column=0, row=1, sticky=W, padx=15)
    btn0.grid(column=0, row=2, sticky=W, padx=15)
    btn1.grid(column=3, row=7)
    btn2.grid(column=4, row=7)
    btn4.grid(column=0, row=3, sticky=W, padx=15)
    btn5.grid(column=0, row=4, sticky=W, padx=15)
    btn55.grid(column=0, row=5, sticky=W, padx=15)
    btn6.grid(column=5, row=5, sticky=W)
    btn6.configure(state="disabled")
    btn7.grid(column=5, row=6, sticky=W)
    btn7.configure(state="disabled")
    btn8.grid(column=0, row=6, sticky=W, padx=15)
    version_lbl.grid(column=0, row=7, sticky=W, padx=15)
    github_lbl.grid(column=0, row=8, sticky=W, padx=15)
    twitter_lbl.grid(column=0, row=9, sticky=W, padx=15)
    bar_lbl.grid(column=2, row=5, sticky=E)
    mosaic_lbl.grid(column=2, row=6, sticky=E)
    input_lbl.grid(column=3, row=4, padx = 10)
    orig_lbl.grid(column=4, row=4)
    select_lbl.grid(column=1, row=2, sticky=W)
    found_images_lbl.grid(column=3, row=2, columnspan=2)
    #empty_lbl.grid(column=5, row=0, padx=65)

    start2()

# 0.1 Checking if decensoring is possible (User has put DCPs, images, originals etc. in place)
def start2():
    global bar_input_length
    global bar_original_length
    global mosaic_input_length
    global mosaic_original_length
    global bar_input_length
    dcp_flag = False # True if no DCP version was found
    no_versions_selected_flag = True # True if no versions were selected

    no_versions_selected_lbl.grid_forget()
    no_versions_lbl.grid_forget()

    init_originals()
    init_versions()
    init_input_images()

    counter = 4
    for vm in vmarks:
        vm.grid(column=1, row=counter, pady=1, sticky=W)
        counter += 1
        btn3.grid(column=1, row=counter, sticky=W)

    
    bar_input_length_lbl.configure(text=str(bar_input_length))
    bar_original_length_lbl.configure(text=str(bar_original_length))
    mosaic_input_length_lbl.configure(text=str(mosaic_input_length))
    mosaic_original_length_lbl.configure(text=str(mosaic_original_length))

    if bar_input_length == 0 and mosaic_input_length == 0:
        no_input_lbl.grid(column=3 ,row=3, columnspan=2)
    else:
        no_input_lbl.grid_forget()

    for c in range(0, len(version_select_chkbtn_states)):
        if version_select_chkbtn_states[c].get() == 1:
            no_versions_selected_flag = False
            break

    if len(versions) == 0:
        dcp_flag = True

    empty_lbl.grid(column=1, row=3)
    if dcp_flag:
        no_versions_lbl.grid(column=1, row=3, sticky=W)
        # btn6.grid_forget()
        # btn7.grid_forget()
    elif no_versions_selected_flag:
        no_versions_selected_lbl.grid(column=1, row=3, sticky=W)
        # btn6.grid_forget()
        # btn7.grid_forget()
    else:
        if bar_input_length > 0:
            btn6.configure(state="active")
        # else:
        #     btn6.grid_forget()
        if mosaic_input_length > 0:
            btn7.configure(state="active")
        # else:
        #     btn7.grid_forget()
    bar_input_length_lbl.grid(column=3, row=5)
    bar_original_length_lbl.grid(column=4, row=5)
    mosaic_input_length_lbl.grid(column=3, row=6)
    mosaic_original_length_lbl.grid(column=4, row=6)

    if bar_or_mosaic == 0:
        window.after(100, start2)
    else:
        both_dec()

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
5. Select the versions you want to decensor with
6. Click the 'Start bar decensor' or 'Start mosaic decensor' button
7. Wait for DeepCreamPy
8. If you want to save all decensored pictures, you want to 'Choose all'
9. If you want to compare the versions decensorings and the original you want to 'Choose manually'
9.5 For every image you want to have in your selected output folder, check the 'Keep' box (Tip: Use the arrow and number keys)
10. Archive the stuff you want to have saved seperately from your output, otherwise it will get deleted
\tI recommend archiving the input and the originals. 
\tThe originals in the archive can be used by the program for future decensorings, so you need not re-add them if you want to decensor an image a second time
11. Profit""")
        f.close()
    except:
        pass
    img = Image.new('RGB', (500, 500), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((170,210), "No image could be found!", fill=(0,0,0))
    img.save(cwd + "/Working/no_original.png")

    # start
    lbl = Label(window, text="DCPAssistant", font=("Arial Bold", 50))
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

    # start2
    bar_input_images = []
    bar_input_length = 0
    bar_original_length = 0
    mosaic_input_images = []
    mosaic_input_length = 0
    mosaic_original_length = 0
    bar_input_length_lbl = Label(window, text="")
    bar_original_length_lbl = Label(window, text="")
    mosaic_input_length_lbl = Label(window, text="")
    mosaic_original_length_lbl = Label(window, text="")
    found_images_lbl = Label(window, text="Found images", font=("Arial Bold", 14))
    no_input_lbl = Label(window, text="No input was found!", foreground="red")
    empty_lbl = Label(window, text="")
    empty2_lbl = Label(window, text="")


    # set output
    output_lbl = Label(window, text="New output folder was set successfully!", foreground="green")
    no_output_lbl = Label(window, text="No new output folder was set!", foreground="red")

    # version_select
    bar_or_mosaic = 0
    bar_lbl = Label(window, text="Bar")
    mosaic_lbl = Label(window, text="Mosaic")
    input_lbl = Label(window, text="Input")
    orig_lbl = Label(window, text="Original")
    select_lbl = Label(window, text="Select versions to use", font=("Arial Bold", 14))
    no_versions_lbl = Label(window, text="No versions of DCP were found!", foreground="red")
    no_versions_selected_lbl = Label(window, text="No versions of DCP are selected!", foreground="red")
    
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
    c_manual = Button(window, text="Select", command=c_manual)
    original_lbl = Label(window, text="original")
    c_next = Button(window, text="Next", command=c_man_update)
    c_stats = Button(window, text="Stats", command=stats)
    c_all = Button(window, text="Keep all", command=c_all)
    iterator_output_images = 0
    versions = [] # All versions that exist inside DeepCreamPy directory
    oldversions = []
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
    output_list = [] # list for output images per version 
    image_count_lbl = Label(window, text="Image 0 of 0")
    not_selected_images = []
    c_back_btn = Button(window, text="Back", command=c_man_back)
    manual_archive = []
    manual_archive_boxes = []
    manual_archive_vars = []
    manual_archive_vars_last = []
    manual = False
    back_id = 0
    next_id = 0
    set_keep_id_list = []
    choose_lbl = Label(window, text="Keep all decensored images or select them manually?", font=("Arial Bold", 12))

    # stats
    stats_lbl = Label(window, text="STATS", font=("Arial Bold", 20))
    decensored_lbl = Label(window, text="Decensored images:")
    cfromall_lbl = Label(window, text="All versions:")
    chosen_text_lbl = Label(window, text="Selected")
    time_text_lbl = Label(window, text="Time")
    finish_btn = Button(window, text="Finish", command=finish)
    decensorednum_lbl = Label(window, text="")
    cfromallnum_lbl = Label(window, text="")
    chosen_lbls = []
    sum_all = 0
    decensored_per_version_lbls = []

    # Archive
    archive_lbl = Label(window, text="ARCHIVE", font=("Arial Bold", 20))
    archive_warning_lbl = Label(window, text="All images not transferred to the Archive\nand images you chose not to keep will get deleted!", font=("Arial Bold", 12), foreground="red")
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
    manual_archive_chkbtn = Checkbutton(window, text="All images where the 'Archive' checkbox was ticked", var=manual_archive_var)

    inlen = 0 # Length of input
    cversions = [] # Labels of all chosen versions
    txtversions = [] # Names of all chosen versions

    process = Process(target=decensorer, args=(0,))

    version_lbl = Label(window, text="Version: beta 1.2.0(TheFirstGreatRefucktoring)")
    github_lbl = Label(window, text="GitHub: https://github.com/DCPAssistant/DCPAssistant")
    twitter_lbl = Label(window, text="Twitter: https://twitter.com/DCPAssistant")

    start()
    window.mainloop()