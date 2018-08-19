# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import audioop
import contextlib
import struct
import wave as wavelib
from CommonRemaker import CommonRemaker



class AudioRemaker(CommonRemaker):

	PATTERN_REMAKED_ASSET = "remaked://%s/%s/%s/%04d.wav"

	adpcm_predictor = 0
	adpcm_step_index = 0
	adpcm_step = 0

	adpcm_index_table = [
		-1, -1, -1, -1, 2, 4, 6, 8,
		-1, -1, -1, -1, 2, 4, 6, 8
	]

	adpcm_stepsize_table = [
		7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
		19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
		50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
		130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
		337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
		876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
		2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
		5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
		15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
	]

	#ulaw_lut = [ 0, 132, 396, 924, 1980, 4092, 8316, 16764 ]

	#adpcm_table = [ 0, 1, 2, 4, 8, 16, 32, 64, -1, -2, -4, -8, -16, -32, -48, -64 ]



	def _adpcm_decode_sample(self, nibble):
		if self.adpcm_step_index < 0:
			self.adpcm_step_index = 0
		elif self.adpcm_step_index > 88:
			self.adpcm_step_index = 88

		self.adpcm_step = self.adpcm_stepsize_table[self.adpcm_step_index]
		self.adpcm_step_index += self.adpcm_index_table[nibble]

		difference = self.adpcm_step >> 3

		if nibble & 1:
			difference += self.adpcm_step >> 2
		if nibble & 2:
			difference += self.adpcm_step >> 1
		if nibble & 4:
			difference += self.adpcm_step
		if nibble & 8:
			difference = -difference
  
		self.adpcm_predictor += difference

		if self.adpcm_predictor < -0x8000:
			self.adpcm_predictor = -0x8000
		elif self.adpcm_predictor > 0x7FFF:
			self.adpcm_predictor = 0x7FFF

		return self.adpcm_predictor



	#def _decode_ulaw(self, number):
		#ULAW_BIAS = 33
		#sign = 0
		#position = 0
		#decoded = 0;

		#number = ~number

		#if number & 0x80:
			#number &= ~(1 << 7)
			#sign = -1

		#position = ((number & 0xF0) >> 4) + 5
		#decoded = (
			#(1 << position) | ((number & 0x0F) << (position - 4)) | (1 << (position - 5))
		#) - ULAW_BIAS;

		#if sign == 0:
			#return decoded
		#else:
			#return (-(decoded))



	#def _decode_ulaw(self, ulawbyte):
		#ulawbyte = ~ulawbyte
		#sign = (ulawbyte & 0x80)
		#exponent = (ulawbyte >> 4) & 0x07
		#mantissa = ulawbyte & 0x0F
		#sample = self.ulaw_lut[exponent] + (mantissa << (exponent + 3));
		#if sign != 0:
			#sample = -sample

		#return sample



	def export_assets(self):
		for wave_index, wave in self.meta_decompiled.data.waves.iteritems():
			if wave.content:
				self.items_total += 1
				status = True

				with open(wave.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					wave_content = f.read()

				# PCM, mono, 16 bit, 11025 Hz (#00+)
				if wave.content.mode == 0:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 2, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# ? PCM, mono, 24 bit, 11025 Hz (#02+)
				elif wave.content.mode == 1:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 3, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# ?? (#05+)
				elif wave.content.mode == 2:
					status = False

				# ? ADPCM (#04+)
				elif wave.content.mode == 3:
					status = False
					##state = None
					##pcm, state = audioop.adpcm2lin(wave_content, 2, state)

					##f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					##f.setparams((1, 2, 22050, len(wave_content), "NONE", "Uncompressed"))
					##f.writeframes(pcm)
					##f.close()
					##continue

					##self.adpcm_predictor = 0
					##self.adpcm_step_index = 0
					##self.adpcm_step = self.adpcm_stepsize_table[self.adpcm_step_index]

					#result = ''
					#index = 0
					#old = 0

					##for original_sample in tqdm(wave_content):
						###if index == 500:
							###index = 0
							###self.adpcm_predictor = 0
							###self.adpcm_step_index = 0
							###self.adpcm_step = self.adpcm_stepsize_table[self.adpcm_step_index]

						##original_sample = ord(original_sample)
						##second_sample = original_sample >> 4
						##first_sample = (second_sample << 4) ^ original_sample
						###first_sample = original_sample >> 4
						###second_sample = (first_sample << 4) ^ original_sample
						###print(hex(original_sample), hex(first_sample), hex(second_sample))

						###high, low = ord(content_byte) >> 4, ord(content_byte) & 0x0F
						###print(content_byte, hex(high), hex(low))

						##result += struct.pack('h', self._adpcm_decode_sample(first_sample))
						##result += struct.pack('h', self._adpcm_decode_sample(second_sample))

						##index += 1

					##for original_sample in tqdm(wave_content, ascii=True, leave=False):
						###result += original_sample + original_sample
						##original_sample = ord(original_sample)
						##print original_sample
						##decoded = self._decode_ulaw(original_sample)
						###print(hex(original_sample), hex(decoded))
						##result += struct.pack('h', decoded)

					##f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					##f.setparams((1, 2, 22050, len(result), "NONE", "Uncompressed"))
					##f.writeframes(result)
					##f.close()

					##for original_sample in tqdm(wave_content, ascii=True):
						##original_sample = ord(original_sample)
						##first_sample = original_sample & 0xF
						##second_sample = original_sample >> 4
						###print "* %s => %s, %s" % (hex(original_sample), first_sample, second_sample)

						##result += struct.pack('h', self._adpcm_decode_sample(first_sample))
						##result += struct.pack('h', self._adpcm_decode_sample(second_sample))

					##with open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb") as f:
						##f.write(result)

					##for original_sample in tqdm(wave_content, ascii=True):
						##print "*"
						##print hex(ord(original_sample))
						##original_sample = struct.unpack('b', original_sample)[0]
						##print original_sample
						##old += original_sample
						##print old

						##result += struct.pack('h', old)

					##f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					##f.setparams((2, 2, 11025, len(result), "NONE", "Uncompressed"))
					##f.writeframes(result)
					##f.close()

					##for original_sample in tqdm(wave_content, ascii=True):
						##original_sample = ord(original_sample)
						##first_sample = original_sample & 0xF
						##second_sample = original_sample >> 4
						###print "* %s => %s, %s" % (hex(original_sample), first_sample, second_sample)

						##result += struct.pack('b', first_sample)
						##result += struct.pack('b', second_sample)

					##with open("%s%04d.bin" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb") as f:
						##f.write(result)

					#for original_sample in tqdm(wave_content, ascii=True):
						#original_sample = ord(original_sample)

						#if original_sample < 128:
							#old = old + (original_sample * original_sample) 
						#else:
							#old = old - ((128 - original_sample) * (128 - original_sample))

						#if old < -0x8000:
							#old = -0x8000
						#elif old > 0x7FFF:
							#old = 0x7FFF

						##print old

						#result += struct.pack('h', old)

					#f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					#f.setparams((1, 2, 11025, len(result), "NONE", "Uncompressed"))
					#f.writeframes(result)
					#f.close()

				# ?? (#35+)
				elif wave.content.mode == 256:
					status = False

				# ?? (#35+)
				elif wave.content.mode == 257:
					status = False

				# ?? (#28+)
				elif wave.content.mode == 258:
					status = False

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1



	def fill_meta(self):
		super(AudioRemaker, self).fill_meta()

		self.meta_remaked.waves = ObjDict()

		for wave_index, wave in self.meta_decompiled.data.waves.iteritems():
			if wave.content:
				wave_path = "%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index))
				duration = 0
				if os.path.isfile(wave_path):
					with contextlib.closing(wavelib.open(wave_path, 'rb')) as f:
						duration = f.getnframes() / float(f.getframerate())

				data_wave = ObjDict()
				data_wave.duration = duration
				data_wave.mode = wave.content.mode
				data_wave.asset = self.PATTERN_REMAKED_ASSET % (self.issue.number, self.source.library, self.source_index, int(wave_index))

				self.meta_remaked.waves[wave_index] = data_wave
