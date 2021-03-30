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

	DemandVoice = ObjDict()
	DemandVoice.ADPCM11 = 0
	DemandVoice.ADPCM12 = 0
	DemandVoice.ADPCM21 = 0
	DemandVoice.ADPCM22 = 0

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

	ulaw_table = [
		0x0000, 0x0008, 0x0010, 0x0018, 0x0020, 0x0028, 0x0030, 0x0038, 0x0040, 0x0048, 0x0050, 0x0058, 0x0060, 0x0068, 0x0070, 0x0078,
		0x0084, 0x0094, 0x00a4, 0x00b4, 0x00c4, 0x00d4, 0x00e4, 0x00f4, 0x0104, 0x0114, 0x0124, 0x0134, 0x0144, 0x0154, 0x0164, 0x0174,
		0x018c, 0x01ac, 0x01cc, 0x01ec, 0x020c, 0x022c, 0x024c, 0x026c, 0x028c, 0x02ac, 0x02cc, 0x02ec, 0x030c, 0x032c, 0x034c, 0x036c,
		0x039c, 0x03dc, 0x041c, 0x045c, 0x049c, 0x04dc, 0x051c, 0x055c, 0x059c, 0x05dc, 0x061c, 0x065c, 0x069c, 0x06dc, 0x071c, 0x075c,
		0x07bc, 0x083c, 0x08bc, 0x093c, 0x09bc, 0x0a3c, 0x0abc, 0x0b3c, 0x0bbc, 0x0c3c, 0x0cbc, 0x0d3c, 0x0dbc, 0x0e3c, 0x0ebc, 0x0f3c,
		0x0ffc, 0x10fc, 0x11fc, 0x12fc, 0x13fc, 0x14fc, 0x15fc, 0x16fc, 0x17fc, 0x18fc, 0x19fc, 0x1afc, 0x1bfc, 0x1cfc, 0x1dfc, 0x1efc,
		0x207c, 0x227c, 0x247c, 0x267c, 0x287c, 0x2a7c, 0x2c7c, 0x2e7c, 0x307c, 0x327c, 0x347c, 0x367c, 0x387c, 0x3a7c, 0x3c7c, 0x3e7c,
		0x417c, 0x457c, 0x497c, 0x4d7c, 0x517c, 0x557c, 0x597c, 0x5d7c, 0x617c, 0x657c, 0x697c, 0x6d7c, 0x717c, 0x757c, 0x797c, 0x7d7c,
		0x0000, 0xfff8, 0xfff0, 0xffe8, 0xffe0, 0xffd8, 0xffd0, 0xffc8, 0xffc0, 0xffb8, 0xffb0, 0xffa8, 0xffa0, 0xff98, 0xff90, 0xff88,
		0xff7c, 0xff6c, 0xff5c, 0xff4c, 0xff3c, 0xff2c, 0xff1c, 0xff0c, 0xfefc, 0xfeec, 0xfedc, 0xfecc, 0xfebc, 0xfeac, 0xfe9c, 0xfe8c,
		0xfe74, 0xfe54, 0xfe34, 0xfe14, 0xfdf4, 0xfdd4, 0xfdb4, 0xfd94, 0xfd74, 0xfd54, 0xfd34, 0xfd14, 0xfcf4, 0xfcd4, 0xfcb4, 0xfc94,
		0xfc64, 0xfc24, 0xfbe4, 0xfba4, 0xfb64, 0xfb24, 0xfae4, 0xfaa4, 0xfa64, 0xfa24, 0xf9e4, 0xf9a4, 0xf964, 0xf924, 0xf8e4, 0xf8a4,
		0xf844, 0xf7c4, 0xf744, 0xf6c4, 0xf644, 0xf5c4, 0xf544, 0xf4c4, 0xf444, 0xf3c4, 0xf344, 0xf2c4, 0xf244, 0xf1c4, 0xf144, 0xf0c4,
		0xf004, 0xef04, 0xee04, 0xed04, 0xec04, 0xeb04, 0xea04, 0xe904, 0xe804, 0xe704, 0xe604, 0xe504, 0xe404, 0xe304, 0xe204, 0xe104,
		0xdf84, 0xdd84, 0xdb84, 0xd984, 0xd784, 0xd584, 0xd384, 0xd184, 0xcf84, 0xcd84, 0xcb84, 0xc984, 0xc784, 0xc584, 0xc384, 0xc184,
		0xbe84, 0xba84, 0xb684, 0xb284, 0xae84, 0xaa84, 0xa684, 0xa284, 0x9e84, 0x9a84, 0x9684, 0x9284, 0x8e84, 0x8a84, 0x8684, 0x8284,
	]


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
		if self.DemandVoice.ADPCM21 > 255:
			self.DemandVoice.ADPCM21 = 255

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


	def export_assets(self):
		for wave_index, wave in tqdm(self.meta_decompiled.data.waves.items(), total=len(self.meta_decompiled.data.waves), desc="data.waves", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			if wave.content:
				self.items_total += 1
				status = True

				with open(wave.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					wave_content = f.read()

				# PCM, 16? bit ----> 8 bit, 11025 Hz?, mono (#00+), stereo (#35+)
				if wave.content.mode == 0:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((2 if wave.content.stereo else 1, 2, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# PCM, 24? bit ----> 12 bit, 11025 Hz?, mono (#02+), stereo (#35+)
				elif wave.content.mode == 1:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((2 if wave.content.stereo else 1, 3, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# uLaw, 8 bit, mono (#05+), stereo (#28+)
				elif wave.content.mode == 2:
					values = []

					for original_sample in wave_content:
						result = self.ulaw_table[original_sample]
						result = struct.pack('i', result)

						values.append(result[0])
						values.append(result[1])

					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((2 if wave.content.stereo else 1, 2, 22050, len(values), "NONE", "Uncompressed"))
					f.writeframes(bytes(values))
					f.close()

				# ADPCM, 4 bit, mono (#04+), stereo (#35+)
				elif wave.content.mode == 3:
					self.DemandVoice.ADPCM11 = 0
					self.DemandVoice.ADPCM12 = 0
					self.DemandVoice.ADPCM21 = 0
					self.DemandVoice.ADPCM22 = 0

					values = []

					for original_sample in wave_content:
						first_sample = original_sample >> 4
						second_sample = original_sample & 0xf

						first_result = self.UnAdpcmL(first_sample)
						second_result = self.UnAdpcmR(second_sample) if wave.content.stereo else self.UnAdpcmL(second_sample)

						first_result = struct.pack('h', first_result)
						second_result = struct.pack('h', second_result)

						values.append(first_result[0])
						values.append(first_result[1])
						values.append(second_result[0])
						values.append(second_result[1])

					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((2 if wave.content.stereo else 1, 2, 22050, len(values), "NONE", "Uncompressed"))
					f.writeframes(bytes(values))
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
				data_wave.stereo = wave.content.stereo
				data_wave.title = wave_title
				data_wave.asset = self.PATTERN_REMAKED_ASSET % (self.issue.number, self.source.library, self.source_index, int(wave_index))

				self.meta_remaked.waves[wave_index] = data_wave
