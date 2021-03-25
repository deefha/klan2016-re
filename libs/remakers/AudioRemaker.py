# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import audioop
import contextlib
import string
import struct
import wave as wavelib
from .CommonRemaker import CommonRemaker


class AudioRemaker(CommonRemaker):

	PATTERN_REMAKED_ASSET = "remaked://%s/%s/%s/%04d.wav"

	CHARTABLE = u"ČüéďäĎŤčěĚĹÍľĺÄÁÉžŽôöÓůÚýÖÜŠĽÝŘťáíóúňŇŮÔšřŕŔ¼§▴▾                           Ë   Ï                 ß         ë   ï ±  ®©  °   ™   "

	adpcm_predictor = 0
	adpcm_step_index = 0
	adpcm_step = 0

	adpcm_index_table = [
		-1, -1, -1, -1, 2, 4, 6, 8,
		-1, -1, -1, -1, 2, 4, 6, 8
	]

	adpcm_stepsize_table = [
		1,      1,      1,      1,      1,      1,      1,      1,      1,      1,      2,      2,      2,      2,      2,      2,
		2,      2,      2,      2,      2,      2,      2,      3,      3,      3,      3,      3,      3,      3,      3,      4,
		4,      4,      4,      4,      4,      5,      5,      5,      5,      5,      6,      6,      6,      6,      7,      7,
		7,      7,      8,      8,      8,      9,      9,      9,     10,     10,     11,     11,     12,     12,     13,     13,
		14,     14,     15,     15,     16,     17,     17,     18,     19,     20,     20,     21,     22,     23,     24,     25,
		26,     27,     28,     29,     31,     32,     33,     35,     36,     38,     39,     41,     43,     44,     46,     48,
		50,     52,     54,     57,     59,     61,     64,     67,     69,     72,     75,     78,     82,     85,     89,     92,
		96,    100,    104,    109,    113,    118,    123,    128,    133,    139,    145,    151,    157,    163,    170,    177,
		185,    192,    200,    209,    217,    227,    236,    246,    256,    267,    278,    289,    301,    314,    327,    341,
		355,    369,    385,    401,    418,    435,    453,    472,    492,    512,    533,    555,    579,    603,    628,    654,
		681,    709,    739,    770,    802,    835,    870,    906,    944,    983,   1024,   1067,   1111,   1157,   1205,   1256,
		1308,   1362,   1419,   1478,   1539,   1604,   1670,   1740,   1812,   1888,   1966,   2048,   2133,   2222,   2314,   2411,
		2511,   2616,   2724,   2838,   2956,   3079,   3207,   3340,   3479,   3624,   3775,   3932,   4096,   4266,   4444,   4629,
		4821,   5022,   5231,   5449,   5676,   5912,   6158,   6414,   6681,   6959,   7249,   7550,   7864,   8192,   8533,   8888,
		9258,   9643,  10044,  10462,  10898,  11351,  11823,  12316,  12828,  13362,  13918,  14497,  15101,  15729,  16383,  17065,
		17776,  18515,  19286,  20088,  20924,  21795,  22702,  23647,  24631,  25656,  26724,  27836,  28994,  30201,  31458,  32767
	]

	#ulaw_lut = [ 0, 132, 396, 924, 1980, 4092, 8316, 16764 ]

	#adpcm_table = [ 0, 1, 2, 4, 8, 16, 32, 64, -1, -2, -4, -8, -16, -32, -48, -64 ]


	DemandVoice = ObjDict()
	DemandVoice.ADPCM11 = 0
	DemandVoice.ADPCM12 = 0
	DemandVoice.ADPCM21 = 0
	DemandVoice.ADPCM22 = 0


	def UnAdpcmL(self, delta):
		sign = 0		# Current adpcm sign bit
		step = 0		# Stepsize */
		valprev = 0		# Virtual previous output value */
		vpdiff = 0		# Current change to valprev */

		valprev = self.DemandVoice.ADPCM12
		step = self.adpcm_stepsize_table[self.DemandVoice.ADPCM11]

		# Step 2 - Find new index value (for later)
		self.DemandVoice.ADPCM11 += self.adpcm_index_table[delta];
		if self.DemandVoice.ADPCM11 < 0:
			self.DemandVoice.ADPCM11 = 0
		if self.DemandVoice.ADPCM11 > 255:
			self.DemandVoice.ADPCM11 = 255

		# Step 3 - Separate sign and magnitude
		sign = delta & 8
		delta = delta & 7

		# Step 4 - update output value
		vpdiff = ((delta * step) >> 2) + (step >> 3)
		if sign:
			valprev -= vpdiff
		else:
			valprev += vpdiff

		# Step 5 - clamp output value
		if valprev > 32767:
			valprev = 32767
		elif valprev < -32768:
			valprev = -32768

		# Step 6 - Update step value
		self.DemandVoice.ADPCM12 = valprev
		return valprev


	def UnAdpcmR(self, delta):
		sign = 0		# Current adpcm sign bit
		step = 0		# Stepsize */
		valprev = 0		# Virtual previous output value */
		vpdiff = 0		# Current change to valprev */

		valprev = self.DemandVoice.ADPCM22
		step = self.adpcm_stepsize_table[self.DemandVoice.ADPCM21]

		# Step 2 - Find new index value (for later)
		self.DemandVoice.ADPCM21 += self.adpcm_index_table[delta];
		if self.DemandVoice.ADPCM21 < 0:
			self.DemandVoice.ADPCM21 = 0
		if self.DemandVoice.ADPCM21 > 88:
			self.DemandVoice.ADPCM21 = 88

		# Step 3 - Separate sign and magnitude
		sign = delta & 8
		delta = delta & 7

		# Step 4 - update output value
		vpdiff = ((delta * step) >> 2) + (step >> 3)
		if sign:
			valprev -= vpdiff
		else:
			valprev += vpdiff

		# Step 5 - clamp output value
		if valprev > 32767:
			valprev = 32767
		elif valprev < -32768:
			valprev = -32768

		# Step 6 - Update step value
		self.DemandVoice.ADPCM22 = valprev
		return valprev


	#def _adpcm_decode_sample(self, nibble):
		#if self.adpcm_step_index < 0:
			#self.adpcm_step_index = 0
		#elif self.adpcm_step_index > 88:
			#self.adpcm_step_index = 88

		#self.adpcm_step = self.adpcm_stepsize_table[self.adpcm_step_index]
		#self.adpcm_step_index += self.adpcm_index_table[nibble]

		#difference = self.adpcm_step >> 3

		#if nibble & 1:
			#difference += self.adpcm_step >> 2
		#if nibble & 2:
			#difference += self.adpcm_step >> 1
		#if nibble & 4:
			#difference += self.adpcm_step
		#if nibble & 8:
			#difference = -difference
  
		#self.adpcm_predictor += difference

		#if self.adpcm_predictor < -0x8000:
			#self.adpcm_predictor = -0x8000
		#elif self.adpcm_predictor > 0x7FFF:
			#self.adpcm_predictor = 0x7FFF

		#return self.adpcm_predictor


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
		for wave_index, wave in self.meta_decompiled.data.waves.items():
			if wave.content:
				self.items_total += 1
				status = True

				with open(wave.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					wave_content = f.read()

				# PCM, 16? bit ----> 8 bit, 11025 Hz?, mono (#00+)
				if wave.content.mode == 0:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 2, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# PCM, 24? bit ----> 12 bit, 11025 Hz?, mono (#02+), stereo (#35+)
				elif wave.content.mode == 1:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 3, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# uLaw, 8 bit, mono (#05+), stereo (#35+)
				elif wave.content.mode == 2:
					status = False

				# ADPCM, 4 bit, mono (#04+), stereo (#28+)
				elif wave.content.mode == 3:
					self.DemandVoice.ADPCM11 = 0
					self.DemandVoice.ADPCM12 = 0
					self.DemandVoice.ADPCM21 = 0
					self.DemandVoice.ADPCM22 = 0

					result = b''

					for original_sample in tqdm(wave_content):
						first_sample = original_sample >> 4
						second_sample = original_sample & 0xf

						first_result = self.UnAdpcmL(first_sample)
						
						if wave.content.stereo:
							second_result = self.UnAdpcmR(second_sample)
						else:
							second_result = self.UnAdpcmL(second_sample)

						result += struct.pack('h', first_result)
						result += struct.pack('h', second_result)

					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 2, 22050, len(result), "NONE", "Uncompressed"))
					f.writeframes(result)
					f.close()

				if status:
					self.items_hit += 1
				else:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 2, 11025, 0, "NONE", "Uncompressed"))
					values = []

					for i in range(0, 22050):
						values.append(0)

					f.writeframes(bytes(values))
					f.close()

					self.items_miss += 1


	def fill_meta(self):
		super(AudioRemaker, self).fill_meta()

		self.meta_remaked.waves = ObjDict()

		for wave_index, wave in self.meta_decompiled.data.waves.items():
			if wave.content:
				wave_path = "%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index))

				with contextlib.closing(wavelib.open(wave_path, "rb")) as f:
					wave_duration = f.getnframes() / float(f.getframerate())

				wave_title = ""
				if self.issue.number >= "03":
					with open(wave.content.data.title.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						wave_title_temp = f.read()

					for char_index, char in enumerate(wave_title_temp):
						if char < 32:
							break
						elif char < 128:
							wave_title += chr(char)
						else:
							wave_title += self.CHARTABLE[char - 128]

				data_wave = ObjDict()
				data_wave.duration = wave_duration
				data_wave.mode = wave.content.mode
				data_wave.title = wave_title
				data_wave.asset = self.PATTERN_REMAKED_ASSET % (self.issue.number, self.source.library, self.source_index, int(wave_index))

				self.meta_remaked.waves[wave_index] = data_wave
