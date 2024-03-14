import os
import shutil
import datetime
import subprocess
class Midifile:
    def mididata(self):
        """
        执行midi.exe文件
        """

        try:
            os.makedirs(f'midi')
        except FileExistsError:
            pass
        backups_midis = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        current_dir = './'
        # 搜索.mid文件并移动到midi文件夹
        for root, dirs, files in os.walk(current_dir):
            print(root)
            for file in files:
                if file.endswith('.mid'):
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(current_dir, 'midi', file)
                    shutil.move(src_file, dst_file)
            if root in ['./cbcommand', './instrument', './particle']:
                try:
                    os.makedirs(f'backups/{backups_midis}')
                except FileExistsError:
                    pass
                shutil.move(root[2:], f'backups/{backups_midis}')
        subprocess.run(['midi.exe'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def midideal(self,filename,soundtrack,num,midi_tick):
        """
        将midi文件读入列表
        soundtrack:音轨数
        num:小节数
        midi_tick:midi的四分之一音符时长
        """
        #初始化准备
        read = open(f'midi\\{filename}.txt','r',encoding='utf-8')
        note_on_list = [['' for i in range(soundtrack + 3)] for j in range(num * 16)]
        note_off_list = [['' for i in range(soundtrack + 3)] for j in range(num * 16)]

        #初始化音轨数、音轨名、总时长
        track_num = -1
        track_name = []
        time_all = 0

        #逐行读入参数，删除末尾换行符
        for line in read:
            line = line.strip("\n")

            #读取乐器名、乐器数+1、时长清零
            if line[:11] == "MetaMessage":
                if line.split(", ")[1][:4] == "name":
                    track_name.append(line.split("'")[3])
                    track_num += 1
                    time_all = 0

            #读取note中的参数，转化为二维列表
            if line.split(" ")[0][:4] == "note":
                note_para = []
                for para in line.split(" "):
                    note_para.append(para.split("="))
                time_all += int(note_para[4][1])

                #note_on起始音符处理
                if note_para[0][0] == 'note_on':
                    #单个音符参数处理："下划线+大音域+小音域"   PS：这里最好加个滑动变阻器
                    tick = '_' + str((int(note_para[2][1]) - 6) // 12 + 1) + str((int(note_para[2][1]) - 6) % 12)
                    #tick = '_' + str(int(note_para[2][1]) // 12) + str((int(note_para[2][1])) % 12 + 6)
                    if note_on_list[time_all // midi_tick][track_num] == '':
                        note_on_list[time_all // midi_tick][track_num] = note_para[3][1] + '+++'
                    tick_all = note_on_list[time_all // midi_tick][track_num].split('+')
                    for tickrate in range(4):
                        if (time_all % midi_tick) // (midi_tick//4) == tickrate:
                            tick_all[tickrate] = tick_all[tickrate] + tick
                    note_on_list[time_all // midi_tick][track_num] = tick_all[0] + '+' + tick_all[1] + '+' + tick_all[2] + '+' + tick_all[3]

                #note_off尾部音符处理
                if note_para[0][0] == 'note_off':
                    #单个音符参数处理："下划线+大音域+小音域"   PS：这里最好加个滑动变阻器
                    tick = '_' + str((int(note_para[2][1]) - 6) // 12 + 1) + str((int(note_para[2][1]) - 6) % 12)
                    #tick = '_' + str(int(note_para[2][1]) // 12) + str((int(note_para[2][1])) % 12 + 6)
                    if note_off_list[time_all // midi_tick][track_num] == '':
                        note_off_list[time_all // midi_tick][track_num] = '+++'
                    tick_all = note_off_list[time_all // midi_tick][track_num].split('+')
                    for tickrate in range(4):
                        if int(round((time_all % midi_tick) / (midi_tick//4))) == tickrate:
                            tick_all[tickrate] = tick_all[tickrate] + tick
                    if int(round((time_all % midi_tick) / (midi_tick//4))) == 4:
                        if note_off_list[time_all // midi_tick + 1][track_num] == '':
                            note_off_list[time_all // midi_tick + 1][track_num] = tick + '+++'
                        else:
                            note_off_list[time_all // midi_tick + 1][track_num] = tick + note_off_list[time_all // midi_tick + 1][track_num]
                    note_off_list[time_all // midi_tick][track_num] = tick_all[0] + '+' + tick_all[1] + '+' + tick_all[2] + '+' + tick_all[3]

        #传入力度大小
        for b in range(soundtrack + 3):
            vol = '64'
            for a in range(len(note_on_list)):
                if note_on_list[a][b] != '':
                    p = note_on_list[a][b].split('+')
                    vol = p[0].split('_')[0]
                if note_on_list[a][b] == '':
                    note_on_list[a][b] = note_on_list[a][b] + vol

        read.close()
        return note_on_list, note_off_list, track_name, track_num
    