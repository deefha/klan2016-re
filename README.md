# KLAN 2016
Časopis nové generace pro novou generaci (po 20 letech)

## Kaitai Struct

http://kaitai.io

### Kaitai Struct Compiler (ksc)

https://github.com/kaitai-io/kaitai_struct_compiler

Kompilace aktuální verze ze zdrojových kódů (jako DEB balíček pro Debian/*buntu):

```bash
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sudo apt-get update
sudo apt-get install sbt git dpkg-dev dpkg-sig lintian fakeroot
git clone https://github.com/kaitai-io/kaitai_struct_compiler
cd kaitai_struct_compiler
mkdir -p jvm/src/main/resources # workaround pro chybu https://github.com/kaitai-io/kaitai_struct/issues/276
sbt compilerJVM/debian:packageBin
cd jvm/target
sudo dpkg -i *.deb
```

### Kaitai Struct Visualizer (ksv)

https://github.com/kaitai-io/kaitai_struct_visualizer

Kompilace aktuální verze ze zdrojových kódů (jako Ruby gem):

```bash
sudo apt-get install ruby
git clone https://github.com/kaitai-io/kaitai_struct_visualizer
cd kaitai_struct_visualizer
gem build kaitai-struct-visualizer.gemspec
sudo gem install kaitai-struct-visualizer-0.7.gem
```
