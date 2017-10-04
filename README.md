# KLAN 2016
Časopis nové generace pro novou generaci (po 20 letech)

## Kaitai Struct

http://kaitai.io

### Kaitai Struct Compiler (ksc)

https://github.com/kaitai-io/kaitai_struct_compiler

```bash
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sudo apt-get update
sudo apt-get install sbt
```

```bash
git clone https://github.com/kaitai-io/kaitai_struct_compiler
cd kaitai_struct_compiler
sbt compilerJVM/debian:packageBin
```


```bash
echo "deb https://dl.bintray.com/kaitai-io/debian jessie main" | sudo tee /etc/apt/sources.list.d/kaitai.list
sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net --recv 379CE192D401AB61
sudo apt-get update
sudo apt-get install kaitai-struct-compiler
```

### Kaitai Struct Visualizer (ksv)

https://github.com/kaitai-io/kaitai_struct_visualizer

```bash
git clone https://github.com/kaitai-io/kaitai_struct_visualizer
cd kaitai_struct_visualizer
gem build kaitai-struct-visualizer.gemspec
sudo gem install kaitai-struct-visualizer-0.7.gem
```
