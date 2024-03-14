import math
from math import pi
import os
class Sounds:

    def sounds(self,sound):
        """
        声音力度前置条件，用音符盒距离的变化模拟强弱音
        ss[[dy,dz],[...],...]其中dy为y轴方向偏移长度，dz同理
        可以根据实际情况修改
        """
        x = round((128 - float(sound[0])) / 8)
        ss = [[int(-3+(-31/16*x)),int(2+(18/16*x))],[int(-2+(-18/16*x)),int(3+(31/16*x))],[int(-2+(-24/16*x)),int(2+(24/16*x))],[int((0)),int(3+(35/16*x))],[int(-3+(-35/16*x)),int((2))],[int(2+(18/16*x)),int(3+(31/16*x))]]
        return ss

    def commandblocksounds(self,sound):
        x = float(sound[0])
        volume = 0.00171429 + 0.00203869*x - 0.00000698*x*x +0.00000041*x*x*x
        return round(volume + 0.01,2)

class Noteblock:

    def commandblock_note_on(self,notedata,volume,filename,instrument):
        """
        读取midi参数，填入命令
        notedata:   数据
        volume:     音量
        filename:   文件名称
        instrument: 乐器名称
        """
        us = [0.5,0.529732,0.561231,0.594604,0.629961,0.667420,0.707107,0.749154,0.793701,0.840896,0.890899,0.943874,1,1.059463,1.122462,1.189207,1.259921,1.334840,1.414214,1.498307,1.587401,1.681793,1.781797,1.887749,2]

        commandblocks = open(f'particle\\{filename}.mcfunction','a+')

        for note in notedata:
            note_write = f'execute as @a at @s run playsound minecraft:{instrument}{note[0]} record @a ~ ~ ~ {volume} {us[int(note[1:])]} {volume}'
            commandblocks.write(str(note_write)+'\n')  
        commandblocks.close()

    def commandblock_note_off(self,notedata,filename,instrument):
        """
        读取midi参数，填入命令
        notedata:   数据
        filename:   文件名称
        instrument: 乐器名称
        """
        commandblocks = open(f'particle\\{filename}.mcfunction','a+')
        for note in notedata:
            stop = f'stopsound @a record minecraft:{instrument}{note[0]}'
            commandblocks.write(str(stop)+'\n')  
        commandblocks.close()

class Clone:

    def piano(self,notedata,dx,dy,dz,filename,path):
        """ 
        读取midi参数，放置音轨
        notedata:   midi数据
        dx:         x轴方向偏移量
        dy:         y轴方向偏移量
        dz:         z轴方向偏移量
        filename:   音轨名称
        path:       音轨路径
        """
        noteblocks = open(f'{path}\\{filename}.mcfunction','a+')

        blocks = f'clone ~1 ~-1 ~ ~2 ~ ~ ~{dx} ~{dy - 1} ~{dz} replace'
        noteblocks.write(str(blocks)+'\n')

        if len(notedata) <= 3 or notedata == [['']]:
            return 0
        else:
            if '' in notedata[0]:
                notedata[0].remove('')
            if '' in notedata[2]:
                notedata[2].remove('')
            if len(notedata[0]) == 3:
                for i in range(3):
                    note = f'clone ~{-int(notedata[0][i][1:])-1} ~-1 ~{int(notedata[0][i][0]) - 5} ~{-int(notedata[0][i][1:])-1} ~ ~{int(notedata[0][i][0]) - 5} ~{dx} ~{dy - 1} ~{1 - i + dz} replace'
                    noteblocks.write(str(note)+'\n')
            if len(notedata[0]) == 2:
                for i in range(2):
                    note = f'clone ~{-int(notedata[0][i][1:])-1} ~-1 ~{int(notedata[0][i][0]) - 5} ~{-int(notedata[0][i][1:])-1} ~ ~{int(notedata[0][i][0]) - 5} ~{dx} ~{dy - 1} ~{i * dz // abs(dz) + dz} replace'
                    noteblocks.write(str(note)+'\n') 
            if len(notedata[0]) == 1:
                note = f'clone ~{-int(notedata[0][0][1:])-1} ~-1 ~{int(notedata[0][0][0]) - 5} ~{-int(notedata[0][0][1:])-1} ~ ~{int(notedata[0][0][0]) - 5} ~{dx} ~{dy - 1} ~{dz} replace'
                noteblocks.write(str(note)+'\n')
            if len(notedata[2]) >= 1:
                blocks_1 = f'clone ~3 ~-1 ~ ~3 ~ ~ ~{dx} ~{dy - 1} ~{abs(dz) + 1} replace'
                noteblocks.write(str(blocks_1)+'\n')
                blocks_2 = f'clone ~4 ~-1 ~ ~4 ~ ~ ~{dx} ~{dy - 1} ~{-1 * abs(dz) - 1} replace'
                noteblocks.write(str(blocks_2)+'\n')
                if len(notedata[2]) == 3:
                    for i in range(3):
                        note = f'clone ~{-int(notedata[2][i][1:])-1} ~-1 ~{int(notedata[2][i][0]) - 5} ~{-int(notedata[2][i][1:])-1} ~ ~{int(notedata[2][i][0]) - 5} ~{dx + i // 2} ~{dy - 1} ~{(i % 2 + 2) * dz // abs(dz) + dz} replace'
                        noteblocks.write(str(note)+'\n')
                if len(notedata[2]) == 2:
                    for i in range(2):
                        note = f'clone ~{-int(notedata[2][i][1:])-1} ~-1 ~{int(notedata[2][i][0]) - 5} ~{-int(notedata[2][i][1:])-1} ~ ~{int(notedata[2][i][0]) - 5} ~{dx} ~{dy - 1} ~{(i + 2) * dz // abs(dz) + dz} replace'
                        noteblocks.write(str(note)+'\n') 
                if len(notedata[2]) == 1:
                    note = f'clone ~{-int(notedata[2][0][1:])-1} ~-1 ~{int(notedata[2][0][0]) - 5} ~{-int(notedata[2][0][1:])-1} ~ ~{int(notedata[2][0][0]) - 5} ~{dx} ~{dy - 1} ~{2 * dz // abs(dz) + dz} replace'
                    noteblocks.write(str(note)+'\n')
            if len(notedata[0]) >= 2 and len(notedata[2]) >= 1:
                blocks_utra = f'clone ~1 ~-1 ~ ~2 ~ ~ ~{dx} ~{dy + 1} ~{dz} replace'
                noteblocks.write(str(blocks_utra)+'\n')

        noteblocks.close()

