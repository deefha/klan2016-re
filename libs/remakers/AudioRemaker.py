# common imports
import os, sys, datetime
from objdict import ObjDict

# specific imports
import audioop
import wave as wavelib
from CommonRemaker import CommonRemaker



class AudioRemaker(CommonRemaker):

	PATTERN_REMAKED_ASSET = "remaked://%s/%s/%s/%04d.wav"

	def export_assets(self):
		for wave_index, wave in self.meta_decompiled.data.waves.iteritems():
			if wave.content:
				with open(wave.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					wave_content = f.read()

				# PCM, mono, 16 bit, 11025 Hz (#00+)
				if wave.content.mode == 0:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 2, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# PCM, mono, 24 bit, 11025 Hz (#02+)
				elif wave.content.mode == 1:
					f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					f.setparams((1, 3, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# ?? (#05+)
				elif wave.content.mode == 2:
					continue

				# ADPCM? (#04+)
				elif wave.content.mode == 3:
					#state = None 
					#pcm, state = audioop.adpcm2lin(wave_content, 1, state)
					##pcm = audioop.alaw2lin(wave_content, 2)

					#f = wavelib.open("%s%04d.wav" % (self.PATH_DATA_REMAKED, int(wave_index)), "wb")
					#f.setparams((1, 2, 11025, len(wave_content), "NONE", "Uncompressed"))
					#f.writeframes(pcm)
					#f.close()
					continue

				# ?? (#35+)
				elif wave.content.mode == 256:
					continue

				# ?? (#35+)
				elif wave.content.mode == 257:
					continue

				# ?? (#28+)
				elif wave.content.mode == 258:
					continue



	def fill_meta(self):
		super(AudioRemaker, self).fill_meta()

		self.meta_remaked.waves = ObjDict()

		for wave_index, wave in self.meta_decompiled.data.waves.iteritems():
			if wave.content:
				data_wave = ObjDict()
				#data_wave.width = wave.content.width
				#data_wave.height = wave.content.height
				data_wave.asset = self.PATTERN_REMAKED_ASSET % (self.issue.number, self.source.library, self.source_index, int(wave_index))

				self.meta_remaked.waves[wave_index] = data_wave
