import mcfunction
import os
volume = mcfunction.Sounds()
note = mcfunction.Noteblock()
clone = mcfunction.Clone()
particle = mcfunction.Simpleparticle()

class Track:

    def commandtracks_note_off(self,mididata,command,instru):
        """
        mididata:midi数据
        command:音轨序号
        instru:乐器名称(要与音轨序号对应上)
        """
        for i in range(0,len(mididata),64):
            for j in range(64):
                for p in command:
                    if mididata[i + j][p] == '' or mididata[i + j][p] == '+++':
                        continue

                    notes = []
                    for data_data in mididata[i + j][p].split('+'):
                        notes.append(data_data.split("_"))

                    for ij in range(4):
                        if notes[ij] == '':
                            continue
                        if '' in notes[ij]:
                            notes[ij].remove('')
                        note.commandblock_note_off(notes[ij], f'{(i + j) // 16 + 1}.{(j) % 16 + 1}.{ij + 1}', instru[p])

    def commandtracks_note_on(self,mididata,command,instru):
        """
        mididata:midi数据
        command:音轨序号
        instru:乐器名称(要与音轨序号对应上)
        """
        try:
            os.makedirs(f'cbcommand')
        except FileExistsError:
            pass
        for i in range(0,len(mididata),64):
            commands = open(f'cbcommand\\p{i // 16 + 1}-p{i // 16 + 4}.mcfunction','w')
            for j in range(64):
                #CB板，用于粒子特效和tppig
                l , r = '{' , '}'
                for nm in range(1,5):
                    v = f'Command:"function mc:particle/{(i + j) // 16 + 1}.{(j) % 16 + 1}.{nm}"'
                    particle = f'setblock ~{j * 2 + nm // 3} ~{-20 + (nm % 2) * -1} ~ minecraft:command_block{l}{v}{r}'
                    commands.write(str(particle)+'\n')
                #note_on数据处理
                for p in command:
                    if '+' not in mididata[i + j][p]:
                        continue

                    notes = []
                    for data_data in mididata[i + j][p].split('+'):
                        notes.append(data_data.split("_"))
                    
                    volume_num = volume.commandblocksounds(notes[0])
                    del notes[0][0]
                    for ij in range(4):
                        if '' in notes[ij]:
                            notes[ij].remove('')
                        if notes[ij] == []:
                            continue
                        note.commandblock_note_on(notes[ij], volume_num, f'{(i + j) // 16 + 1}.{(j) % 16 + 1}.{ij + 1}', instru[p])
            commands.close()

    def note_block_clone(self,mididata,note_block,block_volume):
        """
        mididata:midi数据
        note_block:音轨序号
        """
        try:
            os.makedirs(f'instrument')
        except FileExistsError:
            pass
        if note_block == []:
            return 0
        for p in range(1,(int(len(note_block)) + 1)):
            for i in range(0,len(mididata),64):

                #创建文件夹
                try:
                    os.makedirs(f'instrument\\p{i // 16 + 1}-p{i // 16 + 4}')
                except FileExistsError:
                    pass
                piano_note_block = open(f'instrument\\p{i // 16 + 1}-p{i // 16 + 4}\\piano{p}.mcfunction','w')
                
                for j in range(64):
                    datas = []
                    for data_data in mididata[i + j][note_block[p - 1]].split('+'):
                        datas.append(data_data.split("_"))
                    
                    volume_num = volume.sounds(datas[0])
                    dy , dz = volume_num[block_volume[p - 1]][0] , volume_num[block_volume[p - 1]][1]

                    datas[0][0] = ''
                    clone.piano(datas,(j * 2),dy,dz,f'piano{p}',f'instrument\\p{i // 16 + 1}-p{i // 16 + 4}')
                    clone.piano(datas,(j * 2),dy,(0 - dz),f'piano{p}',f'instrument\\p{i // 16 + 1}-p{i // 16 + 4}')
                
                piano_note_block.close()