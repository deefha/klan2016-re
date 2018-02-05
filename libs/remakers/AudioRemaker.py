import os, sys, pprint

from objdict import ObjDict
import wave as wavelib
import audioop

from CommonRemaker import CommonRemaker



class AudioRemaker(CommonRemaker):

	PATTERN_FILE_CONTENT = "%s%04d/content.bin"

	def export_assets(self):
		for wave_index, wave in self.meta.data.waves.iteritems():
			if wave.content:
				with open(wave.content.data.content.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
					wave_content = f.read()

				# PCM, mono, 16 bit, 11025 Hz (#00+)
				if wave.content.mode == 0:
					f = wavelib.open("%s%04d.wav" % (self.PATH_ASSETS, int(wave_index)), "wb")
					f.setparams((1, 2, 11025, len(wave_content), "NONE", "Uncompressed"))
					f.writeframes(wave_content)
					f.close()

				# PCM, mono, 24 bit, 11025 Hz (#02+)
				elif wave.content.mode == 1:
					f = wavelib.open("%s%04d.wav" % (self.PATH_ASSETS, int(wave_index)), "wb")
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

					#f = wavelib.open("%s%04d.wav" % (self.PATH_ASSETS, int(wave_index)), "wb")
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



	def fill_scheme(self):
		super(AudioRemaker, self).fill_scheme()

		self.scheme.waves = ObjDict()

		for wave_index, wave in self.meta.data.waves.iteritems():
			if wave.content:
				data_wave = ObjDict()
				#data_wave.width = wave.content.width
				#data_wave.height = wave.content.height
				data_wave.asset = "assets://%s/%s/%04d.wav" % (self.issue, self.source, int(wave_index))

				self.scheme.waves[wave_index] = data_wave