class Simpleparticle():

    def tppig(self,nums):
        """
        tppig函数
        """
        try:
            os.makedirs(f'particle')
        except FileExistsError:
            pass
        for j in range(1,nums + 1):
            for i in range(1,17):
                for num in range(1,5):
                    if num % 2 == 1:
                        dx = 0
                        dy = 2
                    else:
                        dx = 1
                        dy = -2
                    particles = open(f'particle\{j}.{i}.{num}.mcfunction','w')
                    redstone = f'setblock ~{dx} ~{dy} ~ minecraft:redstone_block replace'
                    particles.write(str(redstone)+'\n')
                    air = f'setblock ~ ~{0 - dy // 2} ~ minecraft:air replace'
                    particles.write(str(air)+'\n')
                    pig = f'execute as @e[tag=toolpig,type=pig,distance=..50] at @s run tp @s ^ ^ ^0.5'
                    particles.write(str(pig)+'\n')
                    particles.close()

    def data_pos(self,note_on_data,start_pos):
        """
        note_on_data:音高参数
        start_pos:初始坐标
        """
        input_pos = [[] for i in range(len(note_on_data[0]))]
        for i in range(len(note_on_data)):
            for j in range(len(note_on_data[i])):
                if len(note_on_data[i][j]) <= 4:
                    continue
                note = note_on_data[i][j].split('+')
                for ij in range(len(note)):
                    if len(note[ij].split('_')) < 2:
                        continue
                    note_data = note[ij].split('_')[1]
                    if int(note_data[1:]) > 12:
                        input_pos[j].append([start_pos[0] + i * 2 + ij / 2,start_pos[1],start_pos[2] + int(note_data[1:]) % 12,f'{i // 16 + 1}.{i % 16 + 1}.{ij + 1}'])
                    else:
                        input_pos[j].append([start_pos[0] + i * 2 + ij / 2,start_pos[1],start_pos[2] + int(note_data[1:]),f'{i // 16 + 1}.{i % 16 + 1}.{ij + 1}'])
        return input_pos
    
    def para_circle(self,output_pos,high,color_para):
        """
        output_pos:输出坐标
        high:上升高度
        """
        
        for it in range(len(output_pos)):
            particles = open(f'particle\{output_pos[it][3]}.mcfunction','a+')
            
            #圆圈特效
            for j in range(128):
                dx = math.sin(j / 64 * pi) * 2
                dz = math.cos(j / 64 * pi) * 2
                circle = f'particle minecraft:end_rod {output_pos[it][0]} {output_pos[it][1]} {output_pos[it][2]} {round(dx,4)} 0 {round(dz,4)} 0.091 0 force'
                particles.write(str(circle)+'\n')

            #抛物线特效
            if it == len(output_pos) - 1:
                continue
            a_para = -4 * high / (output_pos[it + 1][0] - output_pos[it][0]) / (output_pos[it + 1][0] - output_pos[it][0])
            b_para = 4 * high / (output_pos[it + 1][0] - output_pos[it][0])
            d_z = (output_pos[it + 1][2] - output_pos[it][2]) / (output_pos[it + 1][0] - output_pos[it][0])
            para = f'particleex rgbatickparameter minecraft:firework {output_pos[it][0]} {output_pos[it][1]} {output_pos[it][2]} 0 0 0 0 {output_pos[it + 1][0] - output_pos[it][0]} "x,y,z,cr,cg,cb=t,{round(a_para,6)}*t*t+{round(b_para,6)}*t,{round(d_z,6)}*t,{round(color_para[0]/255,4)},{round(color_para[1]/255,4)},{round(color_para[2]/255,4)}" 0.05 10 120 null 1.0 null'
            particles.write(str(para)+'\n')

            particles.close()
