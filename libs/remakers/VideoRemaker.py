# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from PIL import Image
from .CommonRemaker import CommonRemaker


class VideoRemaker(CommonRemaker):

  def decompress_lzss(self, image_content):
    image_content_unpacked = []

    image_buffer = []
    image_buffer_index = 4096 - 18
    for i in range(4096):
      image_buffer.append(0)

    content_byte_flags = True
    content_byte_flags_value = None
    content_byte_flags_index = None
    content_byte_reference = False
    content_byte_reference_value_first = None
    content_byte_reference_value_second = None

    for content_byte in image_content:
      #print('. %s' % content_byte)

      if content_byte_flags:
        content_byte_flags_value = content_byte
        content_byte_flags_index = 0

        content_byte_flags = False
      else:
        #print("Flags: %s, flags index: %s, flag bit: %s" % (ord(content_byte_flags_value), content_byte_flags_index, ord(content_byte_flags_value) & (2 ** content_byte_flags_index)))

        if content_byte_flags_value & (2 ** content_byte_flags_index):
          image_content_unpacked.append(content_byte)
          #print("Image index: %s, buffer index: %s, value: %s, literal" % (len(image_content_unpacked) - 1, image_buffer_index, ord(image_content_unpacked[len(image_content_unpacked) - 1])))
          #print("---")

          image_buffer[image_buffer_index] = content_byte
          image_buffer_index += 1
          if image_buffer_index == 4096:
            image_buffer_index = 0

          content_byte_flags_index += 1
        else:
          if content_byte_reference:
            content_byte_reference_value_second = content_byte
            reference_index = ((content_byte_reference_value_second & 0xf0) << 4) + content_byte_reference_value_first
            reference_length = ((content_byte_reference_value_second & 0x0f) + 3)

            for x in range(reference_length):
              real_index = reference_index + x
              if real_index >= 4096:
                real_index -= 4096

              image_content_unpacked.append(image_buffer[real_index])
              #print("Image index: %s, buffer index: %s, value: %s, reference index: %s, length: %s, step: %s, real index: %s" % (len(image_content_unpacked) - 1, image_buffer_index, ord(image_content_unpacked[len(image_content_unpacked) - 1]), reference_index, reference_length, x, real_index))

              image_buffer[image_buffer_index] = image_buffer[real_index]
              image_buffer_index += 1
              if image_buffer_index == 4096:
                image_buffer_index = 0

            #print("---")

            content_byte_reference = False
            content_byte_flags_index += 1
          else:
            content_byte_reference_value_first = content_byte
            content_byte_reference = True

        if content_byte_flags_index > 7:
          content_byte_flags = True
          content_byte_flags_value = None
          content_byte_flags_index = None

    return image_content_unpacked


  def decompress_rle(self, image_content):
    image_content_unpacked = []
    content_byte_break = True
    content_byte_break_length = None
    content_byte_break_count = None

    for content_byte in image_content:
      if content_byte_break:
        if content_byte > 127:
          content_byte_break_length = content_byte - 127
          content_byte_break_count = None
        else:
          content_byte_break_length = None
          content_byte_break_count = content_byte + 1

        content_byte_break = False
      else:
        if content_byte_break_count:
          image_content_unpacked.extend([content_byte] * content_byte_break_count)
          content_byte_break = True
        else:
          image_content_unpacked.append(content_byte)
          content_byte_break_length -= 1

          if not content_byte_break_length:
            content_byte_break = True

    return image_content_unpacked


  def export_assets(self):
    for anim_index, anim in tqdm(self.meta_decompiled.data.anims.items(), total=len(self.meta_decompiled.data.anims), desc="data.anims", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
      #if anim.content:
      if int(anim_index) == 1:
        self.items_total += 1
        status = True

        if not os.path.exists("%s%04d" % (self.PATH_DATA_REMAKED, int(anim_index))):
          os.makedirs("%s%04d" % (self.PATH_DATA_REMAKED, int(anim_index)))

        image_colormap = None
        image_content_unpacked = None

        for frame_index, frame in tqdm(anim.content.data.frames.items(), total=len(anim.content.data.frames), desc="anim.frames", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
          #print("Frame: %s" % frame_index)
          for action_index, action in frame.actions.items():

#if ( AnimAction.Action & 01 )
#{
  #FuckDelka = LZSS_Decompress ( UseData+4, TempArea, AnimAction.Len - 4 );
  #SwapTemp = UseData;
  #UseData  = TempArea;
  #TempArea = SwapTemp;
  #AnimAction.Action &= 0xfffe;
#}
            if action.mode & 1:
              #print("%s >> %s" % (action.mode, action.mode & 0xfffe))
              action.mode &= 0xfffe

              with open(action.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
                image_content = f.read()

              ##print(image_content)
              ##print("image_content: %s" % len(image_content))
              image_content_unpacked = self.decompress_lzss(image_content[4:])
              ##print(image_content_unpacked)
              ##print("image_content_unpacked: %s" % len(image_content_unpacked))
              #file_temp = "%s%04d/%04d_unlzss.bin" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index))
              #with open(file_temp, "wb") as f:
                  #f.write(bytes(image_content_unpacked))

              #file_temp_in = "%s%04d/%04d_in_unlzss.bin" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index))
              #file_temp_out = "%s%04d/%04d_out_unlzss.bin" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index))

              #with open(file_temp_in, "wb") as f:
                  #f.write(bytes(image_content[4:]))

              #os.system("%s/scripts/unlzss.so %s %s %s" % (
                  #self.ROOT_ROOT,
                  #file_temp_in,
                  #file_temp_out,
                  #len(image_content[4:])
              #))

              #with open(file_temp_out, "rb") as f:
              ##with open(file_temp, "rb") as f:
                #image_content_unpacked = f.read()

            else:
              #print(action.mode)
              with open(action.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
                image_content_unpacked = f.read()
              pass

#case 0 : // black
#case 2 : // paleta
#case 4 : // copy pic
#case 6 : // brl
#case 8 : // delta
#case 0xA : 10
#case 0xC : 12 // overwrites itself on non LZSS -ed buffer
#RLEDecomp ( TempArea, UseData, FuckDelka );
#para5 = (int) TempArea;
#switch ( ColorMode )
#{
  #case 0 : ASM_AnimForget8  (); break;
  #case 1 : ASM_AnimForget15 (); break;
  #case 2 : ASM_AnimForget16 (); break;
  #case 3 : ASM_AnimForget24 (); break;
#}
#break;
#case 0x10: 16 // titulek
#case 0x12: 18 // toto je vykreslovani hnusu
#case 0x14 : 20
#case 0x16 : 22
  #VPGDecomp ( Handle, UseData );
  #break;
#case 0x18 : 24
  #VPGDecompDiff ( Handle, UseData );
  #// diff frame
  #break;
#case 0x1000 : 4096 if ( AIT->Sound ) AddMonoSamples8    ( UseData, AnimAction.Len );       break;
#case 0x1002 : 4098 if ( AIT->Sound ) AddStereoSamples8  ( UseData, AnimAction.Len >> 1 );  break;
#case 0x1004 : 4100 if ( AIT->Sound ) AddMonoSamples12   ( UseData, (2*AnimAction.Len)/3 ); break;
#case 0x1006 : 4102 if ( AIT->Sound ) AddStereoSamples12 ( UseData, AnimAction.Len/3 );     break;
#case 0x1008 : 4104 if ( AIT->Sound ) AddMonoULaw8       ( UseData, AnimAction.Len );       break;
#case 0x100A : 4106 if ( AIT->Sound ) AddStereoULaw8     ( UseData, AnimAction.Len >> 1 );  break;
#case 0x100C : 4108 if ( AIT->Sound ) AddMonoADPCM4      ( UseData, AnimAction.Len );       break;
#case 0x100E : 4110 if ( AIT->Sound ) AddStereoADPCM4    ( UseData, AnimAction.Len >>1 );   break;

            # paleta
            if action.mode == 2:
              with open(action.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
                image_colormap = f.read()

            # overwrites itself on non LZSS -ed buffer
            if action.mode == 12:
              #image_content_unpacked_final = self.decompress_rle(image_content_unpacked)
              #print(image_content_unpacked_final)
              #print("image_content_unpacked_final: %s" % len(image_content_unpacked_final))

              file_temp_in = "%s%04d/%04d_in_unrle.bin" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index))
              file_temp_out = "%s%04d/%04d_out_unrle.bin" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index))

              with open(file_temp_in, "wb") as f:
                  f.write(bytes(image_content_unpacked))

              os.system("%s/scripts/unrle.so %s %s %s" % (
                  self.ROOT_ROOT,
                  file_temp_in,
                  file_temp_out,
                  len(image_content_unpacked)
              ))

              with open(file_temp_out, "rb") as f:
                image_content_unpacked_final = f.read()

              os.remove(file_temp_in)
              #os.remove(file_temp_out)

              #print("%sx%s" % (int(anim.content.width / 2), int(anim.content.height / 2)))
              #i = Image.frombytes("P", (int(anim.content.width / 2), int(anim.content.height / 2)), bytes(image_content_unpacked_final))
              i = Image.frombytes("P", (int(anim.content.width / 2), int(anim.content.height / 2)), image_content_unpacked_final)
              i.putpalette(image_colormap)
              i.save("%s%04d/%04d.png" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index)))

              #with open("%s%04d/%04d.png" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index)), "wb") as f:
                  #f.write(bytes(image_content_unpacked_final))

              #try:
                #if len(image_content_unpacked_final) > anim.content.width * anim.content.height:
                  #print("%s (%s)" % (len(image_content_unpacked_final), anim.content.width * anim.content.height))
                  #print(len(image_colormap))

                #i = Image.frombytes("P", (anim.content.width, anim.content.height), bytes(image_content_unpacked_final))
                #i.putpalette(image_colormap)
                #i.save("%s%04d/%04d.png" % (self.PATH_DATA_REMAKED, int(anim_index), int(frame_index)))
              #except:
                #pass

        if status:
          self.items_hit += 1
        else:
          self.items_miss += 1


  def fill_meta(self):
    super(VideoRemaker, self).fill_meta()

    self.meta_remaked.anims = ObjDict()

    #for image_index, image in self.meta_decompiled.data.images.items():
      #if image.content:
        #data_image = ObjDict()
        #data_image.width = image.content.width
        #data_image.height = image.content.height
        #data_image.mode = image.content.mode
        #data_image.title = ""
        #data_image.asset = "remaked://%s/%s/%s/%04d.png" % (self.issue.number, self.source.library, self.source_index, int(image_index))

        #if hasattr(self.descriptions, "descriptions") and hasattr(self.descriptions.descriptions, str(image_index)):
          #data_image.title = self.descriptions.descriptions[str(image_index)].title

        #self.meta_remaked.images[image_index] = data_image
