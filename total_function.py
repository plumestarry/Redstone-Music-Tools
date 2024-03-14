#导入模块
import midi
import instr
import mcfunction

#初始化
midis = midi.Midifile()
instrument = instr.Track()
function = mcfunction.Simpleparticle()

#函数运行
class Function_run:

    def fun1(self, midiname, soundtrack, num, midi_tick, noteblocktrack, noteblockvolume, commandtrack, start_pos, color_para):
       
        #part1:将midi文件转化为txt数据参数，处理txt数据参数并转化为列表
        midis.mididata()
        note_on, note_off, track_name, track_num = midis.midideal(midiname, soundtrack, num, midi_tick)

        #part2:在particle文件夹下生成tppig的mcfunction数据包
        function.tppig(num)


        #part3:解析列表数据，生成mcfunction
        instrument.commandtracks_note_off(note_off, commandtrack, track_name)
        instrument.commandtracks_note_on(note_on, commandtrack, track_name)
        instrument.note_block_clone(note_on, noteblocktrack, noteblockvolume)

        if start_pos != '' and color_para != '':
            #part4:将需要逐tick处理的particle特效读入列表并追加写入mcfunction文件
            note_on_pos_list = function.data_pos(note_on,start_pos)
            function.para_circle(note_on_pos_list[0],2,color_para)