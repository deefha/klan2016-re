# KLAN 2016

Nástroje pro reverzní inženýring. Cílem je získat pro všechny instanci každé binární knihovny strukturovaná JSON (meta)data a zdrojové bloby. Z těch bude následně možné vytvářet objekty jednotlivých typů (texty, fonty, obrázky, hudba, audia, videa...) v obecně standardizovaných formátech (HTML, GIF, PNG, MOD, WAV, AVI...).

## Python

https://www.python.org

Instalace:

```bash
sudo apt-get install python python-pip
pip install objdict
```

## Kaitai Struct

http://kaitai.io  
https://github.com/kaitai-io/kaitai_struct  
http://doc.kaitai.io/user_guide.html  
http://doc.kaitai.io/ksy_reference.html

### Kaitai Struct: compiler (ksc)

https://github.com/kaitai-io/kaitai_struct_compiler  
http://doc.kaitai.io/developers.html

Kompilace aktuální verze ze zdrojových kódů (jako DEB balíček pro Debian/*buntu):

```bash
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sudo apt-get update
sudo apt-get install sbt git dpkg-dev dpkg-sig lintian fakeroot
git clone https://github.com/kaitai-io/kaitai_struct_compiler
cd kaitai_struct_compiler
sbt compilerJVM/debian:packageBin
cd jvm/target
sudo dpkg -i *.deb
```

### Kaitai Struct: visualizer (ksv)

https://github.com/kaitai-io/kaitai_struct_visualizer

Kompilace aktuální verze ze zdrojových kódů (jako Ruby gem):

```bash
sudo apt-get install ruby
git clone https://github.com/kaitai-io/kaitai_struct_visualizer
cd kaitai_struct_visualizer
gem build kaitai-struct-visualizer.gemspec
sudo gem install kaitai-struct-visualizer-0.7.gem
```

### Kaitai Struct: runtime library for Python

https://github.com/kaitai-io/kaitai_struct_python_runtime  
https://pypi.python.org/pypi/kaitaistruct  
http://doc.kaitai.io/lang_python.html

Instalace z PyPI:

```bash
sudo apt-get install python python-pip python-enum34
pip install kaitaistruct
```

## 010 Editor

https://www.sweetscape.com/010editor/
